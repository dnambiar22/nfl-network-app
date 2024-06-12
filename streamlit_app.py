import altair as alt
import numpy as np
import pandas as pd
import streamlit as st

st.title("NFL Down and Distance Analysis")

st.subheader("Comparing the Down and Distance Stats for each of the upcoming 2024 Week 1 NFL Games")
dnd = pd.read_csv("Leaguewide_NFL_Down and Distance(1).csv")

week_1_matchups = ['BAL @ KC', 'GB @ PHI', 'PIT @ ATL', 'ARI @ BUF', 'TEN @ CHI', 
                   'NE @ CIN', 'HOU @ IND', 'JAX @ MIA', 'CAR @ NO', 'MIN @ NYG', 
                   'LV @ LAC', 'DEN @ SEA', 'DAL @ CLE', 'WAS @ TB', 'LA @ DET', 'NYJ @ SF']

game_selection = st.selectbox("Select a game", week_1_matchups)

team1, team2 = game_selection.split(' @ ')

team1_dnd_filtered = dnd.loc[dnd['Team'] == team1, ['Team', 'Down & Distance', 'Run %', 'Pass %']]
team2_dnd_filtered = dnd.loc[dnd['Team'] == team2, ['Team', 'Down & Distance', 'Run %', 'Pass %']]

col1, col2 = st.columns([10, 10]) 

with col1:
    st.header(f"{team1} Data")
    st.dataframe(team1_dnd_filtered,width=1000)  

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

grouped = dnd.groupby(['Down & Distance', 'Team'])
sums = grouped[['Total Runs', 'Total Passes', 'Total Plays']].sum()
sums['Run %'] = (sums['Total Runs'] / sums['Total Plays']) * 100
sums['Pass %'] = (sums['Total Passes'] / sums['Total Plays']) * 100

max_percentages = sums.groupby('Down & Distance').apply(lambda x: x.nlargest(1, 'Run %'))
min_percentages = sums.groupby('Down & Distance').apply(lambda x: x.nsmallest(1, 'Run %'))

st.header("Team with the Highest Average Percentage")
st.write(max_percentages[['Run %', 'Pass %', 'Total Runs', 'Total Passes', 'Total Plays']])

st.header("Team with the Lowest Average Percentage")
st.write(min_percentages[['Run %', 'Pass %', 'Total Runs', 'Total Passes', 'Total Plays']])
