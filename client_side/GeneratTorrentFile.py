import os
import hashlib
import bencodepy
import time
from file_to_pieces import divide_file_and_generate_hashes

def create_torrent(file_path, tracker_url, tracker_list=None, piece_length=262144):
    # Open the file and hash pieces
    output_dir = './pieces/'
    all_piece_hashes = divide_file_and_generate_hashes(file_path, output_dir)  # Get concatenated hashes
    
    # Get file details
    file_name = os.path.basename(file_path)
    file_size = os.path.getsize(file_path)
    
    # Create the info dictionary
    info = {
        'piece length': piece_length,
        'pieces': all_piece_hashes,  # Concatenated hash of all pieces
        'name': file_name,
        'length': file_size
    }
    
    # Create the metainfo dictionary with additional fields
    metainfo = {
        'announce': tracker_url,               # Main tracker URL
        'announce-list': tracker_list or [[tracker_url]],  # Optional list of trackers
        'comment': 'Generation du fichier .torrent',   # Optional comment
        'created by': 'mktorrent 1.1',         # Creator information
        'creation date': int(time.time()),     # Unix timestamp
        'info': info                           
    }
    
    # Bencode the dictionary and save to .torrent file
    metainfo_bencoded = bencodepy.encode(metainfo)
    torrent_file_name = file_name + ".torrent"
    
    with open(torrent_file_name, 'wb') as torrent_file:
        torrent_file.write(metainfo_bencoded)
    
    print(f"Torrent file '{torrent_file_name}' created successfully!")

# Usage
file_to_serve = './client_side/res/image.jpg'
tracker_url = 'http://127.0.0.1'
tracker_list = [
    ['127.0.0.1'],
    ['149.0.0.0']
]
create_torrent(file_to_serve, tracker_url, tracker_list)
