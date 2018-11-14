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
      @click.stop="drawer = !drawer">
        <v-icon>perm_identity</v-icon>
      </v-btn>

      </v-toolbar>

    <v-navigation-drawer
      v-model="drawer"
      absolute
      temporary
      right
    >
      <v-list class="pa-1">
        <v-list-tile avatar>
          <v-list-tile-avatar>
            <img src="https://randomuser.me/api/portraits/men/85.jpg">
          </v-list-tile-avatar>

          <v-list-tile-content>
            <v-list-tile-title>{{User}}</v-list-tile-title>
          </v-list-tile-content>
        </v-list-tile>
      </v-list>

      <v-list class="pt-0" dense>
        <v-divider></v-divider>

        <v-list-tile
          v-for="item in items"
          :key="item.title"
        >
          <v-list-tile-action>
            <v-icon>{{item.icon}}</v-icon>
          </v-list-tile-action>

          <v-btn flat
          v-if="item.title === 'Ajustes de cuenta'"          >
            <v-list-tile-title>Ajustes de cuenta</v-list-tile-title>
          </v-btn>
          <v-btn flat
          v-if="item.title === 'Cerrar sesión'"
          v-on:click="logout()"
          >
            <v-list-tile-title>Cerrar sesión</v-list-tile-title>
          </v-btn>
        </v-list-tile>
      </v-list>
    </v-navigation-drawer>

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
      drawer: null,
      items: [
        { title: 'Ajustes de cuenta', icon: 'settings' },
        { title: 'Cerrar sesión', icon: 'power_settings_new' }
      ]
      // userToken: undefined
    }
  },
  methods: {
    logout () {
      this.$store.dispatch('logout', undefined)
      this.$router.push({name: 'Login', params: { }})
    }

  },
  computed: {
    userToken () {
      return this.$store.getters.userToken
    },
    User () {
      return this.$store.getters.userUsername
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
