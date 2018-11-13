<template>
    <v-dialog v-model="dialog" persistent max-width="300">
        <v-btn flat icon slot="activator">
            <v-icon>edit</v-icon>
        </v-btn>
        <v-card>
        <v-card-title class="headline">Edita el tema {{topicId}}</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="tema"
                label="Nuevo tema"
            ></v-text-field>
            </v-flex>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="editTopic(topicId, tema, subjectId)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      tema: undefined
    }
  },
  props: {
    topicId: {
      required: true
    },
    subjectId: {
      required: true
    }
  },
  methods: {
    editTopic: function (topicId, tema, subjectId) {
      let payload = [topicId, tema, subjectId]
      console.log(payload)
      this.$store.dispatch('editTopic', payload)
        .then((response) => {
          // console.log(this.$store.state.subject)
          this.dialog = false
        })
        .catch((error) => {
          console.log('Error')
          console.log(error)
        })
    }
  }
}
</script>
