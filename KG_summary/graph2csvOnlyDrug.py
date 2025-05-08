import networkx as nx
import pandas as pd


graph = nx.read_graphml("/UniD3/KG_building_level2/level2_T1_70B/graph_chunk_entity_relation.graphml")  

drug_nodes = []
for node_id, data in graph.nodes(data=True):
    entity_type = data.get("entity_type", "").strip('"')
    if entity_type == "DRUG":
        drug_nodes.append({
            "id": node_id
        })


df = pd.DataFrame(drug_nodes)
df.to_csv("drug_entities.csv", index=False)
print("DRUG num:", len(df))
