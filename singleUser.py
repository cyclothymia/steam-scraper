import os
from modules.tables import Table
from modules.userscrape import singleUser

if __name__ == "__main__":
    jsonpath = os.path.join("data", "json", "groups")
    if not os.path.exists(jsonpath):
        os.makedirs(jsonpath)

    scraper = singleUser()
    table = Table()
    steamID = "ENTER STEAM ID HERE"
    table.create_table()
    scraper.parseJSONVariables(steamID)
