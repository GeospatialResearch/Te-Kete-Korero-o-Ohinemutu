<template>
  <div :class="{'col-md-4':isOpen, 'col-md-1':!isOpen}" class="container">
    <div :title="isOpen?'Hide information':'Show information'" @click="$store.commit('TOGGLE_LEFT_PANEL')">
      <font-awesome-icon v-if="isOpen" icon="chevron-left" />
      <font-awesome-icon v-if="!isOpen" icon="chevron-right" />
    </div>
  </div>
</template>

<script>

export default {
  data: function () {
    return {

    }
  },
  computed: {
    isOpen () {
      return this.$store.state.showLeftPanel
    }
  }
}
</script>
