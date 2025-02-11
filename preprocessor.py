import re
import pandas as pd
def preprocess(data):
    df = process_chat_data_from_string(data)
    df = process_user_message(df)
    df = extract_datetime_components(df)
    return df


def process_chat_data_from_string(chat_data):
    # Regular expression to match date, time, and message
    pattern = r"(\d{2}/\d{2}/\d{2}, \d{1,2}:\d{2}\s[ap]m) - (.*)"
    
    # Extracting data
    matches = re.findall(pattern, chat_data)
    
    # Creating DataFrame
    df = pd.DataFrame(matches, columns=["DateTime", "Message"])
    
    return df

def process_user_message(df):
    """Function to separate user and message from the given DataFrame."""
    df = df.copy()
    df["User"] = df["Message"].apply(lambda x: x.split(": ", 1)[0] if ": " in x else "Group Notification")
    df["Message"] = df["Message"].apply(lambda x: x.split(": ", 1)[1] if ": " in x else x)
    return df

def extract_datetime_components(df):
    
    df = df.copy()  # Avoid modifying the original DataFrame

    # Replace non-standard spaces with normal spaces
    df["DateTime"] = df["DateTime"].str.replace("\u202F", " ", regex=True)  # Fixes the narrow no-break space issue

    # Convert 'DateTime' column to datetime format
    df["DateTime"] = pd.to_datetime(df["DateTime"], format="%d/%m/%y, %I:%M %p")

    # Extract required details
    df["Day Name"] = df["DateTime"].dt.day_name()
    df["Day"] = df["DateTime"].dt.day
    df["Time"] = df["DateTime"].dt.strftime("%I:%M %p")
    df["Month Name"] = df["DateTime"].dt.month_name()
    df["Year"] = df["DateTime"].dt.year

    return df