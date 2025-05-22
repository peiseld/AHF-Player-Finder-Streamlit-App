import streamlit as st
import requests
from bs4 import BeautifulSoup
import re

# --- Configuration ---
TEAM_ROSTER_URLS = {
    "Team A": "https://gamesheetstats.com/seasons/9319/teams/340709/roster?configuration%5Bfilters%5D=false&configuration%5Binfinite-scroll%5D=false&configuration%5Blogo%5D=false&configuration%5Bnavigation%5D=false&configuration%5Bprimary-colour%5D=%23febe10&configuration%5Bsecondary-colour%5D=%23e22726&filter%5Bdivision%5D=52538%2C52447%2C52412%2C52435",
    "Team B": "https://gamesheetstats.com/seasons/9319/teams/340713/roster?configuration%5Bfilters%5D=false&configuration%5Binfinite-scroll%5D=false&configuration%5Blogo%5D=false&configuration%5Bnavigation%5D=false&configuration%5Bprimary-colour%5D=%23febe10&configuration%5Bsecondary-colour%5D=%23e22726&filter%5Bdivision%5D=52538%2C52447%2C52412%2C52435",
    "Team C": "https://gamesheetstats.com/seasons/9319/teams/340716/roster?configuration%5Bfilters%5D=false&configuration%5Binfinite-scroll%5D=false&configuration%5Blogo%5D=false&configuration%5Bnavigation%5D=false&configuration%5Bprimary-colour%5D=%23febe10&configuration%5Bsecondary-colour%5D=%23e22726&filter%5Bdivision%5D=52538%2C52447%2C52412%2C52435"
}

# --- Streamlit UI ---
st.title("🔎 AHF Player Finder")
search_name = st.text_input("Enter a player's name (partial or full):")

# --- Main logic ---
if search_name:
    search_results = []
    pattern = re.compile(search_name, re.IGNORECASE)

    for team_name, url in TEAM_ROSTER_URLS.items():
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, "html.parser")
            roster_table = soup.find("table")
            if roster_table:
                players = roster_table.find_all("tr")[1:]  # skip header
                for player in players:
                    cols = player.find_all("td")
                    if cols:
                        player_name = cols[0].text.strip()
                        if pattern.search(player_name):
                            search_results.append({
                                "Player": player_name,
                                "Team": team_name,
                                "Roster URL": url
                            })

    if search_results:
        st.success(f"Found {len(search_results)} result(s):")
        for result in search_results:
            st.markdown(f"- **{result['Player']}** on **{result['Team']}** [🔗 View Roster]({result['Roster URL']})")
    else:
        st.warning("No matches found.")
else:
    st.info("Enter a name above to begin searching.")
