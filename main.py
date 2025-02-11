import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import Preprocess_data
import Calculation
import seaborn as sns


st.sidebar.title("Whatsapp Chat Analyzer")

upload_file=st.sidebar.file_uploader("Upload a file")
if upload_file is not None:
    bytes_data=upload_file.getvalue()
    data=bytes_data.decode('utf-8')
    # st.text(data)

    df=Preprocess_data.preprocess(data)
    st.dataframe(df)
    user_detail=df["User_Name"].unique().tolist()

    if "group_notification" in user_detail:
        user_detail.remove("group_notification")

    user_detail.insert(0,"OverAll")
    selected_user=st.sidebar.selectbox("Analysis",user_detail)

    if st.sidebar.button("Analyze"):

        num_message,words,media,links=Calculation.calculations(selected_user,df)

        col1, col2, col3,col4=st.columns(4)

        with col1:
            st.header("Total Messages")
            st.title(num_message)
        with col2:
            st.header("Total Words")
            st.title(words)
        with col3:
            st.header("Media Files")
            st.title(media)
        with col4:
            st.header("Total Links")
            st.title(links)

        if selected_user=="OverAll":
          st.title("Most Busy")
          col1,col2=st.columns(2)

          busy,new_df=Calculation.busy_person(df)

          fig,axes=plt.subplots()

          with col1:
           axes.bar(busy.index,busy.values,color="#7f7f7f")
           plt.xticks(rotation=50)
           st.pyplot(fig)
          with col2:
           st.dataframe(new_df)

          st.title("Most Media")
          df_media = Calculation.media(selected_user, df)

          col1, col2 = st.columns(2)
          with col1:
               fig, ax = plt.subplots(figsize=(8, 6))
               sns.barplot(x=df_media["User_Name"], y=df_media["Message"], palette="viridis")
               plt.xticks(rotation=50, weight="bold")
               ax.set_ylabel([])
               st.pyplot(fig)

        st.title("Most Use Words")
        wc_df=Calculation.most_use_words(selected_user,df)
        plt.figure(figsize=(8, 8))
        plt.imshow(wc_df, interpolation="bilinear")
        plt.axis("off")
        st.pyplot(plt)

        st.title("Most Common Words")
        col1,col2=st.columns(2)
        with col1:
          df_m_c_w=Calculation.most_common_words(selected_user,df)
          st.dataframe(df_m_c_w)
        with col2:
          plt.figure(figsize=(8, 8))
          plt.barh(df_m_c_w[0],df_m_c_w[1],color="#B87333")
          plt.xticks(weight="bold")
          plt.yticks(weight="bold")
          st.pyplot(plt)


        st.title("Time Analysis")
        col1, col2 = st.columns(2)
        df_date_time,day,hour,df_am = Calculation.date_time(selected_user, df)
        with col1:
          plt.figure(figsize=(8, 8))
          plt.plot(df_date_time["month_year"],df_date_time["Message"],color="#7f7f7f",marker="o")
          plt.xticks(rotation=50,weight="bold")
          st.pyplot(plt)
        with col2:
           plt.figure(figsize=(8, 8))
           plt.bar(day["Day_Name"],day["Message"], color="#C0C0C0",)
           plt.xticks(rotation=50,weight="bold")
           st.pyplot(plt)


        st.title("Most Busy Hours")
        plt.figure(figsize=(6,3))
        sns.heatmap(hour)
        plt.xticks(rotation=50,weight="bold")
        st.pyplot(plt)


        st.title("AM vs PM Activity Levels")
        col1,col2=st.columns(2)
        with col1:
         fig,ax=plt.subplots()
         l=["pm","am"]
         ax.pie(df_am["average"],labels=l,autopct="%1.1f%%")
         st.pyplot(fig)
















