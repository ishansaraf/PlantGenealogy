<template>
  <div id="node_info">
    <h1>
      <a :href=node_info.url>
        {{ node_info.name }}
      </a>
    </h1>
    <p>{{ node_info.desc }}</p>
    <!-- <ul><li for parent in parents></li></ul> -->
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

.dot {
  float: right;
  height: 25px;
  width: 25px;
  background-color: orange;
  display: inline-block;
  border-radius: 50%;
}
</style>
