import hashlib
import random
import string
import requests
import bencodepy

class BitTorrentClient:
    def __init__(self, torrent_file):
        # Charger et décoder le fichier .torrent
        self.torrent_data = self.load_torrent(torrent_file)
        
        # Extraire l'URL du serveur tracker depuis le fichier .torrent
        self.server_url = f"{self.torrent_data.get(b'announce').decode('utf-8')}:8080"
        
        # Extraire les hash des pièces depuis la section info
        self.hash_pieces = self.extract_hash_pieces()
        
        # Générer un peer_id unique
        self.peer_id = self.generate_peer_id()

    def load_torrent(self, file_path):
        """ Charger et décoder le fichier .torrent en bencode. """
        with open(file_path, 'rb') as f:
            return bencodepy.decode(f.read())
    
    def extract_hash_pieces(self):
        """ Extraire les hash des pièces à partir de la section info. """
        info_section = self.torrent_data.get(b'info')
        pieces = info_section.get(b'pieces')
        return pieces  # Ceci est une chaîne d'octets contenant les hash concaténés des pièces
    
    def generate_peer_id(self):
        """ Générer un peer_id unique de 20 caractères. """
        prefix = '-HP001-'  # Custom prefix for client version/name
        random_id = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
        return prefix + random_id
    
    def send_request(self, event='started'):
        params = {
        'info_hash': 'abc123',  # Assurez-vous que c'est le bon info_hash
        'peer_id': self.peer_id,
        'event': event,
        'port': 8081,  # Assurez-vous que ce port est correct
        'uploaded': 0,  # Ajouter d'autres paramètres si nécessaire
        'downloaded': 0,
        'left': 0
        }

        # Construct the request correctly
    
        req = requests.Request('GET', self.server_url, params=params)
        prepared_req = req.prepare()  # Préparer la requête

        # Imprimer la requête avant de l'envoyer
        print(f"URL: {prepared_req.url}")
        try:
            response = requests.get(prepared_req.url, timeout=5)  # Use prepared request's URL
            if response.status_code == 200:
                return response.json()  # La réponse du tracker
            else:
                print(f"Tracker failed with status code: {response.status_code}")
        except requests.RequestException as e:
            print(f"Error connecting to tracker: {e}")

        return {"error": "Tracker request failed."}


# Chemin vers le fichier .torrent
torrent_file = 'image.jpg.torrent'

# Créer un client BitTorrent
client = BitTorrentClient(torrent_file)

# Envoyer une requête au tracker
response = client.send_request()
print(response)
 
 
 