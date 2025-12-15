# email_utils.py
import requests
from datetime import datetime, timedelta
import streamlit as st

def fetch_emails(access_token: str, date_str: str):
    """Fetch emails from Microsoft Graph API for the given date."""
    url = "https://graph.microsoft.com/v1.0/me/messages"
    headers = {"Authorization": f"Bearer {access_token}"}
    
    target_date = datetime.strptime(date_str, "%Y-%m-%d")
    start_of_day = target_date.isoformat() + "Z"
    end_of_day = (target_date + timedelta(days=1)).isoformat() + "Z"
    
    params = {
        "$filter": f"receivedDateTime ge {start_of_day} and receivedDateTime lt {end_of_day}",
        "$select": "subject,bodyPreview,receivedDateTime,from",
        "$top": 100
    }

    try:
        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()
        emails = data.get("value", [])
        st.success(f"Fetched {len(emails)} emails.")
        return emails
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to fetch emails: {e}")
        return []
