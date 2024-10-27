import networkx as nx
import matplotlib.pyplot as plt

from datetime import datetime
from collections import Counter, defaultdict

def number_of_edits_by_year(G: nx.Graph) -> None:
    edits = Counter()

    for _, _, data in G.edges(data=True):
        date = datetime.fromtimestamp(int(data['timestamp']))
        year = date.strftime("%Y")

        edits[year] += 1
        
    sorted_years = sorted(edits.keys())
    counts = [edits[year] for year in sorted_years]
    
    plt.figure(figsize=(15, 6))

    plt.bar(sorted_years, counts, color='skyblue')
    plt.xticks(rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Number of Edits')
    plt.title('Wikipedia Edits per Year')

    plt.tight_layout()
    plt.savefig("number_of_edits_by_year.png")
    plt.show()
        
def editor_growth_by_year(G: nx.Graph) -> None:
    edits = defaultdict(lambda: defaultdict(int))
    
    for _, page, data in G.edges(data=True):
        date = datetime.fromtimestamp(int(data['timestamp']))
        year = date.strftime('%Y')
        
        edits[page][year] += 1

    k, n = 10, 3
    years = [str(2001 + i) for i in range(n)]
    
    most_edited_pages = sorted(edits.items(), key=lambda item: sum(item[1].get(year, 0) for year in years), reverse=True)
    k_most_edited_pages = most_edited_pages[:k]

    sorted_years = [str(2001 + i) for i in range(10)]
    total_edits_per_year = [sum(page[1].get(year, 0) for page in k_most_edited_pages) for year in sorted_years]
    
    plt.figure(figsize=(15, 6))

    plt.bar(sorted_years, total_edits_per_year, color='skyblue')
    plt.xticks(rotation=90)
    plt.xlabel('Year')
    plt.ylabel('Number of Edits')
    plt.title(f'Editor growth per year for {k} most edited pages')

    plt.tight_layout()
    plt.savefig("editor_growth_per_year.png")
    plt.show()
    
    
    