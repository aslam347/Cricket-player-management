import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt

API_URL = "http://127.0.0.1:8000"

# -------------------- SIMPLE LOGIN SYSTEM --------------------
def login():
    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "1234":
            st.session_state["logged_in"] = True
            st.success("Login Successful ✅")
        else:
            st.error("Invalid username or password ❌")


if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

if not st.session_state["logged_in"]:
    login()
    st.stop()

# -------------------- MAIN APP --------------------

st.title("🏏 IPL Player Management Dashboard")

menu = st.sidebar.selectbox(
    "Select Action",
    [
        "Add Player",
        "View + Search + Sort",
        "Update Player",
        "Delete Player",
        "Analytics",
        "Export to CSV"
    ]
)



# ---------------- ADD PLAYER ----------------
if menu == "Add Player":
    st.subheader("➕ Add New Player")

    name = st.text_input("Player Name")
    age = st.text_input("Age")
    score = st.number_input("Score", min_value=0)

    if st.button("Add Player"):
        payload = {
            "name": name,
            "age": age,
            "score": score
        }

        response = requests.post(f"{API_URL}/ipl_data", json=payload)

        if response.status_code == 200:
            st.success("✅ Player added successfully")
        else:
            st.error("❌ Failed to add player")


# ---------------- VIEW + SEARCH + SORT ----------------
elif menu == "View + Search + Sort":
    st.subheader("📋 Players List")

    response = requests.get(f"{API_URL}/get_IplData")

    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)

            # 🔎 SEARCH
            search = st.text_input("Search player by name")

            if search:
                df = df[df["name"].str.contains(search, case=False)]

            # 🔽 SORT
            sort_option = st.selectbox(
                "Sort By",
                ["None", "Score (Low to High)", "Score (High to Low)"]
            )

            if sort_option == "Score (Low to High)":
                df = df.sort_values(by="score", ascending=True)

            elif sort_option == "Score (High to Low)":
                df = df.sort_values(by="score", ascending=False)

            st.dataframe(df)

        else:
            st.warning("No players found")
    else:
        st.error("Error fetching data")

elif menu == "Analytics":
    st.subheader("📊 IPL Analytics Dashboard")

    response = requests.get(f"{API_URL}/get_IplData")

    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)

            # Metrics
            avg_score = df["score"].mean()
            max_score = df["score"].max()
            min_score = df["score"].min()

            col1, col2, col3 = st.columns(3)
            col1.metric("Average Score", avg_score)
            col2.metric("Highest Score", max_score)
            col3.metric("Lowest Score", min_score)

            st.markdown("---")

            # Top 5 players
            top_players = df.sort_values(by="score", ascending=False).head(5)

            fig = plt.figure()
            plt.bar(top_players["name"], top_players["score"])
            plt.xticks(rotation=45)
            plt.title("Top 5 Highest Scoring Players")
            st.pyplot(fig)

            st.markdown("---")

            # All players vs Average line
            fig2 = plt.figure()
            plt.plot(df["name"], df["score"], marker='o')
            plt.axhline(y=avg_score, color='r', linestyle='--', label="Average")
            plt.xticks(rotation=45)
            plt.legend()
            plt.title("All Player Scores vs Average")
            st.pyplot(fig2)

        else:
            st.warning("No data available for analytics")

    else:
        st.error("Failed to load data")


# ---------------- DELETE PLAYER ----------------
elif menu == "Delete Player":
    st.subheader("🗑️ Delete Player")

    # Show current players first
    response = requests.get(f"{API_URL}/get_IplData")

    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)

            player_id = st.number_input("Enter Player ID to Delete", min_value=1, step=1)

            if st.button("Delete Player"):
                delete_response = requests.delete(f"{API_URL}/delete_iplData/{player_id}")

                if delete_response.status_code == 200:
                    st.success("✅ Player deleted successfully")
                    st.json(delete_response.json())
                else:
                    st.error("❌ Player not found")

        else:
            st.warning("No players available to delete")

    else:
        st.error("Failed to fetch players")


# ---------------- UPDATE PLAYER ----------------
elif menu == "Update Player":
    st.subheader("✏️ Update Player")

    response = requests.get(f"{API_URL}/get_IplData")

    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)

            player_id = st.number_input("Enter Player ID to Update", min_value=1, step=1)
            name = st.text_input("New Name")
            age = st.text_input("New Age")
            score = st.number_input("New Score", min_value=0)

            if st.button("Update Player"):
                payload = {
                    "name": name,
                    "age": age,
                    "score": score
                }

                response = requests.put(f"{API_URL}/update_iplData/{player_id}", json=payload)

                if response.status_code == 200:
                    st.success("✅ Player updated successfully")
                    st.json(response.json())
                else:
                    st.error("❌ Player not found")

        else:
            st.warning("No players found")

    else:
        st.error("Failed to fetch players")


# ---------------- EXPORT TO CSV ----------------
elif menu == "Export to CSV":
    st.subheader("📤 Export Players to CSV")

    response = requests.get(f"{API_URL}/get_IplData")

    if response.status_code == 200:
        data = response.json()

        if len(data) > 0:
            df = pd.DataFrame(data)
            st.dataframe(df)

            csv = df.to_csv(index=False).encode("utf-8")

            st.download_button(
                label="Download as CSV",
                data=csv,
                file_name="ipl_players.csv",
                mime="text/csv"
            )

        else:
            st.warning("No data available to export")

    else:
        st.error("Error fetching data")
