<template>
  <div class="full-width center-content">
    <div class="container">
      <div class="row">
        <div>
          <welcome-message name="World" />
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import WelcomeMessage from 'components/Home/WelcomeMessage'

export default {
  components: {
    WelcomeMessage
  }
}
</script>
