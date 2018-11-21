<template>
    <v-dialog v-model="dialog" persistent max-width="600px">
        <v-btn slot="activator" flat>
            Editar Examen
        </v-btn>
        <v-card>
            <v-card-title>
            <span class="headline">Editar Examen</span>
            </v-card-title>
             {{exam}}
             {{filteredExam}}
<!--
        <v-flex xs12 sm6>
            <v-text-field
                v-model="name"
                :label="test.name"
            ></v-text-field>
        </v-flex>

        <v-flex xs12 sm6>
            <v-text-field
                v-model="encabezado"
                :label="test.encabezado"
            ></v-text-field>
        </v-flex>
-->
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editOpenQuestion(questionOpenId, text, topicId, pregunta.variables)" >Guardar</v-btn>
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
      tema: undefined,
      tipoPregunta: undefined, // Guarda que tipo de pregunta es
      respuestaVoF: undefined, // Guarda si la pregunta tiene valor de V o F
      pregunta: undefined, // Guardo la pregunta
      respuestaOM: undefined,
      dummyAnswers: [],
      dummyAnswer: undefined,
      variables: []
    }
  },
  components: {
    'CrearVariable': CrearVariable
  },
  props: {
    exam: {
      required: true
    },
    selectedExam: {
      required: true
    }
  },
  methods: {
    saveOpenQuestion (pregunta, topicId, tipoPregunta) {
      console.log(this.variables)
      let payload = [pregunta, topicId, tipoPregunta, this.variables]
      this.variables = []
      this.$store.dispatch('addQuestion', payload)
        .then((response) => {
          console.log('Refrescar variables')
          console.log(this.variables)
          this.reset = true
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    }
  },
  computed: {
    filteredExam () {
      var EExam = this.exam
      EExam = EExam.filter((YaBasta) => {
        return YaBasta.test_id === this.selectedTest
      })
      return EExam
    }
  }
}
</script>
