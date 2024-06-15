import pandas as pd
import streamlit as st
import ast
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA
import plotly.express as px
from sklearn.preprocessing import StandardScaler
import plotly.graph_objects as go

st.title ("Player Clustering Calculator")

st.markdown("Select The Player to See their Position Group and Closest Player in the Club")


clustered = pd.read_csv('EndKMeansClustering.csv')
clustered.sort_values('Player Full Name', ascending=True, inplace=True)

def convert_to_list(cell):
    try:
        return ast.literal_eval(cell)
    except (ValueError, SyntaxError):
        return cell

# Apply the function to the 'Closest Statistics' column
clustered['Closest Statistics'] = clustered['Closest Statistics'].apply(convert_to_list)

cluster_mapping = {
    0: 'Target CF',
    1: 'Build Up CB',
    2: 'Defensive Fullback',
    3: 'Wide Forward',
    4: 'Engine',
    5: 'Complete Winger',
    6: 'Creator Advanced Midfielder',
    7: 'Destroyer',
    8: 'Deep Lying Midfielder'
}

# Replace cluster numbers with corresponding strings
clustered['Other Cluster'] = clustered['Cluster'].replace(cluster_mapping)

players = list(clustered['Player Full Name'].unique())
selected_player = st.selectbox('Choose the Bolts player:', players)
clustered_player = clustered.loc[clustered['Player Full Name'] == selected_player]


position_group = clustered_player['Other Cluster'].values
closest_player = clustered_player['Closest Point'].values

closest_player_stats = clustered_player['Closest Statistics'].reset_index(drop=True)

st.write(f"{selected_player}'s position group is {position_group[0]}.")

st.write(f"{selected_player}'s closest comparable player is {closest_player[0]}.")

st.write(f"{selected_player}'s closest statistics with {closest_player[0]} are {closest_player_stats[0][0]}, {closest_player_stats[0][1]}, and {closest_player_stats[0][2]}.")



update_bolts = pd.read_csv('PCAPlayers.csv')

cluster_highlight = update_bolts.loc[update_bolts['Player Full Name'] == selected_player]
selected_cluster = cluster_highlight['Cluster'].values[0]

fig = go.Figure()

other_clusters_df = update_bolts.loc[update_bolts['Cluster'] != selected_cluster]
fig.add_trace(
    go.Scatter(
        mode='markers',
        x=other_clusters_df['PC1'],
        y=other_clusters_df['PC2'],
        marker=dict(
            color='gray',
            size=10,
        ),
        name='Other Clusters',
        text=other_clusters_df['Player Full Name'],  # Use 'text' instead of 'hoverinfo'
        hoverinfo='text', 
        showlegend=True
    )
)

selected_cluster_df = update_bolts.loc[update_bolts['Cluster'] == selected_cluster]
fig.add_trace(
    go.Scatter(
        mode='markers',
        x=selected_cluster_df['PC1'],
        y=selected_cluster_df['PC2'],
        marker=dict(
            color='lightblue',
            size=10,
        ),
        name=f"{selected_player}'s Cluster",
        text=selected_cluster_df['Player Full Name'],  # Use 'text' instead of 'hoverinfo'
        hoverinfo='text', 
        showlegend=True
    )
)


selected_player_trace = update_bolts[update_bolts['Player Full Name'] == selected_player]
fig.add_trace(
    go.Scatter(
        mode='markers',
        x=selected_player_trace['PC1'],
        y=selected_player_trace['PC2'],
        marker=dict(
            color='blue',
            size=15,
        ),
        name=selected_player,
        hoverinfo='name',
        showlegend=True
    )
)



# Update layout properties
fig.update_layout(
    title="Boston Bolts Player Style Clusters",
    title_font_size=20,  # Adjust the font size as needed
    title_x=0.2,  # Center the title horizontally
    title_y=0.85,
    xaxis_title='',
    yaxis_title='',
    hovermode='closest',  # Show closest data on hover
    showlegend=True,
    annotations=[
        dict(
            text=f"(With {selected_player}'s Cluster in Blue)",
            xref="paper",  # Position relative to paper
            yref="paper",  # Position relative to paper
            x=0.5,         # X position (0 to 1)
            y=1.0,        # Y position (0 to 1)
            showarrow=False,
            font=dict(size=12),
            bordercolor='blue'
        )
    ]
)


# Show the plot
st.plotly_chart(fig)
