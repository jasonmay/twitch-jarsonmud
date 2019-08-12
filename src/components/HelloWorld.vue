<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div style="border: solid 1px black; display: inline-block">
    <svg width="800px" height="640px" id="magic" />
    </div>
  </div>
</template>

<script>
/* eslint-disable */
import {TimelineMax} from 'gsap'
import Navigator from './interface.js';

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data: () => ({
    navigator: new Navigator(7, 7)
  }),
  mounted() {
    const magic = document.getElementById("magic");
    this.navigator.drawRooms(magic);
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
