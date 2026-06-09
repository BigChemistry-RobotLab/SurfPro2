import json
import networkx as nx
from pathlib import Path
import matplotlib.pyplot as plt
from network_layouts import generate_network_layout
from network_layouts import draw_arrow_connectors
from network_layouts import scatter_plot_array


SKIP_NODES = [
    "primary_source",
    "inaccesible",
]


def main():
    text = Path("./data/citation_graph.json").read_text()
    citations = json.loads(text)

    edge_list = []
    for c in citations:
        for d in citations[c]:
            if d in SKIP_NODES:
                continue
            edge_list.append((c, d))

    G = nx.from_edgelist(edge_list, create_using=nx.DiGraph)

    pos = generate_network_layout(G, layout_engine="dot")
    scatter = scatter_plot_array(pos)

    fig, ax = plt.subplots()

    draw_arrow_connectors(
        G,
        pos,
        face_color={e: "k" for e in G.edges},
        edge_color={e: "k" for e in G.edges},
        ax=ax,
        linewidth=0.1,
        alpha=0.8,
        zorder=0,
        shrink_a=5,
        shrink_b=5,
        arrowstyle="-|>",
        path=None,
        connectionstyle="Angle3",  #'Angle3'
        mutation_scale=10,
    )

    node_colors = []
    for n in G.nodes:
        if Path(f"data/sources/{n}/processed_data/{n}.csv").is_file():
            color = "g"
        elif Path(f"split_remainder/{n}").is_dir():
            color = "y"
        else:
            color = "r"

        node_colors.append(color)

    ax.scatter(scatter[0], scatter[1], c=node_colors)

    annotate_graph = True
    if annotate_graph:
        for p in pos:
            ax.annotate(p, xy=pos[p], rotation=45, fontsize=6)
    plt.show()


if __name__ == "__main__":
    main()
