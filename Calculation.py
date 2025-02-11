import re
from wordcloud import WordCloud
from collections import Counter
import pandas as pd


def calculations(selected_user,df):

   if selected_user!="OverAll":
       df=df[df["User_Name"]==selected_user]

   total_messages = df.shape[0]

   words = []
   for message in df["Message"]:
       words.extend(message.split())

   count=0
   for message in df["Message"]:
       if message.strip() == "<Media omitted>":
           count+=1
           #print(repr(message))

   links=[]
   for message in df["Message"]:
       links.extend(re.findall(r'https://\S+',message))


   return total_messages, len(words),count,len(links)

def busy_person(df):
    busy=df["User_Name"].value_counts().head(5)
    new_df=round(df["User_Name"].value_counts()*100/df.shape[0],2).reset_index().rename(
           columns={"User_Name":"Name","count":"Percentage"})
    return busy,new_df

def most_use_words(selected_user,df):
    if selected_user!="OverAll":
        df=df[df["User_Name"]==selected_user]
    text = df["Message"].str.cat(sep=" ")
    word_cloud=WordCloud(width=400, height=400,background_color="white")
    df_wc=word_cloud.generate(text)
    return df_wc

def most_common_words(selected_user,df):
    if selected_user!="OverAll":
       df=df[df["User_Name"]==selected_user]

    temp = df[df["User_Name"] != "group_notification"]
    temp = df[df["Message"] != "<Media omitted>\n"]

    file1 = open(r"stop_hinglish.txt")
    file2 = open(r"english_stop_words.txt")

    d1 = file1.read()
    d2 = file2.read()

    words = []
    for message in temp["Message"]:
        for word in message.lower().split():
            if word not in d1:
                if word not in d2:
                    words.append(word)

    return pd.DataFrame(Counter(words).most_common(20))

def date_time(selected_user,df):
    if selected_user!="OverAll":
       df=df[df["User_Name"]==selected_user]

    df["month_num"] = df["Date"].dt.month
    time_line = df.groupby(["Year", "month_num", "Month"]).count()["Message"].reset_index()

    time = []
    for i in range(time_line.shape[0]):
        time.append(time_line["Month"][i] + "-" + str(time_line["Year"][i]))

    time_line["month_year"]=time
    day = df.groupby("Day_Name").count()["Message"].reset_index()


    periods=[]
    for i in df["Hour"]:
        if i == 12:
            periods.append(str(i) + "-" + str(00))
        else:
            periods.append(str(i) + "-" + str(i + 1))
    df["periods"]=periods
    most_busy_hour=df.pivot_table(index="Day_Name",columns="periods",values="Message",aggfunc="count").fillna(0)

    df_am= pd.DataFrame(df["am/pm"].value_counts())
    df_am["average"]=round(df_am["count"] * 100/df_am["count"].sum(),2)

    return time_line,day,most_busy_hour,df_am


def media(selected_user,df):
    df =df[df["Message"] == "<Media omitted>\n"]
    df_media = df.groupby(["User_Name"])["Message"].count().reset_index()
    df_media.sort_values(by="Message", ascending=False,inplace=True)
    df_media=df_media.head(5)
    return df_media





