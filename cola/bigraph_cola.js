var cy = cytoscape({
    container: document.getElementById('cy'),
    
    style: [
      {
        selector: 'node',
        css:{
          'content': 'data(id)',
          'text-valign': 'center',
          'text-halign': 'center',
        }
      },
      {
        selector: ':parent',
        css: {
          'text-valign': 'top',
          'text-halign': 'center',
        }
      },
    ]
});

var eles = cy.add([
    { group: 'nodes', data: { id: 'a', parent: 'b'}},
    { group: 'nodes', data: { id: 'b' } },
    { group: 'nodes', data: { id: 'c', parent: 'a' }, position: { x: 300, y: 85 } },
    { group: 'nodes', data: { id: 'd' }, position: { x: 215, y: 175 } },
    { group: 'nodes', data: { id: 'e' } },
    { group: 'nodes', data: { id: 'f', parent: 'e' }, position: { x: 300, y: 175 } },
    { group: 'edges', data: { id: 'ad', source: 'a', target: 'd' } },
    { group: 'edges', data: { id: 'eb', source: 'e', target: 'b' } },
    { group: 'edges', data: { id: 'fd', source: 'f', target: 'd' } },
  ]);



cy.layout({name: 'cola'}).run();