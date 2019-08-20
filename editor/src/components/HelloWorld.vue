<template>
  <div class="hello">
    <h1>{{ msg }}</h1>
    <div style="border: solid 1px black; display: inline-block">
    <svg width="800px" height="640px" ref="navigator" />
    </div>
  </div>
</template>

<script>
/* eslint-disable */

export default {
  name: 'HelloWorld',
  props: {
    msg: String
  },
  data: () => ({
    navigator: new Navigator(7, 7)
  }),
  mounted() {
    const navEl = this.$refs.navigator;
    this.navigator.drawRooms(navEl);

    window.addEventListener("keypress", (function(e) {
      let keyDispatch = {
        n: function() {
          this.navigator.goDirection(navEl, 0, -1);
        },
        w: function() {
          this.navigator.goDirection(navEl, -1, 0);
        },
        s: function() {
          this.navigator.goDirection(navEl, 0, 1);
        },
        e: function() {
          this.navigator.goDirection(navEl, 1, 0);
        },
      };
      console.log(this.navigator);
      if (!this.navigator.isMoving()) {
        if (keyDispatch.hasOwnProperty(e.key)) {
          keyDispatch[e.key].bind(this)();
        }
      }
    }).bind(this));
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
