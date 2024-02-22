import os
import json
import sqlite3
import requests
import xmltodict
from multiprocessing import Pool, Process, freeze_support, set_start_method, get_context
from modules.proxy import workingProxy
from datetime import datetime

class singleUser:
    def __init__(self):
        self.jsonpath = "data/json/users/"
        self.url = "https://steamcommunity.com/id/"
        self.urlID = "https://steamcommunity.com/profiles/"
        self.urlxml = "?xml=1"
        self.database = "data/database.db"
    
    def get(self, steamID):
        if steamID.isdigit():
            url = self.urlID + steamID + self.urlxml
        else:
            url = self.url + steamID + self.urlxml
        
        filepath = f"{self.jsonpath}{steamID}.json"
        if os.path.exists(filepath):
            print(f"[-] JSON file already exists for {steamID}")
            return
        try:
            r = requests.get(url)
            if r.status_code == 200:
                xml = r.text
                data = xmltodict.parse(xml)
                with open(filepath, "w") as f:
                    json.dump(data, f, indent=4)
                print(f"[+] JSON file created for /id/{steamID}")
                return
            else:
                print(f"[-] Network Error: {r.status_code}")
                return
        except Exception as e:
            print(f"[-] Exception Error: {e}")
            return
    
    def parseJSON(self, steamID):
        steamID = str(steamID)
        jsonfile = os.path.join(self.jsonpath, f"{steamID}.json")
        if os.path.exists(jsonfile):
            with open(jsonfile, "r") as f:
                data = json.load(f)
                return data
        else:
            print(f"[-] JSON file not found for {steamID}")
            return None
    
    def parseJSONVariables(self, steamID):
        steamID = steamID
        self.get(steamID)
        data = self.parseJSON(steamID)
        if data:
            try:
                profile = data['profile']
                steamID64 = profile.get('steamID64', None)
                steamID = profile.get('steamID', None)
                onlineState = profile.get('onlineState', None)
                stateMessage = profile.get('stateMessage', None)
                privacyState = profile.get('privacyState', None)
                visibilityState = profile.get('visibilityState', None)
                avatarIcon = profile.get('avatarIcon', None)
                avatarMedium = profile.get('avatarMedium', None)
                avatarFull = profile.get('avatarFull', None)
                hoursPlayed2Wk = profile.get('hoursPlayed2Wk', None)
                vacBanned = profile.get('vacBanned', None)
                tradeBanState = profile.get('tradeBanState', None)
                isLimitedAccount = profile.get('isLimitedAccount', None)
                customURL = profile.get('customURL', None)
                memberSince = profile.get('memberSince', None)
                realName = profile.get('realname', None)
                location = profile.get('location', None)
                summary = profile.get('summary', None)
                dateScraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                
                conn = sqlite3.connect(self.database)
                cursor = conn.cursor()
                sql = """INSERT INTO users (steamID64, steamID, onlineState, stateMessage, privacyState, visibilityState, avatarIcon, avatarMedium, avatarFull, hoursPlayed2Wk, vacBanned, tradeBanState, isLimitedAccount, customURL, memberSince, realName, location, summary, dateScraped) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(sql, (steamID64, steamID, onlineState, stateMessage, privacyState, visibilityState, avatarIcon, avatarMedium, avatarFull, hoursPlayed2Wk, vacBanned, tradeBanState, isLimitedAccount, customURL, memberSince, realName, location, summary, dateScraped))
                conn.commit()
                print(f"[+] Data inserted into the SQLite database for {steamID}")
            except Exception as e:
                print(f"[-] An Exception Error has occurred for {steamID}: {e}")
                if conn:
                    conn.rollback()
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()

class multiUser:
    def __init__(self):
        self.jsonpath = "data/json/users/"
        self.url = "https://steamcommunity.com/id/"
        self.urlID = "https://steamcommunity.com/profiles/"
        self.urlxml = "?xml=1"
        self.database = "data/database.db"

    def get(self, steamID):
        if steamID.isdigit():
            url = self.urlID + steamID + self.urlxml
        else:
            url = self.url + steamID + self.urlxml
        
        filepath = f"{self.jsonpath}{steamID}.json"
        if os.path.exists(filepath):
            print(f"[-] JSON file already exists for {steamID}")
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
                if steamID.isdigit():
                    print(f"[+] JSON file created for /profiles/{steamID}")
                else:
                    print(f"[+] JSON file created for /id/{steamID}")
                return
            else:
                print(f"[-] Network Error: {r.status_code}")
                return
        except Exception as e:
            print(f"[-] Exception Error: {e}")
            return
    
    def parseJSON(self, steamID):
        steamID = str(steamID)
        jsonfile = os.path.join(self.jsonpath, f"{steamID}.json")
        if os.path.exists(jsonfile):
            with open(jsonfile, "r") as f:
                data = json.load(f)
                return data
        else:
            print(f"[-] JSON file not found for {steamID}")
            return None

    def parseJSONVariables(self, line):
        steamID = line.strip()
        self.get(steamID)
        data = self.parseJSON(steamID)
        if data:
            try:
                profile = data['profile']
                steamID64 = profile.get('steamID64', None)
                steamID = profile.get('steamID', None)
                onlineState = profile.get('onlineState', None)
                stateMessage = profile.get('stateMessage', None)
                privacyState = profile.get('privacyState', None)
                visibilityState = profile.get('visibilityState', None)
                avatarIcon = profile.get('avatarIcon', None)
                avatarMedium = profile.get('avatarMedium', None)
                avatarFull = profile.get('avatarFull', None)
                hoursPlayed2Wk = profile.get('hoursPlayed2Wk', None)
                vacBanned = profile.get('vacBanned', None)
                tradeBanState = profile.get('tradeBanState', None)
                isLimitedAccount = profile.get('isLimitedAccount', None)
                customURL = profile.get('customURL', None)
                memberSince = profile.get('memberSince', None)
                realName = profile.get('realname', None)
                location = profile.get('location', None)
                summary = profile.get('summary', None)
                dateScraped = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

                conn = sqlite3.connect(self.database)
                cursor = conn.cursor()
                sql = """INSERT INTO users (steamID64, steamID, onlineState, stateMessage, privacyState, visibilityState, avatarIcon, avatarMedium, avatarFull, hoursPlayed2Wk, vacBanned, tradeBanState, isLimitedAccount, customURL, memberSince, realName, location, summary, dateScraped) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"""
                cursor.execute(sql, (steamID64, steamID, onlineState, stateMessage, privacyState, visibilityState, avatarIcon, avatarMedium, avatarFull, hoursPlayed2Wk, vacBanned, tradeBanState, isLimitedAccount, customURL, memberSince, realName, location, summary, dateScraped))
                conn.commit()
                print(f"[+] Data inserted into the SQLite database for {steamID}")
            except Exception as e:
                print(f"[-] An Exception Error has occurred for {steamID}: {e}")
            finally:
                if cursor:
                    cursor.close()
                if conn:
                    conn.close()
