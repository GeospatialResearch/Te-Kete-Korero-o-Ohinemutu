<template>
  <div class="container h-100">
    <div class="d-flex justify-content-center h-100">
      <div class="user-card pt-5" :style="emailError ? 'height:400px': 'height:350px'">
        <div class="d-flex justify-content-center">
          <div class="brand-logo-container">
            <img src="static/img/weaveLogo.png" class="brand-logo" alt="Logo">
          </div>
        </div>
        <h4 class="text-center pb-4">
          Reset Password
        </h4>
        <div v-if="emailLoading" class="d-flex justify-content-center">
          <font-awesome-icon icon="spinner" spin size="lg" />
          <p class="text-center">
            loading...
          </p>
        </div>
        <div v-else-if="!emailCompleted">
          <div class="d-flex justify-content-center">
            <form id="resetPasswordForm">
              <div v-if="emailError" class="alert alert-danger text-center">
                <span>{{ emailErrorReason }}</span>
              </div>
              <div class="input-group mb-3">
                <div class="input-group-append">
                  <span class="input-group-text">
                    <i><font-awesome-icon icon="at" /></i>
                  </span>
                </div>
                <input v-model="inputs.email" value="" type="text" name="" class="form-control input_user" placeholder="Enter email" required @keyup.enter="sendPasswordResetEmail(inputs)">
              </div>
              <div class="d-flex justify-content-center login-container">
                <button type="button" name="button" class="btn login-btn" @click="sendPasswordResetEmail(inputs)">
                  Send email
                </button>
              </div>
            </form>
          </div>
        </div>
        <div v-else class="d-flex justify-content-center">
          <div>
            <p class="text-center">
              Check your inbox for a link to reset your password.
            </p>
            <p class="text-center">
              If an email doesn't appear within a few minutes, check your Spam folder.
            </p>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

import { mapState, mapActions } from 'vuex'

export default {
  data() {
    return {
      inputs: {
        email: ''
      }
    }
  },
  computed: mapState('signup', [
    'emailCompleted',
    'emailError',
    'emailLoading',
    'emailErrorReason'
  ]),
  beforeDestroy() {
    this.$store.dispatch('signup/clearEmailStatus')
  },
  methods: mapActions('signup', [
    'sendPasswordResetEmail',
    'clearEmailStatus',
  ])
}
</script>
