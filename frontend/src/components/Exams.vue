<template>
  <v-card
    color="gray lighten-4"
    flat
    height="500px"
  >
<!---Espacio-->
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>

<!---Boton-->
<v-layout align-center justify-space-around row>
    <v-flex>
      <div>
        <v-btn large router-link to= "/Reactivos">Reactivos</v-btn>
      </div>
    </v-flex>
    <v-flex >
      <div>
        <v-btn large color ="blue darken-4" dark>Exámenes</v-btn>
      </div>
    </v-flex>
</v-layout>

<!---Espacio
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>-->

<!---Test-->
<v-flex xs12 d-flex align-content-center>
  <v-card flat>
    <v-select
      :items="Test"
      item-text="name"
      item-value="test_id"
      single-line auto
      label="Test"
      v-model="selectedTest"
    ></v-select>
  </v-card>
</v-flex>

<v-flex xs12 d-flex>
  <v-card v-if="selectedTest!==undefined" flat>
    <v-btn @click="convertPDF(selectedTest)">Convertir a PDF</v-btn>
  </v-card>
</v-flex>

<v-flex xs12 d-flex>
  <v-card v-if="selectedTest!==undefined" flat>
    <v-btn @click="deletePDF(selectedTest)">Borrar examen</v-btn>
  </v-card>
</v-flex>

<!--Boton de mas-->
<div class="text-xs-center">
     <v-dialog
      v-model="dialog"
      width="600"
      height="200"
    >
      <v-btn fab dark small color="blue-grey darken-2"
        slot="activator" >
         <v-icon dark>add</v-icon>
      </v-btn>
      <!--cosa para que slga scroll up-->
      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          Crear Examen
        </v-card-title>
       <v-container fluid grid list -md>
         <v-text-field
            :value="name"
            label="Nombre de test"
            solo
            v-model="name"
          ></v-text-field>
        <v-textarea
        auto-grow
          solo
          name="input-7-4"
          label="Escribe el encabezado"
          value="header"
          v-model="header"
        ></v-textarea>
       </v-container>

  <v-container id="dropdown-example" grid-list-xl>
    <v-layout row wrap>
      <v-flex xs12 sm4>
        <p>Materia</p>
       <v-select
          :items="Materias"
          item-text="name"
          item-value="subject_id"
          single-line auto
          label="Materias"
          v-model="selectedSubject"
        ></v-select>
      </v-flex>

      <v-flex xs12 sm4>
        <p>Temas</p>
        <v-select
          :items="Temas"
          item-text="name"
          item-value="topic_id"
          single-line auto
          label="Temas"
          v-model="selectedTopic"
        ></v-select>
      </v-flex>

      <v-flex xs12 sm4>
        <p>Cantidad de preguntas</p>
        <v-overflow-btn
          :items="cantidad"
          label="Cantidad"
          target="#dropdown-example"
          item-value="text"
          v-model="cantidadSeleccionada"
        ></v-overflow-btn>

        <v-flex xs12 sm12>
        <p>Tipos de examen</p>
        <v-overflow-btn
          :items="cantidad"
          label="Cantidad"
          target="#dropdown-example"
          item-value="text"
          v-model="tipos"
        ></v-overflow-btn>
        </v-flex >

        <v-btn @click="addTopicQuestion(selectedTopic, cantidadSeleccionada)">Agregar topico</v-btn>
        <v-btn @click="deleteTopicQuestion">Borrar topico</v-btn>

      </v-flex>
    </v-layout>
  </v-container>

        <v-divider></v-divider>

           <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn flat color="primary" @click="dialog = false">Cancelar</v-btn>
              <v-btn flat color="primary" @click="addTest(name, header, tipos)">Aceptar</v-btn>
            </v-card-actions>

      </v-card>
    </v-dialog>
  </div>
<!---Espacio-->
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>

<!--Menu con scrollabe-->

</v-card>
</template>

<script>
export default {
  data: () => ({
    userToken: undefined,
    // Materias: [ ],
    // Temas: [ ],
    Reactivos: ['Que onda?'],
    selectedSubject: [],
    selectedTopic: [],
    selectedQuestion: [],
    readOnly: true,
    dialog: false,
    cantidad: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10'],
    arrayTopicQuestions: [],
    variableTopicQuestions: undefined,
    cantidadSeleccionada: undefined,
    tipos: undefined,
    selectedTest: undefined
  }),
  methods: {
    refreshTopicList: function () {
      this.$store.dispatch('changeTopicList', this.selectedSubject)
        .then(() => {
          // this.Temas = this.$store.getters.topicList
        }).catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    addTest: function (name, header, tipos) {
      let payload = [ name, header, tipos, this.arrayTopicQuestions ]
      // console.log(payload)
      this.$store.dispatch('addtest', payload)
        .then((response) => {
          //
          this.dialog = false
          this.arrayTopicQuestions = []
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    addTopicQuestion (selectedTopic, cantidadSeleccionada) {
      let ArrayTopic = [selectedTopic, cantidadSeleccionada]
      this.arrayTopicQuestions.push(ArrayTopic)
      ArrayTopic = []
      console.log(this.arrayTopicQuestions)
      console.log(this.ArrayTopic)
    },
    deleteTopicQuestion (questionId) {
      this.arrayTopicQuestions.splice(this.variableTopicQuestions, 1)
    },
    convertPDF (selectedTest) {
      console.log(selectedTest)
      this.$store.dispatch('convertPDF', selectedTest)
        .then((response) => {
          //
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    },
    deletePDF (selectedTest) {
      this.$store.dispatch('deletePDF', selectedTest)
        .then((response) => {
          //
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    }
  },
  created () {
    this.userToken = this.$store.getters.userToken
  },
  mounted () {
    this.userToken = this.$store.getters.userToken
    this.Temas = this.$store.getters.topicList
    this.refreshTopicList()
  },
  computed: {
    Materias () {
      return this.$store.getters.subjectList
    },
    Temas () {
      return this.$store.getters.topicList
    },
    Test () {
      return this.$store.getters.testList
    },
    Test2 () {
      return this.$store.getters.testList
    },
    Preguntas () {
      if (this.selectedTopic !== undefined) {
        return this.$store.getters.questionList
      } else {
        return 0
      }
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
