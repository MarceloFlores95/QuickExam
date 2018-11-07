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

<!---Espacio-->
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>

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
        <v-textarea
        auto-grow
          solo
          name="input-7-4"
          label="Escribe el encabezado"
          value=""
        ></v-textarea>
       </v-container>

  <v-container id="dropdown-example" grid-list-xl>
    <v-layout row wrap>
      <v-flex xs12 sm4>
        <p>Materia</p>
        <v-overflow-btn
          :items="Materia"
          label="Materia"
          target="#dropdown-example"
          editable
          item-value='text'
        ></v-overflow-btn>
      </v-flex>

      <v-flex xs12 sm4>
        <p>Temas</p>
        <v-overflow-btn
          :items="Temas"
          label="Temas"
          target="#dropdown-example"
          editable
          item-value = 'text'
        ></v-overflow-btn>
      </v-flex>

      <v-flex xs12 sm4>
        <p>Cantidad</p>
        <v-overflow-btn
          :items="Cantidad"
          label="Cantidad"
          target="#dropdown-example"
          editable
          item-value="text"
        ></v-overflow-btn>
      </v-flex>
    </v-layout>
  </v-container>

        <v-divider></v-divider>

           <v-card-actions>
              <v-spacer></v-spacer>
              <v-btn flat color="primary" @click="dialog = false">caca</v-btn>
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
    dialog: false,
    Materia: ['Quimica', 'Español', 'Historia'],
    Temas: ['TuPu', 'Queti', 'Chupala'],
    Cantidad: ['MiPito']
  })
}
</script>
