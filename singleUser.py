import os
from modules.tables import Table
from modules.userscrape import singleUser

if __name__ == "__main__":
    jsonpath = "data/json/users/"
    if not os.path.exists(jsonpath):
        os.makedirs(jsonpath)

    scraper = singleUser()
    table = Table()
    steamID = "khmora"
    table.create_table()
    scraper.parseJSONVariables(steamID)