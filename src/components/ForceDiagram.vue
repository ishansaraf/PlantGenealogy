<template>
  <div id="chart">
    <h1>Plant Genealogy Tree</h1>
    <label for="colorby"> Color By: </label>
    <select id="colorby" @change="colorStrains()" v-model="selected">
      <option value="type">Strain Type</option>
      <option value="effect">Strongest Effect</option>
      <option value="neg">Biggest Negative</option>
      <option value="med">Strongest Medical Property</option>
    </select>
    <node-info :node_info="current_node" v-show="showCard"></node-info>
  </div>
</template>

<script>
import * as d3 from 'd3';
import strains from '../../Data/strains_formatted.json';
import NodeInfo from './NodeInfo.vue';

export default {
  name: 'ForceDiagram',
  props: {},
  components: {
    'node-info': NodeInfo,
  },
  data() {
    return {
      current_node: {
        name: '',
        url: '',
      },
      selected: 'type',
      keyArea: null,
    };
  },
  computed: {
    showCard() {
      return this.current_node.name !== '';
    },
  },
  mounted() {
    // Has to be mounted as DOM elements are only available after mount
    this.createChart();
  },
  methods: {
    createChart() {
      const width = 1600;
      const height = 1200;
      const circleRadius = 7;
      // remember to update this waaaay below if you change it
      const circleBorder = 1;

      const svg = d3
        .select('#chart')
        .append('div')
        .classed('svg-container', true)
        .append('svg')
        .attr('preserveAspectRatio', 'xMinYMin meet')
        .attr('viewBox', `0 0 ${width} ${height}`)
        .classed('svg-content-responsive', true);

      const g = svg.append('g').attr('class', 'everything'); // See https://bl.ocks.org/puzzler10/4438752bb93f45dc5ad5214efaa12e4a;

      const ringSeperation = 100;
      const linkForce = d3.forceLink().id(d => d.strain_id);
      linkForce.strength(0.05);
      function desiredDistance(d) {
        return 1.1 * ringSeperation * d.distance;
      }
      linkForce.distance(desiredDistance);

      const repulseForce = d3.forceManyBody();
      repulseForce.distanceMax(3 * ringSeperation);
      repulseForce.strength(-30);
      // repulseForce.theta(1.5);
      const centerForce = d3.forceCenter(width / 2, height / 2);

      function calculatePos(d) {
        return (1 + d.depth) * ringSeperation;
      }
      const yForce = d3.forceY(calculatePos);
      yForce.strength(0.9);

      const collideForce = d3.forceCollide(1.1 * circleRadius + circleBorder);

      // Create force layout and add link forces, center gravity, and repulsion force
      const forceSim = d3
        .forceSimulation()
        .force('y', yForce)
        .force('link', linkForce)
        .force('charge', repulseForce)
        .force('collide', collideForce)
        // TODO create some function forceCluster, e.g.
        // function forceCluster(alpha) { TODO }. Place function well below this for cleanliness
        // Then, uncomment this line:
        // .force('cluster', forceCluster)
        .force('center', centerForce);

      // create d3 objects with nodes, labels, and links
      // See http://bl.ocks.org/fancellu/2c782394602a93921faff74e594d1bb1 (open source)
      g.append('defs')
        .append('marker')
        .attr('id', 'arrowhead')
        .attr('viewBox', '-0 -5 10 10')
        .attr('refX', 16)
        .attr('refY', 0)
        .attr('orient', 'auto')
        .attr('markerWidth', 10)
        .attr('markerHeight', 10)
        .attr('xoverflow', 'visible')
        .append('svg:path')
        .attr('d', 'M 0,-5 L 10 ,0 L 0,5')
        .attr('fill', '#999')
        .style('stroke', 'none');

      const zoomArea = g.append('g');

      // And perhaps http://bl.ocks.org/d3noob/5141278 to see another example (no license)
      const link = zoomArea
        .append('g')
        .attr('class', 'links')
        .selectAll('line')
        .data(strains.links)
        .enter()
        .append('line')
        .attr('class', 'link')
        .attr('marker-end', 'url(#arrowhead)');

      const node = zoomArea
        .append('g')
        .attr('class', 'nodes')
        .selectAll('g')
        .data(strains.nodes)
        .enter()
        .append('g');

      // eslint-disable-next-line
      const circles = node
        .append('circle')
        .attr('r', circleRadius)
        .call(
          d3
            .drag()
            .on('start', dragStart)
            .on('drag', drag)
            .on('end', dragEnd),
        )
        .on('click', doClick);

      const keyGroup = g.append('g').attr('class', 'key');

      const key = keyGroup.selectAll('g');
      this.keyArea = key;

      keyGroup
        .append('rect') // Nice rectangle around the key
        .attr('class', 'keyBox')
        .attr('width', 140)
        .attr('height', 50)
        .attr('x', 0)
        .attr('y', 0)
        .attr('fill', '#ffffff')
        .attr('stroke', '#000000');

      // colorStrains('type');
      // colorStrains('effect');
      this.colorStrains('neg');
      // colorStrains('med')

      // eslint-disable-next-line
      // const labels = node
      //  .append('text')
      //  .text(d => d.name)
      //  .attr('x', 6)
      //  .attr('y', 3);

      node.append('title').text(d => d.name);

      // Activate node and link rendering on tick
      forceSim.nodes(strains.nodes).on('tick', tick);
      forceSim.force('link').links(strains.links);
      // forceSim.alphaDecay(0.01);

      // See https://bl.ocks.org/puzzler10/4438752bb93f45dc5ad5214efaa12e4a;
      // add zoom capabilities
      const zoomHandler = d3.zoom().on('zoom', zoom);
      zoomHandler(svg);

      function zoom() {
        zoomArea.attr('transform', d3.event.transform);
      }

      // Provide updated positions for d3 render
      function tick() {
        link
          .attr('x1', d => d.source.x)
          .attr('x2', d => d.target.x)
          .attr('y1', d => d.source.y)
          .attr('y2', d => d.target.y);

        node.attr('transform', d => `translate(${d.x},${d.y})`);
      }

      // https://stackoverflow.com/a/30714153
      let selected;
      let selected_links;
      var highlights = new Array();
      var parents = new Array();
      var relative_nodes;
      const self = this;
      function doClick() {
        if (!selected) {
          selected = this;

          const strainId = d3.select(selected).data()[0].strain_id;

          // const strainInfo = strains.info[strainId];
          d3.select(selected).style('stroke', 'black');
          //looking at links sprouting from a node
          selected_links = d3.selectAll('.link').filter(function(d) {
            return d.source.strain_id === strainId || d.target.strain_id === strainId;
          });

          highlights.push(selected_links);

          //creating list of strains
          for (let i = 0; i < selected_links.data().length; i++) {
            if (!parents.includes(selected_links.data()[i].source.strain_id)) {
              parents.push(selected_links.data()[i].source.strain_id);
              //console.log("added src"+ selected_links.data()[i].source.strain_id)
            } else if (!parents.includes(selected_links.data()[i].target.strain_id)) {
              parents.push(selected_links.data()[i].target.strain_id);
              //console.log("added tgt"+ selected_links.data()[i].target.strain_id)
            } else {
              i++;
            }
          }

          //now making an object of selected nodes

          relative_nodes = d3.selectAll('.node').filter(function(d) {
            return parents.includes(d.source.strain_id) || parents.includes(d.target.strain_id);
          });

          relative_nodes.style('stroke', 'black');
          highlights[0].style('stroke', 'red');
          highlights[0].style('stroke-opacity', '5');
        } else {
          d3.select(selected).style('stroke', '#fff');
          highlights[0].style('stroke', '#999');
          highlights.length = 0;
          parents.length = 0;
          selected = this;
          const strainId = d3.select(selected).data()[0].strain_id;
          selected_links = d3.selectAll('.link').filter(function(d) {
            return d.source.strain_id === strainId || d.target.strain_id === strainId;
          });
          highlights.push(selected_links);
          for (let i = 0; i < selected_links.data().length; i++) {
            if (!parents.includes(selected_links.data()[i].source.strain_id)) {
              parents.push(selected_links.data()[i].source.strain_id);
            } else if (!parents.includes(selected_links.data()[i].target.strain_id)) {
              parents.push(selected_links.data()[i].target.strain_id);
            } else {
              i++;
            }
          }

          relative_nodes = d3.selectAll('.node').filter(function(d) {
            return parents.includes(d.source.strain_id) || parents.includes(d.target.strain_id);
          });

          relative_nodes.style('stroke', 'black');
          highlights[0].style('stroke', 'red');
          highlights[0].style('stroke-opacity', '5');

          d3.select(selected).style('stroke', 'black');
        }
        // TODO update card here
        // Here's an example, just prints all the relevant data for you to dev console
        // Don't ask me why this line is such a complicated mess, probably is a better way...

        // eslint-disable-next-line
        console.log(JSON.stringify(strainInfo));
        self.current_node = strainInfo;
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

    colorStrains() {
      const attrName = this.selected;
      let color;
      const values = [];
      if (attrName === 'type') {
        // Maybe a nice diverging color scheme:
        // color = d3.scaleOrdinal(d3.schemeBrBG[3])
        // Red, purple, blue. Looks ok
        color = d3.scaleOrdinal([d3.schemeSet1[0], d3.schemeSet1[3], d3.schemeSet1[1]]);
        // Or, blue, green, yellow. Looks awful
        // color = d3.scaleOrdinal([d3.schemeSet1[1], d3.schemeSet1[2], d3.schemeSet1[5]]);
        // Red, orange, yellow? Not great
        // color = d3.scaleOrdinal([d3.schemeSet1[0], d3.schemeSet1[4], d3.schemeSet1[5]]);
        let i;
        for (i = 0; i < 3; i += 1) {
          values[i] = {
            label: strains.metadata.cat_enums.type[i],
            color: color.range()[i],
            pos: i,
          };
        }
      } else if (attrName === 'med') {
        // Manual cases from hell
        const unknown = d3.schemeCategory10[9];
        color = d3.scaleOrdinal();
        color.domain([0, 3, 4, 5, 10, 6, 12, 11, 1, 9, 7, 2]);
        color.range(d3.schemeCategory10.concat([unknown, unknown, unknown]));
        let i;
        for (i = 0; i < 9; i += 1) {
          values[i] = {
            label: strains.metadata.cat_enums.med[color.domain()[i]],
            color: color.range()[i],
            pos: i,
          };
        }
        values[9] = {
          label: 'Other',
          color: color.range()[9],
          pos: 9,
        };
      } else if (attrName === 'effect') {
        // Manual cases from hell
        const unknown = d3.schemeCategory10[9];
        color = d3.scaleOrdinal();
        color.domain([9, 7, 0, 4, 13, 3, 5, 2, 10, 8, 1, 6, 11]);
        color.range(d3.schemeCategory10.concat([unknown, unknown, unknown, unknown]));
        let i;
        for (i = 0; i < 9; i += 1) {
          values[i] = {
            label: strains.metadata.cat_enums.effect[color.domain()[i]],
            color: color.range()[i],
            pos: i,
          };
        }
        values[9] = {
          label: 'Other',
          color: color.range()[9],
          pos: 9,
        };
      } else {
        color = d3.scaleOrdinal(d3.schemeCategory10);
        let i;
        for (i = 0; i < strains.metadata.cat_enums_len[attrName]; i += 1) {
          values[i] = {
            label: strains.metadata.cat_enums[attrName][i],
            color: color.range()[i],
            pos: i,
          };
        }
      }
      d3.selectAll('circle').attr('fill', d => color(d[`cat_${attrName}`]));
      d3.selectAll('.keyRepr').remove();
      const tmpGroups = this.keyArea
        .data(values)
        .enter()
        .append('g')
        .attr('class', 'keyRepr');
      tmpGroups
        .append('rect')
        .attr('width', 20)
        .attr('height', 20)
        .attr('x', 10)
        .attr('y', d => 30 * d.pos + 10)
        .attr('fill', d => d.color);
      tmpGroups
        .append('text')
        .text(d => d.label)
        .attr('x', 40)
        .attr('y', d => 30 * d.pos + 25);
      // Update Key rectangle
      d3.selectAll('rect.keyBox').attr('height', 30 * values.length + 10);
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
  font-size: 12px;
}

.svg-container {
  display: inline-block;
  position: relative;
  width: 100%;
  padding-bottom: 100%;
  vertical-align: top;
  overflow: hidden;
}

.svg-content-responsive {
  display: inline-block;
  position: absolute;
  top: 10px;
  left: 0;
}
</style>
