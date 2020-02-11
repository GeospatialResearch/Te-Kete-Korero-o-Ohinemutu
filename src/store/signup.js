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
  }
}
