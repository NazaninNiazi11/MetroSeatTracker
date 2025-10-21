import streamlit as st
import pandas as pd

# Load CSV
df = pd.read_csv("data/stations.csv")

# Function to calculate status & color
def seat_status(seats):
    if seats > 15:
        return "HIGH", "#2ecc71"
    elif seats > 5:
        return "MEDIUM", "#f1c40f"
    else:
        return "LOW", "#e74c3c"

#  Filter by metro lines
lines = df['line'].unique()
selected_lines = st.multiselect("Select metro lines:", options=lines, default=lines)
df_filtered = df[df['line'].isin(selected_lines)]

#  Apply seat_status only if there are rows
if not df_filtered.empty:
    df_filtered['status'], df_filtered['color'] = zip(*df_filtered['seats_available'].apply(seat_status))
else:
    df_filtered['status'] = []
    df_filtered['color'] = []

# Filter by seat status
status_options = ["HIGH", "MEDIUM", "LOW"]
selected_status = st.multiselect("Filter by seat status:", options=status_options, default=status_options)
df_filtered = df_filtered[df_filtered['status'].isin(selected_status)] if not df_filtered.empty else df_filtered

#  Sort by seats
sort_option = st.selectbox("Sort by seats available:", ["Descending", "Ascending"])
if not df_filtered.empty:
    df_filtered = df_filtered.sort_values(by="seats_available", ascending=(sort_option=="Ascending"))

#  Display table or warning
if not df_filtered.empty:
    st.subheader("Filtered Metro Seat Status")
    st.dataframe(df_filtered[['station', 'line', 'seats_available', 'status']])
else:
    st.warning("No stations match the current filter selection.")

# 6️⃣ Color-coded status (optional)
if not df_filtered.empty:
    st.subheader("Seat Availability per Station")
    for i, row in df_filtered.iterrows():
        st.markdown(f"**{row['station']}**: <span style='color:{row['color']}'>{row['status']}</span>", unsafe_allow_html=True)

# 7️⃣ Horizontal bar chart
if not df_filtered.empty:
    st.subheader("Seats Available Across Stations")
    st.bar_chart(df_filtered.set_index('station')['seats_available'])
