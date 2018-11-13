<template>
    <v-dialog v-model="dialog" persistent max-width="300">
        <v-btn flat icon slot="activator">
            <v-icon>edit</v-icon>
        </v-btn>
<!-- Abierta -->
        <v-card v-if="questionOpenId !== undefined">
        <v-card-title class="headline">Edita la pregunta abierta</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="text"
                label="Respuesta"
            ></v-text-field>
            </v-flex>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editOpenQuestion(questionOpenId, text, topicId)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
<!-- True or False -->
        <v-card v-if="questionTFId !== undefined">
        <v-card-title class="headline">Edita la pregunta ToF{{questionOpenId}} {{questionTFId}}</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="text"
                label="Pregunta"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="expression"
                label="Expression"
            ></v-text-field>
        </v-flex>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editTFQuestion(questionTFId, text, topicId, expression)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
<!-- OpcionMultiple -->
        <v-card v-if="questionOMId !== undefined">
        <v-card-title class="headline">Edita la pregunta Multiple{{questionOMId}} {{questionTFId}}</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="text"
                label="Pregunta"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="correctAnswer"
                label="Respuesta Correcta"
            ></v-text-field>
        </v-flex>

        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editOMQuestion(questionOMId, text, topicId, correctAnswer)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>

    </v-dialog>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      pregunta: undefined,
      respuesta: undefined
    }
  },
  props: {
    questionOpenId: {
      required: true
    },
    questionTFId: {
      required: true
    },
    topicId: {
      required: true
    },
    questionOMId: {
      required: true
    }
  },
  methods: {
    editOpenQuestion: function (questionId, text, topicId) {
      let payload = [questionId, text, topicId]
      console.log(payload)
      this.$store.dispatch('editOpenQuestion', payload)
        .then((response) => {
          //
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    editTFQuestion: function (questionId, text, topicId, expression) {
      let payload = [questionId, text, topicId, expression]
      console.log(payload)
      this.$store.dispatch('editTFQuestion', payload)
        .then((response) => {
          //
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    editOMQuestion: function (questionId, text, topicId, correctAnswer) {
      let payload = [questionId, text, topicId, correctAnswer]
      console.log(payload)
      this.$store.dispatch('editOMQuestion', payload)
        .then((response) => {
          //
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error de editOMQuestion')
          console.log(error)
        })
    }
  },
  computed: {
    Respuesta () {
      var Respuesta = this.$store.getters.questionList.OpenQuestion
      /*
      Respuesta = Respuesta.filter((questionID) => {
        return questionID.question_tf_id !== undefined
      })
      */
      return Respuesta
    }
  }
}
</script>
