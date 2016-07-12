(function () {
  'use strict';
  // Set the endpoint for the MCTS data here.
  var mctsDataUrl = "static/data/mcts_data.json";

  var xBuffer = 120;
  var yBuffer = 20;

  var margin = {top: yBuffer, right: xBuffer, bottom: yBuffer, left: xBuffer};
  var width = 960 - margin.right - margin.left;
  var height = 800 - margin.top - margin.bottom;

  var i = 0;
  var duration = 750;
  var root;

  var tree = d3.layout.tree().size([height, width]);

  var diagonal = d3.svg.diagonal()
    .projection(function (d) {
      return [d.x, d.y];
    });

  var svg = d3.select("body").append("svg")
    .attr("width", width + margin.right + margin.left)
    .attr("height", height + margin.top + margin.bottom)
    .append("g")
    .attr("transform", "translate(" + margin.left + "," + margin.top + ")");

  d3.json(mctsDataUrl, function (error, base) {
    if (error) throw error;

    root = base;
    root.x0 = height / 2;
    root.y0 = 0;

    function collapse(d) {
      if (d.children) {
        d._children = d.children;
        d._children.forEach(collapse);
        d.children = null;
      }
    }

    update(root);
  });

  d3.select(self.frameElement).style("height", "800px");

  function update(source) {

    // Compute the new tree layout.
    var nodes = tree.nodes(root.tree).reverse();
    var links = tree.links(nodes);

    // Update the nodes…
    var node = svg.selectAll("g.node")
      .data(nodes, function (d) {
        return d.id || (d.id = ++i);
      });

    // Enter any new nodes at the parent's previous position.
    var nodeEnter = node.enter().append("g")
      .attr("class", "node")
      .attr("transform", function (d) {
        return "translate(" + source.y0 + "," + source.x0 + ")";
      })
      .on("click", click);

    nodeEnter.append("circle")
      .attr("r", 1e-6)
      .style("fill", function (d) {
        return d._children ? "lightsteelblue" : "#fff";
      });

    nodeEnter.append("text")
      .attr("x", function (d) {
        return d.children || d._children ? -10 : 10;
      })
      .attr("dy", ".35em")
      .attr("text-anchor", function (d) {
        return d.children || d._children ? "end" : "start";
      })
      .text(function (d) {
        //return d.id;
        return '';
      })
      .style("fill-opacity", 1e-6);

    nodeEnter.append("svg:title")
      .text(function (d) {
        var text = [];
        for (var key in d) {
          if (d.hasOwnProperty(key)) {
            if (key === 'children') {
              var numChildren = getNumChildren(d);
              text.push('numChildren: ' + numChildren);
            }
            else if (isNaN(parseFloat(d[key])) || key === 'x' || key === 'y') {
              continue;
            }
            else if (d[key] !== undefined) {
              text.push(key + ': ' + String(d[key]));
            }
            else {
              text.push(key + ': 0');
            }
          }
        }
        return text.join(', ');
      });

    // Transition nodes to their new position.
    var nodeUpdate = node.transition()
      .duration(duration)
      .attr("transform", function (d) {
        return "translate(" + d.x + "," + d.y + ")";
      });

    nodeUpdate.select("circle")
      .attr("r", 4.5)
      .style("fill", function (d) {
        return d._children ? "lightsteelblue" : "#fff";
      });

    nodeUpdate.select("text")
      .style("fill-opacity", 1);

    // Transition exiting nodes to the parent's new position.
    var nodeExit = node.exit().transition()
      .duration(duration)
      .attr("transform", function (d) {
        return "translate(" + source.x + "," + source.y + ")";
      })
      .remove();

    nodeExit.select("circle")
      .attr("r", 1e-6);

    nodeExit.select("text")
      .style("fill-opacity", 1e-6);

    // Update the links…
    var link = svg.selectAll("path.link")
      .data(links, function (d) {
        return d.target.id;
      });

    // Enter any new links at the parent's previous position.
    link.enter().insert("path", "g")
      .attr("class", "link")
      .attr("d", function (d) {
        var o = {x: source.x0, y: source.y0};
        return diagonal({source: o, target: o});
      });

    // Transition links to their new position.
    link.transition()
      .duration(duration)
      .attr("d", diagonal);

    // Transition exiting nodes to the parent's new position.
    link.exit().transition()
      .duration(duration)
      .attr("d", function (d) {
        var o = {x: source.x, y: source.y};
        return diagonal({source: o, target: o});
      })
      .remove();
  }

  // Toggle children on click.
  function click(d) {
    if (d.children) {
      d._children = d.children;
      d.children = null;
    } else {
      d.children = d._children;
      d._children = null;
    }
    update(d);
  }

  function getNumChildren(d) {
    var countChildren = 0;
    if (d.children) {
      d.children.forEach(function(subD) {
        countChildren += 1;
        countChildren += getNumChildren(subD);
      }.bind(this))
    }
    return countChildren;
  }
})();
