<template>
  <div>
    <nav id="sidebar" class="sidebar-wrapper">
      <div class="sidebar-content">
        <!-- sidebar-brand  -->
        <div class="sidebar-item sidebar-brand text-center">
          <a href="#">Cultural narratives</a>
        </div>
        <!-- sidebar-header  -->
        <div class="sidebar-item sidebar-header d-flex flex-nowrap">
          <div class="user-pic">
            <img class="img-responsive img-rounded" src="static/img/user.jpg" alt="User picture">
          </div>
          <div class="user-info">
            <span class="user-name">John <strong>Smith</strong>
            </span>
            <span class="user-role">Administrator</span>
            <span class="user-status">
              <i><font-awesome-icon icon="circle" /></i>
              <span>Online</span>
            </span>
          </div>
        </div>
        <!-- sidebar-search  -->
        <div class="sidebar-item sidebar-search">
          <div>
            <div class="input-group">
              <input type="text" class="form-control search-menu" placeholder="Search...">
              <div class="input-group-append">
                <span class="input-group-text">
                  <i aria-hidden="true"><font-awesome-icon icon="search" /></i>
                </span>
              </div>
            </div>
          </div>
        </div>


        <!-- sidebar-menu  -->
        <div class=" sidebar-item sidebar-menu">
          <ul>
            <li class="header-menu">
              <span>General</span>
            </li>
            <li @click="$store.commit('TOGGLE_CONTENT', 'map')">
              <a href="#">
                <i class="fa fa-globe" />
                <!-- <i><font-awesome-icon icon="globe" /></i> -->
                <span class="menu-text">Map</span>
              </a>
            </li>

            <!-- sidebar import dataset  -->
            <div class="sidebar-item sidebar-search pointer">
              <div>
                <div class="input-group">
                  <div class="form-control search-menu text-center label-info" @click="uploadDatasetClicked">
                    Upload dataset
                  </div>
                  <div class="input-group-append">
                    <span class="input-group-text">
                      <i aria-hidden="true"><font-awesome-icon icon="folder-open" /></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <li class="sidebar-dropdown">
              <a href="#">
                <i class="fa fa-layer-group" />
                <!-- <i><font-awesome-icon icon="layer-group" /></i> -->
                <span class="menu-text">My Layers</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li v-for="(layer, layerkey) in internalLayers" :key="layerkey">
                    <a href="#" class="sidebar-line">
                      <span :class="layer.visible ? 'fa fa-check-square': 'fa fa-square'" @click="changeLayerVisibility_intServ(layer, layerkey)" />
                      <span v-if="layer.assigned_name">
                        &emsp;{{ layer.assigned_name }}
                      </span>
                      <span v-else>
                        &emsp;{{ layer.name }}
                      </span>
                      <span class="float-right" data-toggle="popover" data-placement="right" data-trigger="click" title="Layer Options" :data-content="createPopoverLayerOptions(layer, 'internal')">
                        <font-awesome-icon icon="ellipsis-v" />
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
            </li>
            <li class="sidebar-dropdown">
              <a href="#">
                <i class="fa fa-layer-group" />
                <!-- <i><font-awesome-icon icon="layer-group" /></i> -->
                <span class="menu-text">External Layers</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li v-for="(layer, layerkey) in externalLayers" :key="layerkey">
                    <a href="#" class="sidebar-line">
                      <span :class="layer.visible ? 'fa fa-check-square': 'fa fa-square'" @click="changeLayerVisibility_extServ(layer, layerkey)" />
                      &emsp;{{ layer.layername }}
                      <span class="float-right" data-toggle="popover" data-placement="right" data-trigger="hover" title="Layer Information" :data-content="createPopoverInfo(layer)">
                        <font-awesome-icon icon="info" class="layer-info" />
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
            </li>

            <!-- sidebar open panel  -->
            <div class="sidebar-item sidebar-search pointer">
              <div>
                <div class="input-group">
                  <div class="form-control search-menu text-center label-info" @click="openPanel()">
                    Add new narrative
                  </div>
                </div>
              </div>
            </div>
            <li class="sidebar-dropdown">
              <a href="#">
                <i class="fa fa-book-open" />
                <!-- <i><font-awesome-icon icon="book-open" /></i> -->
                <span class="menu-text">My Narratives</span>
                <!-- <span class="badge badge-pill badge-warning">New</span> -->
              </a>
              <div v-if="!stories.length" class="sidebar-submenu">
                <span>
                  No stories available
                </span>
              </div>
              <div v-else class="sidebar-submenu">
                <ul>
                  <li v-for="story in stories" :key="story.id">
                    <a href="#" class="sidebar-line" :title="story.title">
                      <small><font-awesome-icon :icon="['far', 'circle']" size="xs" /></small>
                      <span class="inline-text">
                        <span class="ml-2 ellipsis-text"> {{ story.title }}</span>
                      </span>
                      <span class="float-right" data-toggle="popover" data-placement="right" data-trigger="click" title="Story Options" :data-content="createPopoverStoryOptions(story)">
                        <font-awesome-icon icon="ellipsis-v" />
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
            </li>
            <!-- <li class="sidebar-dropdown">
              <a href="#">
                <i class="fa fa-tachometer-alt" />
                <span class="menu-text">Dashboard</span>
                <span class="badge badge-pill badge-warning">New</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li>
                    <a href="#">
                      Dashboard 1
                      <span class="badge badge-pill badge-success">Pro</span>
                    </a>
                  </li>
                  <li>
                    <a href="#">Dashboard 2</a>
                  </li>
                  <li>
                    <a href="#">Dashboard 3</a>
                  </li>
                </ul>
              </div>
            </li> -->
            <!-- <li class="header-menu">
              <span>Extra</span>
            </li>
            <li>
              <a href="#">
                <i class="fa fa-book" />
                <span class="menu-text">Documentation</span>
              </a>
            </li> -->
            <!-- <li>
              <a href="#">
                <i class="fa fa-calendar" />
                <span class="menu-text">Calendar</span>
              </a>
            </li> -->
            <!-- <li>
              <a href="#">
                <i class="fa fa-folder" />
                <span class="menu-text">Examples</span>
              </a>
            </li> -->
          </ul>
        </div>
        <!-- sidebar-menu  -->
      </div>


      <!-- sidebar-footer  -->
      <div class="sidebar-footer">
        <!-- <div class="dropdown">
          <a href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i class="text-info"><font-awesome-icon icon="bell" /></i>
            <span class="badge badge-pill badge-warning notification">3</span>
          </a>
          <div class="dropdown-menu notifications" aria-labelledby="dropdownMenuMessage">
            <div class="notifications-header">
              <i class="text-info"><font-awesome-icon icon="bell" /></i>
              Notifications
            </div>
            <div class="dropdown-divider" />
            <a class="dropdown-item" href="#">
              <div class="notification-content">
                <div class="icon border border-success text-center">
                  <i class="text-success"><font-awesome-icon icon="check" /></i>
                </div>
                <div class="content">
                  <div class="notification-detail">Lorem ipsum dolor sit amet consectetur adipisicing elit. In totam explicabo</div>
                  <div class="notification-time"> 6 minutes ago</div>
                </div>
              </div>
            </a>
            <a class="dropdown-item" href="#">
              <div class="notification-content">
                <div class="icon border border-info text-center">
                  <i class="text-info"><font-awesome-icon icon="exclamation" /></i>
                </div>
                <div class="content">
                  <div class="notification-detail">Lorem ipsum dolor sit amet consectetur adipisicing elit. In totam explicabo</div>
                  <div class="notification-time">Today</div>
                </div>
              </div>
            </a>
            <a class="dropdown-item" href="#">
              <div class="notification-content">
                <div class="icon border border-warning text-center">
                  <i class="text-warning"><font-awesome-icon icon="exclamation-triangle" /></i>
                </div>
                <div class="content">
                  <div class="notification-detail">Lorem ipsum dolor sit amet consectetur adipisicing elit. In totam explicabo</div>
                  <div class="notification-time">Yesterday</div>
                </div>
              </div>
            </a>
            <div class="dropdown-divider" />
            <a class="dropdown-item text-center" href="#">View all notifications</a>
          </div>
        </div> -->
        <div class="dropdown">
          <a href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i><font-awesome-icon icon="envelope" /></i>
            <span class="badge badge-pill badge-success notification">7</span>
          </a>
          <div class="dropdown-menu messages" aria-labelledby="dropdownMenuMessage">
            <div class="messages-header">
              <i><font-awesome-icon icon="envelope" /></i>
              Messages
            </div>
            <div class="dropdown-divider" />
            <a class="dropdown-item" href="#">
              <div class="message-content">
                <div class="pic">
                  <img src="static/img/user.jpg" alt="">
                </div>
                <div class="content">
                  <div class="message-title">
                    <strong> Jhon doe</strong>
                  </div>
                  <div class="message-detail">Lorem ipsum dolor sit amet consectetur adipisicing elit. In totam explicabo
                  </div>
                </div>
              </div>
            </a>
            <a class="dropdown-item" href="#">
              <div class="message-content">
                <div class="pic">
                  <img src="static/img/user.jpg" alt="">
                </div>
                <div class="content">
                  <div class="message-title">
                    <strong> Jhon doe</strong>
                  </div>
                  <div class="message-detail">Lorem ipsum dolor sit amet consectetur adipisicing elit. In totam explicabo
                  </div>
                </div>
              </div>
            </a>
            <a class="dropdown-item" href="#">
              <div class="message-content">
                <div class="pic">
                  <img src="static/img/user.jpg" alt="">
                </div>
                <div class="content">
                  <div class="message-title">
                    <strong> Jhon doe</strong>
                  </div>
                  <div class="message-detail">Lorem ipsum dolor sit amet consectetur adipisicing elit. In totam explicabo
                  </div>
                </div>
              </div>
            </a>
            <div class="dropdown-divider" />
            <a class="dropdown-item text-center" href="#">View all messages</a>
          </div>
        </div>
        <div class="dropdown">
          <a href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i><font-awesome-icon icon="cog" /></i>
            <span class="badge-sonar" />
          </a>
          <div class="dropdown-menu" aria-labelledby="dropdownMenuMessage">
            <a class="dropdown-item" href="#">My profile</a>
            <a class="dropdown-item" href="#">Help</a>
            <a class="dropdown-item" href="#" @click="$store.commit('TOGGLE_CONTENT', 'themes')">Themes</a>
          </div>
        </div>
        <div>
          <a href="#">
            <i><font-awesome-icon icon="power-off" /></i>
          </a>
        </div>
        <div class="pinned-footer">
          <a href="#">
            <i><font-awesome-icon icon="ellipsis-h" /></i>
          </a>
        </div>
      </div>
    </nav>
    <!-- Modals  -->
    <div id="uploadDatasetModal" class="modal">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Upload dataset
            </h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form v-if="!uploadError" enctype="multipart/form-data" novalidate>
              <p class="text-center">
                <strong>Upload a vector dataset (zipped shapefile or geojson file) or a raster file</strong>
              </p>
              <div class="dropbox">
                <input type="file" :name="uploadFieldName" class="input-file" @change="fileChange($event.target.files)">
                <p>
                  Click to browse or drop something here
                </p>
              </div>
            </form>
            <div v-if="uploadError" class="alert alert-danger text-center">
              <h5>Upload failed with error:</h5>
              <code>{{ uploadError }}</code>
              <hr>
              <p>Please check that your data is valid and try again.</p>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="reset()">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="renameLayerModal" class="modal fade">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Rename layer</h5>
            <button type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <div>
              <label>New name for layer</label>
              <input v-model="layerAssignedName" required type="text" class="form-control form-control-sm" title="New name">
            </div>
          </div>
          <div class="modal-footer">
            <div class="btn-group pull-right">
              <button type="button" class="btn btn-secondary" data-dismiss="modal">
                Cancel
              </button>
              <button type="button" class="btn btn-primary" data-dismiss="modal" @click="assignNewName()">
                Save
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div id="deleteLayerModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Delete Layer</h5>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this layer?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="deleteLayer()">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="deleteStoryModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Delete Story</h5>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this story?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="deleteStory()">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="storyIsBeingEditedWarningModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <h6>A story is being edited, be sure you save the changes before opening another story.</h6>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
  <!-- page-wrapper -->
</template>

<script>
  import 'utils/sidebar'
  import { EventBus } from 'store/event-bus'

  export default {
    data () {
      return {
        uploadFieldName: 'file',
        uploadError: null,
        layerAssignedName: null,
        layerName: null,
        layerToDelete: null,
        storyToDelete: null
      }
    },
    computed: {
      externalLayers () {
        return this.$store.state.externalLayers
      },
      internalLayers () {
        // the popover needs to be re-initialized when reloading the divs
        $(function () {
          $('[data-toggle="popover"]').popover({
            boundary:'window',
            html: true
          })
        })
        return this.$store.state.internalLayers
      },
      map () {
        return this.$store.state.map
      },
      stories () {
        $(function () {
          $('[data-toggle="popover"]').popover({
            boundary:'window',
            html: true
          })
        })
        return this.$store.state.stories
      }
    },
    mounted: function () {
      EventBus.$on('assignLayerNameModalOpen', (layername) => {
        this.layerName = layername
        this.layerAssignedName = this.$store.state.internalLayers[layername].assigned_name
        $('#renameLayerModal').modal('show')
      })

      EventBus.$on('deleteLayerModalOpen', (layername) => {
        this.layerToDelete = layername
        $('#deleteLayerModal').modal('show')
      })

      EventBus.$on('deleteStoryModalOpen', (storyid) => {
        this.storyToDelete = storyid
        $('#deleteStoryModal').modal('show')
      })

      EventBus.$on('storyIsBeingEditedWarning', () => {
        $('#storyIsBeingEditedWarningModal').modal('show')
      })
    },
    methods: {
      openPanel(){
        if (!this.$store.state.storyViewMode) {
          $('#storyIsBeingEditedWarningModal').modal('show')
        } else {
          this.$store.commit('RESET_STORY_FORM')
          this.$store.commit('SET_STORY_VIEW_MODE', false)
          this.$store.commit('SET_PANEL_OPEN', true)
          EventBus.$emit('addStoryGeomsToMap', [])
        }
      },
      uploadDatasetClicked () {
        this.reset()
        if (!this.$store.state.storyViewMode) {
          $('#storyIsBeingEditedWarningModal').modal('show')
        } else {
          $('#uploadDatasetModal').modal('show')
        }
      },
      reset () {
        this.uploadError = null
      },
      fileChange (fileList) {
        // handle file changes
        const formData = new FormData()

        if (!fileList.length) return

        this.$store.state.isUploadingData = true

        // append the files to FormData
        Array
          .from(Array(fileList.length).keys())
          .map(x => {
            formData.append('file', fileList[x], fileList[x].name)
          })

        // close the modal
        $('#uploadDatasetModal').modal('hide')

        // dispatch action to upload file
        this.$store.dispatch('uploadFile', formData)
        .then(response => {
          if (response.ok) {
            if (response.body) {
              EventBus.$emit('addLayer', response.body)  // add argument false if you want to add geojson layer
            }
            this.$store.state.isUploadingData = false
            this.reset()
          } else {
            if (response.body.indexOf('Request') == -1) {
              this.uploadError = response.body[0]
            } else {
              this.uploadError = response.body.split('Request')[0]
            }

            $('#uploadDatasetModal').modal('show')
            this.$store.state.isUploadingData = false
          }
          fileList = ''
        })
        .catch(err => {
          console.error(err)
          // this.uploadError = err.response.body.detail
          // this.currentStatus = STATUS_FAILED
          fileList = ''
        })
      },
      changeLayerVisibility_extServ (layer, layerkey) {
        this.$store.state.externalLayers[layerkey].visible = !this.$store.state.externalLayers[layerkey].visible
        if (this.$store.state.externalLayers[layerkey].visible) {
          EventBus.$emit('createLayer', layer, 'external') // we need to send the configurations of the layer
        } else {
          EventBus.$emit('removeLayer', layerkey)
        }
        // check if there are active layers and show resolution notification if needed
        EventBus.$emit('resolutionNotification')
      },
      changeLayerVisibility_intServ (layer, layerkey) {
        this.$store.state.internalLayers[layerkey].visible = !this.$store.state.internalLayers[layerkey].visible
        if (this.$store.state.internalLayers[layerkey].visible) {
          EventBus.$emit('createLayer', layerkey, 'internal') // the layerkey is enough to request the geoserver layer
        } else {
          EventBus.$emit('removeLayer', layerkey)
        }
      },
      createPopoverInfo (layer) {
        var htmlInfo = layer.attribution
        if (layer.hasOwnProperty('maxresolution')) {
          htmlInfo = htmlInfo + "<p>Due to the density of data in the layer, the layer is visible between the resolutions " +
                              layer.minresolution + " and " + layer.maxresolution + "</p>"
        }
        return htmlInfo
      },
      createPopoverLayerOptions (layer) {
        var disabled = layer.visible ? ' ' : ' disabled'
        var layerOptions = `<div class="layer-options">
                              <a class="dropdown-item` + disabled +`" id="` + layer.name + `_zoomto" href="#">Zoom to layer</a>
                              <a class="dropdown-item` + disabled +`" id="` + layer.name + `_rename" href="#">Rename layer</a>
                              <a class="dropdown-item` + disabled +`" id="` + layer.name + `_restyle" href="#">Edit style</a>
                              <div class="dropdown-divider"></div>
                              <a class="dropdown-item` + disabled +`" id="` + layer.name + `_deleteLayer" href="#">Delete layer</a>
                            </div>`

        return layerOptions
      },
      assignNewName () {
        this.$store.dispatch('renameLayer', { layername: this.layerName, assignedName: this.layerAssignedName })
      },
      deleteLayer () {
        this.$store.dispatch('deleteLayer', this.layerToDelete)
        .then(() => {
          EventBus.$emit('removeLayer', this.layerToDelete)
        })
      },
      deleteStory () {
        this.$store.dispatch('deleteStory', this.storyToDelete)
        .then( () => {
          this.$store.dispatch('deleteUnusedMediaFiles')
          this.$store.dispatch('deleteUnusedGeomAttrs')
        })
        this.$store.commit('SET_PANEL_OPEN', false)
        EventBus.$emit('removeLayer', 'storyGeomsLayer')
        EventBus.$emit('resetDrawnFeature')
      },
      createPopoverStoryOptions (story) {
        var storyOptions = `<div class="layer-options">
                              <a class="dropdown-item" id="` + story.id + `_view" href="#">View story</a>
                              <a class="dropdown-item" id="` + story.id + `_edit" href="#">Edit story</a>
                              <div class="dropdown-divider"></div>
                              <a class="dropdown-item" id="` + story.id + `_deleteStory" href="#">Delete story</a>
                            </div>`

        return storyOptions
      }
    }
  }

</script>
