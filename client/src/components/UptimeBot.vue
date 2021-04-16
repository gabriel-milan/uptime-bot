<template>
  <div class="hello">
    <h1>UptimeBot</h1>
    <h2>Real-time verification for servers availability</h2>
    <p></p>
    <h3>Servers</h3>
    <ul id="server-list">
      <li v-for="(obj, host) in servers" :key="host">
        <md-icon
          :style="{
            color:
              obj.state === true
                ? 'green'
                : obj.state === false
                ? 'red'
                : 'gray',
          }"
          >fiber_manual_record</md-icon
        >
        {{ obj.ip + ":" + obj.port }}
      </li>
    </ul>
  </div>
</template>

<script>
export default {
  name: "UptimeBot",
  data() {
    return {
      updateDelayMs: 5000,
      servers: {},
    };
  },
  mounted() {
    setTimeout(() => {
      this.checkServers();
    }, 0);
    setInterval(() => {
      this.checkServers();
    }, this.updateDelayMs);
  },
  methods: {
    async checkServers() {
      const url = process.env.VUE_APP_BACKEND_URL;
      const res = await fetch(url);
      const data = await res.json();
      this.servers = data;
    },
  },
};
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
