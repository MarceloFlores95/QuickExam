<template>
<v-app>
  <div id="app">
        <v-toolbar color="grey darken-1" dark>
        <v-toolbar-title>
          Quick Exam
        </v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>favorite</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>more_vert</v-icon>
      </v-btn>
    </v-toolbar>
    <v-container grid-list-md text-xs-center>
        <v-layout row wrap>

        <v-flex xs6>
            <v-btn large >Reactivos</v-btn>
        </v-flex>

        <v-flex xs6>
            <v-btn large>Examenes</v-btn>
        </v-flex>

        </v-layout>
    </v-container>
    <router-view/>
  </div>
  </v-app>
</template>

<script>
export default {
  name: 'App'
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
