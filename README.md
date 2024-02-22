# Steam Scraper Project

## Introduction

The Steam Scraper Project is designed to efficiently scrape data from a user profile or group page, and to aggregate data from multiple users and groups in to a singular database stored on the local system.

*NOTE:* The scripts that have multithreading utilised in them require proxies to be put in the `proxies.txt` file. This is to circumvent IP rate limiting as Steam are known to rate limit after a small amount of automated requests.

## Features

| Python Script | Description |
| --------- | ---------------- |
| `singleUser.py` | Get detailed information on a single Steam user's profile. |
| `multiUser.py` | Collect data on multiple users simultaneously from a list. |
| `singleGroup.py` | Extract information from a specific Steam group. |
| `multiGroup.py` | Aggregate data from a Steam group and get a list of members SteamID64 from every additional page of the group. |


## Prerequisites

Before you get started, ensure you have the following installed:

    Python 3.8 or higher
    Pip for Python 3
    Virtualenv (optional, but recommended for managing dependencies)
    requests (from pip)
    xmltodict (from pip)

## Installation

Clone the repository to your local machine:

    git clone https://github.com/cyclothymia/steam-scraper.git

Navigate into the cloned directory:

    cd steam-scraper

*(Optional)* Create and activate a virtual environment:

    virtualenv venv
    source venv/bin/activate  # On Windows, use `venv\Scripts\activate`

Install the required Python packages:

    pip install -r requirements.txt

## Usage

In each individual python script, change the target SteamID or GroupID, then run the needed script for whatever individual purpose you have.
