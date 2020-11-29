var svg = d3.select('svg'),
  width = svg.node().getBoundingClientRect().width,
  height = svg.node().getBoundingClientRect().height;

// svg objects
var link, node;
// the data - an object with nodes and links
var graph;

var linkWidthScale = d3.scaleLinear().range([1, 15]);

// load the data
d3.json('http://localhost:5000/test', function (error, _graph) {
  console.log(_graph);
  if (error) throw error;
  graph = _graph;
  linkWidthScale.domain(
    d3.extent(graph.links, function (d) {
      return d.value;
    })
  );
  initializeDisplay();
  initializeSimulation();
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
    strength: -30,
    distanceMin: 1,
    distanceMax: 2000
  },
  collide: {
    enabled: true,
    strength: 0.7,
    iterations: 1,
    radius: 5
  },
  forceX: {
    enabled: true,
    strength: 0.1,
    x: 0.5
  },
  forceY: {
    enabled: false,
    strength: 0.1,
    y: 0.5
  },
  link: {
    enabled: true,
    distance: 75,
    iterations: 1
  }
};

var linkWidthScale = d3.scaleLinear().range([1, 15]);

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
    .id(function (d) {
      return d.id;
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
    .attr('class', 'links')
    .selectAll('line')
    .data(graph.links)
    .enter()
    .append('line');

  // set the data and properties of node circles
  node = svg
    .append('g')
    .attr('class', 'nodes')
    .selectAll('circle')
    .data(graph.nodes)
    .enter()
    .append('circle')
    .on("mouseover", function(){
      d3.select(this)
        .style("fill", "aliceblue")
        .transition()
        .attr('r', 20);
    })
    .on("mouseout", function(){
      d3.select(this)
        .style("fill", "white")
        .transition()
        .attr('r', 10);
    })
    .on("mousedown", function(d) {

      // displays information on click
      // can't figure out how to display not in svg
      svg.selectAll("text").remove();
      svg.append("text")
        .attr("x", 10)
        .attr("y", 20)
        .text("Name: " + d.id + "<br/>" 
        + " Email: " );
    
    })
    .call(
      d3
        .drag()
        .on('start', dragstarted)
        .on('drag', dragged)
        .on('end', dragended)
    );

  // node tooltip
  node.append('title').text(function (d) {
    return d.id;
  });



  node
    .append('text')
    .attr('dx', 12)
    .attr('dy', '.35em')
    .text(function (d) {
      return d.id;
    })
    .style('stroke', 'black')
    .style('stroke-width', 0.5)
    .style('fill', 'black')
    .style('font-size', '24px');
  // visualize the graph
  updateDisplay();
}

// update the display based on the forces (but not positions)
function updateDisplay() {
  node
    .attr('r', 10)
    .attr('stroke', 'blue')
    .attr('fill', 'white')
    .attr('stroke-width', 4);

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
  d3.select('#alpha_value').style('flex-basis', simulation.alpha() * 100 + '%');
}

//////////// UI EVENTS ////////////

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
