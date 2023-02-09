from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import discovery
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError
from config import Config

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID of a sample document.
SPREADSHEET_ID = Config.SPREADSHEET_ID
RANGE_NAME = Config.RANGE_NAME


def connect(creds):
    """
    Prepare Resource object with methods
    for interacting with the Google Sheets API.
    """
    try:
        service = build("sheets", "v4", credentials=creds)
        return service
    except HttpError as err:
        print(err)
        return None


def get_table(sheetId, rangeName):
    """
    Prints timetable colums.
    """
    values = None
    creds = None
    # The file service_account.json stores the special service acc access token
    if os.path.exists("service_account.json"):
        creds = service_account.Credentials.from_service_account_file(
            "service_account.json", scopes=SCOPES
        )
    else:
        print("No credentials was provided")
        return values
    service = connect(creds)
    if not service:
        print("Connection error")
        return values
    try:
        # Call the Sheets API
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheetId, range=rangeName).execute()
        values = result.get("values", [])

        if not values:
            print("No data found.")

    except HttpError as err:
        print(err)
    return values


def parse_timetable(tableData):
    """Convert raw rows to timetable dict.

    Args:
        tableData (list): Raw Sheet data.

    Returns:
        dict: Timetable structured dict.
    """
    print("Header: %s" % tableData[0][0])
    for row in tableData[1:]:
        print("\t".join([str(elem) for elem in row]))

    table = {}
    for item in tableData[1]:
        table[item] = None
        c = tableData[1].index(item)
        table[item] = list(
            filter(
                lambda x: x != "",
                [str(tableData[r][c]) for r in range(2, len(tableData))],
            )
        )
    return {tableData[0][0]: table}


def request_sheets(sheetId=SPREADSHEET_ID, rangeName=RANGE_NAME):
    """Requests and parse data form sheet.

    Args:
        sheetId (str): Google Sheet ID. Defaults to SPREADSHEET_ID.
        rangeName (str): Range of cells. Defaults to RANGE_NAME.

    Returns:
        dict: Parsed timetable.
    """
    raw_table = get_table(sheetId, rangeName)
    return parse_timetable(raw_table)
