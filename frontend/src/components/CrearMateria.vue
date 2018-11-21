<template>
    <v-dialog v-model="dialog" persistent max-width="600px">
        <v-btn flat icon slot="activator">
            <v-icon>add_box</v-icon>
        </v-btn>
        <v-card>
        <v-card-title class="headline">Añade una nueva materia</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="materia"
                label="Nueva materia"
            ></v-text-field>
            </v-flex>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="saveSubject(materia)" >Guardar</v-btn>
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
  methods: {
    saveSubject: function (payload) {
      // console.log(payload)
      this.$store.dispatch('addSubject', payload)
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
  }
}
</script>
