import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import seaborn as sns
from wordcloud import WordCloud
import warnings
warnings.filterwarnings('ignore')

# Configuration avancée de la page
st.set_page_config(
    page_title="🎵 Spotify Analytics Pro",
    page_icon="🎵",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé pour un design premium
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(135deg, #1DB954, #191414);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        color: white;
        text-align: center;
    }
    
    .metric-container {
        background: linear-gradient(135deg, #f0f2f6, #ffffff);
        padding: 1rem;
        border-radius: 10px;
        border-left: 4px solid #1DB954;
        box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        margin: 0.5rem 0;
    }
    
    .section-header {
        background: linear-gradient(90deg, #1DB954, #1ed760);
        color: white;
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        font-weight: bold;
        text-align: center;
    }
    
    .insight-box {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 1rem 0;
        box-shadow: 0 4px 8px rgba(0,0,0,0.2);
    }
    
    .sidebar .sidebar-content {
        background: linear-gradient(180deg, #191414, #1DB954);
    }
    
    .stSelectbox label {
        color: #1DB954 !important;
        font-weight: bold;
    }
    
    div[data-testid="metric-container"] {
        background-color: #f8f9fa;
        border: 1px solid #e9ecef;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1DB954;
    }
</style>
""", unsafe_allow_html=True)

# Fonction pour charger les données avec cache
@st.cache_data
def load_data():
    try:
        df = pd.read_csv('./songs_normalize.csv')
        return df
    except FileNotFoundError:
        st.error("❌ Fichier 'songs_normalize.csv' non trouvé. Assurez-vous qu'il est dans le même répertoire.")
        return None

# Fonction pour créer des insights automatiques
def generate_insights(df):
    insights = []
    
    # Top genre
    top_genre = df['genre'].value_counts().index[0]
    top_genre_count = df['genre'].value_counts().iloc[0]
    insights.append(f"🎼 **{top_genre}** domine avec {top_genre_count} chansons")
    
    # Artiste le plus prolifique
    top_artist = df['artist'].value_counts().index[0]
    top_artist_count = df['artist'].value_counts().iloc[0]
    insights.append(f"🎤 **{top_artist}** est l'artiste le plus prolifique avec {top_artist_count} chansons")
    
    # Année la plus productive
    top_year = df['year'].value_counts().index[0]
    insights.append(f"📅 **{top_year}** a été l'année la plus productive")
    
    # Corrélation intéressante
    corr_energy_dance = df['energy'].corr(df['danceability'])
    insights.append(f"⚡ Corrélation énergie-danceabilité: **{corr_energy_dance:.2f}**")
    
    # Pourcentage explicite
    explicit_pct = (df['explicit'].sum() / len(df)) * 100
    insights.append(f"🔞 **{explicit_pct:.1f}%** du contenu est explicite")
    
    return insights

# Fonction pour créer un profil radar amélioré
def create_enhanced_radar_chart(df, features, title="Profil Audio"):
    mean_values = df[features].mean()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=mean_values.tolist() + [mean_values.iloc[0]],
        theta=features + [features[0]],
        fill='toself',
        fillcolor='rgba(29, 185, 84, 0.3)',
        line=dict(color='#1DB954', width=3),
        name='Profil Moyen',
        hovertemplate='%{theta}: %{r:.3f}<extra></extra>'
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 1],
                gridcolor='rgba(29, 185, 84, 0.3)',
                tickcolor='#1DB954'
            ),
            angularaxis=dict(
                tickfont=dict(size=12, color='#1DB954')
            )
        ),
        title=dict(
            text=title,
            font=dict(size=20, color='#1DB954'),
            x=0.5
        ),
        showlegend=False,
        height=500
    )
    return fig

# Fonction pour créer des graphiques avec thème Spotify
def create_spotify_theme():
    return dict(
        layout=dict(
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='#191414', size=12),
            colorway=['#1DB954', '#1ed760', '#1aa34a', '#168f3a']
        )
    )

def main():
    # En-tête principal avec style
    st.markdown("""
    <div class="main-header">
        <h1>🎵 SPOTIFY ANALYTICS PRO</h1>
        <h3>Intelligence Musicale & Analyse Avancée</h3>
        <p>Découvrez les tendances cachées de votre musique favorite</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Chargement des données
    df = load_data()
    if df is None:
        return
    
    # Sidebar premium avec logo
    with st.sidebar:
        st.markdown("""
        <div style='text-align: center; padding: 1rem; background: linear-gradient(135deg, #1DB954, #191414); border-radius: 10px; margin-bottom: 1rem; color: white;'>
            <h2>🎵 Navigation</h2>
            <p>Explorez vos données musicales</p>
        </div>
        """, unsafe_allow_html=True)
        
        section = st.selectbox(
            "🎯 Choisissez votre analyse:",
            ["🏠 Dashboard Exécutif", "🎼 Intelligence Genres", "🔗 Corrélations Avancées", 
             "📈 Tendances Temporelles", "⭐ Stars & Hits", "🔞 Contenu & Censure", 
             "☁️ Analyse Textuelle", "🔬 Lab Analytics", "🎯 Recommandations IA"]
        )
        
        # Insights en temps réel dans la sidebar
        st.markdown("---")
        st.markdown("### 💡 Insights Rapides")
        insights = generate_insights(df)
        for insight in insights:
            st.markdown(f"<div style='background: rgba(29, 185, 84, 0.1); padding: 0.5rem; margin: 0.25rem 0; border-radius: 5px; font-size: 0.8rem;'>{insight}</div>", unsafe_allow_html=True)
    
    # Dashboard Exécutif
    if section == "🏠 Dashboard Exécutif":
        st.markdown("<div class='section-header'><h2>📊 DASHBOARD EXÉCUTIF</h2></div>", unsafe_allow_html=True)
        
        # KPIs Principaux
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.metric("🎵 Total Tracks", f"{len(df):,}", delta="Collection complète")
        with col2:
            st.metric("🎤 Artistes Uniques", f"{df['artist'].nunique():,}", delta="+diversité")
        with col3:
            st.metric("🎼 Genres", df['genre'].nunique(), delta="Variété")
        with col4:
            st.metric("📊 Score Popularité Moyen", f"{df['popularity'].mean():.1f}/100", delta=f"{df['popularity'].std():.1f} écart-type")
        with col5:
            st.metric("⭐ Top Hit Score", df['popularity'].max(), delta=f"vs {df['popularity'].min()} min")
        
        st.markdown("---")
        
        # Vue d'ensemble interactive
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Distribution des genres avec effet 3D
            fig_genres_3d = px.pie(
                values=df['genre'].value_counts().head(10).values,
                names=df['genre'].value_counts().head(10).index,
                title="<b>🎼 Distribution des Genres Musicaux</b>",
                color_discrete_sequence=px.colors.qualitative.Set3,
                hole=0.4
            )
            fig_genres_3d.update_traces(
                textposition='inside',
                textinfo='percent+label',
                hovertemplate='<b>%{label}</b><br>Tracks: %{value}<br>Pourcentage: %{percent}<extra></extra>',
                textfont_size=12,
                marker=dict(line=dict(color='#FFFFFF', width=2))
            )
            fig_genres_3d.update_layout(
                height=500,
                font=dict(size=14),
                title_x=0.5,
                showlegend=True,
                legend=dict(orientation="h", yanchor="bottom", y=-0.3, xanchor="center", x=0.5)
            )
            st.plotly_chart(fig_genres_3d, use_container_width=True)
        
        with col2:
            # Profil audio radar
            features = ['danceability', 'energy', 'valence', 'acousticness']
            fig_radar = create_enhanced_radar_chart(df, features, "🎵 Profil Audio Global")
            st.plotly_chart(fig_radar, use_container_width=True)
        
        # Analyse temporelle premium
        st.markdown("### 📈 Evolution Temporelle Premium")
        yearly_data = df.groupby('year').agg({
            'song': 'count',
            'popularity': 'mean',
            'danceability': 'mean',
            'energy': 'mean'
        }).reset_index()
        
        fig_timeline = make_subplots(
            rows=2, cols=2,
            subplot_titles=('📊 Nombre de Tracks', '⭐ Popularité Moyenne', '💃 Danceabilité', '⚡ Énergie'),
            vertical_spacing=0.1
        )
        
        # Nombre de tracks avec gradient
        fig_timeline.add_trace(go.Scatter(
            x=yearly_data['year'], y=yearly_data['song'],
            fill='tonexty', fillcolor='rgba(29, 185, 84, 0.3)',
            line=dict(color='#1DB954', width=3),
            name='Tracks', hovertemplate='%{x}: %{y} tracks<extra></extra>'
        ), row=1, col=1)
        
        # Popularité avec barres colorées
        fig_timeline.add_trace(go.Bar(
            x=yearly_data['year'], y=yearly_data['popularity'],
            marker_color=yearly_data['popularity'],
            marker_colorscale='Viridis',
            name='Popularité', hovertemplate='%{x}: %{y:.1f}/100<extra></extra>'
        ), row=1, col=2)
        
        # Danceabilité
        fig_timeline.add_trace(go.Scatter(
            x=yearly_data['year'], y=yearly_data['danceability'],
            mode='lines+markers', line=dict(color='#ff6b6b', width=3),
            marker=dict(size=8, color='#ff6b6b'),
            name='Danceabilité', hovertemplate='%{x}: %{y:.2f}<extra></extra>'
        ), row=2, col=1)
        
        # Énergie
        fig_timeline.add_trace(go.Scatter(
            x=yearly_data['year'], y=yearly_data['energy'],
            mode='lines+markers', line=dict(color='#4ecdc4', width=3),
            marker=dict(size=8, color='#4ecdc4'),
            name='Énergie', hovertemplate='%{x}: %{y:.2f}<extra></extra>'
        ), row=2, col=2)
        
        fig_timeline.update_layout(height=600, showlegend=False, title_text="<b>📊 Analyse Temporelle Multi-Dimensionnelle</b>")
        st.plotly_chart(fig_timeline, use_container_width=True)
    
    # Intelligence Genres
    elif section == "🎼 Intelligence Genres":
        st.markdown("<div class='section-header'><h2>🎼 INTELLIGENCE GENRES</h2></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Analyse de popularité par genre avec bubble chart
            genre_stats = df.groupby('genre').agg({
                'popularity': ['mean', 'sum'],
                'song': 'count'
            }).round(2)
            genre_stats.columns = ['pop_mean', 'pop_total', 'track_count']
            genre_stats = genre_stats.reset_index()
            
            fig_bubble = px.scatter(
                genre_stats, x='pop_mean', y='pop_total', size='track_count',
                color='genre', hover_data=['track_count'],
                title="<b>🎯 Matrice Performance Genres</b>",
                labels={'pop_mean': 'Popularité Moyenne', 'pop_total': 'Popularité Totale'},
                size_max=60
            )
            fig_bubble.update_traces(opacity=0.8)
            fig_bubble.update_layout(height=500)
            st.plotly_chart(fig_bubble, use_container_width=True)
        
        with col2:
            # Radar comparatif des genres top 5
            top_genres = df['genre'].value_counts().head(5).index
            fig_radar_comp = go.Figure()
            
            colors = ['#1DB954', '#ff6b6b', '#4ecdc4', '#45b7d1', '#f9ca24']
            features_radar = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness']
            
            for i, genre in enumerate(top_genres):
                genre_data = df[df['genre'] == genre]
                values = genre_data[features_radar].mean().tolist()
                values += [values[0]]  # Fermer le radar
                
                fig_radar_comp.add_trace(go.Scatterpolar(
                    r=values,
                    theta=features_radar + [features_radar[0]],
                    fill='toself',
                    name=genre,
                    line_color=colors[i],
                    fillcolor=f'rgba({int(colors[i][1:3], 16)}, {int(colors[i][3:5], 16)}, {int(colors[i][5:7], 16)}, 0.1)'
                ))
            
            fig_radar_comp.update_layout(
                polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                title="<b>🎵 Profils Genres - Top 5</b>",
                height=500
            )
            st.plotly_chart(fig_radar_comp, use_container_width=True)
        
        # Heatmap avancée des caractéristiques par genre
        st.markdown("### 🔥 Heatmap Intelligence Musicale")
        audio_features = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness', 'liveness']
        genre_features = df.groupby('genre')[audio_features].mean()
        
        fig_heatmap = px.imshow(
            genre_features.T,
            labels=dict(x="Genres", y="Caractéristiques Audio", color="Intensité"),
            x=genre_features.index,
            y=audio_features,
            color_continuous_scale='RdYlGn',
            title="<b>🎨 Signature Audio par Genre</b>"
        )
        fig_heatmap.update_layout(height=600)
        st.plotly_chart(fig_heatmap, use_container_width=True)
    
    # Corrélations Avancées
    elif section == "🔗 Corrélations Avancées":
        st.markdown("<div class='section-header'><h2>🔗 CORRÉLATIONS AVANCÉES</h2></div>", unsafe_allow_html=True)
        
        # Matrice de corrélation premium
        numeric_cols = df.select_dtypes(exclude=['object']).columns
        correlation_matrix = df[numeric_cols].corr()
        
        # Masquer la diagonale pour plus de clarté
        mask = np.triu(np.ones_like(correlation_matrix, dtype=bool))
        correlation_matrix_masked = correlation_matrix.mask(mask)
        
        fig_corr_advanced = px.imshow(
            correlation_matrix_masked,
            text_auto='.2f',
            aspect='auto',
            color_continuous_scale='RdBu_r',
            title="<b>🧠 Matrice de Corrélation Intelligence</b>",
            labels=dict(color="Corrélation")
        )
        fig_corr_advanced.update_layout(height=700)
        st.plotly_chart(fig_corr_advanced, use_container_width=True)
        
        # Analyse des corrélations fortes
        col1, col2 = st.columns(2)
        
        with col1:
            # Top corrélations positives
            corr_pairs = []
            for i in range(len(correlation_matrix.columns)):
                for j in range(i+1, len(correlation_matrix.columns)):
                    corr_pairs.append((
                        correlation_matrix.columns[i],
                        correlation_matrix.columns[j],
                        correlation_matrix.iloc[i, j]
                    ))
            
            corr_df = pd.DataFrame(corr_pairs, columns=['Feature1', 'Feature2', 'Correlation'])
            top_positive = corr_df.nlargest(10, 'Correlation')
            
            fig_pos_corr = px.bar(
                top_positive, x='Correlation', y=top_positive['Feature1'] + ' vs ' + top_positive['Feature2'],
                orientation='h',
                color='Correlation',
                color_continuous_scale='Greens',
                title="<b>🔝 Top Corrélations Positives</b>"
            )
            st.plotly_chart(fig_pos_corr, use_container_width=True)
        
        with col2:
            # Scatter plot interactif avancé
            features_list = numeric_cols.tolist()
            x_feature = st.selectbox("Axe X:", features_list, index=0)
            y_feature = st.selectbox("Axe Y:", features_list, index=1)
            
            fig_scatter_adv = px.scatter(
                df, x=x_feature, y=y_feature,
                color='genre', size='popularity',
                hover_data=['artist', 'song'],
                title=f"<b>🎯 {y_feature.title()} vs {x_feature.title()}</b>",
                trendline="ols"
            )
            fig_scatter_adv.update_traces(marker=dict(opacity=0.7))
            st.plotly_chart(fig_scatter_adv, use_container_width=True)
    
    # Tendances Temporelles
    elif section == "📈 Tendances Temporelles":
        st.markdown("<div class='section-header'><h2>📈 TENDANCES TEMPORELLES</h2></div>", unsafe_allow_html=True)
        
        # Timeline interactive avec sélecteur de période
        year_range = st.slider(
            "Sélectionnez la période d'analyse:",
            min_value=int(df['year'].min()),
            max_value=int(df['year'].max()),
            value=(int(df['year'].min()), int(df['year'].max()))
        )
        
        df_filtered = df[(df['year'] >= year_range[0]) & (df['year'] <= year_range[1])]
        
        # Évolution multi-métriques
        yearly_evolution = df_filtered.groupby('year').agg({
            'song': 'count',
            'popularity': 'mean',
            'danceability': 'mean',
            'energy': 'mean',
            'valence': 'mean',
            'explicit': lambda x: (x == True).sum()
        }).reset_index()
        
        fig_evolution = make_subplots(
            rows=2, cols=3,
            subplot_titles=('📊 Volume Production', '⭐ Popularité', '💃 Danceabilité', '⚡ Énergie', '😊 Valence', '🔞 Contenu Explicite'),
            specs=[[{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}],
                   [{"secondary_y": False}, {"secondary_y": False}, {"secondary_y": False}]]
        )
        
        metrics = [('song', 1, 1), ('popularity', 1, 2), ('danceability', 1, 3), 
                  ('energy', 2, 1), ('valence', 2, 2), ('explicit', 2, 3)]
        colors = ['#1DB954', '#ff6b6b', '#4ecdc4', '#f9ca24', '#9b59b6', '#e74c3c']
        
        for i, (metric, row, col) in enumerate(metrics):
            fig_evolution.add_trace(
                go.Scatter(
                    x=yearly_evolution['year'],
                    y=yearly_evolution[metric],
                    mode='lines+markers',
                    line=dict(color=colors[i], width=3),
                    marker=dict(size=8),
                    name=metric
                ),
                row=row, col=col
            )
        
        fig_evolution.update_layout(height=800, showlegend=False, title_text="<b>📊 Evolution Multi-Dimensionnelle</b>")
        st.plotly_chart(fig_evolution, use_container_width=True)
        
        # Analyse des décennies
        st.markdown("### 🕰️ Analyse par Décennies")
        df_filtered['decade'] = (df_filtered['year'] // 10) * 10
        decade_analysis = df_filtered.groupby('decade').agg({
            'song': 'count',
            'popularity': 'mean',
            'danceability': 'mean',
            'energy': 'mean'
        }).reset_index()
        decade_analysis['decade'] = decade_analysis['decade'].astype(str) + 's'
        
        fig_decades = px.bar(
            decade_analysis, x='decade', y='song',
            color='popularity',
            title="<b>🎵 Production Musicale par Décennie</b>",
            labels={'song': 'Nombre de Tracks', 'decade': 'Décennie'},
            color_continuous_scale='Viridis'
        )
        st.plotly_chart(fig_decades, use_container_width=True)
    
    # Stars & Hits
    elif section == "⭐ Stars & Hits":
        st.markdown("<div class='section-header'><h2>⭐ STARS & HITS ANALYSIS</h2></div>", unsafe_allow_html=True)
        
        # Hall of Fame
        col1, col2 = st.columns(2)
        
        with col1:
            # Top artistes avec métriques avancées
            artist_stats = df.groupby('artist').agg({
                'song': 'count',
                'popularity': ['mean', 'max', 'sum'],
                'danceability': 'mean',
                'energy': 'mean'
            }).round(2)
            artist_stats.columns = ['track_count', 'avg_pop', 'max_pop', 'total_pop', 'avg_dance', 'avg_energy']
            artist_stats = artist_stats.reset_index().nlargest(20, 'total_pop')
            
            fig_artists_advanced = px.scatter(
                artist_stats, x='avg_pop', y='track_count',
                size='total_pop', color='max_pop',
                hover_name='artist',
                title="<b>🎤 Matrix Artistes: Impact vs Volume</b>",
                labels={'avg_pop': 'Popularité Moyenne', 'track_count': 'Nombre de Tracks'},
                color_continuous_scale='plasma'
            )
            st.plotly_chart(fig_artists_advanced, use_container_width=True)
        
        with col2:
            # Analyse des hits
            top_hits = df.nlargest(25, 'popularity')[['song', 'artist', 'popularity', 'year', 'genre']]
            
            fig_hits = px.sunburst(
                top_hits, path=['genre', 'artist', 'song'], values='popularity',
                title="<b>🌟 Hiérarchie des Hits</b>",
                color='popularity',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig_hits, use_container_width=True)
        
        # Top tracks avec timeline
        st.markdown("### 🏆 Timeline des Mega-Hits")
        mega_hits = df.nlargest(50, 'popularity')
        
        fig_hits_timeline = px.scatter(
            mega_hits, x='year', y='popularity',
            size='danceability', color='genre',
            hover_name='song',
            hover_data=['artist'],
            title="<b>📈 Evolution des Mega-Hits dans le Temps</b>",
            size_max=20
        )
        fig_hits_timeline.update_traces(opacity=0.8)
        st.plotly_chart(fig_hits_timeline, use_container_width=True)
        
        # Recommandation Engine Preview
        st.markdown("### 🤖 Aperçu Moteur de Recommandations")
        selected_artist = st.selectbox("Sélectionnez un artiste:", df['artist'].unique())
        artist_profile = df[df['artist'] == selected_artist][['danceability', 'energy', 'valence', 'acousticness']].mean()
        
        # Trouver des artistes similaires
        all_artists_profile = df.groupby('artist')[['danceability', 'energy', 'valence', 'acousticness']].mean()
        
        # Calculer la distance euclidienne
        distances = []
        for artist in all_artists_profile.index:
            if artist != selected_artist:
                distance = np.sqrt(((all_artists_profile.loc[artist] - artist_profile) ** 2).sum())
                distances.append((artist, distance))
        
        similar_artists = sorted(distances, key=lambda x: x[1])[:5]
        
        col1, col2 = st.columns(2)
        with col1:
            st.markdown(f"#### 🎵 Profil de {selected_artist}")
            fig_selected_radar = create_enhanced_radar_chart(
                df[df['artist'] == selected_artist], 
                ['danceability', 'energy', 'valence', 'acousticness'],
                f"Profil {selected_artist}"
            )
            st.plotly_chart(fig_selected_radar, use_container_width=True)
        
        with col2:
            st.markdown("#### 🔍 Artistes Similaires")
            for i, (artist, distance) in enumerate(similar_artists):
                similarity_score = max(0, 100 - (distance * 100))
                st.metric(f"#{i+1} {artist}", f"{similarity_score:.1f}% similarité")
    
    # Contenu & Censure
    elif section == "🔞 Contenu & Censure":
        st.markdown("<div class='section-header'><h2>🔞 ANALYSE CONTENU & CENSURE</h2></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Évolution du contenu explicite
            explicit_evolution = df.groupby(['year', 'explicit']).size().unstack(fill_value=0)
            explicit_evolution['total'] = explicit_evolution.sum(axis=1)
            explicit_evolution['explicit_pct'] = (explicit_evolution[True] / explicit_evolution['total'] * 100).fillna(0)
            
            fig_explicit_trend = go.Figure()
            fig_explicit_trend.add_trace(go.Scatter(
                x=explicit_evolution.index,
                y=explicit_evolution['explicit_pct'],
                fill='tonexty',
                mode='lines+markers',
                line=dict(color='#e74c3c', width=3),
                name='% Contenu Explicite'
            ))
            fig_explicit_trend.update_layout(
                title="<b>📈 Evolution du Contenu Explicite (%)</b>",
                xaxis_title="Année",
                yaxis_title="Pourcentage (%)",
                height=400
            )
            st.plotly_chart(fig_explicit_trend, use_container_width=True)
        
        with col2:
            # Distribution par genre du contenu explicite
            explicit_by_genre = df.groupby(['genre', 'explicit']).size().unstack(fill_value=0)
            explicit_by_genre['explicit_pct'] = (explicit_by_genre[True] / (explicit_by_genre[True] + explicit_by_genre[False]) * 100).fillna(0)
            explicit_by_genre = explicit_by_genre.sort_values('explicit_pct', ascending=True)
            
            fig_explicit_genre = px.bar(
                x=explicit_by_genre['explicit_pct'],
                y=explicit_by_genre.index,
                orientation='h',
                title="<b>🎼 Contenu Explicite par Genre (%)</b>",
                color=explicit_by_genre['explicit_pct'],
                color_continuous_scale='Reds'
            )
            fig_explicit_genre.update_layout(height=400)
            st.plotly_chart(fig_explicit_genre, use_container_width=True)
        
        # Analyse comparative explicite vs non-explicite
        st.markdown("### ⚖️ Analyse Comparative: Explicite vs Clean")
        
        comparison_features = ['popularity', 'danceability', 'energy', 'valence']
        explicit_comparison = df.groupby('explicit')[comparison_features].mean()
        
        fig_comparison = go.Figure()
        x_categories = ['Clean Content', 'Explicit Content']
        
        for feature in comparison_features:
            fig_comparison.add_trace(go.Bar(
                name=feature.title(),
                x=x_categories,
                y=[explicit_comparison.loc[False, feature], explicit_comparison.loc[True, feature]],
                text=[f"{explicit_comparison.loc[False, feature]:.2f}", f"{explicit_comparison.loc[True, feature]:.2f}"],
                textposition='auto'
            ))
        
        fig_comparison.update_layout(
            title="<b>📊 Comparaison Caractéristiques: Clean vs Explicit</b>",
            barmode='group',
            height=500
        )
        st.plotly_chart(fig_comparison, use_container_width=True)
    
    # Analyse Textuelle
    elif section == "☁️ Analyse Textuelle":
        st.markdown("<div class='section-header'><h2>☁️ ANALYSE TEXTUELLE AVANCÉE</h2></div>", unsafe_allow_html=True)
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Word Cloud Premium
            if not df['song'].empty:
                text = " ".join(df['song'].dropna().astype(str))
                wordcloud = WordCloud(
                    width=800, height=400,
                    background_color='white',
                    max_words=150,
                    colormap='viridis',
                    relative_scaling=0.5,
                    min_font_size=10
                ).generate(text)
                
                fig, ax = plt.subplots(figsize=(12, 6))
                ax.imshow(wordcloud, interpolation='bilinear')
                ax.axis('off')
                plt.title('🎵 Nuage de Mots - Titres Spotify', fontsize=20, color='#1DB954', pad=20)
                st.pyplot(fig)
        
        with col2:
            # Analyse des mots-clés
            st.markdown("### 🔍 Top Mots-Clés")
            words = ' '.join(df['song'].str.lower()).split()
            word_freq = pd.Series(words).value_counts().head(15)
            
            fig_words = px.bar(
                x=word_freq.values,
                y=word_freq.index,
                orientation='h',
                title="<b>📝 Mots les Plus Fréquents</b>",
                color=word_freq.values,
                color_continuous_scale='viridis'
            )
            fig_words.update_layout(height=500)
            st.plotly_chart(fig_words, use_container_width=True)
        
        # Analyse des titres par longueur
        st.markdown("### 📏 Analyse de la Longueur des Titres")
        df['title_length'] = df['song'].str.len()
        df['word_count'] = df['song'].str.split().str.len()
        
        col1, col2 = st.columns(2)
        with col1:
            fig_length = px.histogram(
                df, x='title_length',
                title="<b>📊 Distribution Longueur des Titres</b>",
                nbins=30,
                color_discrete_sequence=['#1DB954']
            )
            st.plotly_chart(fig_length, use_container_width=True)
        
        with col2:
            fig_words_dist = px.histogram(
                df, x='word_count',
                title="<b>📝 Distribution Nombre de Mots</b>",
                nbins=15,
                color_discrete_sequence=['#ff6b6b']
            )
            st.plotly_chart(fig_words_dist, use_container_width=True)
    
    # Lab Analytics
    elif section == "🔬 Lab Analytics":
        st.markdown("<div class='section-header'><h2>🔬 LABORATOIRE D'ANALYSE</h2></div>", unsafe_allow_html=True)
        
        # Interface de recherche avancée
        st.markdown("### 🎯 Explorateur de Données Personnalisé")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            selected_genres = st.multiselect("Genres:", df['genre'].unique(), default=df['genre'].unique()[:5])
        with col2:
            year_filter = st.slider("Années:", int(df['year'].min()), int(df['year'].max()), (2010, 2020))
        with col3:
            popularity_filter = st.slider("Popularité minimum:", 0, 100, 50)
        
        # Filtrer les données
        filtered_df = df[
            (df['genre'].isin(selected_genres)) & 
            (df['year'] >= year_filter[0]) & 
            (df['year'] <= year_filter[1]) & 
            (df['popularity'] >= popularity_filter)
        ]
        
        st.info(f"📊 {len(filtered_df)} tracks correspondent à vos critères")
        
        # Analyse comparative personnalisée
        col1, col2 = st.columns(2)
        
        with col1:
            # Scatter plot personnalisable
            numeric_features = df.select_dtypes(include=[np.number]).columns.tolist()
            x_axis = st.selectbox("Axe X:", numeric_features, index=0)
            y_axis = st.selectbox("Axe Y:", numeric_features, index=1)
            color_by = st.selectbox("Couleur par:", ['genre'] + numeric_features)
            size_by = st.selectbox("Taille par:", [None] + numeric_features)
            
            fig_custom = px.scatter(
                filtered_df, x=x_axis, y=y_axis,
                color=color_by, size=size_by,
                hover_data=['artist', 'song', 'year'],
                title=f"<b>🔍 {y_axis.title()} vs {x_axis.title()}</b>",
                opacity=0.7
            )
            fig_custom.update_layout(height=500)
            st.plotly_chart(fig_custom, use_container_width=True)
        
        with col2:
            # Statistiques dynamiques
            st.markdown("#### 📈 Statistiques Filtrées")
            
            stats_feature = st.selectbox("Analyser:", numeric_features)
            
            col2a, col2b = st.columns(2)
            with col2a:
                st.metric("Moyenne", f"{filtered_df[stats_feature].mean():.2f}")
                st.metric("Médiane", f"{filtered_df[stats_feature].median():.2f}")
            with col2b:
                st.metric("Écart-type", f"{filtered_df[stats_feature].std():.2f}")
                st.metric("Max", f"{filtered_df[stats_feature].max():.2f}")
            
            # Distribution de la feature sélectionnée
            fig_dist = px.box(
                filtered_df, y=stats_feature, x='genre',
                title=f"<b>📦 Distribution {stats_feature.title()} par Genre</b>"
            )
            fig_dist.update_layout(height=400)
            st.plotly_chart(fig_dist, use_container_width=True)
        
        # Matrice de corrélation sur données filtrées
        st.markdown("### 🧮 Matrice de Corrélation Dynamique")
        selected_features = st.multiselect(
            "Sélectionnez les caractéristiques à analyser:",
            numeric_features,
            default=['popularity', 'danceability', 'energy', 'valence']
        )
        
        if len(selected_features) > 1:
            corr_filtered = filtered_df[selected_features].corr()
            fig_corr_custom = px.imshow(
                corr_filtered,
                text_auto='.2f',
                title="<b>🔗 Corrélations sur Données Filtrées</b>",
                color_continuous_scale='RdBu_r'
            )
            st.plotly_chart(fig_corr_custom, use_container_width=True)
    
    # Recommandations IA
    elif section == "🎯 Recommandations IA":
        st.markdown("<div class='section-header'><h2>🎯 RECOMMANDATIONS IA</h2></div>", unsafe_allow_html=True)
        
        st.markdown("### 🤖 Moteur de Recommandations Intelligent")
        
        # Sélection d'une chanson de référence
        col1, col2 = st.columns([2, 1])
        
        with col1:
            # Interface de recherche de chanson
            search_artist = st.selectbox("Sélectionnez un artiste:", [''] + sorted(df['artist'].unique().tolist()))
            
            if search_artist:
                artist_songs = df[df['artist'] == search_artist]['song'].tolist()
                selected_song = st.selectbox("Sélectionnez une chanson:", artist_songs)
                
                if selected_song:
                    reference_song = df[(df['artist'] == search_artist) & (df['song'] == selected_song)].iloc[0]
                    
                    # Afficher les caractéristiques de la chanson de référence
                    st.markdown(f"#### 🎵 Analyse de: {selected_song} par {search_artist}")
                    
                    col1a, col1b, col1c, col1d = st.columns(4)
                    with col1a:
                        st.metric("Popularité", f"{reference_song['popularity']}/100")
                    with col1b:
                        st.metric("Danceabilité", f"{reference_song['danceability']:.2f}")
                    with col1c:
                        st.metric("Énergie", f"{reference_song['energy']:.2f}")
                    with col1d:
                        st.metric("Valence", f"{reference_song['valence']:.2f}")
                    
                    # Trouver des chansons similaires
                    features_for_similarity = ['danceability', 'energy', 'valence', 'acousticness', 'speechiness', 'liveness']
                    
                    # Calculer la similarité
                    similarities = []
                    reference_features = reference_song[features_for_similarity].values
                    
                    for idx, row in df.iterrows():
                        if idx != reference_song.name:  # Exclure la chanson de référence
                            song_features = row[features_for_similarity].values
                            # Distance euclidienne normalisée
                            distance = np.sqrt(np.sum((reference_features - song_features) ** 2))
                            similarity = max(0, 100 - (distance * 100))
                            similarities.append((idx, similarity))
                    
                    # Trier par similarité et prendre le top 10
                    similarities.sort(key=lambda x: x[1], reverse=True)
                    top_similar = similarities[:10]
                    
                    # Créer le DataFrame des recommandations
                    recommendations = []
                    for idx, similarity in top_similar:
                        song_data = df.iloc[idx]
                        recommendations.append({
                            'Chanson': song_data['song'],
                            'Artiste': song_data['artist'],
                            'Genre': song_data['genre'],
                            'Année': song_data['year'],
                            'Popularité': song_data['popularity'],
                            'Similarité': f"{similarity:.1f}%"
                        })
                    
                    recommendations_df = pd.DataFrame(recommendations)
                    
                    st.markdown("#### 🎯 Top 10 Recommandations")
                    st.dataframe(recommendations_df, use_container_width=True)
        
        with col2:
            if 'reference_song' in locals():
                # Radar chart de comparaison
                fig_comparison_radar = go.Figure()
                
                # Chanson de référence
                ref_values = reference_song[features_for_similarity].values.tolist()
                ref_values += [ref_values[0]]
                
                fig_comparison_radar.add_trace(go.Scatterpolar(
                    r=ref_values,
                    theta=features_for_similarity + [features_for_similarity[0]],
                    fill='toself',
                    name=f"{selected_song}",
                    line_color='#1DB954'
                ))
                
                # Profil moyen des recommandations
                if recommendations:
                    rec_indices = [idx for idx, _ in top_similar[:5]]  # Top 5 pour la moyenne
                    avg_rec_features = df.iloc[rec_indices][features_for_similarity].mean().values.tolist()
                    avg_rec_features += [avg_rec_features[0]]
                    
                    fig_comparison_radar.add_trace(go.Scatterpolar(
                        r=avg_rec_features,
                        theta=features_for_similarity + [features_for_similarity[0]],
                        fill='toself',
                        name="Moy. Recommandations",
                        line_color='#ff6b6b'
                    ))
                
                fig_comparison_radar.update_layout(
                    polar=dict(radialaxis=dict(visible=True, range=[0, 1])),
                    title="<b>🎵 Profil Comparatif</b>",
                    height=400
                )
                st.plotly_chart(fig_comparison_radar, use_container_width=True)
        
        # Analyse des tendances de recommandation
        if 'recommendations_df' in locals() and not recommendations_df.empty:
            st.markdown("### 📊 Analyse des Recommandations")
            
            col1, col2 = st.columns(2)
            
            with col1:
                # Distribution par genre des recommandations
                genre_dist = recommendations_df['Genre'].value_counts()
                fig_rec_genre = px.pie(
                    values=genre_dist.values,
                    names=genre_dist.index,
                    title="<b>🎼 Distribution par Genre</b>",
                    hole=0.4
                )
                st.plotly_chart(fig_rec_genre, use_container_width=True)
            
            with col2:
                # Timeline des recommandations
                fig_rec_timeline = px.scatter(
                    recommendations_df, x='Année', y='Popularité',
                    size=[float(x.replace('%', '')) for x in recommendations_df['Similarité']],
                    hover_name='Chanson',
                    hover_data=['Artiste'],
                    title="<b>📈 Timeline Popularité vs Année</b>",
                    color='Genre'
                )
                st.plotly_chart(fig_rec_timeline, use_container_width=True)
        
        # Section bonus: Générateur de playlist
        st.markdown("---")
        st.markdown("### 🎵 Générateur de Playlist Thématique")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            mood = st.selectbox("Ambiance:", ["Énergique", "Détendue", "Dansante", "Mélancolique", "Festive"])
        with col2:
            playlist_size = st.slider("Taille de la playlist:", 5, 50, 20)
        with col3:
            decade = st.selectbox("Décennie:", ["Toutes"] + [f"{d}s" for d in range(1960, 2030, 10)])
        
        if st.button("🎵 Générer Playlist", type="primary"):
            # Logique de génération basée sur l'ambiance
            mood_filters = {
                "Énergique": {"energy": (0.7, 1.0), "valence": (0.5, 1.0)},
                "Détendue": {"energy": (0.0, 0.5), "valence": (0.3, 0.8)},
                "Dansante": {"danceability": (0.7, 1.0), "energy": (0.6, 1.0)},
                "Mélancolique": {"valence": (0.0, 0.4), "energy": (0.2, 0.6)},
                "Festive": {"danceability": (0.8, 1.0), "valence": (0.7, 1.0), "energy": (0.7, 1.0)}
            }
            
            filtered_playlist = df.copy()
            
            # Appliquer les filtres d'ambiance
            for feature, (min_val, max_val) in mood_filters[mood].items():
                filtered_playlist = filtered_playlist[
                    (filtered_playlist[feature] >= min_val) & 
                    (filtered_playlist[feature] <= max_val)
                ]
            
            # Filtre de décennie
            if decade != "Toutes":
                decade_start = int(decade.replace('s', ''))
                filtered_playlist = filtered_playlist[
                    (filtered_playlist['year'] >= decade_start) & 
                    (filtered_playlist['year'] < decade_start + 10)
                ]
            
            # Sélectionner les meilleures chansons
            if len(filtered_playlist) >= playlist_size:
                playlist = filtered_playlist.nlargest(playlist_size, 'popularity')[
                    ['song', 'artist', 'year', 'genre', 'popularity', 'danceability', 'energy', 'valence']
                ]
                
                st.success(f"🎵 Playlist '{mood}' générée avec {len(playlist)} chansons!")
                st.dataframe(playlist.reset_index(drop=True), use_container_width=True)
                
                # Visualisation de la playlist
                fig_playlist = px.scatter(
                    playlist, x='energy', y='valence',
                    size='popularity', color='genre',
                    hover_name='song',
                    hover_data=['artist', 'year'],
                    title=f"<b>🎵 Carte Émotionnelle - Playlist {mood}</b>"
                )
                st.plotly_chart(fig_playlist, use_container_width=True)
            else:
                st.warning(f"⚠️ Seulement {len(filtered_playlist)} chansons correspondent à vos critères. Essayez d'ajuster les filtres.")

if __name__ == "__main__":
    main()