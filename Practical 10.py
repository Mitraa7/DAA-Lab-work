# Kruskal's Algorithm (Minimum Spanning Tree)

class Edge:
    def __init__(self, u, v, w):
        self.u = u
        self.v = v
        self.w = w


def find(parent, x):
    while parent[x] != x:
        x = parent[x]
    return x


def union(parent, a, b):
    parent[a] = b


def sort_edges(edges):
    edges.sort(key=lambda edge: edge.w)

def main():
    v = int(input("Enter number of vertices: "))
    e = int(input("Enter number of edges: "))

    edges = []

    print("Enter Source Destination Weight:")

    for _ in range(e):
        u, vtx, w = map(int, input().split())
        edges.append(Edge(u, vtx, w))

    
    parent = [i for i in range(v)]

    
    sort_edges(edges)

    total_cost = 0

    print("\nEdges in Minimum Spanning Tree:")

    for edge in edges:
        p1 = find(parent, edge.u)
        p2 = find(parent, edge.v)

        if p1 != p2:
            union(parent, p1, p2)

            print(f"{edge.u} --> {edge.v}  Cost = {edge.w}")
            total_cost += edge.w

    print(f"\nMinimum Cost = {total_cost}")


if __name__ == "__main__":
    main()

# Time Complexity:
# Best Case    : O(E log E)
# Average Case : O(E log E)
# Worst Case   : O(E log E)
#
# Space Complexity:
# O(V)