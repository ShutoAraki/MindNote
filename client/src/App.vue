<template>
  <div id="app">
    <b-navbar id="notes-navbar" type="dark">
      <b-navbar-brand href="/notes/" id="title">MindNotes
      <img src="./assets/brain_logo.png" 
           alt="" width="60px" height="50px">
      </b-navbar-brand>
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
  /* font-family: "Avenir", Helvetica, Arial, sans-serif; */
  font-family: "Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  background-color: rgb(243, 241, 196);

  display: flex;
  flex-direction: column;
}

#notes-navbar {
  background-color: rgb(42, 150, 177);
}

#title {
  /* font-family: "Brush Script MT", cursive;  */
  font-family: "Arial Rounded MT Bold", "Helvetica Rounded", Arial, sans-serif;
  font-size: 45px; 
  font-style: normal; 
  font-variant: normal; 
  font-weight: 200; 
  line-height: 26.4px;
  color:  rgb(255, 255, 255);
}
</style>
