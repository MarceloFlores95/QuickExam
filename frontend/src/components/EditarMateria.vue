<template>
    <v-dialog v-model="dialog" persistent max-width="600px">
        <v-btn flat icon slot="activator">
            <v-icon>edit</v-icon>
        </v-btn>
        <v-card>
          <div v-if="subjectId === undefined">{{subjectId}}</div>
        <v-card-title class="headline">Edita la materia</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="materia"
                :label=filteredSubject
            ></v-text-field>
            </v-flex>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editSubject(subjectId, materia)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      materia: undefined
    }
  },
  props: {
    subjectId: {
      required: true
    }
  },
  methods: {
    editSubject: function (subjectId, materia) {
      let payload = [subjectId, materia]
      // console.log(payload)
      this.$store.dispatch('editSubject', payload)
        .then((response) => {
          // console.log(this.$store.state.subject)
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    }
  },
  computed: {
    filteredSubject () {
      var currentSubject = this.$store.getters.subjectList
      currentSubject = currentSubject.filter((current) => {
        return current.subject_id === this.subjectId
      })
      return currentSubject[0].name
    }
  }
}
</script>
