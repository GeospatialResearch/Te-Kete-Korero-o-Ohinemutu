module.exports = {
  findByName: function (map, name) {
    var layers = map.getLayers();
    var length = layers.getLength();
    for (var i = 0; i < length; i++) {
      if (name === layers.item(i).get('name')) {
        return layers.item(i);
      }
    }
    return null;
  },
  flyTo: function (location, view, done) {
    var duration = 5000;
    var zoom = view.getZoom();
    var parts = 2;
    var called = false;

    function callback(complete) {
      --parts;
      if (called) {
        return;
      }
      if (parts === 0 || !complete) {
        called = true;
        done(complete);
      }
    }

    if (view.getZoom() > 13) {
      view.animate({
        center: location,
        duration: duration
      }, callback)
      view.animate({
        zoom: zoom - 1,
        duration: duration / 2
      }, {
          zoom: zoom,
          duration: duration / 2
        }, callback)
    } else {
      view.animate({
        zoom: 13,
        center: location,
        duration: duration
      })
    }
  }
}
