
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
import json
from db_manager import DBManager  # Import the DBManager class

db_manager = DBManager()  # Initialize the DBManager

# HTTP Request Handler
class TrackerRequestHandler(BaseHTTPRequestHandler):
    
    # Handle GET requests (used by peers to announce themselves)
    def do_GET(self):
        # Parse the query parameters from the request URL
        query_components = parse_qs(urlparse(self.path).query)
        
        # Extract peer information from the request parameters
        info_hash = query_components.get('info_hash', [None])[0]
        peer_id = query_components.get('peer_id', [None])[0]
        ip = query_components.get('ip', [self.client_address[0]])[0]  # Use client IP if not provided
        port = query_components.get('port', [None])[0]
        uploaded = query_components.get('uploaded', [0])[0]
        downloaded = query_components.get('downloaded', [0])[0]
        left = query_components.get('left', [0])[0]
        event = query_components.get('event', [None])[0]

        if None in [info_hash, peer_id, port]:  # Validate required parameters
            self.send_response(400)
            self.end_headers()
            self.wfile.write(b"Missing required parameters")
            return
        
        # Convert data types
        port = int(port)
        uploaded = int(uploaded)
        downloaded = int(downloaded)
        left = int(left)

        # Step 1: Find the torrent by info_hash
        #modified info_hash to binarry
        info_hash = bytes.fromhex(info_hash) if isinstance(info_hash, str) else info_hash
        torrent = db_manager.find_torrent(info_hash)
        #print(torrent)
        if not torrent:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Torrent not found")
            return
        
        torrent_id = torrent[0]#5

        # Step 2: Check if the peer already exists
        peer = db_manager.find_peer(torrent_id, peer_id)#6

        if not peer:
            peer_id_db = db_manager.add_peer(torrent_id, peer_id, ip, port, uploaded, downloaded, left)
        else:
            peer_id_db = peer[0]
        
        # Step 3: Log the announce
        db_manager.log_announce(peer_id_db, torrent_id, event, uploaded, downloaded, left)

        # Step 4: Fetch a list of other peers sharing the same torrent
        peers = db_manager.get_peers(torrent_id, peer_id)
        
        # Step 5: Prepare the response
        peer_list = [{'ip': p[0], 'port': p[1]} for p in peers]
        response = {
            'interval': 1800,  # Announce interval in seconds (30 minutes)
            'peers': peer_list
        }

        # Send the response in JSON format
        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(response).encode('utf-8'))
    
    # Log requests to avoid cluttering the output
    def log_message(self, format, *args):
        return  # Override to suppress log messages

# Server setup
def run_tracker_server():
    server_address = ('', 8080)  # Listen on all interfaces, port 8080
    httpd = HTTPServer(server_address, TrackerRequestHandler)
    print("BitTorrent tracker is running on port 8080...")
    httpd.serve_forever()

run_tracker_server()