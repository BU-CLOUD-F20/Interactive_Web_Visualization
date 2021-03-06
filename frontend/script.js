var svg = d3.select('svg')
      .append("svg")
      .attr("width", "100%")
      .attr("height", "100%")
      .call(d3.zoom().on("zoom", function () {
        svg.attr("transform", d3.event.transform)
      }))
      .append("g"),
  width = 1000,
  height = 1000;

// svg objects
var link, node;
var node_texts;
var color;
var toggle = 0;
// the data - an object with nodes and links
var graph;
var linkWidthScale = d3.scaleLinear().range([1, 15]);
var linkedByIndex = {};


// load the data
d3.json('https://api.jsonbin.io/b/5fc822619abe4f6e7caec8b5', function (error, _graph) {
  console.log(error)
  //console.log(_graph);
  //if (error) console.log(error);
  //graph = _graph;
  console.log(graph);
  linkWidthScale.domain(
    d3.extent(graph.links, function (d) {
      return d.value;
    })
  );
  initializeDisplay();
  initializeSimulation();
  for (i = 0; i < graph.nodes.length; i++) {
      linkedByIndex[i + "," + i] = 1;
  };
  graph.links.forEach(function (d) {
      linkedByIndex[d.source.index + "," + d.target.index] = 1;
  });
  console.log(linkedByIndex)
});

//////////// FORCE SIMULATION ////////////

// force simulator
var simulation = d3.forceSimulation();
// set up the simulation and event to update locations after each tick
function initializeSimulation() {
  simulation.nodes(graph.nodes);
  initializeForces();
  simulation.on('tick', ticked);
}
// values for all forces
forceProperties = {
  center: {
    x: 0.5,
    y: 0.5
  },
  charge: {
    enabled: true,
    strength: -2000,
    distanceMin: 1,
    distanceMax: 2000
  },
  collide: {
    enabled: false, 
    strength: 0.7,
    iterations: 1,
    radius: 50
  },
  forceX: {
    enabled: true,
    strength: 0.05,
    x: 0.5
  },
  forceY: {
    enabled: true,
    strength: 0.05,
    y: 0.5
  },
  link: {
    enabled: true,
    distance: 50,
    iterations: 1
  }
};
var linkWidthScale = d3.scaleLinear().range([1, 15]);
//var nodeRadiusScale = d3.scaleLinear().range([1, 15]);
// add forces to the simulation
function initializeForces() {
  // add forces and associate each with a name
  simulation
    .force('link', d3.forceLink())
    .force('charge', d3.forceManyBody())
    .force('collide', d3.forceCollide())
    .force('center', d3.forceCenter())
    .force('forceX', d3.forceX())
    .force('forceY', d3.forceY());
  // apply properties to each of the forces
  updateForces();
}
// apply new force properties
function updateForces() {
  // get each force by name and update the properties
  simulation
    .force('center')
    .x(width * forceProperties.center.x)
    .y(height * forceProperties.center.y);
  simulation
    .force('charge')
    .strength(forceProperties.charge.strength * forceProperties.charge.enabled)
    .distanceMin(forceProperties.charge.distanceMin)
    .distanceMax(forceProperties.charge.distanceMax);
  simulation
    .force('collide')
    .strength(
      forceProperties.collide.strength * forceProperties.collide.enabled
    )
    .radius(forceProperties.collide.radius)
    .iterations(forceProperties.collide.iterations);
  simulation
    .force('forceX')
    .strength(forceProperties.forceX.strength * forceProperties.forceX.enabled)
    .x(width * forceProperties.forceX.x);
  simulation
    .force('forceY')
    .strength(forceProperties.forceY.strength * forceProperties.forceY.enabled)
    .y(height * forceProperties.forceY.y);
  simulation
    .force('link')
    .id(function (d, i) {
      return d.index;
    })
    .distance(forceProperties.link.distance)
    .iterations(forceProperties.link.iterations)
    .links(forceProperties.link.enabled ? graph.links : []);
  // updates ignored until this is run
  // restarts the simulation (important if simulation has already slowed down)
  simulation.alpha(1).restart();
}
//////////// DISPLAY ////////////
// generate the svg objects and force simulation
function initializeDisplay() {

  // set the data and properties of link lines
  link = svg
    .append('g')
    .attr("ind",function(d,i){ return i})
    .attr('class', 'links')
    .selectAll('line')
    .data(graph.links)
    .enter()
    .append('line')
    .on("mousedown", function(d,i) {
      // display info when node is clicked +`${d.value}`
      text = "Collaborators: "+d.target.id+" and "+d.source.id+" Number of Common Publication(s): "+'\n'+`${d.value}`;
      d3.select('.linkinfo').text(text); 
    });
  // set the data anCollaborators: d+d.target+ properties of node circles
  node = svg
    .append('g')
    .attr('class', 'nodes')
    .selectAll('circle')
    .data(graph.nodes)
    .enter()
    .append('circle')
    // hovering over a node enlarges it to make it easier for the user to differentiate from others
    .on("mouseover", function(){
      d3.select(this)
        .transition()
        .attr('r', 25);
    })
    .on("mouseout", function(){
      d3.select(this)
        .transition()
        .attr('r', 15);
      node.style('opacity', 1);
      link.attr('opacity',1);
    })
    // clicking on a node displays info
    .on("mousedown", function(d) {
      // display info when node is clicked
      text = "Name: "+`${d.id}`+'tspan'+" Email: "+`${d.email}`+" Department: "+`${d.department}`;
      
      d3.select('.nodeinfo').text(text);

      // highlighting direct links and fading undirect links
      var thisNode = d.id
      link.attr("opacity", function(d) {
        return (d.source.id == thisNode || d.target.id == thisNode) ? 1 : 0.1
      });
      // highlighting direct nodes and fading undirect nodes
      d = d3.select(this).node().__data__;
      node.style("opacity", function (o) {
        return neighboring(d, o) | neighboring(o, d) ? 1 : 0.2;
      });
    })
    .call(
      d3
        .drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
    );

  // set the node texts
  node_texts = svg
     .append('g')
     .selectAll("text")
     .data(graph.nodes)
     .enter()
     .append("text")
     .style('fill', 'black')
     .style('user-select', 'none')
     .attr("dx", 12)
     .attr("dy", '.35em')
     .text(function(d){
        return d.id;
     });
  // visualize the graph
  updateDisplay();
}
/*
var last;
//	filtered types
document.getElementById("isolated").addEventListener("click", function(){
  console.log("isolated clicked")
  
    var linkedNodes = [];
    count = -1;
    graph.nodes.filter(function(d){
      graph.links.forEach(function (o) {
        if(((d.index == o.source.index) || (d.index == o.target.index )) &&(linkedByIndex[o.source.index + "," + o.target.index])){
          if(last!=d.index){
            last = d.index;
            count = count + 1;
            graph.nodes.splice(d.index, 1);
            graph.links.splice(d.index, 1);
            linkedNodes[count] = d.index;
          }
        }
      })
    })
    
    var gnodes = d3.selectAll('.nodes')
      .data(linkedNodes)
      .exit().remove();

  updateDisplay();
});
document.getElementById("extended").addEventListener("click", function(){
  console.log("extended clicked")
  
  //updateDisplay();
});

document.getElementById("submit").addEventListener("click", function(){
  console.log("submit clicked")
  var input = document.getElementById("input").value;
  var element = svg.selectAll(".circle")
      .data(graph.nodes.filter(function(d){
        console.log(graph.nodes)
        return graph.nodes == input;
      }));
   
});*/
// update the display based on the forces (but not positions)
function updateDisplay() {
  color = d3.scaleOrdinal()
    .domain(d3.range(node.length))
    .range(d3.schemeCategory10);
  node
    .attr('r', 15)
    .attr("fill",function(d,i){
    			return color(d.department);
    })
    .attr('opacity', 1);
  link
    .attr('stroke-width', function (d) {
      return linkWidthScale(d.value);
    })
    .attr('stroke', 'rgb(0,0,0, 0.5)')
    .attr('opacity', 1);
}
// update the display positions after each simulation tick
function ticked() {
  link
    .attr('x1', function (d) {
      return d.source.x;
    })
    .attr('y1', function (d) {
      return d.source.y;
    })
    .attr('x2', function (d) {
      return d.target.x;
    })
    .attr('y2', function (d) {
      return d.target.y;
    });
  node
    .attr('cx', function (d) {
      return d.x;
    })
    .attr('cy', function (d) {
      return d.y;
    });
  node_texts.attr("x", function(d){ return d.x; })
    .attr("y", function(d){ return d.y; });
  d3.select('#alpha_value').style('flex-basis', simulation.alpha() * 100 + '%');
}
//////////// UI EVENTS ////////////



function neighboring(a, b) {
    return linkedByIndex[a.index + "," + b.index];
}

function dragstarted(d) {
  if (!d3.event.active) simulation.alphaTarget(0.3).restart();
  d.fx = d.x;
  d.fy = d.y;
}
function dragged(d) {
  d.fx = d3.event.x;
  d.fy = d3.event.y;
}
function dragended(d) {
  if (!d3.event.active) simulation.alphaTarget(0.0001);
  d.fx = null;
  d.fy = null;
}
// update size-related forces
d3.select(window).on('resize', function () {
  width = svg.node().getBoundingClientRect().width;
  height = svg.node().getBoundingClientRect().height;
  updateForces();
});
// convenience function to update everything (run after UI input)
function updateAll() {
  updateForces();
  updateDisplay();
}

//wrap the text
function wrap(text, width) {
  text.each(function() {
    let text = d3.select(this),
      words = text.text().split(/\s+/).reverse(),
      word,
      line = [],
      lineNumber = 0,
      lineHeight = 1.1, // ems
      x = text.attr("x"),
      y = text.attr("y"),
      dy = 1.1,
      tspan = text.text(null).append("tspan").attr("x", x).attr("y", y).attr("dy", dy + "em");
    while (word = words.pop()) {
      line.push(word);
      tspan.text(line.join(" "));
      if (tspan.node().getComputedTextLength() > width) {
        line.pop();
        tspan.text(line.join(" "));
        line = [word];
        tspan = text.append("tspan").attr("x", x).attr("y", y).attr("dy", ++lineNumber * lineHeight + dy + "em").text(word);
      }
    }
  });
}
