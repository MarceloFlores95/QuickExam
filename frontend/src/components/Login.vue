<template>
<v-container grid-list-md text-xs-center>
  <div class="Login">
    <h1>Login</h1>
    <v-card>
        <h2>UserName</h2>
        <v-text-field
        v-model="password"
        box
        color="deep-purple"
        counter="6"
        label="UserName"
        style="min-height: 96px"
        type="password"
      ></v-text-field>
      <h2>Password</h2>
      <v-text-field
        v-model="password"
        box
        color="deep-purple"
        counter="6"
        label="Password"
        style="min-height: 96px"
        type="password"
      ></v-text-field>
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
      message: 'UserLogin',
      agreement: false,
      bio: 'Far far away, behind the word mountains, far from the countries Vokalia and Consonantia, there live the blind texts',
      dialog: false,
      email: undefined,
      form: false,
      isLoading: false,
      password: undefined,
      phone: undefined,
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

  }
}
</script>
