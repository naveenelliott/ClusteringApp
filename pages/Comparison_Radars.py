import pandas as pd
import streamlit as st
from mplsoccer import Radar, FontManager, grid
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

st.set_page_config(page_title='Comparison Radars')

st.title("Comparison Radars")

df = st.session_state.clustered_copy

selected_player = df['Player Full Name'][0]
compare_player = df['Player Full Name'][1]

st.markdown(f"This is a comparison of the {selected_player} and his compared player {compare_player} mentioned in the Player Clustering. The radar charts are made up of percentiles amongst all players in the club.")


#       'Total Crosses', 'Total Long', 'Total Forward', 'Total Pass',
#       'Total Recoveries', 'Total Interceptions'
df.rename(columns={'Progr Regain ': 'Progr Regain', 'Blocked Cross': 'Blk Cross', 'Efforts on Goal': 'Shots', 'Pass into Oppo Box': 'Pass into 18', 
                   'Blocked Shot': 'Blk Shot', 'Pass Completion ': 'Pass %', 'Progr Pass Completion ': 'Forward Pass %', 
                   'Total Tackles': 'Tackles', 'Total Def Aerials': 'Def Aerials', 'Total Clears': 'Clears', 'Total Att Aerials': 'Att Aerials', 
                   'Total Crosses': 'Crosses', 'Total Long': 'Long Pass', 'Total Forward': 'Forward Pass', 'Total Pass': 'Total Pass', 
                   'Total Recoveries': 'Ball Recov', 'Total Interceptions': 'Intercepts'}, inplace=True)

new_order = ['Player Full Name', 'Goal', 'Shots', 'Att Aerials', 'Assist', 'Pass into 18', 'Crosses', 'Dribble', 'Loss of Poss', 'Total Pass', 
             'Pass %', 'Forward Pass', 'Forward Pass %', 'Long Pass', 'Ball Recov', 'Intercepts', 'Progr Regain', 'Tackles', 'Tackle %', 'Clears',
             'Def Aerials', 'Blk Shot', 'Blk Cross']

df = df[new_order]

params = [col for col in df.columns if col != 'Player Full Name']
print(params)
low = [0] * len(params)
high = [100] * len(params)

radar = Radar(params, low, high,  round_int=[True]*len(params),
              num_rings=4,
              ring_width=1, center_circle_radius=1)

st.write(df)
del df['Player Full Name']

fig, ax = radar.setup_axis()
rings_inner = radar.draw_circles(ax=ax, facecolor='#D3D3D3', edgecolor='white')
radar_output = radar.draw_radar_compare(df.iloc[0], df.iloc[1], ax=ax,
                                        kwargs_radar={'facecolor': '#6bb2e2', 'alpha': 0.8},
                                        kwargs_compare={'facecolor': 'black', 'alpha': 0.5})
radar_poly, radar_poly2, vertices1, vertices2 = radar_output
ax.scatter(vertices1[:, 0], vertices1[:, 1],
           c='#6bb2e2', edgecolors='#6bb2e2', marker='o', s=50, zorder=2)
ax.scatter(vertices2[:, 0], vertices2[:, 1],
           c='black', edgecolors='black', marker='o', s=50, zorder=2)
range_labels = radar.draw_range_labels(ax=ax, fontsize=11.5)
param_labels = radar.draw_param_labels(ax=ax, fontsize=13)

st.pyplot(fig)