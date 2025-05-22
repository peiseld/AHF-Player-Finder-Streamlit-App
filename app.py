import streamlit as st
import pandas as pd

# Load your CSV file
df = pd.read_csv('ahf_player_stats.csv')  # Replace with your actual file name

# Clean column names (optional but helpful)
df.columns = [col.strip() for col in df.columns]

# Set up the Streamlit app
st.title("AHF Player Finder")

# Search by Player Name
st.header("🔍 Search by Player Name")
player_name = st.text_input("Enter Player Name (partial or full)")

if player_name:
    results = df[df['Player Name'].str.contains(player_name, case=False, na=False)]
    if not results.empty:
        st.write("### Results:")
        st.dataframe(results[['Player Name', 'Team', 'Jersey Number']])
    else:
        st.warning("No matching player found.")

# Search by Jersey Number and Team
st.header("🔍 Search by Jersey Number and Team")
team_name = st.text_input("Enter Team Name")
jersey_number = st.text_input("Enter Jersey Number")

if team_name and jersey_number:
    try:
        jersey_number = int(jersey_number)
        results = df[
            (df['Team'].str.contains(team_name, case=False, na=False)) &
            (df['Jersey Number'] == jersey_number)
        ]
        if not results.empty:
            st.write("### Player Found:")
            st.dataframe(results[['Player Name', 'Team', 'Jersey Number']])
        else:
            st.warning("No player found with that jersey number on that team.")
    except ValueError:
        st.error("Please enter a valid number for the jersey.")

