<template>
  <div class="container h-100">
    <div class="d-flex justify-content-center h-100">
      <div class="user-card" :style="error ? 'height:450px': 'height:400px'">
        <div class="d-flex justify-content-center">
          <div class="brand-logo-container">
            <img src="static/img/weaveLogo.png" class="brand-logo" alt="Logo">
          </div>
        </div>
        <div class="d-flex justify-content-center form-container">
          <form id="loginForm">
            <div v-if="error" class="alert alert-danger text-center">
              <span>{{ error }}</span>
            </div>
            <div class="input-group mb-3">
              <div class="input-group-append">
                <span class="input-group-text">
                  <i><font-awesome-icon icon="user" /></i>
                </span>
              </div>
              <input v-model="credentials.email" value="" type="text" name="" class="form-control input_user" placeholder="Enter your email" required @keyup.enter="submit()">
            </div>
            <div class="input-group mb-2">
              <div class="input-group-append">
                <span class="input-group-text">
                  <i><font-awesome-icon icon="key" /></i>
                </span>
              </div>
              <input v-model="credentials.password" value="" type="password" name="" class="form-control input_pass" placeholder="Enter your password" required @keyup.enter="submit()">
            </div>
            <div class="form-group">
              <div class="custom-control custom-checkbox">
                <input id="customControlInline" type="checkbox" class="custom-control-input">
                <label class="custom-control-label" for="customControlInline">Remember me</label>
              </div>
            </div>
            <div class="d-flex justify-content-center mt-3 login-container">
              <button type="button" name="button" class="btn login-btn" @click="submit()">
                Login
              </button>
            </div>
          </form>
        </div>

        <div class="mt-4">
          <div class="d-flex justify-content-center links">
            Don't have an account? <a href="#" class="ml-2" @click="showSignupForm()">Sign Up</a>
          </div>
          <div class="d-flex justify-content-center links">
            <a href="#" @click="showResetPasswordForm()">Forgot your password?</a>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { EventBus } from 'store/event-bus'

export default {
  data () {
    return {
      credentials: {
        email: '',
        password: ''
      },
      error: ''
    }
  },
  mounted: function () {
    EventBus.$on('removeWasValidated', () => {
      var loginform = document.getElementById("loginForm")
      if (loginform) {
        loginform.classList.remove("was-validated")
        this.credentials.email = ''
        this.credentials.password = ''
        this.error = ''
      }

    })
  },
  methods: {
    submit () {
      var loginform = document.getElementById("loginForm")

      if (loginform.checkValidity()) {
        this.$store.dispatch('logIn', this.credentials)
        .then((response) => {
          if (response.ok) {
            loginform.classList.remove("was-validated")
            this.$emit('close')
          } else {
            this.error = response.body[Object.keys(response.body)[0]][0]
          }
        })
        .catch((error) => {
          this.error = error.body[Object.keys(error.body)[0]][0]
        })

      } else {
        loginform.classList.add("was-validated")
      }
    },
    showSignupForm () {
      EventBus.$emit('showSignupForm')
    },
    showResetPasswordForm () {
      EventBus.$emit('showResetPasswordForm')
    }
  }
}
</script>
