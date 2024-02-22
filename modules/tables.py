from modules.db import Database as db

class Table():
    def __init__(self):
        self.db = db()
        self.sqlGroups = """CREATE TABLE IF NOT EXISTS groups (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        groupID TEXT NOT NULL UNIQUE,
                        groupID64 TEXT NOT NULL,
                        groupName TEXT,
                        groupURL TEXT,
                        headline TEXT,
                        summary TEXT,
                        avatarIcon TEXT,
                        avatarMedium TEXT,
                        avatarFull TEXT,
                        memberCount INTEGER,
                        membersInChat INTEGER,
                        membersInGame INTEGER,
                        membersOnline INTEGER,
                        membersTotal INTEGER,
                        totalPages INTEGER,
                        dateScraped TEXT
                    );"""
        self.sqlUsers = """CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    steamID64 TEXT NOT NULL UNIQUE,
                    steamID TEXT NOT NULL,
                    onlineState TEXT,
                    stateMessage TEXT,
                    privacyState TEXT,
                    visibilityState INTEGER,
                    avatarIcon TEXT,
                    avatarMedium TEXT,
                    avatarFull TEXT,
                    hoursPlayed2Wk FLOAT,
                    vacBanned TEXT,
                    tradeBanState TEXT,
                    isLimitedAccount TEXT,
                    customURL TEXT,
                    memberSince TEXT,
                    realName TEXT,
                    location TEXT,
                    summary TEXT,
                    dateScraped TEXT
                );"""
    
    def check(self):
        self.db.check()

    def create_table(self):
        self.db.create_db()
        self.db.create_table(self.sqlGroups)
        self.db.create_table(self.sqlUsers)
