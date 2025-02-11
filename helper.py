import streamlit as st
import pandas as pd
from wordcloud import WordCloud
import matplotlib.pyplot as plt
import emoji
from collections import Counter
import re
import sys
sys.stdout.reconfigure(encoding='utf-8')


def fetch_stats(df,selected_user):
    Total_msgs = get_total_messages(df, selected_user)
    Total_media = get_total_media_messages(df, selected_user)
    Total_link = get_total_links(df, selected_user)
    return Total_msgs,Total_media,Total_link

def get_total_messages(df, selected_user):
    """Returns the total number of messages sent by the selected user."""
    if selected_user == "Overall":
        return df.shape[0]  # Total rows = total messages
    else:
        return df[df["User"] == selected_user].shape[0]

def get_total_media_messages(df, selected_user):
    """Returns the total number of media messages sent by the selected user."""
    media_messages = df[df["Message"] == "<Media omitted>"]  # Assuming media messages are stored as '<Media omitted>'
    
    if selected_user == "Overall":
        return media_messages.shape[0]
    else:
        return media_messages[media_messages["User"] == selected_user].shape[0]

def get_total_links(df, selected_user):
    """Returns the total number of links sent by the selected user."""
    link_messages = df[df["Message"].str.contains("http", na=False, regex=True)]  # Detect messages containing 'http'
    
    if selected_user == "Overall":
        return link_messages.shape[0]
    else:
        return link_messages[link_messages["User"] == selected_user].shape[0]

def generate_wordcloud(df, selected_user):
    if selected_user != "Overall":
        df = df[df['User'] == selected_user]  # Filter messages for the selected user

    words = []
    for msg in df['Message']:
        words.extend(msg.split())

    # Clean words: remove <, >, ' and filter out 'media' & 'omitted'
    words = [re.sub(r"[<>']", "", word) for word in words]  # Remove <, >, and '
    words = [word for word in words if word.lower() not in ['media', 'omitted']]  # Remove unwanted words

    text = " ".join(words)
    wordcloud = WordCloud(
        width=1000,  # Increased width
        height=1000,  # Make it square
        background_color="black",
        colormap="coolwarm",
        max_words=200,
        contour_color='white',
        contour_width=2
    ).generate(text)

    # Display the word cloud
    fig, ax = plt.subplots(figsize=(10, 10))  # Make figure square
    ax.imshow(wordcloud, interpolation='bilinear')
    ax.axis("off")
    
    st.pyplot(fig)

def generate_emoji_pie_chart(messages):
    all_emojis = []
    
    # Extract emojis from messages
    for msg in messages:
        all_emojis.extend([char for char in msg if emoji.is_emoji(char)])
    
    # Count the occurrences of each emoji
    emoji_counts = Counter(all_emojis)
    
    # Get the top 5 most used emojis
    top_5_emojis = emoji_counts.most_common(5)

    if not top_5_emojis:
        st.warning("No emojis found in the messages!")
        return

    # Separate labels and values for the pie chart
    labels, values = zip(*top_5_emojis)

    # Define modern color palette
    colors = ['#FF5733', '#33FF57', '#3357FF', '#FF33A8', '#FFC300']

    # Create a pie chart with better design
    fig, ax = plt.subplots(figsize=(8, 8))
    wedges, texts, autotexts = ax.pie(
        values, labels=labels, autopct='%1.1f%%', startangle=140, colors=colors,
        wedgeprops={'edgecolor': 'black', 'linewidth': 1.5},  # Add border to slices
        textprops={'fontsize': 14, 'weight': 'bold'},  # Improve text visibility
        pctdistance=0.85  # Adjust position of percentage labels
    )

    # Add a white circle at the center to make a donut chart
    center_circle = plt.Circle((0, 0), 0.60, fc='white')
    fig.gca().add_artist(center_circle)

    # Add title with emoji icon
    ax.set_title("🔥 Top 5 Most Used Emojis 🔥", fontsize=16, fontweight='bold', color='#333')

    # Improve pie chart appearance
    plt.setp(autotexts, size=14, weight="bold", color="white")

    # Display in Streamlit
    st.pyplot(fig)

    