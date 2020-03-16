<template>
  <div>
    <nav id="sidebar" class="sidebar-wrapper">
      <div class="sidebar-content">
        <!-- sidebar-brand  -->
        <div class="sidebar-item sidebar-brand text-center">
          <a href="#" @click="$store.commit('TOGGLE_CONTENT', 'welcome')">{{ translationObj.culturalNarratives[lang] }}</a>
        </div>

        <!-- sidebar-header  -->
        <div class="sidebar-item sidebar-header d-flex flex-nowrap">
          <div v-if="authenticated" class="user-pic">
            <img class="img-responsive img-rounded" src="static/img/user.jpg" alt="User picture">
          </div>
          <div v-if="authenticated" class="user-info">
            <span class="user-name">Welcome, <strong>{{ username }}</strong>
            </span>
            <span class="user-status mt-0">Whanau: </span>
            <span class="user-status mt-0">Hapu: </span>
            <span class="user-status mt-0">Iwi: </span>
            <!-- <span class="user-role">Administrator</span> -->
            <!-- <span class="user-status">
              <i><font-awesome-icon icon="circle" /></i>
              <span>Online</span>
            </span> -->
          </div>
        </div>

        <!-- sidebar-menu  -->
        <div :class="[authenticated ? 'sidebar-item': '', 'sidebar-menu']">
          <ul>
            <li class="header-menu">
              <span>General</span>
            </li>
            <li @click="$store.commit('TOGGLE_CONTENT', 'map')">
              <a href="#">
                <!-- <i class="fa fa-globe" /> using this one the icons shakes when hovering over the icon-->
                <i><font-awesome-icon icon="globe" /></i>
                <span class="menu-text">Go to {{ translationObj.map[lang] }}</span>
              </a>
            </li>

            <!-- sidebar import dataset  -->
            <div v-if="contentToShow=='map'" class="sidebar-item sidebar-search pointer">
              <li class="header-menu">
                <span>Layers</span>
              </li>
              <div v-if="authenticated">
                <div class="input-group input-group-sm">
                  <div class="form-control search-menu text-center label-info" @click="uploadDatasetClicked">
                    {{ translationObj.uploadDataset[lang] }}
                  </div>
                  <div class="input-group-append">
                    <span class="input-group-text">
                      <i aria-hidden="true"><font-awesome-icon icon="folder-open" /></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <li v-if="authenticated && contentToShow=='map'" class="sidebar-dropdown">
              <a href="#" title="Data uploaded by you" @click="dropdownSidebarDropdow($event)">
                <!-- <i class="fa fa-layer-group" /> using this one the icons shakes when hovering over the icon-->
                <i><font-awesome-icon icon="layer-group" /></i>
                <span class="menu-text">{{ translationObj.myLayers[lang] }}</span>
              </a>
              <div class="sidebar-submenu">
                <div v-if="Object.keys(myLayers).length === 0" class="text-center">
                  <span class="no-data-available text-muted">No layers available</span>
                </div>
                <ul v-else>
                  <li v-for="(layer, layerkey) in myLayers" :key="layerkey">
                    <a href="#" class="sidebar-line">
                      <span @click="changeLayerVisibility_intServ(layer, layerkey)">
                        <!-- :class="layer.visible ? 'fa fa-check-square': 'fa fa-square'" -->
                        <span v-if="layer.visible"><font-awesome-icon icon="check-square" /></span>
                        <span v-else><font-awesome-icon icon="square" /></span>
                      </span>
                      <span v-if="layer.assigned_name" class="inline-text">
                        <span class="ml-2 ellipsis-text"> {{ layer.assigned_name }}</span>
                      </span>
                      <span v-else class="inline-text">
                        <span class="ml-2 ellipsis-text"> {{ layer.name }}</span>
                      </span>
                      <span class="float-right">
                        <span v-if="layer.uploaded_by != userPK" class="badge badge-secondary vertical-align-middle" :title="'Layer shared with you by user '+layer.uploaded_by__username">S</span>
                        <span data-toggle="popover" data-placement="right" data-trigger="click" title="Layer Options" :data-content="createPopoverLayerOptions(layer)">
                          <font-awesome-icon icon="ellipsis-v" />
                        </span>
                      </span>

                      <!-- <span class="float-right">
                        <span v-if="story.owner != username" class="badge badge-secondary" title="You are a co-author">C</span>
                        <span data-toggle="popover" data-placement="right" data-trigger="click" title="Narrative Options" :data-content="createPopoverStoryOptions(story)">
                          <font-awesome-icon icon="ellipsis-v" />
                        </span>
                      </span> -->
                    </a>
                  </li>
                </ul>
              </div>
            </li>
            <li v-if="contentToShow=='map'" class="sidebar-dropdown">
              <a href="#" title="Data from External Data Services" @click="dropdownSidebarDropdow($event)">
                <!-- <i class="fa fa-layer-group" /> using this one the icons shakes when hovering over the icon-->
                <i><font-awesome-icon icon="layer-group" /></i>
                <span class="menu-text">{{ translationObj.extLayers[lang] }}</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li v-for="(layer, layerkey) in externalLayers" :key="layerkey">
                    <a href="#" class="sidebar-line">
                      <span @click="changeLayerVisibility_extServ(layer, layerkey)">
                        <span v-if="layer.visible"><font-awesome-icon icon="check-square" /></span>
                        <span v-else><font-awesome-icon icon="square" /></span>
                      </span>
                      <span class="inline-text">
                        <span class="ml-2 ellipsis-text"> {{ layer.layername }}</span>
                      </span>
                      <span class="float-right pl-2" data-toggle="popover" data-placement="right" data-trigger="click" title="Layer Information" :data-content="createPopoverInfo(layer)">
                        <font-awesome-icon icon="info" class="layer-info" />
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
            </li>
            <li v-if="contentToShow=='map'" class="sidebar-dropdown">
              <a href="#" title="Data uploaded and managed by admin" @click="dropdownSidebarDropdow($event)">
                <!-- <i class="fa fa-layer-group" /> using this one the icons shakes when hovering over the icon-->
                <i><font-awesome-icon icon="layer-group" /></i>
                <span v-if="isAdmin" class="menu-text">Other layers</span>
                <span v-else class="menu-text">Default layers</span>
              </a>
              <div class="sidebar-submenu">
                <ul>
                  <li v-if="allStoriesGeomsLayer && allStoriesGeomsLayer.allUsedStoriesGeometries">
                    <a href="#" class="sidebar-line">
                      <span @click="changeLayerVisibility_allStoriesGeomsLayer()">
                        <span v-if="allStoriesGeomsLayer.visible"><font-awesome-icon icon="check-square" /></span>
                        <span v-else><font-awesome-icon icon="square" /></span>
                      </span>
                      <span class="inline-text">
                        <span class="ml-2 ellipsis-text"> {{ allStoriesGeomsLayer.layername }}</span>
                      </span>
                      <span class="float-right pl-2" data-toggle="popover" data-placement="right" data-trigger="click" title="Layer Options" :data-content="createPopoverLayerOptions(allStoriesGeomsLayer)">
                        <font-awesome-icon icon="ellipsis-v" />
                      </span>
                    </a>
                  </li>
                  <li v-for="(layer, layerkey) in defaultLayers" :key="layerkey">
                    <a href="#" class="sidebar-line">
                      <span @click="changeLayerVisibility_intServ(layer, layerkey)">
                        <!-- :class="layer.visible ? 'fa fa-check-square': 'fa fa-square'" -->
                        <span v-if="layer.visible"><font-awesome-icon icon="check-square" /></span>
                        <span v-else><font-awesome-icon icon="square" /></span>
                      </span>
                      <span v-if="layer.assigned_name">
                        &emsp;{{ layer.assigned_name }}
                      </span>
                      <span v-else>
                        &emsp;{{ layer.name }}
                      </span>
                      <span class="float-right pl-2" data-toggle="popover" data-placement="right" data-trigger="click" title="Layer Options" :data-content="createPopoverLayerOptions(layer)">
                        <font-awesome-icon icon="ellipsis-v" />
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
            </li>

            <!-- sidebar open panel  -->
            <div v-if="contentToShow=='map'" class="sidebar-item sidebar-search pointer">
              <li class="header-menu">
                <span>Narratives</span>
              </li>
              <div v-if="authenticated">
                <div class="input-group input-group-sm">
                  <div class="form-control search-menu text-center label-info" @click="openPanel()">
                    {{ translationObj.addNewNarrative[lang] }}
                  </div>
                  <div class="input-group-append">
                    <span class="input-group-text">
                      <i aria-hidden="true"><font-awesome-icon :icon="['far', 'newspaper']" /></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
            <li v-if="authenticated && contentToShow=='map'" class="sidebar-dropdown">
              <a href="#" @click="dropdownSidebarDropdow($event)">
                <!-- <i class="fa fa-book-open" /> using this one the icons shakes when hovering over the icon-->
                <i><font-awesome-icon icon="book-open" /></i>
                <span class="menu-text">{{ translationObj.myNarratives[lang] }}</span>
                <!-- <span class="badge badge-pill badge-warning">New</span> -->
              </a>
              <div class="sidebar-submenu">
                <div v-if="!myNarratives.length" class="text-center">
                  <span class="no-data-available text-muted">No narratives available</span>
                </div>
                <ul v-else>
                  <li v-for="story in myNarratives" :key="story.id">
                    <a href="#" class="justify-content-between" :title="story.title.eng">
                      <small><font-awesome-icon :icon="['far', 'circle']" size="xs" /></small>
                      <span class="inline-text">
                        <span class="ml-2 ellipsis-text"> {{ story.title.eng }}</span>
                      </span>
                      <span class="float-right">
                        <span v-if="story.owner != username" class="badge badge-secondary vertical-align-middle" title="You are a co-author">C</span>
                        <span data-toggle="popover" data-placement="right" data-trigger="click" title="Narrative Options" :data-content="createPopoverStoryOptions(story)">
                          <font-awesome-icon icon="ellipsis-v" />
                        </span>
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
            </li>

            <li v-if="contentToShow=='map'" class="sidebar-dropdown">
              <a href="#" @click="dropdownSidebarDropdow($event)">
                <!-- <i class="fa fa-book-open" /> using this one the icons shakes when hovering over the icon-->
                <i><font-awesome-icon icon="book-open" /></i>
                <span v-if="authenticated" class="menu-text">{{ translationObj.otherNarratives[lang] }}</span>
                <span v-else class="menu-text">Public Narratives</span>
              </a>
              <div class="sidebar-submenu">
                <div v-if="!otherNarratives.length" class="text-center">
                  <span class="no-data-available text-muted">No narratives available</span>
                </div>
                <ul v-else>
                  <li v-for="story in otherNarratives" :key="story.id">
                    <a href="#" class="justify-content-between" :title="story.title.eng">
                      <small><font-awesome-icon :icon="['far', 'circle']" size="xs" /></small>
                      <span class="inline-text">
                        <span class="ml-2 ellipsis-text"> {{ story.title.eng }}</span>
                      </span>
                      <span class="float-right pl-2" data-toggle="popover" data-placement="right" data-trigger="click" title="Narrative Options" :data-content="createPopoverStoryOptions(story)">
                        <font-awesome-icon icon="ellipsis-v" />
                      </span>
                    </a>
                  </li>
                </ul>
              </div>
            </li>

            <!-- sidebar-search  -->
            <div v-if="contentToShow=='map'" class="sidebar-item sidebar-search">
              <div>
                <div class="input-group input-group-sm">
                  <input v-model="filter.freeText" type="text" class="form-control search-menu" placeholder="Filter narratives..." @keyup="filterNarratives()">
                  <div class="input-group-append" title="Advanced filter">
                    <button class="btn btn-dark" type="button" @click="advancedFilterModal()">
                      <i aria-hidden="true"><font-awesome-icon icon="filter" /></i>
                    </button>
                  </div>
                  <div class="input-group-append" title="Clear filter">
                    <button class="btn btn-dark" type="button" @click="clearNarrativesFilter()">
                      <i aria-hidden="true"><font-awesome-icon icon="times" /></i>
                    </button>
                  </div>
                </div>

                <div class="m-2">
                  <span v-for="atua in filter.atua" :key="atua" class="badge badge-pill badge-light m-1" title="Atua">{{ allAtuas.find(x => x.id == atua).name }}</span>
                  <span v-for="type in filter.storyType" :key="type" class="badge badge-pill badge-light m-1" title="Story Type">{{ allStoryTypes.find(x => x.id == type).type }}</span>
                </div>
              </div>
            </div>


            <li v-show="filter.freeText || filter.atua.length !== 0 || filter.storyType.length !== 0" class="sidebar-dropdown">
              <a href="#" @click="dropdownSidebarDropdow($event)">
                <i><font-awesome-icon icon="book-open" /></i>
                <span class="menu-text">Filtered narratives</span>
                <span class="badge badge-pill badge-secondary">{{ filteredStories.length }}</span>
              </a>
              <div v-if="!filter.freeText && filter.atua.length == 0 && filter.storyType.length == 0" class="sidebar-submenu">
                <div class="text-center">
                  <span>No filter defined</span>
                </div>
              </div>
              <div v-else class="sidebar-submenu">
                <div v-if="filteredStories.length === 0">
                  <div class="text-center">
                    <span>No narratives matching the filter</span>
                  </div>
                </div>
                <div v-else>
                  <ul>
                    <li v-for="story in filteredStories" :key="story.id">
                      <a href="#" class="justify-content-between" :title="story.title">
                        <small><font-awesome-icon :icon="['far', 'circle']" size="xs" /></small>
                        <span class="inline-text">
                          <span class="ml-2 ellipsis-text"> {{ story.title.eng }}</span>
                        </span>
                        <span class="float-right pl-2" data-toggle="popover" data-placement="right" data-trigger="click" title="Narrative Options" :data-content="createPopoverStoryOptions(story)">
                          <font-awesome-icon icon="ellipsis-v" />
                        </span>
                      </a>
                    </li>
                  </ul>
                </div>
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
    <div id="BeingEditedByWarningModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content modal-margin-top">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <h6>Currently this story is being edited by {{ editor?allUsers.filter(user=>user.id === editor)[0].username:'' }}, so please close this story for now and come back later.</h6>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="storyIsBeingEditedWarningModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content modal-margin-top">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <h6>A story is being edited, be sure you save the changes before opening another story or doing other operations.</h6>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="advancedFilterModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Filter Narratives</h5>
          </div>
          <div class="modal-body pl-5 pr-5">
            <h6>By Atua</h6>
            <select v-model="filter.atua" class="form-control form-control-sm mb-3" multiple title="Hold the Ctrl key to select more than one Atua" @change="filterNarratives()">
              <option v-for="item in allAtuas" :key="item.id" :value="item.id">
                {{ item.name }}
              </option>
            </select>
            <h6>By Story Type</h6>
            <select v-model="filter.storyType" class="form-control form-control-sm mb-3" multiple title="Hold the Ctrl key to select more than one Story Type" @change="filterNarratives()">
              <option v-for="item in allStoryTypes" :key="item.id" :value="item.id">
                {{ item.type }}
              </option>
            </select>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="shareLayerModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Share layer
              <p class="mb-0 mt-2 modal-header-description">
                Share this layer with other users and they will be able to see it
              </p>
            </h4>
          </div>
          <div class="modal-body">
            <h5 v-if="allOtherUsers" class="mb-0">
              Users
            </h5>
            <div v-if="userPK">
              <vue-bootstrap-typeahead ref="usersAutocomplete" v-model="user_query" :serializer="s => s.username" :data="allOtherUsers.filter(user=>!layerSharedWith.includes(user.id))" placeholder="Type a username" @hit="setLayerSharedWith($event)" />
              <div class="coauthor-box">
                <ul class="coauthor-list">
                  <li v-for="userid in layerSharedWith" :key="userid" class="coauthor col-md-12">
                    <div class="col-md-10">
                      <div class="user-image">
                        <img src="static/img/user.jpg">
                      </div>
                      {{ allOtherUsers.filter(user=>user.id === userid)[0].username }}
                    </div>
                    <div class="col-md-2 vertical-align-middle">
                      <font-awesome-icon icon="times-circle" size="lg" color="grey" class="float-right" @click="stopSharingLayerModalOpen(userid)" />
                    </div>
                  </li>
                </ul>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="onClose()">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="stopSharingLayerModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content delete-coauthor-modal">
          <div class="modal-header">
            <h5>Stop sharing layer</h5>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to stop sharing this layer with user {{ userToRemoveFromLayerSharing?allOtherUsers.filter(user=>user.id === userToRemoveFromLayerSharing)[0].username:'' }}?</p>
            <p>
              This user will no longer be able to see this layer.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="setLayerSharedWithout(userToRemoveFromLayerSharing)">
              Delete
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
  import { langObj } from 'utils/initialTranslObj'
  import { each, intersection, some, without } from 'underscore'
  import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'

  export default {
    components: {
      VueBootstrapTypeahead
    },
    data () {
      return {
        uploadFieldName: 'file',
        uploadError: null,
        layerAssignedName: null,
        layerName: null,
        layerToDelete: null,
        storyToDelete: null,
        editor: null,
        filter: {
          atua: [],
          storyType: [],
          freeText: null
        },
        filteredStories: [],
        myNarratives: [],
        otherNarratives: [],
        myLayers: [],
        defaultLayers: [],
        user_query:'',
        layerSharedWith: [],
        layerToShare: null,
        userToRemoveFromLayerSharing: null
      }
    },
    computed: {
      externalLayers () {
        return this.$store.state.externalLayers
      },
      internalLayers () {
        // the popover needs to be re-initialized when reloading the divs
        this.reinitialisePopups()
        return this.$store.state.internalLayers
      },
      map () {
        return this.$store.state.map
      },
      stories () {
        // the popover needs to be re-initialized when reloading the divs
        this.reinitialisePopups()
        return this.$store.state.stories
      },
      lang () {
        return this.$store.state.lang
      },
      translationObj () {
        if (this.$store.state.websiteTranslObj) {
          return this.$store.state.websiteTranslObj
        } else {
          return langObj
        }
      },
      allStoriesGeomsLayer () {
        return this.$store.state.allStoriesGeomsLayer
      },
      allAtuas() {
        return this.$store.state.allAtuas
      },
      allUsers() {
        return this.$store.state.allUsers
      },
      allStoryTypes () {
        return this.$store.state.allStoryTypes
      },
      authenticated () {
        return this.$store.state.authenticated
      },
      username () {
        var username
        if (this.$store.state.user) {
          username = this.$store.state.user.username
        }
        return username
      },
      userPK () {
        var userpk
        if (this.$store.state.user) {
          userpk = this.$store.state.user.pk
        }
        return userpk
      },
      isAdmin () {
        return this.$store.state.isAdmin
      },
      contentToShow () {
        return this.$store.state.contentToShow
      },
      allOtherUsers() {
        var users
        if (this.$store.state.user) {
          users = this.$store.state.allUsers.filter(user=>(user.id!=this.userPK && user.id!=1))
        }
        return users
      }
    },
    watch: {
      stories: function () {
        this.filterNarratives()

        this.myNarratives = []
        this.otherNarratives = []
        if (this.authenticated) {
          each(this.stories, (story) => {
            if (story.owner == this.username ||  story.co_authors.indexOf(this.userPK)>=0) {
              this.myNarratives.push(story)
            } else {
              this.otherNarratives.push(story)
            }
          })
        } else {
          this.otherNarratives = this.stories
        }
      },
      internalLayers: {
        handler: function () {
          try {
            this.myLayers = {}
            this.defaultLayers = {}
            if (this.authenticated) {
              each(this.internalLayers, (layer, layerkey) => {
                if (layer.uploaded_by == this.userPK ||  layer.shared_with.indexOf(this.userPK)>=0) {
                  this.myLayers[layerkey] = layer
                } else {
                  this.defaultLayers[layerkey] = layer
                }
              })
            } else {
              this.defaultLayers =  $.extend(true, {}, this.internalLayers)
            }

            this.reinitialisePopups()
          } catch (err) {
            // Do nothing, this is fine.
          }
        },
        deep: true
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

      EventBus.$on('showStoryIsBeingEditedByWarning', (editorid) => {
        this.editor = editorid
        $('#BeingEditedByWarningModal').modal('show')
      })

      EventBus.$on('storyIsBeingEditedWarning', () => {
        $('#storyIsBeingEditedWarningModal').modal('show')
      })

      EventBus.$on('closeSidebar', () => {
        if($(".page-wrapper").hasClass("toggled"))
        {
          $(".page-wrapper").toggleClass("toggled")
        }
      })

      EventBus.$on('shareLayerModalOpen', (layername) => {
        this.layerToShare = layername
        console.log(layername)
        console.log(this.internalLayers)
        this.layerSharedWith = this.internalLayers[layername].shared_with
        $('#shareLayerModal').modal('show')
      })
    },
    methods: {
      openPanel (){
        if (!this.$store.state.storyViewMode) {
          // this.$store.state.date_type_temp = ''
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
        $('input[type="file"]').val(null);
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
          EventBus.$emit('resetSelectedFeatures')
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
          EventBus.$emit('resetSelectedFeatures')
        }
      },
      changeLayerVisibility_allStoriesGeomsLayer () {
        this.$store.state.allStoriesGeomsLayer.visible = !this.$store.state.allStoriesGeomsLayer.visible
        if (this.$store.state.allStoriesGeomsLayer.visible) {
          this.$store.commit('RESTORE_ALL_USEDSTORIESGEOMETRIES')
        } else {
          EventBus.$emit('removeLayer', 'allStoriesGeomsLayer')
          EventBus.$emit('resetSelectedFeatures')
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
        var layerOptions
        if (layer.layername === this.allStoriesGeomsLayer.layername) {
          layerOptions = `<div class="layer-options">
                                <a class="dropdown-item` + disabled +`" id="` + this.allStoriesGeomsLayer.name + `_zoomto" href="#">Zoom to layer</a>
                              </div>`
        } else {
          if (layer.uploaded_by == this.userPK || this.isAdmin) {
            layerOptions = `<div class="layer-options">
                                  <a class="dropdown-item` + disabled +`" id="` + layer.name + `_zoomto" href="#">Zoom to layer</a>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.name + `_rename" href="#">Rename layer</a>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.name + `_restyle" href="#">Edit style</a>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.name + `_share" href="#">Share layer</a>
                                  <div class="dropdown-divider"></div>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.name + `_deleteLayer" href="#">Delete layer</a>
                                </div>`
          } else {
            layerOptions = `<div class="layer-options">
                                  <a class="dropdown-item` + disabled +`" id="` + layer.name + `_zoomto" href="#">Zoom to layer</a>
                                </div>`
          }
        }

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
        var storyOptions
        if (story.owner === this.username || this.isAdmin) {
          storyOptions = `<div class="layer-options">
                            <a class="dropdown-item" id="` + story.id + `_view" href="#">View narrative</a>
                            <a class="dropdown-item" id="` + story.id + `_edit" href="#">Edit narrative</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" id="` + story.id + `_deleteStory" href="#">Delete narrative</a>
                          </div>`

        } else if (story.co_authors.indexOf(this.userPK)>=0) {
          storyOptions = `<div class="layer-options">
                            <a class="dropdown-item" id="` + story.id + `_view" href="#">View narrative</a>
                            <a class="dropdown-item" id="` + story.id + `_edit" href="#">Edit narrative</a>
                          </div>`

        } else {
          storyOptions = `<div class="layer-options">
                            <a class="dropdown-item" id="` + story.id + `_view" href="#">View narrative</a>
                          </div>`
        }

        return storyOptions
      },
      reinitialisePopups () {
        $(function () {
          $('[data-toggle="popover"]').popover({
            boundary:'window',
            html: true
          })
        })
      },
      advancedFilterModal () {
        $('#advancedFilterModal').modal('show')
      },
      filterNarratives () {
        this.filteredStories = []

        each(this.stories, (story) => {
          var filterStory_byAtua
          var filterStory_byType
          var filterStory_byFreeText

          if (this.filter.freeText !== null && this.filter.freeText !== "") {
            filterStory_byFreeText = false
            if (JSON.stringify(story.title).toLowerCase().includes(this.filter.freeText.toLowerCase())) {
              filterStory_byFreeText = true
            }
            if (JSON.stringify(story.summary).toLowerCase().includes(this.filter.freeText.toLowerCase())) {
              filterStory_byFreeText = true
            }
            some(story.storyBodyElements, (elem) => {
              if (elem.element_type === 'TEXT') {
                if (JSON.stringify(elem.text).toLowerCase().includes(this.filter.freeText.toLowerCase())) {
                  filterStory_byFreeText = true
                }
              }
            })
          }

          if (this.filter.atua.length > 0) {
            var atuaInters = intersection(story.atua, this.filter.atua)
            if (atuaInters !== undefined && atuaInters.length !== 0) {
              filterStory_byAtua = true
            } else {
              filterStory_byAtua = false
            }
          }

          if (this.filter.storyType.length > 0) {
            if (this.filter.storyType.includes(story.story_type.id)) {
              filterStory_byType = true
            } else {
              filterStory_byType = false
            }
          }

          var filterStory = [filterStory_byAtua, filterStory_byType, filterStory_byFreeText]

          if (filterStory.every(element => element === undefined) || filterStory.includes(false)) {
            // do not filter the story
          } else {
            this.filteredStories.push(story)
          }
        })

        this.reinitialisePopups()

      },
      clearNarrativesFilter () {
        this.filteredStories = []
        this.filter = {
          atua: [],
          storyType: [],
          freeText: null
        }
      },
      dropdownSidebarDropdow (event) {
        $(".sidebar-submenu").slideUp(200)
        if ($(event.target).parent().hasClass("active")) {
          $(".sidebar-dropdown").removeClass("active")
          $(event.target).parent().removeClass("active")
        } else {
          $(".sidebar-dropdown").removeClass("active")
          $(event.target).next(".sidebar-submenu").slideDown(200)
          $(event.target).parent().addClass("active")
        }
      },
      setLayerSharedWith (value) {
        this.$refs.usersAutocomplete.inputValue = ''
        this.layerSharedWith.push(value.id)
        console.log(this.layerSharedWith)
        this.$store.dispatch('setLayerSharing', { 'layername': this.layerToShare, 'shared_with': this.layerSharedWith })
      },
      stopSharingLayerModalOpen (userid) {
        this.userToRemoveFromLayerSharing = userid
        $('#stopSharingLayerModal').modal('show')
      },
      setLayerSharedWithout (userid) {
        this.$refs.usersAutocomplete.inputValue = ''
        this.layerSharedWith=without(this.layerSharedWith, userid)
        console.log(this.layerSharedWith)
        this.$store.dispatch('setLayerSharing', { 'layername': this.layerToShare, 'shared_with': this.layerSharedWith })
      },
      onClose () {
        this.$refs.usersAutocomplete.inputValue = ''
      },
    }
  }

</script>
