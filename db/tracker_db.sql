BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "torrents" (
	"id"	INTEGER,
	"info_hash"	BLOB NOT NULL,
	"name"	TEXT,
	"size"	INTEGER,
	"created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"last_seen"	DATETIME,
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "peers" (
	"id"	INTEGER,
	"torrent_id"	INTEGER NOT NULL,
	"peer_id"	BLOB NOT NULL,
	"ip"	TEXT NOT NULL,
	"port"	INTEGER NOT NULL,
	"uploaded"	INTEGER DEFAULT 0,
	"downloaded"	INTEGER DEFAULT 0,
	"left"	INTEGER DEFAULT 0,
	"is_seed"	BOOLEAN DEFAULT 0,
	"last_announce"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("torrent_id") REFERENCES "torrents"("id"),
	PRIMARY KEY("id" AUTOINCREMENT)
);
CREATE TABLE IF NOT EXISTS "announce_log" (
	"id"	INTEGER,
	"peer_id"	INTEGER NOT NULL,
	"torrent_id"	INTEGER NOT NULL,
	"event"	TEXT,
	"uploaded"	INTEGER,
	"downloaded"	INTEGER,
	"left"	INTEGER,
	"timestamp"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	FOREIGN KEY("peer_id") REFERENCES "peers"("id"),
	PRIMARY KEY("id" AUTOINCREMENT),
	FOREIGN KEY("torrent_id") REFERENCES "torrents"("id")
);
COMMIT;
