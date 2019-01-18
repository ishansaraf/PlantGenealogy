<template>

  <svg :viewbox="viewbox" :width="width" :height="height" :d="svg" style="width: 100%; height: auto;">
    <g stroke="#000">
      <rect v-for="n in nodes" :key="n.id" :x="n.x" :y="n.y" :height="n.height" :width="n.width" :fill="n.fill"><title>{{n.title}}</title></rect>
    </g>
    <g fill='none' stroke-opacity="0.50">
      <!--TODO stroke color-->
      <g v-for="l in links" :key="l.id" style="mix-blend-mode: multiply;"><path :d="l.d" :stroke="l.stroke" :stroke-width="l.strokewidth"></path><title>{{l.title}}</title></g>
    </g>
    <g style="font: 10px sans-serif;">
       <text v-for="t in texts" :key="t.id" :x="t.x" :y="t.y" dy="0.35em" :text-anchor="t.textanchor">{{t.text}}</text>
    </g>
  </svg>
</template>
<script>
// import * as d3 from "d3";
import { sankey, sankeyLinkHorizontal } from 'd3-sankey'
export default {
  name: 'sankey',
  data() {
    return {
      svg: '',
      src: {    nodes: [
        { id: "A1", name:"A1"},
        { id: "A2", name:"A2"},
        { id: "B1", name:"B1"}
    ],
    links: [
        { source: "A1", target: "B1", value: 27 },
        { source: "A1", target: "A2", value: 27 }
    ]},
      width:'1200',
      height:'600',
    };
  },

  computed: {
    viewbox(){
      return `0,0,${this.width},${this.height}`
    },
    graph(){

        const mysankey = sankey()
                         .size([this.width, this.height])
                         .nodeId(d => d.id)
                         .nodeWidth(20)
                         .nodePadding(20)
        let mygraph = mysankey(this.src);
        console.log(mygraph)
        return mygraph;
    },
      texts() {
        var that = this;
        if (this.graph){
         return this.graph.nodes.map(function(d) {
            return {
              id: d.id,
              x: d.x0 < that  .width / 2 ? d.x1 + 6 : d.x0 - 6,
              y: (d.y1 + d.y0) / 2,
              dy: "0.35em",
              textanchor: d.x0 < that.width / 2 ? "start" : "end",
              text: d.name,

            };
          });
    }
    return null;
  },
  links(){
    var link =sankeyLinkHorizontal();

          // console.log(link)
    //TODO pretty colors
        if (this.graph){
         return this.graph.links.map(function(d) {
            return {
              id: d.id,
              d:link(d),
              stroke: "#ff0000",//TODO
              strokewidth: Math.max(1, d.width),
              title: `${d.source.name} => ${d.target.name}`

            };
          });
    }
    return null

  },
      nodes() {
        if (this.graph){
         return this.graph.nodes.map(function(d) {
            return {
              id: d.id,
              x: d.x0,
              y: d.y0,
              height: d.y1-d.y0,
              width: d.x1-d.x0,
              fill: "#ff0000",//TODO
              title: `${d.name}\nTODO`

            };
          });
    }
    return null;
}
  },
  mounted: function() {
  //Sources:
  //https://beta.observablehq.com/@mbostock/d3-sankey-diagram
  //https://medium.com/tyrone-tudehope/composing-d3-visualizations-with-vue-js-c65084ccb686

  //https://jarrettmeyer.com/2018/05/31/creating-a-d3-sankey-graph



  // this.svg.append("g")
  //     .attr("stroke", "#000")
  //   .selectAll("rect")
  //   .data(nodes)
  //   .enter().append("rect")
  //     .attr("x", d => d.x0)
  //     .attr("y", d => d.y0)
  //     .attr("height", d => d.y1 - d.y0)
  //     .attr("width", d => d.x1 - d.x0)
  //     .attr("fill", d => color(d.name))
  //   .append("title")
  //     .text(d => `${d.name}\n${format(d.value)}`);

  // const link = this.svg.append("g")
  //     .attr("fill", "none")
  //     .attr("stroke-opacity", 0.5)
  //   .selectAll("g")
  //   .data(links)
  //   .enter().append("g")
  //     .style("mix-blend-mode", "multiply");

  // if (edgeColor === "path") {
  //   const gradient = link.append("linearGradient")
  //       .attr("id", d => (d.uid = this.$el.uid("link")).id)
  //       .attr("gradientUnits", "userSpaceOnUse")
  //       .attr("x1", d => d.source.x1)
  //       .attr("x2", d => d.target.x0);

  //   gradient.append("stop")
  //       .attr("offset", "0%")
  //       .attr("stop-color", d => color(d.source.name));

  //   gradient.append("stop")
  //       .attr("offset", "100%")
  //       .attr("stop-color", d => color(d.target.name));
  // }

  // link.append("path")
  //     .attr("d", sankeyLinkHorizontal())
  //     .attr("stroke", d => edgeColor === "path" ? d.uid
  //         : edgeColor === "input" ? color(d.source.name)
  //         : color(d.target.name))
  //     .attr("stroke-width", d => Math.max(1, d.width));

  // link.append("title")
  //     .text(d => `${d.source.name} → ${d.target.name}\n${format(d.value)}`);

   },
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
h3 {
  margin: 40px 0 0;
}
ul {
  list-style-type: none;
  padding: 0;
}
li {
  display: inline-block;
  margin: 0 10px;
}
a {
  color: #42b983;
}
</style>
