var cy = window.cy = cytoscape({
  container: document.getElementById('cy'),

  boxSelectionEnabled: false,

  style: [
    {
      selector: 'node',
      css: {
        'content': 'data(id)',
        'text-valign': 'center',
        'text-halign': 'center',
        //'shape': 'triangle',
      }
    },
    {
      selector: ':parent',
      css: {
        'text-valign': 'top',
        'text-halign': 'center',
      }
    },
    {
      selector: 'edge',
      css: {
        'curve-style': 'bezier',

      }
    },
    
    {
      selector: "node[id='anchor']",
      css: {
        'height': 1,
        'width': 1,
        'content': ' ',
      }
    },
    

  ],

  elements: {
    nodes: [
      //{ data: { id: 'a', parent: 'b' }, position: { x: 215, y: 85 } },
      { data: { id: 'a', parent: 'b' } },
      { data: { id: 'b' } },
      { data: { id: 'c', parent: 'a' }, position: { x: 300, y: 85 } },
      { data: { id: 'd' }, position: { x: 215, y: 175 } },
      { data: { id: 'e' } },
      { data: { id: 'f', parent: 'e' }, position: { x: 300, y: 175 } },
      { data: { id: 'anchor'}}

    ],
    edges: [
      { data: { id: 'ad', source: 'a', target: 'd' } },
      { data: { id: 'eb', source: 'e', target: 'b' } },
      { data: { id: 'fd', source: 'f', target: 'd' } },
      { data: { id: 'anchorb', source: 'b', target: 'anchor'}},
      { data: { id: 'anchorf', source: 'f', target: 'anchor'}},
      { data: { id: 'anchord', source: 'anchor', target: 'd'}},
      
      
    ]
  },

  layout: { name: 'preset', padding: 5}

});

