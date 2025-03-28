from http.server import BaseHTTPRequestHandler, HTTPServer
import urllib.parse as urlparse
import secrets
import webbrowser
import threading
import requests
import base64

CLIENT_ID = '...'
CLIENT_SECRET = '...'
REDIRECT_URI = 'http://localhost:8888/callback/' 
SCOPE = "user-library-read, user-read-playback-state, user-modify-playback-state, user-read-currently-playing" 
STATE = secrets.token_urlsafe(16) # generates a random token for security

class MyHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path.startswith('/login'):
            self.handle_login()
        elif self.path.startswith('/callback'):
            self.handle_callback()

    def handle_login(self):
        self.send_response(302)
        self.send_header('Location', self.get_spotify_auth_url())
        self.end_headers()

    def handle_callback(self):
        query_components = urlparse.parse_qs(urlparse.urlparse(self.path).query) 
        code = query_components.get('code', [None])[0] # authorization code
        state_received = query_components.get('state', [None])[0] 
        if state_received != STATE:
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b'State mismatch')
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(f'Code: {code}'.encode())
            threading.Thread(target=spotify_server.shutdown).start()
            self.server.server_code = code

    def get_spotify_auth_url(self): # builds and returns URL for Spotify authentication
        params = {
            'response_type': 'code',
            'client_id': CLIENT_ID,
            'scope': SCOPE,
            'redirect_uri': REDIRECT_URI,
            'state': STATE
        }

        url = 'https://accounts.spotify.com/authorize?' + urlparse.urlencode(params)

        return url

def run_server():
    server_address = ('', 8888)
    global spotify_server
    spotify_server = HTTPServer(server_address, MyHandler)
    spotify_server.serve_forever()

def get_access_token(code):
    encoded_credentials = base64.b64encode(f"{CLIENT_ID}:{CLIENT_SECRET}".encode()).decode("utf-8")

    token_headers = {
        "Authorization": "Basic " + encoded_credentials,
        "Content-Type": "application/x-www-form-urlencoded"
    }

    token_data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": REDIRECT_URI
    }

    response = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
    response.raise_for_status()

    return response.json()


server_thread = threading.Thread(target=run_server) # starts the HTTP server in a separated thread
server_thread.start()
webbrowser.open(f'http://localhost:8888/login')
server_thread.join() # blocks the main thread until the server thread finishes

code = spotify_server.server_code
token = get_access_token(code)

print(f'client_id = "{CLIENT_ID}"')
print(f'client_secret = "{CLIENT_SECRET}"')
print(f'code = "{code}"')
print(f'token = "{token.get("access_token")}"')
print(f'refresh_token = "{token.get("refresh_token")}"')
