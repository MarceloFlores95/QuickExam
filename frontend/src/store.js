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
      password: undefined,
      userToken: undefined,
      session: false
    },
    subject: [],
    subjectList: {
    },
    topic: [],
    topicList: '',
    questionList: {
    }
  },
  getters: {
    userUsername: state => {
      return state.user.username
    },
    userToken: state => {
      return state.user.userToken
    },
    userPassword: state => {
      return state.user.password
    },
    activeSession: state => {
      return state.user.session
    },
    subject: state => {
      return state.subject
    },
    subjectList: state => {
      return state.subjectList
    },
    topic: state => {
      return state.topic
    },
    topicList: state => {
      return state.topicList
    },
    questionList: state => {
      return state.questionList
    }
  },
  mutations: {
    increment (state) {
      state.count++
    },
    saveToken (state, payload) {
      state.user.userToken = payload
    },
    saveUsername (state, payload) {
      state.user.username = payload
    },
    savePassword (state, payload) {
      state.user.password = payload
    },
    changeSession (state, payload) {
      state.user.session = true
    },
    saveSubject (state, payload) {
      state.subject = payload
    },
    changeSubjectList (state, payload) {
      // console.log('Muestro payload changeSubjectList')
      // console.log(payload)
      Vue.set(state, 'subjectList', payload)
      // state.subjectList = payload
    },
    saveTopic (state, payload) {
      state.topic = payload
    },
    changeTopicList (state, payload) {
      Vue.set(state, 'topicList', payload)
    },
    changeQuestionList (state, payload) {
      Vue.set(state.questionList, 'OpenQuestion', payload)
    },
    changeTFQuestionList (state, payload) {
      Vue.set(state.questionList, 'TFQuestion', payload)
    }
  },
  actions: {
    userRegister: (context, payload) => {
      return new Promise((resolve, reject) => {
        UserApi.post('/api/register', {
          username: payload.username,
          password: payload.password
        })
          .then((response) => {
            // console.log('Entro')
            // console.log(response)
            context.commit('saveToken', response.data.token)
            context.commit('saveUsername', payload.username)
            context.commit('savePassword', payload.password)
            context.commit('changeSession', true)
            resolve()
          }).catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    },
    userLogin: (context, payload) => {
      return new Promise((resolve, reject) => {
        UserApi.post('/api/login', {
          username: payload.username,
          password: payload.password
        })
          .then((response) => {
            // console.log('Entro')
            // console.log(response)
            context.commit('saveToken', response.data.token)
            context.commit('saveUsername', payload.username)
            context.commit('savePassword', payload.password)
            context.commit('changeSession', true)
            resolve()
          }).catch((error) => {
            reject(error)
          })
      })
    },
    addSubject: (context, payload) => {
      return new Promise((resolve, reject) => {
        UserApi.post('/api/subject', {
          name: payload
        }, {headers: {
          'X-API-KEY': context.getters.userToken
        }})
          .then((response) => {
            UserApi.get('/api/subject', {headers: {
              'X-API-KEY': context.getters.userToken
            }})
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeSubjectList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de add')
            console.log(error)
            // reject(error)
          })
      })
    },
    changeSubjectList: (context, payload) => {
      return new Promise((resolve, reject) => {
        UserApi.get('/api/subject', {headers: {
          'X-API-KEY': context.getters.userToken
        }})
          .then((response) => {
            // console.log('Response de changesubject')
            // console.log(response)
            context.commit('changeSubjectList', response.data)
            resolve()
          }).catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    },
    editSubject: (context, payload) => {
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/update/subject', {
          name: payload[1]
        }, {
          headers: {'X-API-KEY': context.getters.userToken
          },
          params: {
            subject_id: payload[0]
          }
        })
          .then((response) => {
            UserApi.get('/api/subject', {headers: {
              'X-API-KEY': context.getters.userToken
            }})
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeSubjectList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de edit')
            console.log(error)
          })
      })
    },
    deleteSubject: (context, payload) => {
      // console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/delete/subject',
          {subject_id: payload}, {
            headers: {'X-API-KEY': context.getters.userToken
            }
          })
          .then((response) => {
            UserApi.get('/api/subject', {headers: {
              'X-API-KEY': context.getters.userToken
            }})
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeSubjectList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de edit')
            console.log(error)
          })
      })
    },
    addTopic: (context, payload) => {
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/topic', {
          name: payload[0],
          subject_id: payload[1]
        }, {headers: {
          'X-API-KEY': context.getters.userToken
        }})
          .then((response) => {
            UserApi.get('/api/topic', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {subject_id: payload[1]}
            })
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeTopicList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de add')
            console.log(error)
          })
      })
    },
    changeTopicList: (context, payload) => {
      // console.log('changes')
      // console.log(context.getters.userToken)
      return new Promise((resolve, reject) => {
        UserApi.get('/api/topic', {
          headers: {'X-API-KEY': context.getters.userToken
          },
          params: {subject_id: payload}
        })
          .then((response) => {
            console.log('Response de changetopics')
            console.log(response)
            context.commit('changeTopicList', response.data)
            resolve()
          }).catch((error) => {
            console.log('Error de ChangeTopicList')
            console.log(error)
          })
      })
    },
    editTopic: (context, payload) => {
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('api/update/topic', {
          name: payload[1]
        }, {
          headers: {'X-API-KEY': context.getters.userToken
          },
          params: {
            topic_id: payload[0]
          }
        })
          .then((response) => {
            UserApi.get('/api/topic', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {subject_id: payload[2]}
            })
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeTopicList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de edit')
            console.log(error)
          })
      })
    },
    deleteTopic: (context, payload) => {
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/delete/topic',
          {topic_id: payload[1]}, {
            headers: {'X-API-KEY': context.getters.userToken
            }
          })
          .then((response) => {
            UserApi.get('api/topic', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {subject_id: payload[0]}
            })
              .then((response) => {
                console.log('Response de changetopics')
                console.log(response)
                context.commit('changeTopicList', response.data)
                resolve()
              }).catch((error) => {
                console.log('Error')
                console.log(error)
              })
          })
          .catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    },
    addQuestion: (context, payload) => {
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/question/open', {
          text: payload[0]
        }, {
          headers: { 'X-API-KEY': context.getters.userToken
          },
          params: {
            topic_id: payload[1]
          }
        })
          .then((response) => {
            UserApi.get('/api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[1]}
            })
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de AddQuestion')
            console.log(error)
          })
      })
    },
    changeQuestionList: (context, payload) => {
      console.log('changeQuestion')
      return new Promise((resolve, reject) => {
        UserApi.get('api/question', {
          headers: {'X-API-KEY': context.getters.userToken
          },
          params: {topic_id: payload}
        })
          .then((response) => {
            console.log('Response de changeQuestion')
            console.log(response)
            context.commit('changeQuestionList', response.data)
            resolve()
          }).catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    },
    editOpenQuestion: (context, payload) => {
      console.log('editOpenQuestion')
      return new Promise((resolve, reject) => {
        UserApi.post('/api/update/question/open', {
          text: payload[1]
        }, {
          headers: {'X-API-KEY': context.getters.userToken
          },
          params: {
            question_open_id: payload[0]
          }
        })
          .then((response) => {
            UserApi.get('/api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[2]}
            })
              .then((response) => {
                console.log('Response de changeQuestion')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve()
              }).catch((error) => {
                console.log('Error')
                console.log(error)
              })
          })
      })
    },
    deleteQuestion: (context, payload) => {
      console.log('deleteQuestion')
      return new Promise((resolve, reject) => {
        UserApi.post('/api/delete/question/open',
          {question_open_id: payload[0]}, {
            headers: {'X-API-KEY': context.getters.userToken
            }
          })
          .then((response) => {
            UserApi.get('api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[1]}
            })
              .then((response) => {
                console.log('Response de changeQuestionList')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve()
              }).catch((error) => {
                console.log('Error')
                console.log(error)
              })
          })
          .catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    },
    addTFQuestion: (context, payload) => {
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/question/tf', {
          text: payload[0],
          expression: payload[3]
        }, {
          headers: { 'X-API-KEY': context.getters.userToken
          },
          params: {
            topic_id: payload[1]
          }
        })
          .then((response) => {
            UserApi.get('/api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[1]}
            })
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de AddTFQuestion')
            console.log(error)
          })
      })
    },
    deleteQuestionTF: (context, payload) => {
      console.log('deleteQuestionTF')
      return new Promise((resolve, reject) => {
        UserApi.post('/api/delete/question/tf',
          {question_tf_id: payload[0]}, {
            headers: {'X-API-KEY': context.getters.userToken
            }
          })
          .then((response) => {
            console.log('Get question')
            UserApi.get('api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[1]}
            })
              .then((response) => {
                console.log('Response de changeQuestionList')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve()
              }).catch((error) => {
                console.log('Error')
                console.log(error)
              })
          })
          .catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    },
    editTFQuestion: (context, payload) => {
      console.log('editTFQuestion')
      return new Promise((resolve, reject) => {
        UserApi.post('/api/update/question/tf', {
          text: payload[1],
          expression: payload[3]
        }, {
          headers: {'X-API-KEY': context.getters.userToken
          },
          params: {
            question_tf_id: payload[0]
          }
        })
          .then((response) => {
            UserApi.get('/api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[2]}
            })
              .then((response) => {
                console.log('Response de changeQuestion')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve()
              }).catch((error) => {
                console.log('Error')
                console.log(error)
              })
          })
      })
    },
    addOMQuestion: (context, payload) => {
      console.log(payload)
      return new Promise((resolve, reject) => {
        UserApi.post('/api/question/multi', {
          text: payload[0],
          correct_answer: payload[3]
        }, {
          headers: { 'X-API-KEY': context.getters.userToken
          },
          params: {
            topic_id: payload[1]
          }
        })
          .then((response) => {
            UserApi.get('/api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[1]}
            })
              .then((response) => {
                console.log('Response despues del get')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve(response)
              })
              .catch((error) => {
                console.log('Error de commit')
                console.log(error)
              })
          }).catch((error) => {
            console.log('Error de AddOmQuestion')
            console.log(error)
          })
      })
    },
    editOMQuestion: (context, payload) => {
      console.log('editOMQuestion')
      return new Promise((resolve, reject) => {
        UserApi.post('/api/update/question/multi', {
          text: payload[1],
          correct_answer: payload[3]
        }, {
          headers: {'X-API-KEY': context.getters.userToken
          },
          params: {
            question_multi_id: payload[0]
          }
        })
          .then((response) => {
            UserApi.get('/api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[2]}
            })
              .then((response) => {
                console.log('Response de changeQuestion')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve()
              }).catch((error) => {
                console.log('Error')
                console.log(error)
              })
          })
      })
    },
    deleteQuestionOM: (context, payload) => {
      console.log('deleteQuestionOM')
      return new Promise((resolve, reject) => {
        UserApi.post('/api/delete/question/multi',
          {question_multi_id: payload[0]}, {
            headers: {'X-API-KEY': context.getters.userToken
            }
          })
          .then((response) => {
            console.log('Get question')
            UserApi.get('api/question', {
              headers: {'X-API-KEY': context.getters.userToken
              },
              params: {topic_id: payload[1]}
            })
              .then((response) => {
                console.log('Response de changeQuestionList')
                console.log(response)
                context.commit('changeQuestionList', response.data)
                resolve()
              }).catch((error) => {
                console.log('Error')
                console.log(error)
              })
          })
          .catch((error) => {
            console.log('Error')
            console.log(error)
          })
      })
    }
  }
})
