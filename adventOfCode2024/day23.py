def intersection(lst1, lst2):
    return set(lst1).intersection(lst2)


with open("day23.txt") as input_file:
    edges = set((sorted(x.split('-'))[0], sorted(x.split('-'))[1]) for x in input_file.read().split('\n'))
    nodes = {}
    triplets = set()
    for edge in edges:
        start, end = edge
        if start in nodes:
            nodes[start].append(end)
        else:
            nodes[start] = [end]
        if end in nodes:
            nodes[end].append(start)
        else:
            nodes[end] = [start]
    for start_node, node_edges in nodes.items():
        for end_node in node_edges:
            if intersection(nodes[start_node], nodes[end_node]):
                for x in intersection(nodes[start_node], nodes[end_node]):
                    triplets.add(tuple(sorted([start_node, end_node, x])))
    count = 0
    for triplet in triplets:
        for node in triplet:
            if node.startswith('t'):
                # print(triplet)
                count+=1
                break
    print(count)


import networkx as nx

def find_largest_regular_graph(G):

    max_size = 0
    max_regular_subgraph = None

    for k in range(G.number_of_nodes(), 0, -1):
        for H in nx.find_cliques(G):
            if len(H) < k:
                continue
            subgraph = G.subgraph(H)
            if nx.is_regular(subgraph) and subgraph.number_of_nodes() > max_size:
                max_size = subgraph.number_of_nodes()
                max_regular_subgraph = subgraph

    return max_regular_subgraph

# Example usage
G = nx.Graph()
G.add_edges_from(edges)

largest_regular_subgraph = find_largest_regular_graph(G)

if largest_regular_subgraph:
    print("Nodes:", sorted(largest_regular_subgraph.nodes))
    print("Edges:", largest_regular_subgraph.edges)
    largest_regular = sorted(largest_regular_subgraph.nodes)
    output = ''
    for node in largest_regular:
        output += "," + node
    print(output[1:])
else:
    print("No regular subgraph found.")

