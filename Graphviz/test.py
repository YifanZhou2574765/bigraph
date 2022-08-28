from os import fdopen
from graphviz import Graph
#from networkx.drawing.nx_agraph import graphviz_layout
from IPython import display


g = Graph(name='testG', format="png")
g.compound=True

with g.subgraph(name='cluster_1') as c:
    c.attr(color='white')
    with c.subgraph(name='cluster_2') as c:
        c.attr(label='region0', color='black')
        with c.subgraph(name='cluster_3') as c:
            c.attr(label='A')
            with c.subgraph(name='cluster_4') as c:
                c.attr(label='Snd')  
                c.node('M')
                with c.subgraph(name='cluster_5') as c:
                    c.attr(lbabel='Ready')
                    c.node('Fun')  
                
                    

#g.edge('A', 'M') #会增加一个名为A的node
#g.edge('cluster_3', 'anchorNode') #成功
g.edge('region0', 'anchorNode') 

g.engine = "fdp"
#display.display(g)
g.view()