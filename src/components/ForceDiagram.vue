<template>
  <div id="chart">
    <h2>D3 is confusing - But here's a force layout graph</h2>
  </div>
</template>

<script>
import * as d3 from 'd3';
import strains from '../../Data/strains_formatted.json';

export default {
  name: 'ForceDiagram',
  props: {},
  mounted() {
    // Has to be mounted as DOM elements are only available after mount
    this.createChart();
  },
  methods: {
    createChart() {
      const width = 1800;
      const height = 800;

      const svg = d3
        .select('#chart')
        .append('svg')
        .attr('width', width)
        .attr('height', height);
      //  .call(d3.zoom()
      //    .scaleExtent([1, 8])
      //    .on('zoom', zoom));
      // Based on https://bl.ocks.org/mbostock/3680957

      const color = d3.scaleOrdinal(d3.schemeCategory10);

      const linkForce = d3.forceLink().id(d => d.id);
      linkForce.distance(100);
      const repulseForce = d3.forceManyBody();
      repulseForce.distanceMax(500);
      repulseForce.strength(-200);
      // repulseForce.theta(1.5);
      const centerForce = d3.forceCenter(width / 2, height / 2);
      const radialForce = d3.forceRadial(calculateRadius, width / 2, height); // height / 2
      radialForce.strength(0.2);
      const yForce = d3.forceY(height);

      // Create force layout and add link forces, center gravity, and repulsion force
      const forceSim = d3
        .forceSimulation()
        .force('y', yForce)
        .force('link', linkForce)
        .force('charge', repulseForce)
        .force('center', centerForce)
        .force('radial', radialForce);

      // create d3 objects with nodes, labels, and links
      // See http://bl.ocks.org/fancellu/2c782394602a93921faff74e594d1bb1 (open source)
      svg.append('defs').append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 13)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 13)
        .attr('markerHeight', 13)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke', 'none');

      // And perhaps http://bl.ocks.org/d3noob/5141278 to see another example (no license)
      const link = svg
        .append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(strains.links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('marker-end', 'url(#arrowhead)');
        // .attr('stroke-width', d => Math.sqrt(d.value));

      const node = svg
        .append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(strains.nodes)
        .enter()
        .append('g');

      // eslint-disable-next-line
      const circles = node
        .append('circle')
        .attr('r', 10)
        .attr('fill', d => color(d.group))
        .call(
          d3
            .drag()
            .on('start', dragStart)
            .on('drag', drag)
            .on('end', dragEnd),
        );

      // eslint-disable-next-line
      const labels = node
        .append('text')
        .text(d => d.name)
        .attr('x', 6)
        .attr('y', 3);

      node.append('title').text(d => d.id);

      // Activate node and link rendering on tick
      forceSim.nodes(strains.nodes).on('tick', tick);
      forceSim.force('link').links(strains.links);
      // forceSim.alphaDecay(0.01);

      function calculateRadius(d) {
        return 100 + d.depth * 100;
      }

      // function zoom() {
      //  svg.attr('transform', d3.event.transform);
      // }

      // Provide updated positions for d3 render
      function tick() {
        link
          .attr('x1', d => d.source.x)
          .attr('x2', d => d.target.x)
          .attr('y1', d => d.source.y)
          .attr('y2', d => d.target.y);

        node.attr('transform', d => `translate(${d.x},${d.y})`);
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
        d.fy = d3.event.y;
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
  stroke-width: 1px;
}

text {
  font-family: sans-serif;
  font-size: 10px;
}
</style>
