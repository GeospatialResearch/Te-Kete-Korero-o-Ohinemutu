<template>
  <div>
    <nav id="sidebar" class="sidebar-wrapper">
      <div class="sidebar-content">
        <!-- sidebar-brand  -->
        <div class="sidebar-item sidebar-brand">
          <a href="#">pro sidebar</a>
        </div>
        <!-- sidebar-header  -->
        <div class="sidebar-item sidebar-header d-flex flex-nowrap">
          <div class="user-pic">
            <img class="img-responsive img-rounded" src="static/img/user.jpg" alt="User picture">
          </div>
          <div class="user-info">
            <span class="user-name">Jhon <strong>Smith</strong>
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

        <!-- sidebar import dataset  -->
        <div class="sidebar-item sidebar-search">
          <div>
            <div class="input-group">
              <!-- <input class="form-control search-menu" @click="uploadDatasetClicked" placeholder="Upload dataset"> -->
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

        <!-- sidebar-menu  -->
        <div class=" sidebar-item sidebar-menu">
          <ul>
            <li class="header-menu">
              <span>General</span>
            </li>
            <!-- <li class="sidebar-dropdown">
              <a href="#">
                <i class="fa fa-shopping-cart" />
                <span class="menu-text">E-commerce</span>
                <span class="badge badge-pill badge-danger">3</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li>
                    <a href="#">Products
                    </a>
                  </li>
                  <li>
                    <a href="#">Orders</a>
                  </li>
                  <li>
                    <a href="#">Credit cart</a>
                  </li>
                </ul>
              </div>
            </li>
            <li class="sidebar-dropdown">
              <a href="#">
                <i class="far fa-gem" />
                <span class="menu-text">Components</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li>
                    <a href="#">General</a>
                  </li>
                  <li>
                    <a href="#">Panels</a>
                  </li>
                  <li>
                    <a href="#">Tables</a>
                  </li>
                  <li>
                    <a href="#">Icons</a>
                  </li>
                  <li>
                    <a href="#">Forms</a>
                  </li>
                </ul>
              </div>
            </li>
            <li class="sidebar-dropdown">
              <a href="#">
                <i class="fa fa-chart-line" />
                <span class="menu-text">Charts</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li>
                    <a href="#">Pie chart</a>
                  </li>
                  <li>
                    <a href="#">Line chart</a>
                  </li>
                  <li>
                    <a href="#">Bar chart</a>
                  </li>
                  <li>
                    <a href="#">Histogram</a>
                  </li>
                </ul>
              </div>
            </li> -->
            <li @click="$store.commit('TOGGLE_CONTENT', 'map')">
              <a href="#">
                <i><font-awesome-icon icon="globe" /></i>
                <span class="menu-text">Map</span>
              </a>
            </li>
            <li class="sidebar-dropdown">
              <a href="#">
                <i><font-awesome-icon icon="layer-group" /></i>
                <span class="menu-text">Layers</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li>
                    <a href="#">Google maps</a>
                  </li>
                  <li>
                    <a href="#">Open street map</a>
                  </li>
                </ul>
              </div>
            </li>
            <li class="sidebar-dropdown">
              <a href="#">
                <i><font-awesome-icon icon="book-open" /></i>
                <span class="menu-text">Stories</span>
                <span class="badge badge-pill badge-warning">New</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li>
                    <a href="#">
                      Story 1
                      <span class="badge badge-pill badge-success">Pro</span>
                    </a>
                  </li>
                  <li>
                    <a href="#">Story 2</a>
                  </li>
                  <li>
                    <a href="#">Story 3</a>
                  </li>
                </ul>
              </div>
            </li>
            <li class="sidebar-dropdown">
              <a href="#">
                <i><font-awesome-icon icon="tachometer-alt" /></i>
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
            </li>
            <li class="header-menu">
              <span>Extra</span>
            </li>
            <li>
              <a href="#">
                <i><font-awesome-icon icon="book" /></i>
                <span class="menu-text">Documentation</span>
                <span class="badge badge-pill badge-primary">Beta</span>
              </a>
            </li>
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
        <div class="dropdown">
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
                  <!-- <i class="fas fa-check text-success border border-success" /> -->
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
                  <!-- <i class="fas fa-exclamation text-info border border-info" /> -->
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
                  <!-- <i class="fas fa-exclamation-triangle text-warning border border-warning" /> -->
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
        </div>
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
            <form enctype="multipart/form-data" novalidate>
              <p>Upload a dataset (zipped shapefile or other spatial dataset format)</p>
              <div class="dropbox">
                <input type="file" :name="uploadFieldName" class="input-file" @change="fileChange($event.target.files)">
                <p>
                  Click to browse or drop something here
                </p>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="reset()">Close</button>
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
    methods: {
      uploadDatasetClicked () {
        $('#uploadDatasetModal').modal('show')
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

        $('#uploadDatasetModal').modal('hide')
        this.$store.dispatch('uploadFile', formData)
        .then(response => {
          console.log(response)
          if (response.ok) {
            EventBus.$emit('addLayer', response.body)
            // this.currentStatus = STATUS_SUCCESS
            // this.uploadSuccess = response.body
            // delay(this.zoomExtents, 1000)
          } else {
            // this.currentStatus = STATUS_FAILED
            console.error(response)
            // this.uploadError = response.body.error
          }
          fileList = ''
        })
        .catch(err => {
          console.error(err)
          // this.uploadError = err.response.body.detail
          // this.currentStatus = STATUS_FAILED
          fileList = ''
        })
      }
    }
  }

</script>
