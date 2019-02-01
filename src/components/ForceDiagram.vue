<template>
  <div id="chart">
    <h1>D3 is confusing</h1>
    <h2>But here's a force layout graph</h2>
  </div>
</template>

<script>
import * as d3 from 'd3';
import strains from '../../Data/strains_formatted.json'
export default {
  name: 'ForceDiagram',
  props: {},
  mounted: function() {
    // Has to be mounted as DOM elements are only available after mount
    this.createChart();
  },
  methods: {
    createChart() {
      const width = 900;
      const height = 600;

      const svg = d3
        .select('#chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height);

      const color = d3.scaleOrdinal(d3.schemeCategory10);

      // Create force layout and add link forces, center gravity, and repulsion force
      const forceSim = d3
        .forceSimulation()
        .force(
          'link',
          d3.forceLink().id(function(d) {
            return d.id;
          }),
        )
        .force('charge', d3.forceManyBody())
        .force('center', d3.forceCenter(width / 2, height / 2));

      // create d3 objects with nodes, labels, and links
      const link = svg
        .append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(strains.links)
        .enter()
        .append('line')
        .attr('stroke-width', function(d) {
          return Math.sqrt(d.value);
        });

      const node = svg
        .append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(strains.nodes)
        .enter()
        .append('g');

      const circles = node
        .append('circle')
        .attr('r', 10)
        .attr('fill', function(d) {
          return color(d.group);
        })
        .call(
          d3
            .drag()
            .on('start', dragStart)
            .on('drag', drag)
            .on('end', dragEnd),
        );

      const labels = node
        .append('text')
        .text(function(d) {
          return d.name;
        })
        .attr('x', 6)
        .attr('y', 3);

      node.append('title').text(function(d) {
        return d.id;
      });

      // Activate node and link rendering on tick
      forceSim.nodes(strains.nodes).on('tick', tick);
      forceSim.force('link').links(strains.links);

      // Provide updated positions for d3 render
      function tick() {
        link
          .attr('x1', function(d) {
            return d.source.x;
          })
          .attr('x2', function(d) {
            return d.target.x;
          })
          .attr('y1', function(d) {
            return d.source.y;
          })
          .attr('y2', function(d) {
            return d.target.y;
          });

        node.attr('transform', function(d) {
          return 'translate(' + d.x + ',' + d.y + ')';
        });
      }

      // Handles alpha forces to deal with node select and drag
      function dragStart(d) {
        if (!d3.event.active) {
          forceSim.alphaTarget(0.3).restart();
        }
        d.fx = d.x;
        d.fy = d.y;
      }

      function drag(d) {
        d.fx = d3.event.x;
        d.fy = d.event.y;
      }

      function dragEnd(d) {
        if (!d3.event.active) {
          forceSim.alphaTarget(0);
          d.fx = null;
          d.fy = null;
        }
      }
    },
  },
};
</script>

<style>
.links line {
  stroke: #999;
  stroke-opacity: 0.6;
}

.nodes circle {
  stroke: #fff;
  stroke-width: 1.5px;
}

text {
  font-family: sans-serif;
  font-size: 10px;
}
</style>
