<template>
    <v-dialog v-model="dialog" persistent max-width="600px">
        <v-btn flat slot="activator">
            Agregar variable
        </v-btn>
        <v-card>
        <v-card-title class="headline">Añade una nueva variable</v-card-title>
        <v-flex xs12 sm6>
            <v-text-field
                v-model="value"
                label="Valor"
            ></v-text-field>
            <v-text-field
                v-model="symbol"
                label="Simbolo"
            ></v-text-field>
            <v-overflow-btn
              :items="tipos"
              label="Tipos"
              segmented
              target="#dropdown-example"
              v-model="tipo"
            ></v-overflow-btn>
        </v-flex>
        <v-card-actions>
            <v-spacer></v-spacer>
            <v-btn color="green darken-1" flat @click.native="dialog = false">Cancelar</v-btn>
            <v-btn color="green darken-1" flat v-on:click="saveVariable(value, symbol, tipo)" >Guardar</v-btn>
        </v-card-actions>
        </v-card>
    </v-dialog>
</template>

<script>
export default {
  data () {
    return {
      dialog: false,
      tema: undefined,
      value: undefined,
      symbol: undefined,
      tipo: undefined,
      tipos: [
        {id: 'int', text: 'int', callback: () => console.log('Integer')},
        {id: 'dec', text: 'dec', callback: () => console.log('Decimal')},
        {id: 'str', text: 'str', callback: () => console.log('String')}
      ],
      variable: undefined,
      arrayVariable: []
    }
  },
  props: {
    questionOpenId: {
      required: true
    },
    reset: {
      required: true
    }
  },
  methods: {
    saveVariable: function (value, symbol, tipo) {
      this.variable = [value, symbol, tipo]
      this.arrayVariable.push(this.variable)
      this.dialog = false
      this.$emit('clicked', this.arrayVariable)
      this.arrayVariable = []
    }
  }
}
</script>
