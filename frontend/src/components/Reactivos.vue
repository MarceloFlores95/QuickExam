<template>
  <v-card>

 <v-container grid-list-md text-xs-center>
    <v-layout row wrap>

      <v-flex xs2>
        <v-card>
          <v-card-text class="px-0">Materia</v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs7 d-flex>
        <v-card>
          <v-select
          :items="Materias"
          label="Materias"
        ></v-select>
        </v-card>
      </v-flex>

      <v-flex xs3>
        <v-card>
            <v-btn flat icon>
                <v-icon>add_box</v-icon>
            </v-btn>
            <v-btn flat icon>
                <v-icon >edit</v-icon>
            </v-btn>
            <v-btn flat icon>
                <v-icon >delete</v-icon>
            </v-btn>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>

  <v-container grid-list-md text-xs-center>
    <v-layout row wrap>

      <v-flex xs2>
        <v-card>
          <v-card-text class="px-0">Temas</v-card-text>
        </v-card>
      </v-flex>

      <v-flex xs7 d-flex>
        <v-card>
          <v-select
          :items="Temas"
          label="Temas"
        ></v-select>
        </v-card>
      </v-flex>

      <v-flex xs3>
        <v-card>
            <v-btn flat icon>
                <v-icon>add_box</v-icon>
            </v-btn>
            <v-btn flat icon>
                <v-icon >edit</v-icon>
            </v-btn>
            <v-btn flat icon>
                <v-icon >delete</v-icon>
            </v-btn>
        </v-card>
      </v-flex>

    </v-layout>
  </v-container>

  <v-container grid-list-md text-xs-center>
      <v-layout row wrap>
      <v-flex xs12>
        <v-card>
          <v-card-text class="px-0">Preguntas</v-card-text>
        </v-card>
      </v-flex>
<!--Elaboracion de preguntas-->
      <v-flex xs2>
        <v-card>
          <v-dialog v-model="dialog" persistent max-width="600px">
            <v-btn slot="activator" color="black" dark flat icon>
              <v-icon>add_box</v-icon>
            </v-btn>
            <v-card>
              <v-card-title>
                <span class="headline">Reactivo</span>
              </v-card-title>
              <v-card-text>
                <v-container grid-list-md>
                  <v-layout wrap>
                    <v-flex xs12>
                      <v-text-field label="Escribte tu pregunta..." required></v-text-field>
                    </v-flex>
                  </v-layout>
                </v-container>
                <small>*indicates required field</small>
              </v-card-text>
              <v-card-actions>
                <v-spacer></v-spacer>
                <v-btn color="blue darken-1" flat @click.native="dialog = false">Close</v-btn>
                <v-btn color="blue darken-1" flat @click.native="dialog = false">Save</v-btn>
              </v-card-actions>
            </v-card>
          </v-dialog>
        </v-card>
      </v-flex>

      <v-flex xs7 d-flex >
        <v-card>
          <v-text-field
            label="Quieres ver mi nepe?"
            single-line
            solo
            readonly
          ></v-text-field>
        </v-card>
      </v-flex>

      <v-flex xs3>
        <v-card>
            <v-btn flat icon>
                <v-icon >edit</v-icon>
            </v-btn>
            <v-btn flat icon>
                <v-icon >delete</v-icon>
            </v-btn>
        </v-card>
      </v-flex>
<!---->
       </v-layout>
  </v-container>
<!---->
  </v-card>
</template>

<script>
export default {
  data: () => ({
    dialog: false,
    Materias: ['Quimica', 'Español', 'Historia', 'Inglés'],
    Temas: ['Hentai', 'Grammar', 'Historia Mundial'],
    Reactivos: ['Que pedo morra?']
  })
}
</script>
