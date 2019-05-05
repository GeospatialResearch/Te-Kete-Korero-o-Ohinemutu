// src/store/api.js

import Vue from 'vue'
import VueResource from 'vue-resource'

Vue.use(VueResource)

export default {
  get (url, request, options) {
    return Vue.http.get(url, request, options)
      .then((response) => Promise.resolve(response))
      .catch((error) => Promise.reject(error))
  },
  post (url, request, options) {
    return Vue.http.post(url, request, options)
      .then((response) => Promise.resolve(response))
      .catch((error) => Promise.reject(error))
  },
  patch (url, request, options) {
    return Vue.http.patch(url, request, options)
      .then((response) => Promise.resolve(response))
      .catch((error) => Promise.reject(error))
  },
  put (url, request, options) {
    return Vue.http.put(url, request, options)
      .then((response) => Promise.resolve(response))
      .catch((error) => Promise.reject(error))
  },
  delete (url, request, options) {
    return Vue.http.delete(url, request, options)
      .then((response) => Promise.resolve(response))
      .catch((error) => Promise.reject(error))
  }
}
