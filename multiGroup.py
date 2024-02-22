import os
from modules.tables import Table
from modules.groupscrape import multiGroup

if __name__ == "__main__":
    jsonpath = "data/json/groups/"
    if not os.path.exists(jsonpath):
        os.makedirs(jsonpath)
    
    scraper = multiGroup()
    table = Table()
    groupID = "hentaii"
    table.create_table()
    scraper.parseJSONVariables(groupID)