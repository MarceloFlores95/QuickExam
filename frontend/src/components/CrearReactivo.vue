<template>
            <v-dialog v-model="dialog" persistent max-width="800px">
        <v-btn slot="activator" color="black" dark flat icon>
            <v-icon>add_box</v-icon>
        </v-btn>
        <v-card>
            <v-card-title>
            <span class="headline">Reactivo</span>
            </v-card-title>
            <v-card>

    <v-card-text>
      <v-container fluid>
        <v-layout row wrap>
          <v-flex xs12>
            <v-radio-group v-model="tipoPregunta" :mandatory="true" row>
                <v-radio label="Opcion Multiple" value="Opcion Multiple"></v-radio>
                <v-radio label="Verdadero o Falso" value="Verdadero o Falso"></v-radio>
                <v-radio label="Abierta" value="Abierta"></v-radio>
            </v-radio-group>
          </v-flex>
        </v-layout>
      </v-container>
    </v-card-text>
  </v-card>

 </v-card>
  <v-card v-if="tipoPregunta==='Opcion Multiple'">
        <v-card-text>
        <v-container grid-list-md>
            <v-layout wrap>
            <v-flex xs12>
                <v-text-field label="Escribe tu pregunta..."
                required
                v-model="pregunta"
                ></v-text-field>
            </v-flex>
            </v-layout>
        </v-container>
        <v-flex xs12>
            <v-text-field
            label="Escribe la respuesta correcta"
            required
            v-model="respuestaOM"></v-text-field>
        </v-flex>

        <v-btn flat icon v-on:click="addDummyAnswer(questionOMId)">
            <v-icon >add_circle</v-icon>
        </v-btn>
        <v-btn flat icon v-on:click="deleteDummyAnswer(questionOMId)">
            <v-icon >delete_forever</v-icon>
        </v-btn>

        <div
            v-for="(respuesta, index) in dummyAnswers"
            v-bind:key="index"
            v-bind:title="dummyAnswers"
          >
        <v-text-field
          label="Agrega respuesta incorrecta"
          solo
          v-model="dummyAnswers[index]"
        ></v-text-field>
        </div>
        <CrearVariable @clicked="guardoArreglo"></CrearVariable>

        </v-card-text>
 </v-card>

 <v-card v-if="tipoPregunta==='Verdadero o Falso'">
            <v-card-text>
            <v-container grid-list-md>
                <v-layout wrap>
                <v-flex xs12>
                    <v-text-field
                    label="Escribe tu pregunta..."
                    required
                    v-model="pregunta"></v-text-field>
                </v-flex>
                </v-layout>
            </v-container>
             <v-flex xs12>
                    <v-text-field
                    label="Escribe la expresion de tu respuesta..."
                    required
                    v-model="respuestaVoF"></v-text-field>
                </v-flex>
              <CrearVariable @clicked="guardoArreglo"></CrearVariable>
            <small>*indicates required field</small>
            </v-card-text>
 </v-card>

 <v-card v-if="tipoPregunta==='Abierta'">
            <v-card-text>
            <v-container grid-list-md>
                <v-layout wrap>
                <v-flex xs12>
                    <v-text-field
                    label="Escribe tu pregunta..."
                    required
                    v-model="pregunta"></v-text-field>
                </v-flex>
              <CrearVariable @clicked="guardoArreglo"></CrearVariable>
                </v-layout>
            </v-container>
            </v-card-text>

 </v-card>
 <v-card>
     <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="saveOpenQuestion(pregunta, topicId, tipoPregunta)" v-if="tipoPregunta==='Abierta'">Guardar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="saveTFQuestion(pregunta, topicId, tipoPregunta, respuestaVoF)" v-if="tipoPregunta==='Verdadero o Falso'">Guardar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="saveOMQuestion(pregunta, topicId, tipoPregunta, respuestaOM, dummyAnswers)" v-if="tipoPregunta==='Opcion Multiple'">Guardar</v-btn>
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
    topicId: {
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
    },
    saveTFQuestion (pregunta, topicId, tipoPregunta, respuestaVoF) {
      let payload = [pregunta, topicId, tipoPregunta, respuestaVoF, this.variables]
      this.$store.dispatch('addTFQuestion', payload)
        .then((response) => {
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error saveTFQuestion')
          console.log(error)
        })
    },
    saveOMQuestion (pregunta, topicId, tipoPregunta, respuestaOM, dummyAnswers) {
      let payload = [pregunta, topicId, tipoPregunta, respuestaOM, dummyAnswers, this.variables]
      this.$store.dispatch('addOMQuestion', payload)
        .then((response) => {
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error saveOMQuestion')
          console.log(error)
        })
    },
    addDummyAnswer (questionId) {
      this.dummyAnswers.push(this.dummyAnswer)
      let payload = [this.dummyAnswer, questionId]
      console.log(payload)
    },
    deleteDummyAnswer (questionId) {
      this.dummyAnswers.splice(this.dummyAnswer, 1)
    },
    guardoArreglo (value) {
      this.variables = this.variables.concat(value)
      // console.log('Guardo Arreglo')
      // console.log(this.variables)
    }
  }
}
</script>
