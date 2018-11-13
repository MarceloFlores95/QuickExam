<template>
<v-container grid-list-md text-xs-center>
  <div class="Login">
    <h1 class="text-sm-left">Login</h1>
    <v-card>
        <h2 class="text-sm-left">UserName</h2>
        <v-text-field
        v-model="user.username"
        box
        color="deep-purple"
        counter="6"
        label="UserName"
        style="min-height: 96px"
      ></v-text-field>
      <h2 class="text-sm-left">Password</h2>
      <v-text-field
        v-model="user.password"
        box
        color="deep-purple"
        counter="6"
        label="Password"
        style="min-height: 96px"
        type="password"
      ></v-text-field>

      <v-btn v-on:click="userLogin(user)">Login </v-btn>
      <v-btn v-on:click="userRegister(user)">Register </v-btn>
    </v-card>
  </div>
  </v-container>
</template>

<script>
/*
    <v-text-field
        v-model="password"
        :rules="[rules.password, rules.length(6)]"
        box
        color="deep-purple"
        counter="6"
        label="Password"
        style="min-height: 96px"
        type="password"
      ></v-text-field>
*/
export default {
  name: 'UserLogin',
  data () {
    return {
      user: {
        username: undefined,
        password: undefined
      },
      message: 'UserLogin',
      dialog: false,
      isLoading: false,
      rules: {
        email: v => (v || '').match(/@/) || 'Please enter a valid email',
        length: len => v => (v || '').length >= len || `Invalid character length, required ${len}`,
        password: v => (v || '').match(/^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*(_|[^\w])).+$/) ||
          'Password must contain an upper case letter, a numeric character, and a special character',
        required: v => !!v || 'This field is required'
      }
    }
  },
  components: {

  },
  methods: {
    userRegister: function (payload) {
      this.$store.dispatch('userRegister', payload)
        .then((response) => {
          console.log(this.$store.state.user.username)
          console.log(this.$store.state.user.password)
          console.log(this.$store.state.user.userToken)
          this.$router.push({name: 'Reactivos', params: { }})
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    userLogin: function (payload) {
      this.$store.dispatch('userLogin', payload)
        .then((response) => {
          // console.log(response)
          // console.log(this.$store.state.user.username)
          // console.log(this.$store.state.user.password)
          // console.log(this.$store.state.user.userToken)
          this.$router.push({name: 'Reactivos', params: { }})
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    }
  }
}
</script>
