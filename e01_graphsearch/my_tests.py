#C:/Users/Umberto/Anaconda2/Scripts/activate
#conda activate Anaconda2
node = 'D'
graph = {'A': {'B': 20, 'C': 30, 'D': 25},
        'B': {'A': 20, 'C': 20},
        'C': {'A': 30, 'B': 20},
        'D': {'A': 25}
        }
"""successors={}

for action in graph[node]:
    step_cost = graph[node][action]
    successors[action]=step_cost

print successors """
import ex_graphsearch_UC as f
f.Node('B','A',10,1)


succ= f.expand(f.Node.state,graph)
print f.Node('B','A',10,1)
f.Node.children=succ
print f.Node.children
