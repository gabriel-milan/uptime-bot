// Adapted from
// https://github.com/rajkharvar/vue-made-with-love
// all credits for the original developers

<template>
  <div class="made-with-love">
    <a :href="`https://github.com/` + repo">
      <img
        :alt="`Star me at https://github.com/` + repo"
        :src="`https://img.shields.io/github/stars/` + repo + `?style=social`"
      />
    </a>
    <p>
      {{ code ? "&lt;/&gt;" : "Made" }} with ❤️
      {{ by ? "by" : "" }}
      <span v-if="by" class="by">
        <a :href="link" v-if="link">{{ by }}</a>
        {{ !link ? by : "" }}
      </span>
      {{ after_message }}
      <br />
    </p>
  </div>
</template>

<script>
export default {
  name: "MadeWithLove",
  props: {
    by: {
      type: String,
      default: "",
    },
    link: {
      type: String,
      default: "",
    },
    code: {
      type: Boolean,
      default: false,
    },
    after_message: {
      type: String,
      default: "",
    },
    repo: {
      type: String,
      default: "",
    },
  },
};
</script>

<style lang="scss" scoped>
.made-with-love {
  text-align: center;
  background: transparent;
  font-family: Avenir, Helvetica, Arial, sans-serif;
  p {
    position: absolute;
    width: 100%;
    left: 0;
  }
  .by {
    font-weight: bold;
    a {
      text-decoration: none;
      color: inherit;
      &:hover {
        border-bottom: 1px solid;
      }
    }
  }
}
</style>
