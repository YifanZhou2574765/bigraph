from graphviz import Graph

g = Graph(name='testG', format="png")

with g.subgraph(name='border') as c:
    with c.subgraph(name='cluster') as c:
        c.attr(label='region0')
        with c.subgraph(name='cluster') as c:
            c.attr(label='A')
            with c.subgraph(name='cluster') as c:
                c.attr(label='Snd')
                c.node('M') 
                with c.subgraph(name='cluster') as c:
                    c.attr(label='Ready')
                    c.node('Fun')       
            

g.view()
