<template>
  <v-card
    color="gray lighten-4"
    flat
    height="500px"
  >

<!---Boton-->
<v-container grid-list-md text-xs-center>
<v-layout row wrap>
    <v-flex xs6>
            <v-btn large router-link to= "/Reactivos">Reactivos</v-btn>
        </v-flex>

        <v-flex xs6>
            <v-btn large router-link to= "/Exams">Examenes</v-btn>
        </v-flex>
</v-layout>
</v-container>

<v-container>
  <v-layout align-center justify-center row fill-height/>
          <v-flex xs12 sm6>
              <v-text-field
                  v-model="user"
                  label="User"
                  :value="user"
                  :readonly=editVar
              ></v-text-field>
          </v-flex>
          <v-flex xs12 sm6>

              <v-text-field
                  v-model="password"
                  label="Password"
                  :value="password"
                  :readonly=editVar
              ></v-text-field>
          </v-flex>
          <v-btn flat icon slot="activator"
          v-on:click="edit"
          v-if="editVar == true">
            <v-icon>edit</v-icon>
        </v-btn>
        <v-btn flat icon slot="activator"
        v-on:click="edit"
        v-if="editVar == false">
            <v-icon>save</v-icon>
        </v-btn>
</v-container>
</v-card>
</template>

<script>
export default {
  data: () => ({
    userToken: undefined,
    user: undefined,
    password: undefined,
    editVar: true
  }),
  methods: {
    edit: function () {
      this.editVar = !this.editVar
      if (this.editVar === true) {
        this.changeData()
      }
      console.log(this.editVar)
    },
    changeData: function () {
      let payload = [this.user, this.password]
      this.$store.dispatch('changeData', payload)
        .then((response) => {
          this.$router.push({name: 'Reactivos', params: { }})
        })
    }
  },
  created () {
    this.userToken = this.$store.getters.userToken
    this.user = this.$store.getters.userUsername
    this.password = this.$store.getters.userPassword
  },
  mounted () {

  },
  computed: {
    Materias () {
      return this.$store.getters.subjectList
    },
    Temas () {
      return this.$store.getters.topicList
    }
  }
}
/*
Reflexion sobre el proyecto
*/
</script>
