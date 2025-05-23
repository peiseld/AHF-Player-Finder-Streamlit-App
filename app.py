import streamlit as st
import pandas as pd

# Load your CSV file
df = pd.read_csv('player_list_2425.csv')  # Replace with your actual file name

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

# Search by Jersey Number and Team with partial + dropdown
st.header("🔍 Search by Jersey Number and Team")

# User types part of a team name
partial_team = st.text_input("Type part of the team name to filter:")

# Get unique teams, filter if user typed something
teams = df['Team'].dropna().unique()
if partial_team:
    filtered_teams = [team for team in teams if partial_team.lower() in team.lower()]
else:
    filtered_teams = sorted(teams)

# Dropdown of matching teams
selected_team = st.selectbox("Select Team", filtered_teams)

# Jersey number input
jersey_number = st.text_input("Enter Jersey Number")

# Search logic
if selected_team and jersey_number:
    results = df[
        df['Team'].str.lower() == selected_team.lower() &
        df['Jersey Number'].astype(str).str.contains(jersey_number.strip(), na=False)
    ]
    if not results.empty:
        st.write("### Matching Players:")
        st.dataframe(results[['Player Name', 'Team', 'Jersey Number']])
    else:
        st.warning("No player found with that jersey number on that team.")
