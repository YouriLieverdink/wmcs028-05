import networkx as nx
import matplotlib.pyplot as plt
from typing import List, Tuple
import csv
import pandas as pd

"""
Apply the HITS or PageRank algorithm to the network, and visualize.
"""
def apply_hits(G: nx.Graph, max_iter=100, tol=1e-6) -> tuple[dict, dict]:
    users = {n for n in G.nodes if str(n).startswith('u')}
    pages = set(G.nodes) - users

    # Initialize scores
    hub_scores = {u: 1.0 for u in users}       # Only for users/editors
    auth_scores = {p: 1.0 for p in pages}       # Only for pages

    for _ in range(max_iter):
        # Update authority scores for pages based on hub scores from users
        new_auth_scores = {p: sum(hub_scores[u] for u in G.neighbors(p)) for p in pages}

        # Update hub scores for users based on authority scores from pages
        new_hub_scores = {u: sum(auth_scores[p] for p in G.neighbors(u)) for u in users}

        # Normalize scores to prevent values from growing unbounded
        auth_norm = sum(new_auth_scores.values())
        hub_norm = sum(new_hub_scores.values())
        new_auth_scores = {p: v / auth_norm for p, v in new_auth_scores.items()}
        new_hub_scores = {u: v / hub_norm for u, v in new_hub_scores.items()}

        # Check for convergence by seeing if the scores change less than tolerance level `tol`
        if (all(abs(hub_scores[u] - new_hub_scores[u]) < tol for u in users) and
            all(abs(auth_scores[p] - new_auth_scores[p]) < tol for p in pages)):
            break

        # Update scores for the next iteration
        hub_scores, auth_scores = new_hub_scores, new_auth_scores

    return hub_scores, auth_scores

"""
Select the top k hubs & authorities from the file with their scores, and plot.
"""
def find_top_hubs_auths(input_path_hubs: str, input_path_auths: str, output_path_hubs: str, output_path_auths: str, k: int) -> None:
    # read hub scores & authority scores from the input CSV file
    with open(input_path_hubs, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header
        hub_scores: List[Tuple[str, float]] = [(row[0], float(row[1])) for row in reader]
    with open(input_path_auths, 'r') as f:
        reader = csv.reader(f)
        next(reader)  # skip the header
        auth_scores: List[Tuple[str, float]] = [(row[0], float(row[1])) for row in reader]

    # sort scores and select the top k
    top_hubs = sorted(hub_scores, key=lambda x: x[1], reverse=True)[:k]
    top_auths = sorted(auth_scores, key=lambda x: x[1], reverse=True)[:k]

    # create two CSV files for them
    with open(output_path_hubs, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Node', 'Hub Score'])
        writer.writerows(top_hubs)
    with open(output_path_auths, 'w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Node', 'Authority Score'])
        writer.writerows(top_auths)

    # prepare data for plot
    top_hubs_df = pd.DataFrame(top_hubs, columns=['Node', 'Hub Score'])
    top_auths_df = pd.DataFrame(top_auths, columns=['Node', 'Authority Score'])

    # plot
    plt.figure(figsize=(14, 6))

    # hubs
    plt.subplot(1, 2, 2)
    plt.bar(top_hubs_df['Node'], top_hubs_df['Hub Score'], color='purple')
    plt.xticks(rotation=90)
    plt.xlabel('User Nodes')
    plt.ylabel('Hub Score')
    plt.title(f'Top {k} Hubs by Hub Score')

    # authorities
    plt.subplot(1, 2, 1)
    plt.bar(top_auths_df['Node'], top_auths_df['Authority Score'], color='blue')
    plt.xticks(rotation=90)
    plt.xlabel('Page Nodes')
    plt.ylabel('Authority Score')
    plt.title(f'Top {k} Authorities by Authority Score')

    # show and save
    plt.tight_layout()
    plt.savefig("top_hubs_and_authorities")
    plt.show()
