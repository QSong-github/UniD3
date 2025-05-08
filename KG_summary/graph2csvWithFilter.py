import networkx as nx
import pandas as pd
import random

def is_numeric(s):
    """Check if a string represents a numeric value."""
    try:
        float(s)  # Try converting to float
        return True
    except ValueError:
        return False

def save_filtered_graphml_to_csv(graphml_file, node_csv, edge_csv, entity_types):
    G = nx.read_graphml(graphml_file)

    if entity_types is not None:
        filtered_nodes = {node: attrs for node, attrs in G.nodes(data=True) if attrs.get("entity_type") in entity_types}
    else:
        filtered_nodes = {node: attrs for node, attrs in G.nodes(data=True)}

    node_data = []
    for node, attrs in filtered_nodes.items():
        attrs['node_id'] = node 
        node_data.append(attrs)
    
    edge_data = []
    for source, target, attrs in G.edges(data=True):
        weight = attrs.get("weight", "1")  
        keywords = attrs.get("keywords", "")

        if float(weight) > 1:
            attrs["weight"] = round(random.uniform(0.1, 1.0), 2)

        if is_numeric(keywords):
            attrs["keywords"] = " "
        
        if source in filtered_nodes and target in filtered_nodes:
            attrs['source'] = source
            attrs['target'] = target
            edge_data.append(attrs)
    

    pd.DataFrame(node_data).to_csv(node_csv, index=False)
    pd.DataFrame(edge_data).to_csv(edge_csv, index=False)


t1={'"DRUG"','"DISEASE"', '"GENE"', '"DRUG CLASS"', '"DRUG TYPE"', '"DISEASE SUBTYPE"', '"DISEASE CATEGORY"', '"GENE/TARGET"', '"GENES"', '"GENE FAMILY"', '"GENE/PROTEIN"'}
t2={'"DRUG"','"DISEASE"', '"GENE"', '"DRUG CLASS"', '"DISEASE SUBTYPE"', '"DISEASE CATEGORY"', '"GENE/TARGET"', '"GENES"', '"GENE FAMILY"', '"GENE/PROTEIN"', '"GENE MUTATION"'}
t3={'"DRUG"','"DISEASE"', '"GENE"', '"DRUG CLASS"', '"DISEASE SUBTYPE"', '"DISEASE CATEGORY"', '"GENE/TARGET"', '"GENES"', '"GENE FAMILY"', '"GENE/PROTEIN"', '"GENE MUTATION"', '"GENE VARIANT"', '"GENE SET"', '"GENE GROUP"'}
selected_entity_type = t2
selected_entity_type = None


save_filtered_graphml_to_csv("/UniD3/KG_building_level2/level2_T3_70B/graph_chunk_entity_relation.graphml", "./output/filtered_nodes.csv", "./output/filtered_edges.csv", entity_types=selected_entity_type)



