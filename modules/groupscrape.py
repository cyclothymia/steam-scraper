import os
import json
import sqlite3
import requests
import xmltodict
from multiprocessing import Pool, Process, freeze_support, set_start_method, get_context
from modules.proxy import workingProxy
from datetime import datetime

class singleGroup:
    def __init__(self):
        self.jsonpath = os.path.join("data", "json", "groups")
        self.txtpath = os.path.join("data", "txt", "groups")
        self.url = "https://steamcommunity.com/groups/"
        self.urlxml = "/memberslistxml/?xml=1"
        self.database = "data/database.db"
    
    def get(self, groupID):
        url = self.url + groupID + self.urlxml
        filepath = os.path.join(self.jsonpath, f"{groupID}.json")
        if os.path.exists(filepath):
            print(f"[-] JSON file already exists for {groupID}")
            return
        try:
            r = requests.get(url)
            if r.status_code == 200:
                xml = r.text
                data = xmltodict.parse(xml)
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"[+] JSON file created for /groups/{groupID}")
                return
            else:
                print(f"[-] Network Error: {r.status_code}")
                return
        except Exception as e:
            print(f"[-] Exception Error: {e}")
            return
    
    def parseJSON(self, groupID):
        groupID = str(groupID)
        jsonfile = os.path.join(self.jsonpath, f"{groupID}.json")
        if os.path.exists(jsonfile):
            with open(jsonfile, "r") as f:
                data = json.load(f)
                return data
        else:
            print(f"[-] JSON file not found for {groupID}")
            return None
    
    def parseJSONVariables(self, groupID):
        groupID = groupID
        txt_path = os.join.path(self.txtpath, f"{groupID}.txt")
        self.get(groupID)
        data = self.parseJSON(groupID)
        if data:
            try:
                base = data['memberList']
                group = data['memberList']['groupDetails']
                groupID64 = base.get('groupID64', None)
                groupName = group.get('groupName', None)
                groupURL = group.get('groupURL', None)
                headline = group.get('headline', None)
                summary = group.get('summary', None)
                avatarIcon = group.get('avatarIcon', None)
                avatarMedium = group.get('avatarMedium', None)
                avatarFull = group.get('avatarFull', None)
                memberCount = group.get('memberCount', None)
                membersInChat = group.get('membersInChat', None)
                membersInGame = group.get('membersInGame', None)
                membersOnline = group.get('membersOnline', None)
                memberCount = base.get('memberCount', None)
                totalPages = base.get('totalPages', None)
                dateScraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                members = data['memberList']['members']['steamID64']
                if not os.path.exists(txt_path):
                    os.makedirs(txt_path)
                    with open(txt_path, "w") as f:
                        for member in members:
                            f.write(member + "\n")
                    print(f"[+] Text file created for /groups/{groupID}")
                
                conn = sqlite3.connect(self.database)
                cursor = conn.cursor()
                sql = """INSERT INTO groups (groupID, groupID64, groupName, groupURL, headline, summary, avatarIcon, avatarMedium, avatarFull, memberCount, membersInChat, membersInGame, membersOnline, totalPages, dateScraped)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(sql, (groupID, groupID64, groupName, groupURL, headline, summary, avatarIcon, avatarMedium, avatarFull, memberCount, membersInChat, membersInGame, membersOnline, totalPages, dateScraped))
                conn.commit()
                print(f"[+] Data inserted into the SQLite database for {groupID}")
            except Exception as e:
                print(f"[-] An Exception Error has occurred for {groupID}: {e}")
                if conn:
                    conn.rollback()
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

class multiGroup:
    def __init__(self):
        self.jsonpath = os.path.join("data", "json", "groups")
        self.txtpath = os.path.join("data", "txt", "groups")
        self.url = "https://steamcommunity.com/groups/"
        self.urlxml = "/memberslistxml/?xml=1"
        self.database = "data/database.db"
    
    def get(self, groupID):
        url = self.url + groupID + self.urlxml
        filepath = os.path.join(self.jsonpath, f"{groupID}.json")
        if os.path.exists(filepath):
            print(f"[-] JSON file already exists for {groupID}")
            return
        try:
            r = requests.get(url)
            if r.status_code == 200:
                xml = r.text
                data = xmltodict.parse(xml)
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"[+] JSON file created for /groups/{groupID}")
                return
            else:
                print(f"[-] Network Error: {r.status_code}")
                return
        except Exception as e:
            print(f"[-] Exception Error: {e}")
            return
    
    def getMulti(self, groupID, page):
        url = self.url + groupID + self.urlxml + f"&p={page}"
        filepath = os.path.join(self.jsonpath, f"{groupID}_{page}.json")
        if os.path.exists(filepath):
            print(f"[-] JSON file already exists for {groupID}_{page}")
            return
        try:
            prox = workingProxy()
            proxy = {
                "http": "http://" + prox
            }
            r = requests.get(url, proxies=proxy, timeout=5)
            if r.status_code == 200:
                xml = r.text
                data = xmltodict.parse(xml)
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"[+] JSON file created for /groups/{groupID}_{page}")
                return
            else:
                print(f"[-] Network Error: {r.status_code}")
                return
        except Exception as e:
            print(f"[-] Exception Error: {e}")
            return
    
    def parseJSON(self, groupID):
        groupID = str(groupID)
        jsonfile = os.path.join(self.jsonpath, f"{groupID}.json")
        if os.path.exists(jsonfile):
            with open(jsonfile, "r") as f:
                data = json.load(f)
                return data
        else:
            print(f"[-] JSON file not found for {groupID}")
            return None
    
    def parseJSONMulti(self, groupID, page):
        groupID = str(groupID)
        jsonfile = os.path.join(self.jsonpath, f"{groupID}_{page}.json")
        if os.path.exists(jsonfile):
            with open(jsonfile, "r") as f:
                data = json.load(f)
                return data
        else:
            print(f"[-] JSON file not found for {groupID}_{page}")
            return None
    
    def parseJSONVariables(self, groupID):
        groupID = groupID
        txt_path = os.join.path(self.txtpath, f"{groupID}.txt")
        page = 1
        self.get(groupID)
        data = self.parseJSON(groupID)
        if data:
            try:
                base = data['memberList']
                group = data['memberList']['groupDetails']
                groupID64 = base.get('groupID64', None)
                groupName = group.get('groupName', None)
                groupURL = group.get('groupURL', None)
                headline = group.get('headline', None)
                summary = group.get('summary', None)
                avatarIcon = group.get('avatarIcon', None)
                avatarMedium = group.get('avatarMedium', None)
                avatarFull = group.get('avatarFull', None)
                memberCount = group.get('memberCount', None)
                membersInChat = group.get('membersInChat', None)
                membersInGame = group.get('membersInGame', None)
                membersOnline = group.get('membersOnline', None)
                memberCount = base.get('memberCount', None)
                totalPages = base.get('totalPages', None)
                dateScraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                conn = sqlite3.connect(self.database)
                cursor = conn.cursor()
                sql = """INSERT INTO groups (groupID, groupID64, groupName, groupURL, headline, summary, avatarIcon, avatarMedium, avatarFull, memberCount, membersInChat, membersInGame, membersOnline, totalPages, dateScraped)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(sql, (groupID, groupID64, groupName, groupURL, headline, summary, avatarIcon, avatarMedium, avatarFull, memberCount, membersInChat, membersInGame, membersOnline, totalPages, dateScraped))
                conn.commit()
                
                while page <= int(totalPages):
                    if not os.path.exists(txt_path):
                        os.makedirs(txt_path)
                    self.getMulti(groupID, page)
                    data = self.parseJSONMulti(groupID, page)
                    members = data['memberList']['members']['steamID64']
                    with open(txt_path, "a") as f:
                        for member in members:
                            f.write(member + "\n")
                    print(f"[+] Text file updated for /groups/{groupID}")
                    page += 1
                print(f"[+] Data inserted into the SQLite database for {groupID}")
            except Exception as e:
                print(f"[-] An Exception Error has occurred for {groupID}: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
