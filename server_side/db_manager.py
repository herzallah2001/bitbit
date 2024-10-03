import sqlite3
import time

class DBManager:
    def __init__(self, db_path='./server_side/db/tracker_db'):
        self.db_path = db_path

    # Establishes a connection to the SQLite database
    def connect(self):
        return sqlite3.connect(self.db_path)

    # Inserts a new peer into the peers table
    def add_peer(self, torrent_id, peer_id, ip, port, uploaded, downloaded, left):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO peers (torrent_id, peer_id, ip, port, uploaded, downloaded, left, is_seed, last_announce)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, (torrent_id, peer_id, ip, port, uploaded, downloaded, left, int(left == 0), int(time.time())))
        conn.commit()
        peer_id_db = cursor.lastrowid
        conn.close()
        return peer_id_db

    # Logs peer announce event
    def log_announce(self, peer_id, torrent_id, event, uploaded, downloaded, left):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO announce_log (peer_id, torrent_id, event, uploaded, downloaded, left, timestamp)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (peer_id, torrent_id, event, uploaded, downloaded, left, int(time.time())))
        conn.commit()
        conn.close()

    # Finds a torrent by its info_hash
    def find_torrent(self, info_hash):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM torrents WHERE info_hash = ?", (info_hash,))
        torrent = cursor.fetchone()
        conn.close()
        return torrent

    # Finds a peer by torrent_id and peer_id
    def find_peer(self, torrent_id, peer_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM peers WHERE torrent_id = ? AND peer_id = ?", (torrent_id, peer_id))
        peer = cursor.fetchone()
        conn.close()
        return peer

    # Fetches a list of peers for a given torrent_id
    def get_peers(self, torrent_id, peer_id):
        conn = self.connect()
        cursor = conn.cursor()
        cursor.execute("SELECT ip, port FROM peers WHERE torrent_id = ? AND peer_id != ? LIMIT 50", (torrent_id, peer_id))
        peers = cursor.fetchall()
        conn.close()
        return peers
