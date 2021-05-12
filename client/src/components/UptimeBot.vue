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
    <h3>
      {{ toomanyrequests ? "Stop spamming our back-end, please :)" : "" }}
    </h3>
    <form
      id="app"
      @submit="checkForm"
      action="javascript:void(0);"
    >
    <h3>Check a custom server by filling the form</h3>
      <p v-if="errors.length">
        <b>Please fix the following:</b>
        <ul>
          <li v-bind:key=error.id v-for="error in errors">{{ error }}</li>
        </ul>
      </p>
      <p>
        <label for="ip">Hostname </label>
        <input
          id="ip"
          v-model="ip"
          type="text"
          name="ip"
        >
      </p>
      <p>
        <label for="port">Port </label>
        <input
          id="port"
          v-model="port"
          type="number"
          name="port"
          min="0"
        >
      </p>
      <p>
        <input
          type="submit"
          value="Check"
        >
      </p>
    </form>
  </div>
</template>

<script>
export default {
  name: "UptimeBot",
  data() {
    return {
      errors: [],
      ip: null,
      port: null,
      updateDelayMs: 5000,
      servers: {},
      customServer: {},
      toomanyrequests: false,
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
      if (res.status == 200) {
        const data = await res.json();
        this.servers = data;
        this.toomanyrequests = false;
      } else if (res.status == 429) {
        this.toomanyrequests = true;
      }
    },
    async checkForm(e) {
      if (this.ip && this.port) {
        const url = process.env.VUE_APP_BACKEND_URL;
        const res = await fetch(url, {
          method: "POST",
          body: JSON.stringify({ ip: this.ip, port: this.port }),
          headers: {
            "Content-type": "application/json; charset=UTF-8",
          },
        });
        if (res.status == 200) {
          const data = await res.json();
          alert(
            "Hostname " +
              data.ip +
              " at port " +
              data.port +
              " is " +
              (data.state ? "UP! :)" : "DOWN :(")
          );
        } else if (res.status == 429) {
          alert("Stop spamming our back-end! :)");
        }
      }
      this.errors = [];
      if (!this.ip) {
        this.errors.push("You didn't provide a hostname.");
      }
      if (!this.port) {
        this.errors.push("You didn't provide a port.");
      }
      e.preventDefault();
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
