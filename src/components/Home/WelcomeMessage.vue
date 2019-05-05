<template>
  <div id="test">
    <h3>Hello {{ name }} from my Vue.js page, built with Webpack 4!!</h3>
    <div class="input-group mb-3">
      <div class="input-group-prepend">
        <span id="basic-addon1" class="input-group-text">@</span>
      </div>
      <input type="text" class="form-control" placeholder="Username" aria-label="Username" aria-describedby="basic-addon1">
    </div>
    <label for="flavor">Favorite ice cream flavor?</label>
    <input name="flavor" @input="changed">
    <div>
      <p>You chose {{ $store.getters.flavor }}</p>
    </div>
    <p>Have a cup of coffee: <font-awesome-icon icon="coffee" /></p>
  </div>
</template>

<script>

export default {
  props: {
    name: {
      type: String,
      required: true
    }
  },
  methods: {
    changed: function (event) {
      this.$store.commit('change', event.target.value)
      console.log($("#test"))
    }
  }
}
</script>
