import streamlit as st
import pandas as pd
from streamlit_agraph import agraph, Node, Edge, Config
import json
from pathlib import Path


st.title("Exploring the Finest: 3 Top Grape Varieties and Their 5 Best Wines")

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


config = Config(width=1000,
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
