import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.title("NFL Network Data Science Practicum Project")

st.subheader("Tendency Report - Breaking Down Jacksonville vs. Miami")
dnd = pd.read_csv("Leaguewide_NFL_Down and Distance(1).csv")
field_positions = pd.read_csv("Leaguewide_NFL_Field Positions.csv")

week_1_matchups = ['BAL @ KC', 'GB @ PHI', 'PIT @ ATL', 'ARI @ BUF', 'TEN @ CHI', 
                   'NE @ CIN', 'HOU @ IND', 'JAX @ MIA', 'CAR @ NO', 'MIN @ NYG', 
                   'LV @ LAC', 'DEN @ SEA', 'DAL @ CLE', 'WAS @ TB', 'LA @ DET', 'NYJ @ SF']

jax_dnd_filtered = dnd.loc[dnd['Team'] == 'JAX', ['Team', 'Down & Distance', 'Run %', 'Pass %']]
mia_dnd_filtered = dnd.loc[dnd['Team'] == 'MIA', ['Team', 'Down & Distance', 'Run %', 'Pass %']]

# Add images for JAX and MIA
jax_image_url = "jax_img.png"  
mia_image_url = "mia_img.png" 

col3, col4 = st.columns([10, 10])

with col3:
    st.header("")
    st.image(jax_image_url, width=100)  # Adjust the width as needed
    st.header("JAX Data")
    st.dataframe(jax_dnd_filtered, width=1000)

with col4:
    st.header("")
    st.image(mia_image_url, width=100)  # Adjust the width as needed
    st.header("MIA Data")
    st.dataframe(mia_dnd_filtered, width=1000)

jax_fp_filtered = field_positions.loc[field_positions['Team'] == 'JAX', [ 'Field Position', 'Run %', 'Pass %']]
mia_fp_filtered = field_positions.loc[field_positions['Team'] == 'MIA', [ 'Field Position', 'Run %', 'Pass %']]

st.header("Field Position Data for JAX and MIA")

col5, col6 = st.columns([10, 10])

with col5:
    st.subheader("JAX Field Position Data")
    st.dataframe(jax_fp_filtered, width=1500)

with col6:
    st.subheader("MIA Field Position Data")
    st.dataframe(mia_fp_filtered, width=1500)

game_selection = st.selectbox("Select a game", week_1_matchups)

team1, team2 = game_selection.split(' @ ')

team1_dnd_filtered = dnd.loc[dnd['Team'] == team1, ['Team', 'Down & Distance', 'Run %', 'Pass %']]
team2_dnd_filtered = dnd.loc[dnd['Team'] == team2, ['Team', 'Down & Distance', 'Run %', 'Pass %']]

col1, col2 = st.columns([10, 10]) 

with col1:
    st.header(f"{team1} Data")
    st.dataframe(team1_dnd_filtered, width=1000)  

with col2:
    st.header(f"{team2} Data")
    st.dataframe(team2_dnd_filtered, height=400) 

grouped = dnd.groupby('Down & Distance')
sums = grouped[['Total Runs', 'Total Passes', 'Total Plays']].sum()
sums['Run %'] = (sums['Total Runs'] / sums['Total Plays']) * 100
sums['Pass %'] = (sums['Total Passes'] / sums['Total Plays']) * 100

st.header("League Averages")
st.write(sums)

dnd['Total Runs'] = dnd['Total Runs'].astype(int)
dnd['Total Passes'] = dnd['Total Passes'].astype(int)
dnd['Total Plays'] = dnd['Total Plays'].astype(int)

st.subheader("Comparing the Down and Distance Stats for each of the upcoming 2024 Week 1 NFL Games")

grouped = dnd.groupby(['Down & Distance', 'Team'])
sums = grouped[['Total Runs', 'Total Passes', 'Total Plays']].sum()
sums['Run %'] = (sums['Total Runs'] / sums['Total Plays']) * 100
sums['Pass %'] = (sums['Total Passes'] / sums['Total Plays']) * 100

# Reset the index to ensure 'Down & Distance' and 'Team' are columns
sums = sums.reset_index()

max_run_percentages = sums.groupby('Down & Distance', group_keys=False).apply(lambda x: x.nlargest(1, 'Run %')).reset_index(drop=True)
max_pass_percentages = sums.groupby('Down & Distance', group_keys=False).apply(lambda x: x.nlargest(1, 'Pass %')).reset_index(drop=True)

min_run_percentages = sums.groupby('Down & Distance', group_keys=False).apply(lambda x: x.nsmallest(1, 'Run %')).reset_index(drop=True)
min_pass_percentages = sums.groupby('Down & Distance', group_keys=False).apply(lambda x: x.nsmallest(1, 'Pass %')).reset_index(drop=True)

st.header("Team with the Highest Run Percentage")
st.write(max_run_percentages[['Down & Distance', 'Team', 'Run %', 'Total Runs', 'Total Plays']])

st.header("Team with the Highest Pass Percentage")
st.write(max_pass_percentages[['Down & Distance', 'Team', 'Pass %', 'Total Passes', 'Total Plays']])

st.header("Team with the Lowest Run Percentage")
st.write(min_run_percentages[['Down & Distance', 'Team', 'Run %', 'Total Runs', 'Total Plays']])

st.header("Team with the Lowest Pass Percentage")
st.write(min_pass_percentages[['Down & Distance', 'Team', 'Pass %', 'Total Passes', 'Total Plays']])

# Sort the data for Down & Distance and Field Position
sorted_dnd = dnd.sort_values(by=['Down & Distance', 'Run %'], ascending=[True, False])
sorted_dnd_pass = dnd.sort_values(by=['Down & Distance', 'Pass %'], ascending=[True, False])

sorted_fp = field_positions.sort_values(by=['Field Position', 'Run %'], ascending=[True, False])
sorted_fp_pass = field_positions.sort_values(by=['Field Position', 'Pass %'], ascending=[True, False])

# Display the sorted data for Down & Distance
st.subheader("Down & Distance Sorted by Run Percentage")
st.dataframe(sorted_dnd, width=1000)

st.subheader("Down & Distance Sorted by Pass Percentage")
st.dataframe(sorted_dnd_pass, width=1000)

# Display the sorted data for Field Position
st.subheader("Field Position Sorted by Run Percentage")
st.dataframe(sorted_fp, width=1000)

st.subheader("Field Position Sorted by Pass Percentage")
st.dataframe(sorted_fp_pass, width=1000)
