import streamlit as st
import pandas as pd
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
import urllib.request
import json
import plotly.graph_objects as go


st.set_page_config(layout="wide")
# df = pd.read_csv('mini-projet/donnees_ventes_etudiants.csv')
# Charger les données depuis un fichier CSV
@st.cache_data
def load_data():
    df = pd.read_csv('mini-projet/donnees_ventes_etudiants.csv')
    return df
df = load_data()




# Convertir la colonne de dates en datetime
df['order_date'] = pd.to_datetime(df['order_date'])

# Créer une nouvelle colonne "State Complet" en remplaçant les noms abrégés par les noms complets
state_abbr_to_full = {
   'AL': 'Alabama',
    'AK': 'Alaska',
    'AZ': 'Arizona',
    'AR': 'Arkansas',
    'CA': 'California',
    'CO': 'Colorado',
    'CT': 'Connecticut',
    'DE': 'Delaware',
    'FL': 'Florida',
    'GA': 'Georgia',
    'HI': 'Hawaii',
    'ID': 'Idaho',
    'IL': 'Illinois',
    'IN': 'Indiana',
    'IA': 'Iowa',
    'KS': 'Kansas',
    'KY': 'Kentucky',
    'LA': 'Louisiana',
    'ME': 'Maine',
    'MD': 'Maryland',
    'MA': 'Massachusetts',
    'MI': 'Michigan',
    'MN': 'Minnesota',
    'MS': 'Mississippi',
    'MO': 'Missouri',
    'MT': 'Montana',
    'NE': 'Nebraska',
    'NV': 'Nevada',
    'NH': 'New Hampshire',
    'NJ': 'New Jersey',
    'NM': 'New Mexico',
    'NY': 'New York',
    'NC': 'North Carolina',
    'ND': 'North Dakota',
    'OH': 'Ohio',
    'OK': 'Oklahoma',
    'OR': 'Oregon',
    'PA': 'Pennsylvania',
    'RI': 'Rhode Island',
    'SC': 'South Carolina',
    'SD': 'South Dakota',
    'TN': 'Tennessee',
    'TX': 'Texas',
    'UT': 'Utah',
    'VT': 'Vermont',
    'VA': 'Virginia',
    'WA': 'Washington',
    'WV': 'West Virginia',
    'WI': 'Wisconsin',
    'WY': 'Wyoming'
}
df['State Complet'] = df['State'].map(state_abbr_to_full)

# Ajout les coordonnées géographiques (latitude et longitude)
state_coordinates = {
    'Alabama': {'latitude': 32.806671, 'longitude': -86.791130},
    'Alaska': {'latitude': 61.370716, 'longitude': -152.404419},
    'Arizona': {'latitude': 33.729759, 'longitude': -111.431221},
    'Arkansas': {'latitude': 34.969704, 'longitude': -92.373123},
    'California': {'latitude': 36.116203, 'longitude': -119.681564},
    'Colorado': {'latitude': 39.059811, 'longitude': -105.311104},
    'Connecticut': {'latitude': 41.597782, 'longitude': -72.755371},
    'Delaware': {'latitude': 39.318523, 'longitude': -75.507141},
    'Florida': {'latitude': 27.766279, 'longitude': -81.686783},
    'Georgia': {'latitude': 33.040619, 'longitude': -83.643074},
    'Hawaii': {'latitude': 21.094318, 'longitude': -157.498337},
    'Idaho': {'latitude': 44.240459, 'longitude': -114.478828},
    'Illinois': {'latitude': 40.349457, 'longitude': -88.986137},
    'Indiana': {'latitude': 39.849426, 'longitude': -86.258278},
    'Iowa': {'latitude': 42.011539, 'longitude': -93.210526},
    'Kansas': {'latitude': 38.526600, 'longitude': -96.726486},
    'Kentucky': {'latitude': 37.668140, 'longitude': -84.670067},
    'Louisiana': {'latitude': 31.169546, 'longitude': -91.867805},
    'Maine': {'latitude': 44.693947, 'longitude': -69.381927},
    'Maryland': {'latitude': 39.063946, 'longitude': -76.802101},
    'Massachusetts': {'latitude': 42.230171, 'longitude': -71.530106},
    'Michigan': {'latitude': 43.326618, 'longitude': -84.536095},
    'Minnesota': {'latitude': 45.694454, 'longitude': -93.900192},
    'Mississippi': {'latitude': 32.741646, 'longitude': -89.678696},
    'Missouri': {'latitude': 38.456085, 'longitude': -92.288368},
    'Montana': {'latitude': 46.921925, 'longitude': -110.454353},
    'Nebraska': {'latitude': 41.125370, 'longitude': -98.268082},
    'Nevada': {'latitude': 38.313515, 'longitude': -117.055374},
    'New Hampshire': {'latitude': 43.452492, 'longitude': -71.563896},
    'New Jersey': {'latitude': 40.298904, 'longitude': -74.521011},
    'New Mexico': {'latitude': 34.840515, 'longitude': -106.248482},
    'New York': {'latitude': 42.165726, 'longitude': -74.948051},
    'North Carolina': {'latitude': 35.630066, 'longitude': -79.806419},
    'North Dakota': {'latitude': 47.528912, 'longitude': -99.784012},
    'Ohio': {'latitude': 40.388783, 'longitude': -82.764915},
    'Oklahoma': {'latitude': 35.565342, 'longitude': -96.928917},
    'Oregon': {'latitude': 44.572021, 'longitude': -122.070938},
    'Pennsylvania': {'latitude': 40.590752, 'longitude': -77.209755},
    'Rhode Island': {'latitude': 41.680893, 'longitude': -71.511780},
    'South Carolina': {'latitude': 33.856892, 'longitude': -80.945007},
    'South Dakota': {'latitude': 44.299782, 'longitude': -99.438828},
    'Tennessee': {'latitude': 35.747845, 'longitude': -86.692345},
    'Texas': {'latitude': 31.054487, 'longitude': -97.563461},
    'Utah': {'latitude': 40.150032, 'longitude': -111.862434},
    'Vermont': {'latitude': 44.045876, 'longitude': -72.710686},
    'Virginia': {'latitude': 37.769337, 'longitude': -78.169968},
    'Washington': {'latitude': 47.400902, 'longitude': -121.490494},
    'West Virginia': {'latitude': 38.491226, 'longitude': -80.954570},
    'Wisconsin': {'latitude': 44.268543, 'longitude': -89.616508},
    'Wyoming': {'latitude': 42.755966, 'longitude': -107.302490}
}

def get_latitude(state):
    return state_coordinates.get(state, {}).get('latitude')

def get_longitude(state):
    return state_coordinates.get(state, {}).get('longitude')

df['Latitude'] = df['State Complet'].apply(get_latitude)
df['Longitude'] = df['State Complet'].apply(get_longitude)

# Filtrage des données
st.title("Dashboard de Ventes")

# Période de vente
st.subheader("Période de Vente")
col_start,col_end = st.columns(2)
start_date = col_start.date_input("Date de début", df['order_date'].min())
end_date = col_end.date_input("Date de fin", df['order_date'].max())
# Convertir les dates de début et de fin en datetime64[ns]
start_date = pd.to_datetime(start_date)
end_date = pd.to_datetime(end_date)

# Filtrer le DataFrame en fonction de la période sélectionnée
filtered_df = df[(df['order_date'] >= start_date) & (df['order_date'] <= end_date)]

# Filtrage interactif
st.sidebar.subheader("Choisir votre filtre")
regions = st.sidebar.multiselect("Région", filtered_df['Region'].unique())


# Appliquer les filtres progressivement
if regions:
    filtered_df = filtered_df[filtered_df['Region'].isin(regions)]
    states = st.sidebar.multiselect("State", filtered_df['State Complet'].unique())
else:
    states = st.sidebar.multiselect("State", filtered_df['State Complet'].unique())
if states:
    filtered_df = filtered_df[filtered_df['State Complet'].isin(states)]
    countries = st.sidebar.multiselect("Pays", filtered_df['County'].unique())
else:
    countries = st.sidebar.multiselect("Pays", filtered_df['County'].unique())
if countries:
    filtered_df = filtered_df[filtered_df['County'].isin(countries)]
    cities = st.sidebar.multiselect("Ville", filtered_df['City'].unique())
else:
    cities = st.sidebar.multiselect("Ville", filtered_df['City'].unique())
if cities:
    filtered_df = filtered_df[filtered_df['City'].isin(cities)]
    status = st.sidebar.multiselect("Statut de la commande", filtered_df['status'].unique())
else:
    status = st.sidebar.multiselect("Statut de la commande", filtered_df['status'].unique())
if status:
    filtered_df = filtered_df[filtered_df['status'].isin(status)]

# Afficher les données filtrées
if not filtered_df.empty:
    st.write(filtered_df)
else:
    st.write("Aucune donnée ne correspond aux filtres sélectionnés")


# KPIs
total_sales = filtered_df['total'].sum()
distinct_customers = filtered_df['cust_id'].nunique()
total_orders = filtered_df['order_id'].nunique()

st.subheader("Les KPIs")
col1, col2, col3 = st.columns(3)
col1.subheader(f"Nombre total de Ventes: {total_sales}")
col2.subheader(f"Nombre distinct de Clients: {distinct_customers}")
col3.subheader(f"Nombre total de Commandes: {total_orders}")

# Graphiques interactifs
st.subheader("Graphiques")
# Afficher les données filtrées
if not filtered_df.empty:
    # Divisez la page en deux colonnes
    col1, col2 = st.columns(2)
    # Graphique 1 : Diagramme en barre pour le nombre total de ventes par catégorie
    with col1:
        fig1 = px.bar(filtered_df, x='category',y ='Nombre de vente', title='Nombre total de ventes par Catégorie')
        st.plotly_chart(fig1, use_container_width=True)

    # Graphique 2 : Diagramme circulaire pour le nombre total de ventes par région
    with col2:
        fig2 = px.pie(filtered_df, names='Region', title='Répartition des ventes par Région')
        st.plotly_chart(fig2, use_container_width=True)

    # Graphique 3 : Créer un graphique en barres pour le TOP 10 des meilleurs clients
    with col1:
        top_sellers = filtered_df['full_name'].value_counts().head(10).reset_index()
        top_sellers.columns = ['Client', 'Count']
        fig3 = px.bar(top_sellers, x='Client', y='Count', title='TOP 10 des Meilleurs Clients')
        st.plotly_chart(fig3, use_container_width=True)

    # Graphique 4 : Histogramme de la répartition de l'âge des clients
    with col2:
        # Créez un histogramme en utilisant Plotly Express
        fig = px.histogram(filtered_df, x='age', nbins=20, title="Répartition de l'âge des clients")

        # Personnalisation des couleurs
        fig.update_traces(marker_color='skyblue')

        # Titre et étiquettes des axes
        fig.update_layout(xaxis_title='Âge', yaxis_title='Nombre de clients')

        # Affichez le graphique Plotly
        st.plotly_chart(fig, use_container_width=True)

        # fig4, ax4 = plt.subplots()
        # sns.histplot(filtered_df['age'], kde=True, color='skyblue')
        # plt.title("Répartition de l'âge des clients")
        # plt.xlabel('Âge')
        # plt.ylabel('Nombre de client')
        # st.pyplot(fig4)

    # graphique 5 : Nombre total de Ventes par Mois
    with col1:
        
        monthly_sales = filtered_df.groupby([filtered_df['order_date'].dt.year, filtered_df['order_date'].dt.month])['total'].sum()
        monthly_sales.index = pd.to_datetime(monthly_sales.index.map(lambda x: f"{x[0]}-{x[1]}-01"))

        st.subheader("Nombre total de Ventes par Mois")
        fig6 = px.line(monthly_sales, x=monthly_sales.index, y=monthly_sales.values, title="Nombre total de Ventes par Mois")
        st.plotly_chart(fig6, use_container_width=True)

    # graphique 6 : Carte choroplèthe
    with col2:
        # Récupérer le GeoJSON des États
        with urllib.request.urlopen('https://raw.githubusercontent.com/PublicaMundi/MappingAPI/master/data/geojson/us-states.json') as response:
            states_geojson = json.load(response)


        # Carte choroplèthe
        st.subheader("Nombre total de Ventes par État")
        state_sales = df.groupby('State Complet')['total'].sum().reset_index()
        fig = px.choropleth(
            state_sales,
            geojson=states_geojson,
            locations='State Complet',
            featureidkey="properties.name",
            color='total',
            color_continuous_scale="Viridis",
            range_color=(state_sales['total'].min(), state_sales['total'].max()),
            scope="usa",
            labels={'total': 'Nombre total de Ventes'}
        )
        # Mettre à jour la mise en page de la carte
        fig.update_geos(fitbounds="locations", visible=False)
        st.plotly_chart(fig, use_container_width=True)
        
else:
    st.write("Aucune donnée ne correspond aux filtres sélectionnés")

# # Diagramme en barre pour le nombre total de ventes par catégorie
# fig1 = px.bar(filtered_df, x='category', title='Nombre total de ventes par Catégorie')
# st.plotly_chart(fig1, use_container_width=True)

# # Diagramme circulaire pour le nombre total de ventes par région
# fig2 = px.pie(filtered_df, names='Region', title='Répartition des ventes par Région')
# st.plotly_chart(fig2, use_container_width=True)

# # Obtenir le TOP 10 des meilleurs Clients
# top_sellers = filtered_df['full_name'].value_counts().head(10).reset_index()
# top_sellers.columns = ['Client', 'Count']

# # Créer un graphique en barres
# fig3 = px.bar(top_sellers, x='Client', y='Count', title='TOP 10 des Meilleurs Clients')


# # Histogramme de la répartition de l'âge des clients
# st.subheader("Répartition de l'âge des clients")
# fig4, ax4 = plt.subplots()
# sns.histplot(filtered_df['age'], kde=True, color='skyblue')
# plt.title("Répartition de l'âge des clients")
# plt.xlabel('Âge')
# plt.ylabel('Nombre de client')
# st.pyplot(fig4)


# # Diagramme en barre du nombre d'hommes et de femmes
# st.subheader("Répartition par Genre (Hommes/Femmes)")
# fig5, ax5 = plt.subplots()
# sns.countplot(x='Gender', data=filtered_df, palette='Set2')
# plt.title('Répartition par Genre (Hommes/Femmes)')
# plt.xlabel('Genre')
# plt.ylabel('Nombre de clients')
# # Afficher le graphique en barres
# st.pyplot(fig5)


# # Récupérer le GeoJSON des États
#         with urllib.request.urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
#             states_geojson = json.load(response)

#         # Carte choroplèthe
#         st.subheader("Nombre total de Ventes par État")
#         state_sales = df.groupby('State Complet')['total'].sum().reset_index()
#         fig = px.choropleth(
#             state_sales,
#             geojson=states_geojson,
#             locations='State Complet',
#             color='total',
#             color_continuous_scale="Viridis",
#             range_color=(state_sales['total'].min(), state_sales['total'].max()),
#             scope="usa",
#             labels={'total': 'Nombre total de Ventes'}
#         )
#         # Mettre à jour la mise en page de la carte
#         fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0})
#         # Afficher la carte dans Streamlit
#         st.plotly_chart(fig, use_container_width=True)
