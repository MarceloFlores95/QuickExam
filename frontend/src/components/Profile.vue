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

<p>Nombre de usuario</p>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="user"
                :label="user"
                readonly
            ></v-text-field>
        </v-flex>
        <p>Contraseña</p>
        <v-flex xs12 sm6>

            <v-text-field
                v-model="password"
                :label="password"
                readonly
            ></v-text-field>
        </v-flex>
</v-card>
</template>

<script>
export default {
  data: () => ({
    userToken: undefined,
    user: undefined,
    password: undefined
  }),
  methods: {
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
  },
  watch: {
    selectedSubject: function (selectedSubject) {
      this.refreshTopicList()
    },
    selectedTopic: function (selectedTopic) {
      this.refreshQuestionList()
    }
  }
}
/*
Reflexion sobre el proyecto
*/
</script>
