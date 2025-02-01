import os
import json
import google.oauth2.credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# Google Fit API Scopes
SCOPES = ['https://www.googleapis.com/auth/fitness.activity.read']

# Load credentials from JSON
def authenticate_google_fit():
    creds = None
    if os.path.exists('token.json'):
        creds = google.oauth2.credentials.Credentials.from_authorized_user_file('token.json', SCOPES)
    
    if not creds or not creds.valid:
        flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
        creds = flow.run_local_server(port=0)
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return creds

# Fetch Google Fit Data
def get_fit_data():
    creds = authenticate_google_fit()
    service = build('fitness', 'v1', credentials=creds)
    
    # Get Step Count
    dataset_id = f"{int((24 * 60 * 60 * 1000000000) * -1)}-{int(0)}"
    data_source = "derived:com.google.step_count.delta:com.google.android.gms:estimated_steps"

    request = service.users().dataset().aggregate(userId="me", body={
        "aggregateBy": [{"dataTypeName": "com.google.step_count.delta"}],
        "bucketByTime": {"durationMillis": 86400000},
        "startTimeMillis": int(0),
        "endTimeMillis": int(0)
    })

    response = request.execute()
    steps = response['bucket'][0]['dataset'][0]['point'][0]['value'][0]['intVal'] if response['bucket'] else 0

    return steps

# Get Steps Example
if __name__ == "__main__":
    steps = get_fit_data()
    print(f"Today's Steps: {steps}")
