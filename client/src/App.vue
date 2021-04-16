<template>
  <div id="app">
    <UptimeBot />
    <br />
    <MadeWithLove
      by="Gabriel Milan"
      link="https://github.com/gabriel-milan/"
      repo="gabriel-milan/uptime-bot"
    />
  </div>
</template>

<script>
import UptimeBot from "./components/UptimeBot.vue";
import MadeWithLove from "./components/MadeWithLove.vue";

export default {
  name: "App",
  components: {
    UptimeBot,
    MadeWithLove,
  },
};
</script>

<style>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}
</style>
