<template>
  <div class="container h-100">
    <div class="d-flex justify-content-center h-100">
      <div class="user_card pt-5">
        <div class="text-center pt-5 pb-4">
          <h2>Reset Password Confirm</h2>
        </div>
        <div v-if="resetLoading" class="text-center">
          loading...
        </div>
        <div v-else-if="!resetCompleted">
          <div class="main-registration main-center">
            <form class="form ml-4 mr-4">
              <div v-if="resetError" class="alert alert-danger">
                <p>{{ resetErrorReason }}</p>
              </div>
              <div class="input-group mb-4">
                <div class="input-group-append">
                  <span class="input-group-text">
                    <i><font-awesome-icon icon="key" /></i>
                  </span>
                </div>
                <input v-model="inputs.password1" value="" type="password" name="" class="form-control input_pass" placeholder="Password" required @keyup.enter="resetPassword()">
              </div>
              <div class="input-group mb-4">
                <div class="input-group-append">
                  <span class="input-group-text">
                    <i><font-awesome-icon icon="key" /></i>
                  </span>
                </div>
                <input v-model="inputs.password2" value="" type="password" name="" class="form-control input_pass" placeholder="Confirm password" required @keyup.enter="resetPassword()">
              </div>
            </form>
            <div class="mt-4 mb-2 ml-4 mr-4">
              <button class="btn btn-primary login-btn btn-block" @click="resetPassword()">
                Reset password
              </button>
            </div>
          </div>
        </div>
        <div v-else class="text-center">
          <h4 class="pb-3">
            Your password has been reset.
          </h4>
          <h6>
            Click the Login button and insert your new credentials.
          </h6>
          <h6>
            Or click
            <a href="">here</a>
            to go Home.
          </h6>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { mapState } from 'vuex'

export default {
  data() {
    return {
      inputs: {
        password1: '',
        password2: '',
        uid: this.$route.params.uid,
        token: this.$route.params.token,
      }
    }
  },
  computed: mapState('signup', [
    'resetCompleted',
    'resetError',
    'resetLoading',
    'resetErrorReason'
  ]),
  beforeDestroy() {
    this.$store.dispatch('signup/clearResetStatus')
  },
  methods: {
    resetPassword () {
      this.$store.dispatch('signup/resetPassword', this.inputs)
    }
  }
}
</script>
