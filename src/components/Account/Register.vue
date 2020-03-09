<template>
  <div class="container h-100">
    <div class="d-flex justify-content-center h-100">
      <div class="user-card" :style="error ? 'height:500px': 'height:450px'">
        <div class="d-flex justify-content-center">
          <div class="brand-logo-container">
            <img src="static/img/weaveLogo.png" class="brand-logo" alt="Logo">
          </div>
        </div>
        <div v-if="registrationLoading" class="d-flex justify-content-center form-container">
          <p class="text-center">
            loading...
          </p>
        </div>
        <div v-else-if="!registrationCompleted">
          <div class="d-flex justify-content-center form-container">
            <form id="signupForm">
              <div v-if="error" class="alert alert-danger text-center">
                <span>{{ error }}</span>
              </div>
              <div class="input-group mb-2">
                <div class="input-group-append">
                  <span class="input-group-text">
                    <i><font-awesome-icon icon="user" /></i>
                  </span>
                </div>
                <input v-model="inputs.username" value="" type="text" name="" class="form-control input_user" placeholder="Enter username" required @keyup.enter="createAccount()">
              </div>
              <div class="input-group mb-2">
                <div class="input-group-append">
                  <span class="input-group-text">
                    <i><font-awesome-icon icon="at" /></i>
                  </span>
                </div>
                <input v-model="inputs.email" value="" type="text" name="" class="form-control input_user" placeholder="Enter email" required @keyup.enter="createAccount()">
              </div>
              <div class="input-group mb-2">
                <div class="input-group-append">
                  <span class="input-group-text">
                    <i><font-awesome-icon icon="key" /></i>
                  </span>
                </div>
                <input v-model="inputs.password1" value="" type="password" name="" class="form-control input_pass" placeholder="Enter password" required @keyup.enter="createAccount()">
              </div>
              <div class="input-group mb-4">
                <div class="input-group-append">
                  <span class="input-group-text">
                    <i><font-awesome-icon icon="key" /></i>
                  </span>
                </div>
                <input v-model="inputs.password2" value="" type="password" name="" class="form-control input_pass" placeholder="Confirm password" required @keyup.enter="createAccount()">
              </div>
              <div class="d-flex justify-content-center login-container">
                <button type="button" name="button" class="btn login-btn" @click="createAccount()">
                  Create account
                </button>
              </div>
            </form>
          </div>
          <div class="mt-3">
            <div class="d-flex justify-content-center links">
              Already have an account? <a href="#" class="ml-2" @click="showLoginForm()">Login</a>
            </div>
            <div class="d-flex justify-content-center links">
              <a href="#">Forgot your password?</a>
            </div>
          </div>
        </div>
        <div v-else class="d-flex justify-content-center form-container">
          <div>
            <h4 class="text-center mb-4">
              Registration complete.
            </h4>
            <p class="text-center">
              You should receive an email shortly with instructions on how to
              activate your account.
            </p>
            <p class="text-center">
              If you do not receive the confirmation message within a few minutes of signing up, please check your Spam folder.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { EventBus } from 'store/event-bus'
import { mapState } from 'vuex'

export default {
  data() {
    return {
      inputs: {
        username: '',
        email: '',
        password1: '',
        password2: '',
      },
      error: ''
    }
  },
  computed: mapState('signup', [
    'registrationCompleted',
    'registrationError',
    'registrationLoading',
  ]),
  beforeDestroy() {
    this.$store.dispatch('signup/clearRegistrationStatus')
    var signupform = document.getElementById("signupForm")
    if (signupform) {
      signupform.classList.remove("was-validated")
    }
  },
  methods: {
    showLoginForm () {
      EventBus.$emit('showLoginForm')
    },
    createAccount () {
      var signupform = document.getElementById("signupForm")

      if (signupform.checkValidity()) {

        this.$store.dispatch('signup/createAccount', this.inputs)
        .then((response) => {
          if (!response.ok) {
            this.error = response.body[Object.keys(response.body)[0]][0]
          }
        })
        .catch((error) => {
          this.error = error.body[Object.keys(error.body)[0]][0]
        })
      } else {
        signupform.classList.add("was-validated")
      }
    }
  }
}
</script>
