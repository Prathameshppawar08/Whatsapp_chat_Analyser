import streamlit as st
import preprocessor , helper
import re
# Sidebar
st.sidebar.title("📊 Analyse your chats")
st.sidebar.subheader("By Pratham")
st.sidebar.subheader("Upload your chat file")

# File uploader
uploaded_file = st.sidebar.file_uploader("Choose a file", type=["txt", "csv"])

if uploaded_file:
    st.sidebar.success("File uploaded successfully! ✅")
    bytes_data = uploaded_file.getvalue()
    data = bytes_data.decode("utf-8")
    df = preprocessor.preprocess(data)
    
    total_messages = df.shape[0]  # 🔹 Added line
    st.markdown("<p style='font-size:24px; font-weight:bold;'>Overall Messages</p>", unsafe_allow_html=True)

    st.dataframe(df)

    # Fetching the users
    unique_users = df['User'].unique().tolist()
    unique_users.remove('Group Notification')
    unique_users.sort()
    unique_users.insert(0,"Overall")

    selected_user = st.sidebar.selectbox("Select User to be analysed" , unique_users)
    if selected_user == "Overall":
        filtered_df = df[['User', 'Message']]
    else:
        filtered_df = df[df['User'] == selected_user][['User', 'Message']]
    
    st.dataframe(filtered_df)  # Display only the selected user's messages


    if st.sidebar.button("Show Analysis"):
        Total_msgs, Total_media, Total_links = helper.fetch_stats(df, selected_user)

        st.markdown("""
            <style>
                .stat-box {
                    text-align: center;
                    padding: 20px;
                    border-radius: 10px;
                    box-shadow: 2px 2px 10px rgba(0, 0, 0, 0.1);
                    font-size: 20px;
                    font-weight: bold;
                    color: white;
                }
                .messages { background-color: #FF6B6B; }
                .media { background-color: #1E90FF; }
                .links { background-color: #28A745; }
            </style>
        """, unsafe_allow_html=True)

        col1, col2, col3 = st.columns(3)

        with col1:
            st.markdown(f'<div class="stat-box messages">📩<br>Total Messages<br><h2>{Total_msgs}</h2></div>', unsafe_allow_html=True)

        with col2:
            st.markdown(f'<div class="stat-box media">📸<br>Total Media Shared<br><h2>{Total_media}</h2></div>', unsafe_allow_html=True)

        with col3:
            st.markdown(f'<div class="stat-box links">🔗<br>Links Shared<br><h2>{Total_links}</h2></div>', unsafe_allow_html=True)


       # Extract words from messages
        words = []
        for msg in df['Message']:
            words.extend(msg.split())
        words = [re.sub(r"[<>']", "", word) for word in words]  # Remove <, >, and '
        words = [word for word in words if word.lower() not in ['media', 'omitted']]

        st.subheader("📌 Word Cloud - Most Frequent Words")
        helper.generate_wordcloud(df, selected_user)
        
        helper.generate_emoji_pie_chart(df["Message"])