import hashlib
import random
import string
import requests

class BitTorrentClient :
    def __init__(self,servers, hash_pieces ):
     self.servers= servers
     ## on peut choisir un de deux choices , le server tracker fait identifie chaque noeud dans le reseau 
     ## sinon , chaque noeud a la responsibility pour identifie lui meme de facon unique    
     ## par exemple version et client name + random numbers 
     self.peer_id = self.generate_peer_id()  # Generate if not provided
     self.hash_pieces= hash_pieces
     
    def generate_peer_id(self):
        # Generate a unique 20-byte peer_id (e.g., CL001-random)
        prefix = '-HP001-'  # Custom prefix for client version/name
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return prefix + random_id
    
    
    def sendRequest(self,event='started'):
        params = {
            'hash_pieces': self.hash_pieces,
            'peerId': self.peerId,
            'event': event,
            'port': 6881
        }
        for server in self.servers : 
            try :
                response = requests.get(server,params=params,timeout=5)
                if response.status_code == 200:
                    return response.json()  # La reponse du server
                else:
                    print(f"Tracker at {server} failed with status code: {response.status_code}")
            except requests.RequestException as e:
                print(f"Error connecting to tracker at {server}: {e}")
            
        return {"error": "All tracker servers failed."}


servers = [
    "https://tracker.example.com/announce", 
    "https://backup-tracker.example.com/announce"
]

client = BitTorrentClient(servers, info_hash="some_hash_pieces qu'on la recupere d'apres le fichier .torrent")
response = client.send_request()
print(response)