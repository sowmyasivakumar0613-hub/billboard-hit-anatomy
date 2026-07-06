import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(page_title="50 Years of Billboard Hits", layout="wide")

st.title("🎵 50 Years of Billboard Hit Song Anatomy")
st.markdown("Exploring how the #1 song of each year has changed, using Spotify audio features.")

# Headline metrics
col1, col2, col3, col4 = st.columns(4)
col1.metric("Songs analyzed", "64", "1958-2021")
col2.metric("Acousticness drop", "-80%", "1950s → 2020s", delta_color="inverse")
col3.metric("Peak happiness decade", "1970s", "valence: 0.79")
col4.metric("Energy-Valence link", "0.69", "strong correlation")

st.divider()

# Load data
merged = pd.read_csv(r"C:\Users\Jiyoon\billboard-project\data\processed\merged.csv")
decade_avg = merged.groupby('decade')[
    ['tempo','energy','valence','danceability','acousticness','speechiness']
].mean().round(3)

# Sidebar controls
st.sidebar.header("Controls")
feature = st.sidebar.selectbox(
    "Choose a feature to explore:",
    ['energy','valence','tempo','danceability','acousticness','speechiness']
)

tab1, tab2, tab3, tab4 = st.tabs(["📈 Trends", "🕸️ Decade Fingerprint", "🔍 Explore Songs", "🌐 3D Sound Space"])
# ---------------- TAB 1: Trends ----------------
with tab1:
    st.subheader(f"📈 {feature.capitalize()} across decades")

    fig1 = px.line(
        decade_avg.reset_index(), x='decade', y=feature, markers=True,
        color_discrete_sequence=['#1DB954']
    )
    fig1.update_traces(line=dict(width=3), marker=dict(size=10))
    fig1.update_layout(
        xaxis_title="Decade", yaxis_title=feature.capitalize(),
        plot_bgcolor='white', hovermode='x unified'
    )
    st.plotly_chart(fig1, use_container_width=True)

    insights = {
        'energy': "Energy climbed steadily from the 1950s (0.40) to the 2020s (0.63) — modern hits hit harder.",
        'valence': "Valence (happiness) peaked in the 1970s (0.79) and has generally declined since, dropping to 0.35 by 2020.",
        'tempo': "Tempo dipped through the 70s-90s, then climbed again in the 2010s-2020s.",
        'danceability': "Danceability rose sharply post-2000s, reflecting the shift toward dance-pop and hip-hop influenced production.",
        'acousticness': "The most dramatic shift in the dataset — acousticness collapsed from 0.83 (1950s) to ~0.10 (2000s onward), and has stayed low since.",
        'speechiness': "Speechiness spiked in the 2000s-2010s, tracking hip-hop and rap's growing chart dominance."
    }
    st.info(f"💡 **What this shows:** {insights[feature]}")

# ---------------- TAB 2: Decade Fingerprint ----------------
with tab2:
    st.subheader("🕸️ Decade audio fingerprint")
    st.caption("Click decade names in the legend to isolate and compare specific decades")

    features_radar = ['energy','valence','danceability','acousticness','speechiness']
    fig2 = go.Figure()

    colors = px.colors.sequential.Viridis
    for i, (decade, row) in enumerate(decade_avg.iterrows()):
        vals = row[features_radar].tolist()
        fig2.add_trace(go.Scatterpolar(
            r=vals + [vals[0]],
            theta=features_radar + [features_radar[0]],
            name=str(int(decade)) + 's',
            fill='toself', opacity=0.5,
            line=dict(color=colors[i % len(colors)])
        ))

    fig2.update_layout(
        polar=dict(radialaxis=dict(range=[0,1], showticklabels=True)),
        height=500
    )
    st.plotly_chart(fig2, use_container_width=True)

# ---------------- TAB 3: Explore Songs ----------------
with tab3:
    st.subheader("Explore the underlying songs")

    merged['data_status'] = merged['energy'].notna().map({True: '✅ Matched', False: '⚠️ Not matched'})

    st.caption(f"{merged['energy'].notna().sum()} of {len(merged)} songs matched to Spotify audio data. "
               "Unmatched songs (⚠️) had title formatting differences or were absent from the "
               "enriched dataset entirely. See README for details.")

    st.dataframe(
        merged[['year','song','artist','data_status','tempo','energy','valence','danceability','acousticness','speechiness']],
        use_container_width=True,
        hide_index=True
    )

with tab4:
    st.subheader("🌐 Songs in 3D sound space")
    st.caption("Each point is one #1 song, positioned by energy, valence, and danceability. Rotate by clicking and dragging.")

    plot_df = merged.dropna(subset=['energy','valence','danceability'])

    fig3 = px.scatter_3d(
        plot_df,
        x='energy', y='valence', z='danceability',
        color='decade',
        hover_data=['song', 'artist', 'year'],
        color_continuous_scale='Viridis',
        opacity=0.8
    )
    fig3.update_traces(marker=dict(size=6))
    fig3.update_layout(
        scene=dict(
            xaxis_title='Energy',
            yaxis_title='Valence',
            zaxis_title='Danceability',
            bgcolor='rgba(0,0,0,0)'
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(color='white'),
        height=650
    )
    st.plotly_chart(fig3, use_container_width=True)

    st.info("💡 **What to look for:** hover over points to see the song title. Notice how older decades (darker purple) cluster toward lower energy/danceability, while recent decades (yellow) shift toward the upper right.")
# Key findings
st.subheader("📌 Key findings")
st.markdown("""
- **Acousticness collapsed** from 0.83 (1950s) to ~0.10 (2000s onward)
- **Acousticness is a "hub" feature** — negatively linked to energy, danceability, and valence
- **Energy and valence are strongly correlated** (0.69) — energetic songs tend to sound happier
- **Valence peaked in the 1970s**, generally declining since
- **Speechiness rose sharply in the 2000s-2010s**, reflecting hip-hop's chart influence
""")