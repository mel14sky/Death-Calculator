import time
from datetime import datetime, timedelta
import os

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

folder = os.path.dirname(os.path.abspath(__file__))

SCOPES = ['https://www.googleapis.com/auth/calendar.events']

def add_to_google_calendar(target_unix_time):
    creds = None
    token_path = os.path.join(folder, 'token.json')
    creds_path = os.path.join(folder, 'credentials.json')

    # token.json stores the user login
    if os.path.exists(token_path):
        creds = Credentials.from_authorized_user_file(token_path, SCOPES)
        
    #if valid credentials, lets user login
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            if not os.path.exists(creds_path):
                print("\n[ERROR] 'credentials.json' not found.")
                print("You must download OAuth client credentials from the Google Cloud Console.")
                return

            flow = InstalledAppFlow.from_client_secrets_file(creds_path, SCOPES)
            creds = flow.run_local_server(port=0)
            
        # Save the credentials for next time
        with open(token_path, 'w') as token:
            token.write(creds.to_json())

    try:
        service = build('calendar', 'v3', credentials=creds)

        # Convert UNIX time to a datetime object
        target_date = datetime.fromtimestamp(target_unix_time)
        
        # Format dates for Google Calendar API (YYYY-MM-DD for all-day events)
        start_date_str = target_date.strftime('%Y-%m-%d')
        # Google Calendar requires the end date to be the day AFTER the event for all-day events
        end_date_str = (target_date + timedelta(days=1)).strftime('%Y-%m-%d') 

        event = {
          'summary': 'You will die on this day 💀',
          'description': 'make the most of the time you have left',
          'start': {
            'date': start_date_str,
          },
          'end': {
            'date': end_date_str,
          },
          'colorId': '11', # Makes the event red
        }

        print("\nAdding event to Google Calendar...")
        event = service.events().insert(calendarId='primary', body=event).execute()
        print(f"Calendar Event created successfully: {event.get('htmlLink')}\n")
        time.sleep(2)

    except Exception as error:
        print(f'An error occurred connecting to Google Calendar: {error}')
        time.sleep(2)

def date2unix(date):
    try:
        dt = datetime.strptime(date, "%d/%m/%Y")
        return int(dt.timestamp())
    except ValueError:
        return None


date = input("enter date? [d/mm/yyyy] ")
unix = date2unix(date)
add_to_google_calendar(unix)
