<template>
<v-app>
  <div id="app">
        <v-toolbar color="grey darken-1" dark>
        <v-toolbar-title>
          Quick Exam
        </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon
      v-if="userToken !== undefined"
      router-link to= "/profile">
        <v-icon>perm_identity</v-icon>
      </v-btn>
    </v-toolbar>
    <v-container grid-list-md text-xs-center>
        <v-layout row wrap>

        </v-layout>
    </v-container>
    <router-view/>
  </div>
  </v-app>
</template>

<script>
export default {
  name: 'App',
  data () {
    return {
      // userToken: undefined
    }
  },
  computed: {
    userToken () {
      return this.$store.getters.userToken
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
