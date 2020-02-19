import api from './api.js'

export default {
  namespaced: true,
  state: {
    registrationCompleted: false,
    registrationError: false,
    registrationLoading: false,
    activationCompleted: false,
    activationError: false,
    activationLoading: false,
    emailCompleted: false,
    emailError: false,
    emailLoading: false,
    emailErrorReason: '',
    resetCompleted: false,
    resetError: false,
    resetLoading: false,
    resetErrorReason: ''
  },
  mutations: {
    REGISTRATION_BEGIN (state) {
      state.registrationLoading = true
    },
    REGISTRATION_SUCCESS (state) {
      state.registrationCompleted = true
      state.registrationError = false
      state.registrationLoading = false
    },
    REGISTRATION_FAILURE (state) {
      state.registrationError = true
      state.registrationLoading = false
    },
    REGISTRATION_CLEAR (state) {
      state.registrationCompleted = false
      state.registrationError = false
      state.registrationLoading = false
    },
    ACTIVATION_BEGIN (state) {
      state.activationLoading = true
    },
    ACTIVATION_CLEAR (state) {
      state.activationCompleted = false
      state.activationError = false
      state.activationLoading = false
    },
    ACTIVATION_FAILURE (state) {
      state.activationError = true
      state.activationLoading = false
    },
    ACTIVATION_SUCCESS (state) {
      state.activationCompleted = true
      state.activationError = false
      state.activationLoading = false
    },
    PASSWORD_EMAIL_BEGIN (state) {
      state.emailLoading = true
    },
    PASSWORD_EMAIL_CLEAR (state) {
      state.emailCompleted = false
      state.emailError = false
      state.emailLoading = false
    },
    PASSWORD_EMAIL_FAILURE (state, response) {
      state.emailError = true
      state.emailLoading = false
      state.emailErrorReason = response.body[Object.keys(response.body)[0]][0]
    },
    PASSWORD_EMAIL_SUCCESS (state) {
      state.emailCompleted = true
      state.emailError = false
      state.emailLoading = false
    },
    PASSWORD_RESET_BEGIN (state) {
      state.resetLoading = true
    },
    PASSWORD_RESET_CLEAR (state) {
      state.resetCompleted = false
      state.resetError = false
      state.resetLoading = false
    },
    PASSWORD_RESET_FAILURE (state, response) {
      state.resetError = true
      state.resetLoading = false
      state.resetErrorReason = response.body[Object.keys(response.body)[0]][0]
    },
    PASSWORD_RESET_SUCCESS (state) {
      state.resetCompleted = true
      state.resetError = false
      state.resetLoading = false
    }
  },
  actions: {
    createAccount (store, payload) {
      store.commit('REGISTRATION_BEGIN')
      return api.post(process.env.API_HOST + '/auth/registration/', payload)
        .then((response) => {
          store.commit('REGISTRATION_SUCCESS')
          return response
        })
        .catch((error) => {
          store.commit('REGISTRATION_FAILURE')
          return error
        })
    },
    clearRegistrationStatus (store) {
      store.commit('REGISTRATION_CLEAR')
    },
    activateAccount (store, key) {
      store.commit('ACTIVATION_BEGIN')
      return api.post(process.env.API_HOST + '/auth/registration/verify-email/', { key: key })
        .then(() => store.commit('ACTIVATION_SUCCESS'))
        .catch(() => store.commit('ACTIVATION_FAILURE'))
    },
    clearActivationStatus (store) {
      store.commit('ACTIVATION_CLEAR')
    },
    sendPasswordResetEmail (store, email) {
      store.commit('PASSWORD_EMAIL_BEGIN')
      return api.get(process.env.API_HOST + '/v1' + '/check_email/?email=' + email.email)
        .then((response) => {
          if (response.body.emailExists) {
            return api.post(process.env.API_HOST + '/auth/password/reset/', email)
              .then((response) => {
                if (!response.ok) {
                  store.commit('PASSWORD_EMAIL_FAILURE', response)
                } else {
                  store.commit('PASSWORD_EMAIL_SUCCESS')
                }
              })
              .catch((error) => {
                store.commit('PASSWORD_EMAIL_FAILURE', error)
              })
          } else {
            store.state.emailError = true
            store.state.emailLoading = false
            store.state.emailErrorReason = 'This email is not registered yet.'
          }
        })
        .catch((error) => { console.log(error) })
    },
    clearEmailStatus (store) {
      store.commit('PASSWORD_EMAIL_CLEAR')
    },
    resetPassword (store, inputs) {
      store.commit('PASSWORD_RESET_BEGIN')
      return api.post(process.env.API_HOST + '/auth/password/reset/confirm/', { uid: inputs.uid, token: inputs.token, new_password1: inputs.password1, new_password2: inputs.password2 })
        .then((response) => {
          if (!response.ok) {
            store.commit('PASSWORD_RESET_FAILURE', response)
          } else {
            store.commit('PASSWORD_RESET_SUCCESS')
          }
        })
        .catch((error) => {
          store.commit('PASSWORD_RESET_FAILURE', error)
        })
    },
    clearResetStatus (store) {
      store.commit('PASSWORD_RESET_CLEAR')
    }
  }
}
