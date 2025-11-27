import streamlit as st
import requests
import pandas as pd
import matplotlib.pyplot as plt
import logging

BASE_URL = "http://127.0.0.1:8000"

# -------------- LOGGING ----------------
logging.basicConfig(
    filename="activity.log",
    level=logging.INFO,
    format="%(asctime)s - %(message)s"
)

st.set_page_config(page_title="Cricket Player Management", layout="wide")

# -------------- LOGIN ----------------

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:

    st.title("🔐 Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username == "admin" and password == "cricket123":
            st.session_state.logged_in = True
            st.session_state.username = username
            logging.info("Admin logged in")
            st.rerun()
        else:
            st.error("Invalid login")

    st.stop()

# -------------- MAIN APP ----------------

st.sidebar.success(f"Logged in as: {st.session_state.username}")

menu = st.sidebar.selectbox(
    "Choose Option",
    [
        "Add Player",
        "Update Player",
        "View Players",
        "Top Batsman",
        "Top Bowler",
        "Performance Graph",
        "AI Insights",
        "Best XI (Suggested)",
        "Download CSV",
        "Logout"
    ]
)


# ---------------- ADD PLAYER ----------------

# if menu == "Add Player":
#
#     st.header("📥 Add Player")
#
#     with st.form("add_form"):
#
#         name = st.text_input("Name")
#         role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder"])
#         matches = st.number_input("Matches", 0)
#         runs = st.number_input("Runs", 0)
#         wickets = st.number_input("Wickets", 0)
#         strike_rate = st.number_input("Strike Rate", 0.0)
#         economy_rate = st.number_input("Economy Rate", 0.0)
#         best = st.text_input("Best Performance")
#
#         if st.form_submit_button("Add Player"):
#
#             data = {
#                 "name": name,
#                 "role": role,
#                 "matches": matches,
#                 "runs": runs,
#                 "wickets": wickets,
#                 "strike_rate": strike_rate,
#                 "economy_rate": economy_rate,
#                 "best_performance": best
#             }
#
#             r = requests.post(f"{BASE_URL}/add_player", json=data)
#
#             if r.status_code == 200:
#                 st.success("Player Added ✅")
#                 logging.info(f"Added {name}")

if menu == "Add Player":

    st.header("📥 Add Player")

    # ✅ Role selector OUTSIDE form so UI updates instantly
    role = st.selectbox("Role", ["Batsman", "Bowler", "All-rounder"])

    with st.form("add_player_form"):

        name = st.text_input("Name")
        matches = st.number_input("Matches", min_value=0, step=1)

        # ===== CONDITIONAL FIELDS BASED ON ROLE =====

        if role == "Batsman":
            runs = st.number_input("Runs", min_value=0, step=1)
            strike_rate = st.number_input("Strike Rate", min_value=0.0)
            # auto for non-relevant fields
            wickets = 0
            economy_rate = 0.0

        elif role == "Bowler":
            wickets = st.number_input("Wickets", min_value=0, step=1)
            economy_rate = st.number_input("Economy Rate", min_value=0.0)
            # auto for non-relevant fields
            runs = 0
            strike_rate = 0.0

        else:  # All-rounder
            runs = st.number_input("Runs", min_value=0, step=1)
            wickets = st.number_input("Wickets", min_value=0, step=1)
            strike_rate = st.number_input("Strike Rate", min_value=0.0)
            economy_rate = st.number_input("Economy Rate", min_value=0.0)

        best = st.text_input("Best Performance")

        submit = st.form_submit_button("Add Player")

        if submit:
            data = {
                "name": name,
                "role": role,
                "matches": matches,
                "runs": runs,
                "wickets": wickets,
                "strike_rate": strike_rate,
                "economy_rate": economy_rate,
                "best_performance": best,
            }

            res = requests.post(f"{BASE_URL}/add_player", json=data)

            if res.status_code == 200:
                st.success("✅ Player added successfully")
            else:
                st.error("❌ Failed to add player")
#-----------------------------Update Player------------------------------------------


elif menu == "Update Player":

    st.subheader("✏️ Update Player Details")

    # Get all players
    res = requests.get(f"{BASE_URL}/get_players")

    if res.status_code == 200 and res.json():

        df = pd.DataFrame(res.json())

        role_select = st.selectbox(
            "Select Role",
            ["Batsman", "Bowler", "All-rounder"]
        )

        filtered_df = df[df["role"] == role_select]

        if filtered_df.empty:
            st.warning(f"No {role_select} found")
            st.stop()

        # ---------------- Select Player ----------------
        player_map = dict(zip(filtered_df["name"], filtered_df["id"]))
        selected_name = st.selectbox("Select Player", list(player_map.keys()))
        selected_id = player_map[selected_name]

        selected_player = filtered_df[filtered_df["id"] == selected_id].iloc[0]

        # ---------------- Form ----------------
        with st.form("update_form"):

            name = st.text_input("Name", selected_player["name"])
            role = st.selectbox("Role", ["Batsman","Bowler","All-rounder"],
                                index=["Batsman","Bowler","All-rounder"].index(selected_player["role"]))

            matches = st.number_input("Matches", value=int(selected_player["matches"]))

            # Show based on role
            if role in ["Batsman", "All-rounder"]:
                runs = st.number_input("Runs", value=int(selected_player["runs"]))
                strike_rate = st.number_input("Strike Rate", value=float(selected_player["strike_rate"]))
            else:
                runs = 0
                strike_rate = 0

            if role in ["Bowler", "All-rounder"]:
                wickets = st.number_input("Wickets", value=int(selected_player["wickets"]))
                economy_rate = st.number_input("Economy Rate", value=float(selected_player["economy_rate"]))
            else:
                wickets = 0
                economy_rate = 0

            best_performance = st.text_input(
                "Best Performance",
                selected_player["best_performance"]
            )

            update_btn = st.form_submit_button("✅ Update Player")

            if update_btn:

                payload = {
                    "name": name,
                    "role": role,
                    "matches": matches,
                    "runs": runs,
                    "wickets": wickets,
                    "strike_rate": strike_rate,
                    "economy_rate": economy_rate,
                    "best_performance": best_performance
                }

                resp = requests.put(f"{BASE_URL}/update_player/{selected_id}", json=payload)

                if resp.status_code == 200:
                    st.success("🎉 Player updated successfully")
                    logging.info(f"{st.session_state.username} - Updated {name}")
                else:
                    st.error("❌ Failed to update")
    else:
        st.error("Backend not responding")


# ---------------- VIEW + UPDATE + DELETE ----------------

elif menu == "View Players":

    st.header("📋 All Players")

    res = requests.get(f"{BASE_URL}/get_players")

    if res.status_code == 200 and res.json():

        df = pd.DataFrame(res.json())

        df = df[[
            "id",
            "name",
            "role",
            "matches",
            "runs",
            "wickets",
            "strike_rate",
            "economy_rate",
            "best_performance"
        ]]

        st.dataframe(df, use_container_width=True)

        st.subheader("❌ Delete")

        selected_id = st.number_input("Enter Player ID", min_value=1)

        if st.button("Delete Player"):
            requests.delete(f"{BASE_URL}/delete_player/{selected_id}")
            st.success("Deleted ✅")
            st.rerun()

    else:
        st.warning("No data found")


# ---------------- TOP BATSMAN ----------------

elif menu == "Top Batsman":

    res = requests.get(f"{BASE_URL}/top_batsman")

    if res.status_code == 200:

        p = res.json()

        st.success(f"🏆 {p['name']}")
        st.markdown(f"""
        **Role:** {p['role']}  
        **Runs:** {p['runs']}  
        **Strike Rate:** {p['strike_rate']}  
        **Best Performance:** {p['best_performance']}
        """)


# ---------------- TOP BOWLER ----------------

elif menu == "Top Bowler":

    res = requests.get(f"{BASE_URL}/top_bowler")

    if res.status_code == 200:

        p = res.json()

        st.success(f"🎯 {p['name']}")
        st.markdown(f"""
        **Role:** {p['role']}  
        **Wickets:** {p['wickets']}  
        **Economy Rate:** {p['economy_rate']}  
        **Best Performance:** {p['best_performance']}
        """)


# ---------------- PERFORMANCE GRAPH ----------------
# elif menu == "Performance Graph":
#
#     st.subheader("📊 Performance (Compact)")
#
#     res = requests.get(f"{BASE_URL}/get_players")
#
#     # ✅ First check if data really exists
#     if res.status_code == 200 and res.json() is not None and len(res.json()) > 0:
#
#         df = pd.DataFrame(res.json())
#
#         # ✅ Safety check (avoid NoneType error)
#         if "name" in df.columns and "runs" in df.columns:
#
#             fig, ax = plt.subplots(figsize=(4, 3))
#
#             ax.bar(df["name"], df["runs"], width = 0.5)
#             ax.set_title("Runs by Players", fontsize=10)
#             ax.set_xlabel("Player", fontsize=8)
#             ax.set_ylabel("Runs", fontsize=8)
#
#
#
#             plt.xticks(rotation=30, fontsize=7)
#             plt.yticks(fontsize=7)
#
#             # ✅ NEW Streamlit syntax (no more warning)
#             st.pyplot(fig, width="content")
#
#         else:
#             st.warning("Required columns not found in data")
elif menu == "Performance Graph":

    st.subheader("📊 Role-based Performance Analysis")

    res = requests.get(f"{BASE_URL}/get_players")

    if res.status_code == 200 and res.json():

        df = pd.DataFrame(res.json())

        if len(df) == 0:
            st.warning("No players available")
            st.stop()

        # --- Split by role ---
        batsmen = df[df["role"] == "Batsman"]
        bowlers = df[df["role"] == "Bowler"]
        all_rounders = df[df["role"] == "All-rounder"]

        col1, col2, col3 = st.columns(3)

        # =======================
        # 🏏 BATSMAN GRAPH
        # =======================
        with col1:
            st.write("### 🏏 Batsmen (Runs)")

            if not batsmen.empty:
                fig1, ax1 = plt.subplots(figsize=(3.5, 2.5))
                ax1.bar(batsmen["name"], batsmen["runs"], width=0.6)
                ax1.set_title("Runs", fontsize=9)
                plt.xticks(rotation=30, fontsize=7)
                plt.yticks(fontsize=7)
                st.pyplot(fig1)
            else:
                st.info("No Batsman data")

        # =======================
        # 🎯 BOWLER GRAPH
        # =======================
        with col2:
            st.write("### 🎯 Bowlers (Wickets)")

            if not bowlers.empty:
                fig2, ax2 = plt.subplots(figsize=(3.5, 2.5))
                ax2.bar(bowlers["name"], bowlers["wickets"], width=0.6)
                ax2.set_title("Wickets", fontsize=9)
                plt.xticks(rotation=30, fontsize=7)
                plt.yticks(fontsize=7)
                st.pyplot(fig2)
            else:
                st.info("No Bowler data")

        # =======================
        # 🔥 ALL-ROUNDER GRAPH
        # =======================
        with col3:
            st.write("### 🔥 All-Rounders")

            if not all_rounders.empty:
                fig3, ax3 = plt.subplots(figsize=(3.5, 2.5))

                ax3.bar(all_rounders["name"], all_rounders["runs"], width=0.3, label="Runs")
                ax3.bar(all_rounders["name"], all_rounders["wickets"], width=0.3, bottom=0, label="Wickets")

                ax3.set_title("Runs + Wickets", fontsize=9)
                plt.xticks(rotation=30, fontsize=7)
                plt.yticks(fontsize=7)
                ax3.legend(fontsize=6)

                st.pyplot(fig3)
            else:
                st.info("No All-rounder data")

    else:
        st.error("Backend not responding")

#------------------------------AI Insights----------------------------------------

elif menu == "AI Insights":

    st.subheader("🧠 Player Insights & Rating")

    res = requests.get(f"{BASE_URL}/get_players")

    if res.status_code == 200 and res.json():

        df = pd.DataFrame(res.json())

        # Choose player
        player_map = dict(zip(df["name"], df["id"]))
        selected_name = st.selectbox("Select Player", list(player_map.keys()))
        selected_id = player_map[selected_name]

        # Call backend insights
        insight_res = requests.get(f"{BASE_URL}/player_insights/{selected_id}")

        if insight_res.status_code == 200:
            data = insight_res.json()

            col1, col2 = st.columns(2)

            with col1:
                st.markdown(f"### {data['name']} ({data['role']})")
                st.metric("Overall Rating (0–10)", data["overall_rating"])
                st.metric("Batting Score", data["batting_score"])
                st.metric("Bowling Score", data["bowling_score"])

            with col2:
                st.markdown("### Suggested Role")
                st.success(data["suggested_role"])
                st.markdown(
                    f"""
                    **Matches:** {data['matches']}  
                    **Runs:** {data['runs']}  
                    **Wickets:** {data['wickets']}  
                    **Strike Rate:** {data['strike_rate']}  
                    **Economy Rate:** {data['economy_rate']}  
                    """
                )

        else:
            st.error("Could not fetch insights")

    else:
        st.warning("No players in database")


#----------------------Best XI (Suggested)--------------------------------
elif menu == "Best XI (Suggested)":

    st.subheader("🏆 Suggested Best XI")

    res = requests.get(f"{BASE_URL}/best_xi")

    if res.status_code == 200:
        data = res.json()

        st.info(f"Team Size: {data['team_size']} players")

        df = pd.DataFrame(data["players"])

        # Order columns nicely
        df = df[["id", "name", "role", "matches", "runs", "wickets", "strike_rate", "economy_rate"]]

        st.dataframe(df, use_container_width=True)

    else:
        st.error("Unable to generate Best XI – add more players first.")




#-------------------Download CSV----------------------
elif menu == "Download CSV":

    st.subheader("⬇️ Download Players Data as CSV")

    res = requests.get(f"{BASE_URL}/get_players")

    if res.status_code == 200 and res.json():

        df = pd.DataFrame(res.json())

        # Reorder the columns
        df = df[[
            "id",
            "name",
            "role",
            "matches",
            "runs",
            "wickets",
            "strike_rate",
            "economy_rate",
            "best_performance"
        ]]

        st.dataframe(df, use_container_width=True)

        # Convert to CSV
        csv_data = df.to_csv(index=False).encode("utf-8")

        # Download button
        st.download_button(
            label="📥 Download CSV File",
            data=csv_data,
            file_name="cricket_players.csv",
            mime="text/csv"
        )

        logging.info(f"{st.session_state.username} - Downloaded CSV file")

    else:
        st.warning("No player data found in database ❌")




# ---------------- LOGOUT ----------------

elif menu == "Logout":
    st.session_state.logged_in = False
    st.success("Logged out ✅")
    st.rerun()
