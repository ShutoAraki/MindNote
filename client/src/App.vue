<template>
  <div id="app">
    <b-navbar id="notes-navbar" type="dark">
      <b-navbar-brand href="#">MindNotes</b-navbar-brand>
      <b-navbar-nav class="ml-auto">
        <b-button size="sm" class="my-2 my-sm-0" v-on:click="change_view">{{ opposite_view }}</b-button>
      </b-navbar-nav>
    </b-navbar>
    <router-view />
  </div>
</template>

<script>
export default {
  computed: {
    opposite_view() {
      if (this.$route.path.startsWith('/notes')) {
        return 'Note Map';
      } else {
        return 'Notes';
      }
    }
  },
  methods: {
    change_view() {
      if (this.$route.path.startsWith('/notes')) {
        this.$router.push('/map');
      } else {
        this.$router.push('/notes');
      }
    }
  },
}
</script>

<style>
html,
body,
#app {
  width: 100%;
  height: 100%;
}

#app {
  font-family: "Avenir", Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;

  display: flex;
  flex-direction: column;
}

#notes-navbar {
  background-color: rgb(221, 205, 65);
}
</style>
