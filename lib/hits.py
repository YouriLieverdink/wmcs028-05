import networkx as nx
import matplotlib.pyplot as plt

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