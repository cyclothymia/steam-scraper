import os
from modules.tables import Table
from modules.groupscrape import multiGroup

if __name__ == "__main__":
    jsonpath = os.path.join("data", "json", "users")
    if not os.path.exists(jsonpath):
        os.makedirs(jsonpath)
    
    scraper = multiGroup()
    table = Table()
    groupID = "ENTER GROUP ID HERE"
    table.create_table()
    scraper.parseJSONVariables(groupID)
