<template>
  <div id="node_info">
    <h1>
      <a :href=node_info.url>
        {{ node_info.name }}
      </a>
    </h1>
    <p>{{ node_info.desc }}</p>
    <h3>Parents:</h3>
    <ul>
      <!-- eslint-disable-next-line -->
      <li v-for="parent in node_info.parents_readable">
        {{ parent }}
      </li>
    </ul>
    <div style="display: inline-block">
      <h4 style="float: left">Main Effect: {{node_info.main_effect}}</h4>
      <h4 style="float: right">Main Medicinal Use: {{node_info.main_med}}</h4>
      <h4 style="float: left">Main Flavor: {{node_info.main_flavor}}</h4>
    </div>
  </div>
</template>

<script>
export default {
  name: 'NodeInfo',
  props: {
    node_info: {},
  },
};
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
#node_info {
  width: 70%;
  padding: 10px;
  text-align: start;
  margin: 25px auto;
  border: 1px solid lawngreen;
}

a {
  color: lawngreen;
}

h4 {
  padding-right: 30px;
}
</style>
