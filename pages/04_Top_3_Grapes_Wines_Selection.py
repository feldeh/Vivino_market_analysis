import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import json
from pathlib import Path
import matplotlib.pyplot as plt
import seaborn as sns
import sqlite3


db_path = Path.cwd() / 'data' / 'db' / 'vivino.db'
conn = sqlite3.connect(db_path)
cursor = conn.cursor()


def fetch_top3_grapes():
    query = """
    SELECT
        grapes.name AS grape_name,
        sum(most_used_grapes_per_country.wines_count) AS global_wine_count
    FROM grapes
    JOIN most_used_grapes_per_country ON most_used_grapes_per_country.grape_id = grapes.id
    GROUP BY grapes.id
    ORDER BY global_wine_count
    DESC
    LIMIT 3;
    """
    df = pd.read_sql(query, conn)
    return df


df = fetch_top3_grapes()

st.title("Exploring the Finest: 3 Top Grape Varieties and Their Best Wines")

col1, col2 = st.columns(2)

with col2:
    st.markdown("##### Top 3 grapes by wine count")
    st.write(df)

with col1:
    st.markdown("##### Global Wine Count vs Grape Name")
    fig, ax = plt.subplots(figsize=(8, 6))
    ax = sns.barplot(x='grape_name', y='global_wine_count', data=df, color='lightgreen', width=0.4)
    ax.set_ylabel('Global Wine Count')
    ax.set_xlabel('Grape Name')
    plt.xticks(rotation=45, ha='right')
    st.pyplot(fig)


grape_wine_path = Path.cwd() / "data" / "csv_streamlit" / "grape_wine.csv"
df = pd.read_csv(grape_wine_path)


unique_grapes = df.grape.unique()
unique_wines = df.wines_names.unique()

json_df = df.to_json(orient="values")
dict_converted = json.loads(json_df)

nodes = []
edges = []
grapes = []
wines = []

for data in dict_converted:
    type_grape = data[4]
    wines_names = data[1]
    rank = data[2]

    if wines_names not in wines:
        nodes.append(Node(id=wines_names, label=str(rank), shape='CURVE_SMOOTH', color='#FDD00F'))
        wines.append(wines_names)

    if type_grape not in grapes:
        nodes.append(Node(id=type_grape, label=type_grape, shape='CURVE_SMOOTH', color='#07A7A6'))
        grapes.append(type_grape)

    edges.append(Edge(source=wines_names, target=type_grape))


config = Config(width=750,
                height=950,
                directed=True,
                physics=True,
                hierarchical=False,
                nodeHighlightBehavior=True,
                highlightColor="#F7A7A6",
                collapsible=True,
                node={'labelProperty': 'label'}
                )

return_value = agraph(nodes=nodes,
                      edges=edges,
                      config=config)
