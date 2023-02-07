from __future__ import print_function

import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from apiclient import discovery
from google.oauth2 import service_account
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets.readonly"]

# The ID of a sample document.
SAMPLE_SPREADSHEET_ID = "1IjLE8q79Si2RaajefVRHuPUdqlSvNaN-H7MS3L9thxM"
SAMPLE_RANGE_NAME = "Sheet1!A1:H13"


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


def get_table(sheetId, rangeId):
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
        result = sheet.values().get(spreadsheetId=sheetId, range=rangeId).execute()
        values = result.get("values", [])

        if not values:
            print("No data found.")
            return values

        print(values[1][0])
        for row in values:
            print("\t".join([str(elem) for elem in row[1:]]))
    except HttpError as err:
        print(err)
    return values
