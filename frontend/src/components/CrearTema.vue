<template>
    <v-dialog v-model="dialog" persistent max-width="600px">
        <v-btn flat icon slot="activator">
            <v-icon>add_box</v-icon>
        </v-btn>
        <v-card>
        <v-card-title class="headline">Añade un nuevo tema</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="tema"
                label="Nuevo tema"
            ></v-text-field>
        </v-flex>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="saveTopic(tema,subjectId)" >Guardar</v-btn>
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
    subjectId: {
      required: true
    }
  },
  methods: {
    saveTopic: function (tema, subject) {
      let payload = [tema, subject]
      this.$store.dispatch('addTopic', payload)
        .then((response) => {
          // console.log(this.$store.state.subject)
          // this.refreshTopicList()
          // this.$destroy()
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
