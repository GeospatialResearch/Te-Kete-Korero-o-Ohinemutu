var EventBus = require('store/event-bus.js').EventBus
var _ = require('underscore')
const store = require('store').default

$(function () {
  // Resize map on window resize
  $(window).on('resize', function(){
    // var w = window.outerWidth;
    // var h = window.outerHeight;
    // var txt = "Window size: width=" + w + ", height=" + h;
    // console.log(txt)
    if(window.outerWidth > window.outerHeight) {
      store.commit('SET_ORIENTATION', 'landscape')
    } else {
      store.commit('SET_ORIENTATION', 'portrait')
    }
    _.delay(() => {
      EventBus.$emit("updateMapWidth")
      EventBus.$emit("updateMapHeight")
    }, 100)
  })

  //toggle sidebar
  $("#toggle-sidebar").click(function () {
      $(".page-wrapper").toggleClass("toggled");
      _.delay(() => {
        EventBus.$emit("updateMapWidth")
      }, 100)

  });

  //Pin sidebar
  $("#pin-sidebar").click(function () {
      if ($(".page-wrapper").hasClass("pinned")) {
          // unpin sidebar when hovered
          $(".page-wrapper").removeClass("pinned");
          $("#sidebar").unbind( "hover");
      } else {
          $(".page-wrapper").addClass("pinned");
          $("#sidebar").hover(
              function () {
                  $(".page-wrapper").addClass("sidebar-hovered");
              },
              function () {
                  $(".page-wrapper").removeClass("sidebar-hovered");
              }
          )
      }
  });

  //toggle sidebar overlay
  $("#overlay").click(function () {
      $(".page-wrapper").toggleClass("toggled");
      _.delay(() => {
        EventBus.$emit("updateMapWidth")
      }, 100)
  });

  //switch between themes
  var themes = "default-theme legacy-theme chiller-theme ice-theme cool-theme light-theme";
  $('[data-theme]').click(function () {
    $('[data-theme]').removeClass("selected");
    $(this).addClass("selected");
    $('.page-wrapper').removeClass(themes);
    $('.page-wrapper').addClass($(this).attr('data-theme'));
  });

  // switch between background images
  var bgs = "bg1 bg2 bg3 bg4";
  $('[data-bg]').click(function () {
    $('[data-bg]').removeClass("selected");
    $(this).addClass("selected");
    $('.page-wrapper').removeClass(bgs);
    $('.page-wrapper').addClass($(this).attr('data-bg'));
  });

  // toggle background image
  $("#toggle-bg").change(function (e) {
    e.preventDefault();
    $('.page-wrapper').toggleClass("sidebar-bg");
  });

  // toggle border radius
  $("#toggle-border-radius").change(function (e) {
    e.preventDefault();
    $('.page-wrapper').toggleClass("boder-radius-on");
  });

  // custom scroll bar is only used on desktop
  if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
    $(".sidebar-content").mCustomScrollbar({
      axis: "y",
      autoHideScrollbar: true,
      scrollInertia: 300,
      mouseWheel:{
      enable:true,
      scrollAmount:50
      }
    });
    $(".sidebar-content").addClass("desktop");
  }

  // Hide any open sidebar layer popover when the anywhere else in the body is clicked
  $('body').on('click', function (e) {
    $('[data-toggle=popover]').each(function () {
      if (!$(this).is(e.target) && $(this).has(e.target).length === 0 ) {
        $(this).popover('hide')
      }
      // && $('.popover').has(e.target).length === 0 // avoids to hide the popover if we click on it
    })
  })

  // Send EventBus on internal layer click option
  $(document.body).on('click', "[id*='_zoomto']" ,function(){
    var layer_name = $(this).attr('id').replace("_zoomto", "")
    if (layer_name === 'allStoriesGeomsLayer') {
      EventBus.$emit('zoomToLayer', {layerName:layer_name})
    } else {
      EventBus.$emit('zoomToLayer', {layerName:layer_name, layerType:'internal'})
    }
  })
  $(document.body).on('click', "[id*='_restyle']" ,function(){
    var layer_id = $(this).attr('id').replace("_restyle", "")
    EventBus.$emit('restyleLayer', layer_id)
  })
  $(document.body).on('click', "[id*='_deleteLayer']" ,function(){
    var layer_id = $(this).attr('id').replace("_deleteLayer", "")
    EventBus.$emit('deleteLayerModalOpen', layer_id)
  })
  $(document.body).on('click', "[id*='_copyright']" ,function(){
    var layer_id = $(this).attr('id').replace("_copyright", "")
    EventBus.$emit('addCopyrightLayerModalOpen', layer_id)
  })
  $(document.body).on('click', "[id*='_rename']" ,function(){
    var layer_id = $(this).attr('id').replace("_rename", "")
    EventBus.$emit('assignLayerNameModalOpen', layer_id)
  })
  $(document.body).on('click', "[id*='_share']" ,function(){
    var layer_id = $(this).attr('id').replace("_share", "")
    EventBus.$emit('shareLayerModalOpen', layer_id)
  })

  // Send EventBus on story click option
  $(document.body).on('click', "[id*='_view']" ,function(){
    var story_id = $(this).attr('id').replace("_view", "")
    EventBus.$emit('openNarrative', story_id)
    // TODO: Open modal with Narrative Info instead of open narrative immediately
  })
  // $(document.body).on('click', "[id*='_edit']" ,function(){
  //   if (!store.state.storyViewMode) {
  //     EventBus.$emit('storyIsBeingEditedWarning')
  //   } else {
  //     var story_id = $(this).attr('id').replace("_edit", "")
  //     store.dispatch('getStoryContent',story_id)
  //     .then((story) => {
  //       if (!story.being_edited_by || story.being_edited_by == store.state.user.id) {
  //         store.dispatch('updateEditor', {'story_id': story_id,'editor': store.state.user.id,"action":"set"})
  //         if (story.story_type) {
  //           story.story_type_id = story.story_type.id
  //         }
  //         EventBus.$emit('initialiseBootstrapSelect')
  //         store.commit('SET_STORY_VIEW_MODE', false)
  //         store.commit('SET_PANEL_OPEN', true)
  //         EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)
  //
  //       }
  //       else {
  //         store.commit('SET_STORY_VIEW_MODE', true)
  //         store.commit('SET_PANEL_OPEN', true)
  //         EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)
  //         EventBus.$emit('showStoryIsBeingEditedByWarning',story.being_edited_by)
  //       }
  //     })
  //   }
  // })
  $(document.body).on('click', "[id*='_deleteStory']" ,function(){
    var storyid = $(this).attr('id').replace("_deleteStory", "")
    EventBus.$emit('deleteStoryModalOpen', storyid)
  })
});
