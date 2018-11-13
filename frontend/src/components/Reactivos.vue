<template>
<!--v-if="userToken !== String"-->
  <v-card>

 <v-container grid-list-md text-xs-center>
    <v-layout row wrap>

        <v-flex xs6>
            <v-btn large color ="blue darken-4" dark >Reactivos</v-btn>
        </v-flex>

        <v-flex xs6>
            <v-btn large router-link to= "/Exams">Examenes</v-btn>
        </v-flex>

      <v-flex xs2>
        <v-card flat>
          <v-card-text class="px-0">Materia</v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs7 d-flex>
        <v-card flat>
          <v-select
          :items="Materias"
          item-text="name"
          item-value="subject_id"
          single-line auto
          label="Materias"
          v-model="selectedSubject"
        ></v-select>
        </v-card>
      </v-flex>

      <v-flex xs3>
        <v-card flat>
            <CrearMateria></CrearMateria>
            <EditarMateria :subjectId="selectedSubject"></EditarMateria>
            <v-btn flat icon v-on:click="deleteSubject()">
                <v-icon >delete</v-icon>
            </v-btn>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>

  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>

      <v-flex xs2>
        <v-card flat>
          <v-card-text class="px-0">Temas</v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs7 d-flex>
        <v-card flat>
          <v-select
          :items="Temas"
          item-text="name"
          item-value="topic_id"
          single-line auto
          label="Temas"
          v-model="selectedTopic"
        ></v-select>
        </v-card>
      </v-flex>

      <v-flex xs3>
        <v-card flat>
            <CrearTema :subjectId="selectedSubject"></CrearTema>
            <EditarTema :topicId="selectedTopic" :subjectId="selectedSubject"></EditarTema>
            <v-btn flat icon v-on:click="deleteTopic()">
                <v-icon >delete</v-icon>
            </v-btn>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>

  <v-container grid-list-md text-xs-center>
      <v-layout row wrap>
      <v-flex xs12>
        <v-card flat v-if="selectedTopic !== undefined">
          <h2>Preguntas</h2>
        </v-card>
      </v-flex>
<!--Elaboracion de preguntas-->
      <v-flex xs2>
        <v-card flat
        v-if="selectedTopic !== undefined">
          <CrearReactivo :topicId="selectedTopic"></CrearReactivo>
        </v-card>
      </v-flex>
<!--Preguntas Abiertas-->
      <v-flex xs10>
        <div v-for="pregunta in Preguntas.OpenQuestion"
        :key="pregunta.question_open_id">

        <v-flex xs9>
        <v-card flat >
          <v-text-field
            :value="pregunta.text"
            :label="pregunta.question_open_id"
            solo
            v-model="pregunta.text"
            :readonly="readOnly"
          ></v-text-field>

        </v-card>
        </v-flex>

        <v-flex xs3>
            <v-card flat>
            <EditarReactivo
            :questionOpenId="pregunta.question_open_id"
            :questionTFId="pregunta.question_tf_id"
            :questionOMId="pregunta.question_multi_id"
            :topicId="selectedTopic"
            ></EditarReactivo>
            <!--No Funciona-->
            <v-btn flat icon
            v-on:click="deleteQuestion(pregunta.question_open_id, selectedTopic)"
            v-if="pregunta.question_open_id !== undefined">
                <v-icon >delete</v-icon>
            </v-btn>
            <!--Funciona-->
            <v-btn flat icon
            v-on:click="deleteQuestionTF(pregunta.question_tf_id, selectedTopic)"
            v-if="pregunta.question_tf_id !== undefined">
                <v-icon >delete</v-icon>
            </v-btn>
            <!--No Funciona-->
            <v-btn flat icon
            v-on:click="deleteQuestionOM(pregunta.question_multi_id, selectedTopic)"
            v-if="pregunta.question_multi_id !== undefined">
                <v-icon >delete</v-icon>
            </v-btn>
        </v-card>
        </v-flex>

        </div>
      </v-flex>
<!---->
       </v-layout>
  </v-container>
<!---->
  </v-card>
</template>
<!--
<template v-else>
<v-card>
  <h1>Error</h1>
  <br>
  <label>Please go to login page :) </label>
  <br>
  <v-btn :to='"/Login"' >Login </v-btn>

</v-card>
</template>
-->

<script>
import CrearMateria from './CrearMateria.vue'
import CrearTema from './CrearTema.vue'
import EditarMateria from './EditarMateria.vue'
import EditarTema from './EditarTema.vue'
import CrearReactivo from './CrearReactivo.vue'
import EditarReactivo from './EditarReactivo.vue'
export default {
  data: () => ({
    userToken: undefined,
    // Materias: [ ],
    // Temas: [ ],
    Reactivos: ['Que onda?'],
    selectedSubject: [],
    selectedTopic: undefined,
    selectedQuestion: [],
    readOnly: true
  }),
  methods: {
    userLogin: function (payload) {
      if (payload === undefined) {
        this.$router.push({name: 'Login', params: { }})
      }
    },
    deleteSubject: function () {
      console.log('Ejecuto deleteSubject')
      console.log(this.selectedSubject)
      this.$store.dispatch('deleteSubject', this.selectedSubject)
        .then(() => {
        //
        }).catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    deleteTopic: function () {
      console.log('Ejecuto deleteTopic')
      console.log(this.selectedTopic)
      let payload = [this.selectedSubject, this.selectedTopic]
      this.$store.dispatch('deleteTopic', payload)
        .then(() => {
          //
        }).catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    refreshTopicList: function () {
      // console.log('Ejecuto topiclist')
      // console.log(this.selectedSubject)
      this.$store.dispatch('changeTopicList', this.selectedSubject)
        .then(() => {
          // this.Temas = this.$store.getters.topicList
        }).catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    refreshQuestionList: function () {
      this.$store.dispatch('changeQuestionList', this.selectedTopic)
        .then(() => {
          // Popo
        }).catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    deleteQuestion: function (questionId, topicId) {
      let payload = [questionId, topicId]
      console.log(payload)
      this.$store.dispatch('deleteQuestion', payload)
    },
    deleteQuestionTF: function (questionId, topicId) {
      let payload = [questionId, topicId]
      console.log(payload)
      this.$store.dispatch('deleteQuestionTF', payload)
    },
    deleteQuestionOM: function (questionId, topicId) {
      let payload = [questionId, topicId]
      console.log(payload)
      this.$store.dispatch('deleteQuestionOM', payload)
    }
  },
  created () {
    this.userToken = this.$store.getters.userToken
    // this.refreshSubjectList()
    this.userLogin(this.userToken)
    this.$store.dispatch('changeSubjectList')
      .then(() => {
        // this.Materias = this.$store.getters.subjectList
      }).catch((error) => {
        console.log('Error')
        console.log(error)
      })
  },
  mounted () {
    this.userToken = this.$store.getters.userToken
    this.Temas = this.$store.getters.topicList
    this.refreshSubjectList()
    this.refreshTopicList()
    this.refreshQuestionList()
  },
  computed: {
    Materias () {
      return this.$store.getters.subjectList
    },
    Temas () {
      return this.$store.getters.topicList
    },
    Preguntas () {
      if (this.selectedTopic !== undefined) {
        return this.$store.getters.questionList
      } else {
        return 0
      }
    }
    /*
    filteredSubjects () {
      var userSubjects = this.Materias
      userSubjects = userSubjects.filter((Materia) => {
        console.log(Materia.name)
        return Materia.name
      })
      console.log('Materias filtered')
      console.log(userSubjects.name)
      return userSubjects
    }
    */
  },
  watch: {
    selectedSubject: function (selectedSubject) {
      this.refreshTopicList()
    },
    selectedTopic: function (selectedTopic) {
      this.refreshQuestionList()
    }
  },
  components: {
    'CrearMateria': CrearMateria,
    'CrearTema': CrearTema,
    'EditarMateria': EditarMateria,
    'EditarTema': EditarTema,
    'CrearReactivo': CrearReactivo,
    'EditarReactivo': EditarReactivo
  }
}
</script>
