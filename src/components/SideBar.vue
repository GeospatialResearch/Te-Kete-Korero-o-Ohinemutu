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
          <div v-if="authenticated" class="user-pic" @click="$store.commit('TOGGLE_CONTENT', 'profile')">
            <img v-if="avatar" class="img-responsive img-rounded" :src="mediaRoot + avatar" alt="User picture">
            <img v-else class="img-responsive img-rounded" src="static/img/user.jpg" alt="User picture">
          </div>
          <div v-if="authenticated" class="user-info">
            <span class="user-name">Welcome, <strong>{{ username }}</strong>
            </span>
            <span v-if="user.is_superuser" class="badge badge-pill badge-secondary mt-3 role-badge">Administrator</span>
            <span v-if="user.is_staff && !user.is_superuser" class="badge badge-pill badge-secondary mt-3 role-badge">Tool Manager</span>
          </div>
        </div>

        <!-- sidebar-menu  -->
        <div :class="[authenticated ? 'sidebar-item': '', 'sidebar-menu']">
          <div :class="[contentToShow == 'map' && authenticated ? 'dark-background': '', 'text-center pt-2']">
            <span v-if="getDataSpin" style="color:#c7c7c7;">
              <font-awesome-icon icon="sync-alt" spin />Loading...
            </span>
          </div>

          <ul>
            <!-- <li class="header-menu">
              <span>General</span>
            </li> -->
            <li v-if="contentToShow != 'map'" class="mt-4" @click="$store.commit('TOGGLE_CONTENT', 'map')">
              <a href="#">
                <!-- <i class="fa fa-map" /> using this one the icons shakes when hovering over the icon-->
                <i><font-awesome-icon icon="map" /></i>
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
                <span v-if="user && user.is_superuser" class="menu-text">Other layers</span>
                <span v-else class="menu-text">Internal layers</span>
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
                      <span class="inline-text">
                        <span v-if="layer.assigned_name" class="ml-2 ellipsis-text">{{ layer.assigned_name }}</span>
                        <span v-else class="ml-2 ellipsis-text">{{ layer.name }}</span>
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
                  <div class="form-control search-menu text-center label-info pointer" @click="searchModal()">
                    Search Narratives
                  </div>
                  <div class="input-group-append">
                    <span class="input-group-text">
                      <i aria-hidden="true"><font-awesome-icon icon="filter" /></i>
                    </span>
                  </div>
                </div>
              </div>
            </div>
          </ul>
        </div>
        <!-- sidebar-menu  -->
      </div>


      <!-- sidebar-footer  -->
      <div class="sidebar-footer">
        <div>
          <a href="#" title="Refresh data" @click="refresh()">
            <i v-if="getDataSpin"><font-awesome-icon icon="sync-alt" spin /></i>
            <i v-else><font-awesome-icon icon="sync-alt" /></i>
          </a>
        </div>
        <div class="dropdown">
          <a href="#" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
            <i><font-awesome-icon icon="cog" /></i>
            <!-- <span class="badge-sonar" /> -->
          </a>
          <div class="dropdown-menu" aria-labelledby="dropdownMenuMessage">
            <a v-if="authenticated" class="dropdown-item" href="#" @click="$store.commit('TOGGLE_CONTENT', 'profile')">My profile</a>
            <a v-if="authenticated" class="dropdown-item" href="#" @click="openWhanauSettings()">Whānau Page</a>
            <a v-if="authenticated && kaitiakis.includes(user.id)" class="dropdown-item" href="#" @click="openKaitiakiSettings()">Kaitiaki Page</a>
            <a v-if="authenticated && user && (user.is_superuser || user.is_staff)" class="dropdown-item" href="#" @click="openNestsSettings()">Nests settings Page</a>
            <a v-if="authenticated && user && (user.is_superuser || user.is_staff)" class="dropdown-item" href="#" @click="openUsersSettings()">Users settings Page</a>
            <!-- <a v-if="authenticated && user && (user.is_superuser || user.is_staff)" class="dropdown-item" href="#" @click="openUsersSettings()">Kaitiaki Page</a> -->
            <a class="dropdown-item" href="#">Help</a>
            <a class="dropdown-item" href="#" @click="$store.commit('TOGGLE_CONTENT', 'themes')">Look & Feel</a>
          </div>
        </div>
        <!-- <div>
          <a href="#">
            <i><font-awesome-icon icon="power-off" /></i>
          </a>
        </div> -->
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
    <div id="addCopyrightLayerModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Add copyright</h5>
          </div>
          <div class="modal-body">
            <div>
              <h6 class="mb-4">
                Add a copyright statement to your layer so the source can be acknowledged.
              </h6>
              <span class="text-muted">Examples: Sourced from ... and licensed for reuse under the licence ... | Created by user ...</span>
              <input v-model="layercopyrightText" required type="text" class="form-control form-control-sm mt-2" title="Add copyright">
            </div>
          </div>
          <div class="modal-footer">
            <div class="btn-group pull-right">
              <button type="button" class="btn btn-primary" data-dismiss="modal" @click="addCopyright()">
                Save
              </button>
            </div>
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
    <!-- <div id="advancedFilterModal" class="modal fade">
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
            <h6>By Type of Narrative</h6>
            <select v-model="filter.storyType" class="form-control form-control-sm mb-3" multiple title="Hold the Ctrl key to select more than one Type of Narrative" @change="filterNarratives()">
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
    </div> -->
    <div id="searchModal" class="modal fade">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Search Narratives</h5>
          </div>
          <div class="modal-body pl-5 pr-5">
            <div class="input-group input-group-sm">
              <input v-model="filter.freeText" type="text" class="form-control search-menu" placeholder="Type text to search...">
              <div class="input-group-append" title="Clear filter">
                <button class="btn btn-dark" type="button" @click="clearNarrativesFilter()">
                  <i aria-hidden="true"><font-awesome-icon icon="times" /></i>
                </button>
              </div>
              <div class="input-group-append" title="Advanced filter">
                <button class="btn btn-secondary" data-toggle="collapse" data-target="#advancedFilters">
                  <font-awesome-icon icon="filter" />
                </button>
              </div>
              <div class="input-group-append">
                <button class="btn btn-success" @click="filterStories(filter.freeText, filter.atua, filter.storyType)">
                  Search
                </button>
              </div>
            </div>
            <div id="advancedFilters" class="collapse pt-3 pb-0 ml-2">
              <div class="card card-body">
                <h6>By Atua</h6>
                <select v-model="filter.atua" class="form-control form-control-sm mb-3" multiple title="Hold the Ctrl key to select more than one Atua" @change="filterNarratives()">
                  <option v-for="item in allAtuas" :key="item.id" :value="item.id">
                    {{ item.name }}
                  </option>
                </select>
                <h6>By Type of Narrative</h6>
                <select v-model="filter.storyType" class="form-control form-control-sm mb-3" multiple title="Hold the Ctrl key to select more than one Type of Narrative" @change="filterNarratives()">
                  <option v-for="item in allStoryTypes" :key="item.id" :value="item.id">
                    {{ item.type }}
                  </option>
                </select>
              </div>
            </div>
            <div class="modal-body pt-5 pb-0 ml-2">
              <div v-if="filteredStories.length === 0">
                <div class="text-center">
                  <span>No narratives matching the filter</span>
                </div>
              </div>
              <div v-else>
                <div v-for="story in filteredStories" :key="story.id">
                  <div class="row pb-4">
                    <div class="col-sm-9">
                      <h6 class="text-muted">
                        <span title="Narrative title"><i><font-awesome-icon icon="book-open" /></i>&nbsp;&nbsp;{{ story.title.eng }}</span> &mdash; <small title="Type of Narrative"><i>{{ allStoryTypes.find(x => x.id == story.story_type).type }}</i></small>
                      </h6>
                      <h6 title="Narrative summary" class="ml-4">
                        <i>{{ story.summary.eng }}</i>
                      </h6>
                      <p class="ml-4">
                        <i v-if="authenticated && allUsers">
                          <small>Story by {{ allUsers.filter(x=>x.id === story.owner)[0].username }}</small>
                        </i>
                        <i class="ml-4">
                          <small><b>Contains: {{ story.contains[0] }}{{ story.contains[1] }}{{ story.contains[2] }}</b></small>
                        </i>
                      </p>
                    </div>
                    <div v-if="stories.filter(s=>s.id === story.id).length != 0" class="col-sm-3 text-center">
                      <button type="button" class="btn btn-sm btn-primary" title="Open narrative" @click="openNarrative(story.id)">
                        Open narrative
                      </button>
                    </div>
                    <div v-else class="col-sm-3 text-center">
                      <button type="button" disabled class="btn btn-sm btn-primary" title="Send mail">
                        Send <i class="fa fa-envelope" />
                      </button>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="closeSearchCollapse()">
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
          <div v-if="allOtherUsers" class="modal-body">
            <h5 class="mb-0">
              Users
            </h5>
            <div v-if="userPK">
              <vue-bootstrap-typeahead ref="usersAutocomplete" v-model="user_query" :serializer="s => s.username +' - '+ s.first_name +' '+ s.last_name" :data="allOtherUsers.filter(user=>!layerSharedWith.includes(user.id))" placeholder="Type a username" @hit="setLayerSharedWith($event)" />
              <div class="coauthor-box">
                <ul class="coauthor-list">
                  <li v-for="userid in layerSharedWith" :key="userid" class="coauthor col-md-12">
                    <div class="col-md-10">
                      <div class="user-image">
                        <img src="static/img/user.jpg">
                      </div>
                      {{ getAuthFullName(userid) }}
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
  // import { each, intersection, some, without } from 'underscore'
  import { each, without } from 'underscore'
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
        layercopyrightText: null,
        layerId: null,
        layerToDelete: null,
        storyToDelete: null,
        editor: null,
        filter: {
          atua: [],
          storyType: [],
          freeText: ''
        },
        filteredStories: [],
        myNarratives: [],
        otherNarratives: [],
        myLayers: [],
        defaultLayers: [],
        user_query:'',
        layerSharedWith: [],
        layerToShare: null,
        userToRemoveFromLayerSharing: null,
        mediaRoot: process.env.API_HOST,
        allOtherUsers: [],
        getDataSpin: false
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
      detectableStories(){
        return this.$store.state.detectableStories
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
      user () {
        return this.$store.state.user
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
          userpk = this.$store.state.user.id
        }
        return userpk
      },
      avatar () {
        var avatar
        if (this.$store.state.user) {
          if (this.$store.state.user.profile) {
            avatar = this.$store.state.user.profile.avatar
          }
        }
        return avatar
      },
      contentToShow () {
        return this.$store.state.contentToShow
      },
      kaitiakis(){
        return this.$store.state.kaitiakis
      }
    },
    watch: {
      stories: {
        handler: function () {
          try {
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
          } catch (e) {
            // Do nothing, this is fine.
          }
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
      },
      allUsers: {
        deep: true,
        handler: function (newVal) {
          var users
          if (this.$store.state.user) {
            users = newVal.filter(user=>(user.id!=this.userPK && user.id!=1))
          }
          this.allOtherUsers = users
        }
      }
    },
    mounted: function () {
      EventBus.$on('addCopyrightLayerModalOpen', (layerid) => {
        this.layerId = layerid
        this.layercopyrightText = this.$store.state.internalLayers[layerid].copyright_text
        $('#addCopyrightLayerModal').modal('show')
      })

      EventBus.$on('assignLayerNameModalOpen', (layerid) => {
        this.layerId = layerid
        this.layerAssignedName = this.$store.state.internalLayers[layerid].assigned_name
        $('#renameLayerModal').modal('show')
      })

      EventBus.$on('deleteLayerModalOpen', (layerid) => {
        this.layerToDelete = layerid
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

      EventBus.$on('shareLayerModalOpen', (layerid) => {
        this.layerToShare = layerid
        this.layerSharedWith = this.internalLayers[layerid].shared_with
        $('#shareLayerModal').modal('show')
      })
    },
    methods: {
      openPanel (){
        if (!this.$store.state.storyViewMode) {
          // this.$store.state.date_type_temp = ''
          $('#storyIsBeingEditedWarningModal').modal('show')
        } else {
          EventBus.$emit('initialiseBootstrapSelect')
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
              EventBus.$emit('addUploadedLayer', response.body)  // add argument false if you want to add geojson layer
            }
            this.$store.state.isUploadingData = false
            this.reset()
            EventBus.$emit('addCopyrightLayerModalOpen',response.body['id'])
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
          EventBus.$emit('createLayer', layer.id, 'internal')
        } else {
          EventBus.$emit('removeLayer', layer.gs_layername)
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
          if (layer.uploaded_by == this.userPK || (this.user && this.user.is_superuser)) {
            layerOptions = `<div class="layer-options">
                                  <a class="dropdown-item` + disabled +`" id="` + layer.gs_layername + `_zoomto" href="#">Zoom to layer</a>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.id + `_rename" href="#">Rename layer</a>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.id + `_copyright" href="#">Edit copyright</a>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.id + `_restyle" href="#">Edit style</a>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.id + `_share" href="#">Share layer</a>
                                  <div class="dropdown-divider"></div>
                                  <a class="dropdown-item` + disabled +`" id="` + layer.id + `_deleteLayer" href="#">Delete layer</a>
                                </div>`
          } else {
            layerOptions = `<div class="layer-options">
                                  <a class="dropdown-item` + disabled +`" id="` + layer.gs_layername + `_zoomto" href="#">Zoom to layer</a>
                                </div>`
          }
        }

        return layerOptions
      },
      addCopyright () {
        this.$store.dispatch('addCopyrightText', { layerid: this.layerId, copyrightText: this.layercopyrightText })
      },
      assignNewName () {
        this.$store.dispatch('renameLayer', { layerid: this.layerId, assignedName: this.layerAssignedName })
      },
      deleteLayer () {
        var gs_layername = this.internalLayers[this.layerToDelete].gs_layername
        this.$store.dispatch('deleteLayer', {'gs_layername': gs_layername, 'layerid': this.layerToDelete} )
        .then(() => {
          EventBus.$emit('removeLayer', gs_layername)
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
        // if (story.owner === this.username || (this.user && this.user.is_superuser)) {
        //   storyOptions = `<div class="layer-options">
        //                     <a class="dropdown-item" id="` + story.id + `_view" href="#">View narrative</a>
        //                     <a class="dropdown-item" id="` + story.id + `_edit" href="#">Edit narrative</a>
        //                     <div class="dropdown-divider"></div>
        //                     <a class="dropdown-item" id="` + story.id + `_deleteStory" href="#">Delete narrative</a>
        //                   </div>`
        //
        // } else if (story.co_authors.indexOf(this.userPK)>=0) {
        //   storyOptions = `<div class="layer-options">
        //                     <a class="dropdown-item" id="` + story.id + `_view" href="#">View narrative</a>
        //                     <a class="dropdown-item" id="` + story.id + `_edit" href="#">Edit narrative</a>
        //                   </div>`
        //
        // } else {
        //   storyOptions = `<div class="layer-options">
        //                     <a class="dropdown-item" id="` + story.id + `_view" href="#">View narrative</a>
        //                   </div>`
        // }

        if (story.owner === this.username || (this.user && this.user.is_superuser)) {
          storyOptions = `<div class="layer-options">
                            <a class="dropdown-item" id="` + story.id + `_view" href="#">View narrative</a>
                            <div class="dropdown-divider"></div>
                            <a class="dropdown-item" id="` + story.id + `_deleteStory" href="#">Delete narrative</a>
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
      filterNarratives () {
        // this.filteredStories = []
        //
        // each(this.stories, (story) => {
        //   var filterStory_byAtua
        //   var filterStory_byType
        //   var filterStory_byFreeText
        //
        //   if (this.filter.freeText !== null && this.filter.freeText !== "") {
        //     filterStory_byFreeText = false
        //     if (JSON.stringify(story.title).toLowerCase().includes(this.filter.freeText.toLowerCase())) {
        //       filterStory_byFreeText = true
        //     }
        //     if (JSON.stringify(story.summary).toLowerCase().includes(this.filter.freeText.toLowerCase())) {
        //       filterStory_byFreeText = true
        //     }
        //     some(story.storyBodyElements, (elem) => {
        //       if (elem.element_type === 'TEXT') {
        //         if (JSON.stringify(elem.text).toLowerCase().includes(this.filter.freeText.toLowerCase())) {
        //           filterStory_byFreeText = true
        //         }
        //       }
        //     })
        //   }
        //
        //   if (this.filter.atua.length > 0) {
        //     var atuaInters = intersection(story.atua, this.filter.atua)
        //     if (atuaInters !== undefined && atuaInters.length !== 0) {
        //       filterStory_byAtua = true
        //     } else {
        //       filterStory_byAtua = false
        //     }
        //   }
        //
        //   if (this.filter.storyType.length > 0) {
        //     if (this.filter.storyType.includes(story.story_type.id)) {
        //       filterStory_byType = true
        //     } else {
        //       filterStory_byType = false
        //     }
        //   }
        //
        //   var filterStory = [filterStory_byAtua, filterStory_byType, filterStory_byFreeText]
        //
        //   if (filterStory.every(element => element === undefined) || filterStory.includes(false)) {
        //     // do not filter the story
        //   } else {
        //     this.filteredStories.push(story)
        //   }
        // })
        //
        // this.reinitialisePopups()

      },
      clearNarrativesFilter () {
        this.filteredStories = []
        this.filter = {
          atua: [],
          storyType: [],
          freeText: ''
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
        this.$store.dispatch('setLayerSharing', { 'layerid': this.layerToShare, 'shared_with': this.layerSharedWith })
      },
      stopSharingLayerModalOpen (userid) {
        this.userToRemoveFromLayerSharing = userid
        $('#stopSharingLayerModal').modal('show')
      },
      setLayerSharedWithout (userid) {
        this.$refs.usersAutocomplete.inputValue = ''
        this.layerSharedWith=without(this.layerSharedWith, userid)
        this.$store.dispatch('setLayerSharing', { 'layerid': this.layerToShare, 'shared_with': this.layerSharedWith })
      },
      onClose () {
        this.$refs.usersAutocomplete.inputValue = ''
      },
      openWhanauSettings () {
        this.getData()
        this.$store.commit('TOGGLE_CONTENT', 'whanau')
      },
      openKaitiakiSettings () {
        this.getData()
        this.$store.commit('TOGGLE_CONTENT', 'kaitiaki')
      },
      openNestsSettings () {
        this.getData()
        this.$store.commit('TOGGLE_CONTENT', 'nests')
      },
      openUsersSettings () {
        this.getDataSpin = true
        this.getData()
        this.$store.commit('TOGGLE_CONTENT', 'users')
        this.getDataSpin = false
      },
      getData () {
        this.$store.dispatch('getUsers')
        this.$store.dispatch('getProfiles')
        this.$store.dispatch('getSectors')
        this.$store.dispatch('getNests')
        this.$store.dispatch('getUser') // to update user invitations
        this.$store.dispatch('getKaitiakis') // to update nest's kaitiakis
        this.$store.dispatch('getAllPublications') // to get all publications
        this.$store.dispatch('getStoryReviews') // to get story reviews
      },
      refresh () {
        this.getDataSpin = true
        this.getData()
        this.getDataSpin = false
      },
      openNarrative(story_id){
        // close the modal
        $('#searchModal').modal('hide')
        if (!this.$store.state.storyViewMode) {
          EventBus.$emit('storyIsBeingEditedWarning')
        } else {
          this.$store.dispatch('getStoryContent', story_id)
          .then((story) => {
            this.$store.commit('SET_STORY_VIEW_MODE', true)
            this.$store.commit('SET_PANEL_OPEN', true)
            EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)
          })
        }
      },
      searchModal () {
        this.clearNarrativesFilter()
        $('#searchModal').modal('show')
      },
      filterStories (text, atua, storytype){
        this.$store.dispatch('filterStories', { 'text': text, 'atua': atua, 'storytype':storytype})
        .then((response) => {
          this.filteredStories = response.body
        })
      },
      closeSearchCollapse(){
        $('#advancedFilters').collapse('hide');
      },
      getAuthFullName(userid){
        let author = this.allOtherUsers.filter(user=>user.id === userid)[0]
        return `${author.username} ( ${author.first_name} ${author.last_name} )`
      }
    }
  }

</script>
