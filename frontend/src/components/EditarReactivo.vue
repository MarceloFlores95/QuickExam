<template>
    <v-dialog v-model="dialog" persistent max-width="600px">
        <v-btn flat icon slot="activator">
            <v-icon>edit</v-icon>
        </v-btn>
<!-- Abierta -->
        <v-card v-if="questionOpenId !== undefined">
        <v-card-title class="headline">Edita la pregunta abierta</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="text"
                :label="pregunta.text"
            ></v-text-field>
        </v-flex>

        <div v-for="variable in pregunta.variables"
        :key="variable.variable_id">
        <v-flex xs12 sm6>
            <v-text-field
                v-model="variable.values"
                :label="variable.values"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="variable.symbol"
                :label="variable.symbol"
            ></v-text-field>
        </v-flex>
        <v-overflow-btn
              :items="tipos"
              :label="variable.type"
              segmented
              target="#dropdown-example"
              v-model="variable.type"
            ></v-overflow-btn>
        </div>
        <CrearVariable @clicked="guardoArreglo"></CrearVariable>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editOpenQuestion(questionOpenId, text, topicId, pregunta.variables)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
<!-- True or False -->
        <v-card v-if="questionTFId !== undefined">
        <v-card-title class="headline">Edita la pregunta ToF</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="text"
                :label="pregunta.text"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="expression"
                :label="pregunta.expression"
            ></v-text-field>
        </v-flex>

        <div v-for="variable in pregunta.variables"
        :key="variable.variable_id">
        <v-flex xs12 sm6>
            <v-text-field
                v-model="variable.values"
                :label="variable.values"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="variable.symbol"
                :label="variable.symbol"
            ></v-text-field>
        </v-flex>
        <v-overflow-btn
              :items="tipos"
              :label="variable.type"
              segmented
              target="#dropdown-example"
              v-model="variable.type"
            ></v-overflow-btn>
        </div>
        <CrearVariable @clicked="guardoArreglo"></CrearVariable>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editTFQuestion(questionTFId, text, topicId, expression, pregunta.variables)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
<!-- OpcionMultiple -->
        <v-card v-if="questionOMId !== undefined">
        <v-card-title class="headline">Edita la pregunta Multiple</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="text"
                :label="pregunta.text"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
          <p>Respuesta Correcta</p>
            <v-text-field
                v-model="correct_answer"
                :label="pregunta.correct_answer"
            ></v-text-field>
        </v-flex>
        <p>Respuesta Incorrecta</p>

        <div v-for="incorrecta in pregunta.dummies"
        :key="incorrecta.dummy_answer_id">
          <v-flex xs12 sm6>
              <v-text-field
                  v-model="incorrecta.answer"
                  :label="incorrecta.answer"
              ></v-text-field>
          </v-flex>
        </div>
        <p>Variable</p>
        <div v-for="variable in pregunta.variables"
        :key="variable.variable_id">
        <v-flex xs12 sm6>
            <v-text-field
                v-model="variable.values"
                :label="variable.values"
            ></v-text-field>
        </v-flex>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="variable.symbol"
                :label="variable.symbol"
            ></v-text-field>
        </v-flex>
        <v-overflow-btn
              :items="tipos"
              :label="variable.type"
              segmented
              target="#dropdown-example"
              v-model="variable.type"
            ></v-overflow-btn>
        </div>
        <CrearVariable @clicked="guardoArreglo"></CrearVariable>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editOMQuestion(questionOMId, text, topicId, correct_answer, pregunta.dummies, pregunta.variables)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
import CrearVariable from './CrearVariable.vue'
export default {
  data () {
    return {
      dialog: false,
      respuesta: undefined,
      variables: [],
      tipos: [
        {id: 'int', text: 'int', callback: () => console.log('Integer')},
        {id: 'dec', text: 'dec', callback: () => console.log('Decimal')},
        {id: 'str', text: 'str', callback: () => console.log('String')}
      ]
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
    },
    pregunta: {
      required: true
    }
  },
  components: {
    'CrearVariable': CrearVariable
  },
  methods: {
    editOpenQuestion: function (questionId, text, topicId, variables) {
      let payload = [questionId, text, topicId, variables]
      console.log(payload)
      this.$store.dispatch('editOpenQuestion', payload)
        .then((response) => {
          //
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error editOpenQuestion')
          console.log(error)
        })
    },
    editTFQuestion: function (questionId, text, topicId, expression, variables) {
      let payload = [questionId, text, topicId, expression, variables]
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
    editOMQuestion: function (questionId, text, topicId, correct, dummies, variables) {
      let payload = [questionId, text, topicId, correct, dummies, variables]
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
    },
    guardoArreglo (value) {
      this.variables = this.variables.concat(value)
      // console.log('Guardo Arreglo')
      // console.log(this.variables)
    }
  },
  computed: {
    Respuesta () {
      var Respuesta = this.$store.getters.questionList.OpenQuestion
      if (this.questionOMId !== null) {
        Respuesta = Respuesta.filter((questionID) => {
          return questionID.question_multi_id === this.questionOMId
        })
      }
      if (this.questionOpenId !== null) {
        Respuesta = Respuesta.filter((questionID) => {
          return questionID.question_open_id === this.questionOpenId
        })
      }
      if (this.questionTFId !== null) {
        Respuesta = Respuesta.filter((questionID) => {
          return questionID.question_tf_id === this.questionTFId
        })
      }
      return Respuesta
    }
  }
}
</script>
