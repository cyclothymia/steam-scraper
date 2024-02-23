import os
from modules.tables import Table
from modules.groupscrape import singleGroup

if __name__ == "__main__":
    jsonpath = os.path.join("data", "json", "groups")
    if not os.path.exists(jsonpath):
        os.makedirs(jsonpath)

    scraper = singleGroup()
    table = Table()
    groupID = "valve"
    table.create_table()
    scraper.parseJSONVariables(groupID)
