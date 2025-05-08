import pandas as pd

def process_graph_data(node_file, edge_file, output_file):
    node_df = pd.read_csv(node_file, sep=None, engine='python')
    edge_df = pd.read_csv(edge_file, sep=None, engine='python')
    
    node_df.columns = node_df.columns.str.strip()
    edge_df.columns = edge_df.columns.str.strip()
    
    print("Node file columns:", node_df.columns)
    print("Edge file columns:", edge_df.columns)
    
    node_content = {}
    
    for _, row in node_df.iterrows():
        node_id = row['node_id']
        content = f"entity: {row['node_id']} "
        content += f"entity_type: {row['entity_type']} "
        content += f"entity description: {row['description']} "
        node_content[node_id] = content
    
    for _, row in edge_df.iterrows():
        source, target = row['source'], row['target']
        edge_info = f"relation weight: {row['weight']} relation: {row['description']} keywords: {row['keywords']} "
        
        if source in node_content:
            node_content[source] += edge_info + f"connected to: {target} "
        if target in node_content:
            node_content[target] += edge_info + f"connected to: {source} "
    
    for key in node_content:
        node_content[key] = node_content[key].replace('\t', ' ')
    

    result_df = pd.DataFrame(list(node_content.items()), columns=['node', 'content'])
    result_df.to_csv(output_file, index=False)
    

process_graph_data('/UniD3/KG_summary/output/filtered_nodes.csv', '/UniD3/KG_summary/output/filtered_edges.csv', 'summary.csv')
