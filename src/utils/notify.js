module.exports = {
  success: function (message) {
    $.notify({
      message: message,
      icon: 'fa fa-check-circle'
    }, {
      type: 'success',
      z_index: 2000
    })
  },
  info: function (message) {
    $.notify({
      message: message,
      icon: 'fa fa-info-circle'
    }, {
      type: 'info',
      z_index: 2000
    })
  },
  warning: function (message) {
    $.notify({
      message: message,
      icon: 'fa fa-exclamation-circle'
    }, {
      type: 'warning',
      z_index: 2000,
      mouse_over: 'pause',
      animate: {
        enter: 'animated fadeInDown',
        exit: 'animated fadeOutUp'
      }
    })
  },
  error: function (message) {
    $.notify({
      message: message,
      icon: 'fa fa-exclamation-triangle'
    }, {
      type: 'danger',
      z_index: 2000,
      timer: 6000
    })
  },
  close: function () {
    $.notifyClose()
  }
}
