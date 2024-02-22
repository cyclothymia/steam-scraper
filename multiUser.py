import os
from multiprocessing import Pool, Process, freeze_support, set_start_method, get_context
from modules.tables import Table
from modules.userscrape import multiUser

if __name__ == "__main__":
    freeze_support()
    jsonpath = "data/json/users/"
    if not os.path.exists(jsonpath):
        os.makedirs(jsonpath)
    
    table = Table()
    table.create_table()
    scraper = multiUser()
    file_path = "steamids.txt"
    with open(file_path) as steamIDs:
        lines = steamIDs.readlines()
    pool = Pool(processes=100)
    pool.map(scraper.parseJSONVariables, lines)