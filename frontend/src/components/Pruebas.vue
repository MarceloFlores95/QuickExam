<template>
  <v-card
    color="gray lighten-4"
    flat
    height="500px"
  >
<!---Titulo-->
    <v-toolbar color="indigo darken-4" dark>
    <v-card-text>
        <v-toolbar-title>Quick Exam</v-toolbar-title>
    </v-card-text>
    </v-toolbar>

<!---Espacio-->
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>

<!---Boton-->
<v-layout align-center justify-space-around row>
    <v-flex>
      <div>
        <v-btn large>Reactivos</v-btn>
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
      width="500"
    >
      <v-btn
        slot="activator"
        color="red lighten-2"
        dark
      >
        Click Me
      </v-btn>

      <v-card>
        <v-card-title
          class="headline grey lighten-2"
          primary-title
        >
          Privacy Policy
        </v-card-title>

        <v-card-text>
          Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in culpa qui officia deserunt mollit anim id est laborum.
        </v-card-text>

        <v-divider></v-divider>

        <v-card-actions>
          <v-spacer></v-spacer>
          <v-btn
            color="primary"
            flat
            @click="dialog = false"
          >
            I accept
          </v-btn>
        </v-card-actions>
      </v-card>
    </v-dialog>
  </div>
 <v-btn fab dark small color="indigo">
      <v-icon dark>add</v-icon>
   </v-btn>
<!---Texto-
 <v-window v-model="step">
          <v-text-field
            label="Escribe el encabezado"
          ></v-text-field>
</v-window>
!-->

<!--Imagen-
 <v-layout align-center justify-space-around row>
   <v-spacer></v-spacer>
    <v-flex>
     <v-card>
         <v-container>
            <v-flex
              v-for="n in 1"
              :key="n"
              xs4
              d-flex
            >
                <v-img
                  :src="`https://picsum.photos/500/300?image=${n * 1}`"
                  aspect-ratio="1"
                  class="grey lighten-2"
                >
                </v-img>
            </v-flex>
        </v-container>
      </v-card>
    </v-flex>
    <v-flex>
     <v-card>
         <v-container>
          <v-layout row wrap>
            <v-flex
              v-for="n in 1"
              :key="n"
              xs4
              d-flex
            >
              <v-card flat tile class="d-flex">
                <v-img
                  :src="`https://picsum.photos/500/300?image=${n * 1}`"
                  aspect-ratio="1"
                  class="grey lighten-2"
                >
                </v-img>
              </v-card>
            </v-flex>
          </v-layout>
        </v-container>
      </v-card>
    </v-flex>
  </v-layout>
  !-->
<!---Espacio-->
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>

<!--Menu con scrollabe-->
  <div
    class="hide-overflow"
    style="position: relative;"
  >
    <v-toolbar
      absolute
      color="indigo darken-4" dark
      scroll-off-screen
      scroll-target="#scrolling-techniques"
    >

      <v-toolbar-title>To cola guardada</v-toolbar-title>

      <v-spacer></v-spacer>

      <v-btn icon>
        <v-icon>search</v-icon>
      </v-btn>

      <v-btn icon>
        <v-icon>favorite</v-icon>
      </v-btn>
    </v-toolbar>
    <div
      id="scrolling-techniques"
      class="scroll-y"
      style="max-height: 300px;"
    >
      <v-container style="height: 500px;"></v-container>
    </div>
  </div>
<!---Espacio-->
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>
<!---Espacio-->
 <v-container grid-list-md text-xs-center>
   <v-flex v-for="i in 1" :key="`1${i}`" xs1>
    </v-flex>
</v-container>
<!--ToolBar-->
 <v-toolbar color="indigo darken-4" dark>
    </v-toolbar>
</v-card>
</template>

<script>
export default {
  data: () => ({
  })
}
</script>
