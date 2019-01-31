<template>
  <div id="app">
    <ForceDiagram></ForceDiagram>
  </div>
</template>

<script>
import ForceDiagram from './components/ForceDiagram.vue';

export default {
  name: 'app',
  components: {
    ForceDiagram,
  },
};
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
