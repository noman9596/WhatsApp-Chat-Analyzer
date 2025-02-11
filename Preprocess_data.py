import re
import pandas as pd

def preprocess(data):
    #                    02/10/2020, 2:28 am - Darshan Rander (TSEC, IT): Yup
    pattern_of_text = r"\d{1,2}/\d{1,2}/\d{2,4},\s\d{1,2}:\d{2}\s[APap][mM]\s-\s"

    # Returns a list where the string has been split at each match
    message = re.split(pattern_of_text, data)[1:]

    # Returns a list containing all matches
    dates = re.findall(pattern_of_text, data)
    am_pm = []
    for i in dates:
        am_pm.append(re.findall(r"\b(am|pm)\b", i))
    df_am = pd.DataFrame(am_pm)
    df_am.rename(columns={0:"am-pm"}, inplace=True)


    df = pd.DataFrame({"Date": dates})
    # '26/01/2020, 4:19 pm - '
    df['Date'] = pd.to_datetime(df['Date'], format='%d/%m/%Y, %H:%M %p - ')

    user = []
    messages = []
    for i in message:
        # Split based on pattern
        split = re.split(r'([\w\W]+?):\s', i)
        if len(split) > 1:
            user.append(split[1])
            messages.append(split[2])
        else:
            user.append("group_notification")
            messages.append(split[0])

    df['User_Name'] = user
    df['Message'] = messages

    df["Hour"] = df["Date"].dt.hour
    df["Minute"] = df["Date"].dt.minute
    df["am/pm"]=df_am["am-pm"]
    df['Day_Name'] = df['Date'].dt.day_name()
    df["Day"] = df["Date"].dt.day
    df["Month"] = df["Date"].dt.month_name()
    df["Year"] = df["Date"].dt.year

    return df


