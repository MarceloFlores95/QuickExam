import Vue from 'vue'
import Vuex from 'vuex'
import axios from 'axios'

Vue.use(Vuex)

const userServiceURL = 'http://localhost:5000'
const UserApi = axios.create({
  baseURL: userServiceURL,
  timeout: 5000,
  headers: {'Content-Type': 'application/json'}
})

export const store = new Vuex.Store({
  state: {
    count: 0,
    user: {
      username: undefined,
      password: undefined
    }
  },
  getters: {
    userUsername: state => {
      return state.user.username
    }
  },
  mutations: {
    increment (state) {
      state.count++
    }
  },
  actions: {
    userRegister: (context, payload) => {
      console.log('Payload')
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/register', {
          username: payload.username,
          password: payload.password
        })
          .then((response) => {
            console.log('Espero que jale')
            console.log(response)
            resolve()
          }).catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    }
  }
})
