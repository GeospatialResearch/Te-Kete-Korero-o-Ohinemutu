<template>
  <div class="content-info">
    <div class="row p-4">
      <div class="form-group col-md-12">
        <h3>Themes</h3>
        <p>Here are more themes that you can use</p>
      </div>
    </div>
    <div class="row p-4">
      <div class="form-group col-md-12">
        <a href="#" data-theme="default-theme" class="theme default-theme selected" />
        <a href="#" data-theme="chiller-theme" class="theme chiller-theme" />
        <a href="#" data-theme="legacy-theme" class="theme legacy-theme" />
        <a href="#" data-theme="ice-theme" class="theme ice-theme" />
        <a href="#" data-theme="cool-theme" class="theme cool-theme" />
        <a href="#" data-theme="light-theme" class="theme light-theme" />
      </div>
      <div class="form-group col-md-12">
        <p>You can also use background image </p>
      </div>
      <div class="form-group col-md-12">
        <a href="#" data-bg="bg1" class="theme theme-bg selected" />
        <a href="#" data-bg="bg2" class="theme theme-bg" />
        <a href="#" data-bg="bg3" class="theme theme-bg" />
        <a href="#" data-bg="bg4" class="theme theme-bg" />
      </div>
      <div class="form-group col-md-12">
        <div class="custom-control custom-switch">
          <input id="toggle-bg" type="checkbox" class="custom-control-input" checked>
          <label class="custom-control-label" for="toggle-bg">Background image</label>
        </div>
      </div>
      <div class="form-group col-md-12">
        <div class="custom-control custom-switch">
          <input id="toggle-border-radius" type="checkbox" class="custom-control-input">
          <label class="custom-control-label" for="toggle-border-radius">Border radius</label>
        </div>
      </div>
    </div>
    <hr>
    <div class="row p-4">
      <div class="form-group col-md-12">
        <a href="https://github.com/azouaoui-med/pro-sidebar-template" class="btn btn-dark" target="_blank">
          <i class="fab fa-github" /> View source</a>
        <a href="https://github.com/azouaoui-med/pro-sidebar-template/archive/gh-pages.zip" class="btn btn-outline-dark" target="_blank">
          <i class="fa fa-download" /> Download
        </a>
      </div>
    </div>
    <hr>
  </div>
</template>

<script>

export default {
  computed: {
  }
}
</script>
