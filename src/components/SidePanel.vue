<template>
  <div id="sidePanel" :class="[getOrientation === 'portrait' ? {'col-sm-12 col-xs-12':togglePanel, 'col-sm-0 col-xs-0':!togglePanel} : {'col-sm-5 col-xs-5':togglePanel, 'col-sm-0 col-xs-0':!togglePanel}]">
    <div class="d-flex flex-md-row justify-content-between m-0 p-0 pb-2 sticky bottom-shadow">
      <div class="col-md-6 p-0">
        <div class="mt-3 pl-3">
          <div class="form-check form-check-inline">
            <input id="inlineRadio1" v-model="storyLang" class="form-check-input" type="radio" name="optstorylang" value="eng" @change="onChangeStoryLang()">
            <label class="form-check-label" for="inlineRadio1">English</label>
          </div>
          <div class="form-check form-check-inline">
            <input id="inlineRadio2" v-model="storyLang" class="form-check-input" type="radio" name="optstorylang" value="mao" @change="onChangeStoryLang()">
            <label class="form-check-label" for="inlineRadio2">Te Reo</label>
          </div>
        </div>
      </div>
      <div class="col-md-6 btn p-0 pr-3">
        <font-awesome-icon icon="times" class="float-right mt-2" size="2x" @click="closeStory()" />
      </div>
    </div>

    <div v-if="isStoryViewMode" class="mb-3">
      <!-- view mode -->
      <div class="pl-3 pr-3 pt-4 printme_1" style="background-color:#ffffff;">
        <span class="badge badge-warning mb-2 p-2 pointer" title="Show narrative status" @click="showNarrativeInfoOpenModal()">
          <font-awesome-icon icon="info-circle" />
          Narrative status
        </span>
        <span v-if="story.story_type" class="badge badge-success mb-2 p-2 float-right" title="Type of Narrative">{{ story.story_type.type }}</span>
        <div title="Story Date">
          <p v-if="story.approx_time.type === 'PRECISE_DATE'" class="badge badge-light mb-2 p-2 float-right">
            {{ story.approx_time.date }}
          </p>
          <div v-if="story.approx_time.type === 'YEAR_RANGE'">
            <p v-if="story.approx_time.end_time" class="badge badge-light mb-2 p-2 float-right">
              {{ story.approx_time.start_time }} - {{ story.approx_time.end_time }}
            </p>
            <p v-else class="badge badge-light mb-2 p-2 float-right">
              {{ story.approx_time.start_time }} - present
            </p>
          </div>
          <p v-if="story.approx_time.type === 'PRECISE_YEAR'" class="badge badge-light mb-2 p-2 float-right">
            {{ story.approx_time.year }}
          </p>
          <p v-if="story.approx_time.type === 'TIMELESS'" class="badge badge-light mb-2 p-2 float-right">
            Timeless
          </p>
        </div>
        <div class="mt-5">
          <div v-if="story.title">
            <div v-show="storyLang === 'eng'">
              <h4 title="Story title">
                <span v-if="story.title.eng">{{ story.title.eng }}</span>
                <span v-else class="text-muted font-italic">No title defined in English</span>
              </h4>
              <p class="story-summary" title="Story summary">
                <span v-if="story.summary.eng">{{ story.summary.eng }}</span>
                <span v-else class="text-muted font-italic">No summary defined in English</span>
              </p>
            </div>
            <div v-show="storyLang === 'mao'">
              <h4 title="Story title">
                <span v-if="story.title.mao">{{ story.title.mao }}</span>
                <span v-else class="text-muted font-italic">No title defined in Te Reo</span>
              </h4>
              <p class="story-summary" title="Story summary">
                <span v-if="story.summary.mao">{{ story.summary.mao }}</span>
                <span v-else class="text-muted font-italic">No summary defined in Te Reo</span>
              </p>
            </div>
          </div>
          <p class="font-italic mb-0">
            <small>&mdash; Story by {{ story.owner }}</small>
            <span v-if="story.co_authors && story.co_authors.length > 0">
              <small>, Co-created with</small>
              <small v-for="(auth, i) in storyCoAuthors" :key="auth.id">
                <span v-if="i!=0">,</span>
                {{ auth.username }}
              </small>
            </span>
          </p>
          <div v-if="story.atua" class="float-right" style="font-size:13px;">
            Atua:
            <i v-for="atua in allAtuas" :key="atua.id">
              <strong v-if="story.atua.includes(atua.id)" :key="atua.id">
                {{ atua.name }}&nbsp;
              </strong>
            </i>
          </div>
          <p v-if="isStoryViewMode && story.comments" class="text-muted mt-4 pointer" style="font-size:13px;">
            <span @click="seeComments()">
              <font-awesome-icon icon="comments" />
              Comments ({{ story.comments.length }})
            </span>
          </p>
          <hr class="mt-1">
        </div>
      </div>

      <div v-for="element in story.storyBodyElements" :key="element.id" class="col-md-12 pl-4 pr-4 pb-2">
        <font-awesome-icon v-if="element.content_type" disabled icon="info-circle" color="grey" class="pointer float-right" :title="element.content_type.type" />
        <div :class="element.content_type?'mr-4':''">
          <div v-if="element.element_type == 'TEXT'" class="printme_1">
            <div v-show="storyLang === 'eng'" class="ql-text mb-4" v-html="element.texteng" />
            <div v-show="storyLang === 'mao'" class="ql-text mb-4" v-html="element.textmao" />
          </div>
          <div v-if="element.element_type == 'GEOM'">
            <div :id="element.geom_attr.id" class="story-elem-geom pointer text-center m-4 p-1" title="Zoom to geometry" @click="zoomToGeometry(element)">
              <i><font-awesome-icon icon="map-marked-alt" size="lg" class="pointer" /></i>&nbsp;
              <strong v-show="storyLang === 'eng'">
                <span v-if="element.geom_attr.name.eng">{{ element.geom_attr.name.eng }}</span>
                <span v-else class="text-muted font-italic">No name defined in English</span>
              </strong>
              <strong v-show="storyLang === 'mao'">
                <span v-if="element.geom_attr.name.mao">{{ element.geom_attr.name.mao }}</span>
                <span v-else class="text-muted font-italic">No name defined in Te Reo</span>
              </strong>
            </div>
          </div>
          <div class="align-center">
            <div v-if="element.element_type == 'IMG'" class="printme_1">
              <img :src="mediaRoot + element.mediafile_name" class="story-elem-img img-fluid">
              <span class="fa-stack fa-1x positioner-magnify" @click="magnifyImage(element)">
                <i class="fa fa-circle fa-stack-2x icon-background" />
                <i class="fa fa-search-plus fa-stack-1x" />
              </span>
            </div>

            <video v-if="element.element_type == 'VIDEO'" controls controlsList="nodownload" class="story-elem-video">
              <source :src="mediaRoot + element.mediafile_name" type="video/mp4">
              Your browser does not support the video tag.
            </video>
            <audio v-if="element.element_type == 'AUDIO'" controls controlsList="nodownload">
              <source :src="mediaRoot + element.mediafile_name" type="audio/mpeg">
              Your browser does not support the audio element.
            </audio>
            <div class="printme_1">
              <p v-if="element.element_type != 'TEXT' && storyLang === 'eng' && element.media_description" class="media-caption">
                {{ element.media_description.eng }}
              </p>
              <p v-if="element.element_type != 'TEXT' && storyLang === 'mao' && element.media_description" class="media-caption">
                {{ element.media_description.mao }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </div>
    <div v-else class="pl-3 pr-3 mt-3">
      <!-- edit mode -->
      <form :id="story.id + '_storyform'">
        <div class="row col-md-12">
          <h5 class="mb-0">
            Title
          </h5>
          <input v-show="storyLang === 'eng'" v-model="story.titleeng" required type="text" class="form-control form-control-sm mb-3" placeholder="Title">
          <input v-show="storyLang === 'mao'" v-model="story.titlemao" :required="(story.titleeng == null || story.titleeng == '') ? true : false" type="text" class="form-control form-control-sm mb-3" placeholder="Taitara">
          <div class="invalid-feedback">
            Title is mandatory
          </div>

          <h5 class="mb-0">
            Date
          </h5>
          <span class="text-muted pl-1" @click="showUserManualModal('DateTheNarrative')"><font-awesome-icon icon="info-circle" class="pointer" /></span>
          <select v-model="story.approx_time.type" required class="selectpicker form-control form-control-sm mb-3" @change="onChange">
            <option key="SELECT" value="" selected disabled>
              Select date type
            </option>
            <option key="PRECISE_DATE" value="PRECISE_DATE">
              Precise date
            </option>
            <option key="YEAR_RANGE" value="YEAR_RANGE">
              Year range
            </option>
            <option key="PRECISE_YEAR" value="PRECISE_YEAR">
              Precise year
            </option>
            <option key="TIMELESS" value="TIMELESS">
              Timeless
            </option>
          </select>
          <div v-if="story.approx_time.type === 'PRECISE_DATE'" class="container">
            <div class="row col-md-12 text-center">
              <div class="col-md-3" />
              <div class="form-group col-md-6">
                <input v-model="story.approx_time.date" required type="date" class="form-control form-control-sm" title="Date">
              </div>
              <div class="col-md-3" />
            </div>
          </div>

          <div v-if="story.approx_time.type === 'YEAR_RANGE'" class="container">
            <div class="row col-md-12">
              <div class="form-group col-md-6">
                <input v-model="story.approx_time.start_time" required min="1" max="2020" type="number" class="form-control form-control-sm" title="Start date" placeholder="Start (year)">
              </div>
              <div class="form-group col-md-6">
                <input v-model="story.approx_time.end_time" :disabled="!story.approx_time.start_time" :min="story.approx_time.start_time" max="2020" type="number" class="form-control form-control-sm" title="End date" placeholder="End (year)">
                <div class="invalid-feedback">
                  The end date must be equal or greater than the start date.
                </div>
              </div>
            </div>
          </div>

          <div v-if="story.approx_time.type === 'PRECISE_YEAR'" class="container">
            <div class="row col-md-12 text-center">
              <div class="col-md-3" />
              <div class="form-group col-md-6">
                <input v-model="story.approx_time.year" required min="1" max="2020" type="number" class="form-control form-control-sm" title="Year" placeholder="year">
              </div>
            </div>
          </div>
          <h5 class="mt-0.5 mb-0">
            Type of Narrative
          </h5>
          <span class="text-muted pl-1" @click="showUserManualModal('NarrativeType')"><font-awesome-icon icon="info-circle" class="pointer" /></span>
          <select v-model="story.story_type_id" required class="selectpicker form-control form-control-sm mb-3">
            <option key="SELECT" value="" selected disabled>
              Select type of narrative
            </option>
            <option v-for="item in allStoryTypes" :key="item.id" :value="item.id">
              {{ item.type }}
            </option>
          </select>

          <h5 v-if="story.atua" class="mb-0">
            Atua
          </h5>
          <span class="text-muted pl-1" @click="showUserManualModal('Atua')"><font-awesome-icon icon="info-circle" class="pointer" /></span>
          <select v-model="story.atua" required class="selectpicker form-control form-control-sm mb-3" multiple title="Hold the Ctrl key to select more than one Atua">
            <option v-for="item in allAtuas" :key="item.id" :value="item.id">
              {{ item.name }}
            </option>
          </select>

          <h5 class="mb-0">
            Summary
          </h5>
          <textarea v-show="storyLang === 'eng'" v-model="story.summaryeng" required class="form-control form-control-sm" rows="3" placeholder="Summary" />
          <textarea v-show="storyLang === 'mao'" v-model="story.summarymao" :required="(story.summaryeng == null || story.summaryeng == '') ? true : false" class="form-control form-control-sm" rows="3" placeholder="Whakarāpopototanga" />
          <div class="invalid-feedback">
            Summary is mandatory
          </div>
          <div class="form-group pt-4 mb-0 pl-1">
            <div class="custom-control custom-checkbox">
              <input id="customControlInline" v-model="story.is_detectable" type="checkbox" class="custom-control-input">
              <label class="custom-control-label" for="customControlInline">Yes, I want the story to be detectable (it can be searched but only the title and summary are visible)</label>
            </div>
          </div>
        </div>
      </form>

      <hr>
      <p class="text-muted">
        <!-- <font-awesome-icon icon="info-circle" /> -->
        <span class="text-muted pl-1" @click="showUserManualModal('AddElementsToYourNarrative')"><font-awesome-icon icon="info-circle" class="pointer" /></span>
        Use the button below to add new elements to the story and reorder the elements dragging and dropping them.
      </p>
      <div class="btn-group dropright mb-4">
        <button type="button" :disabled="isDrawMode || isGeomMediaMode || isReuseMode" class="btn btn-primary btn-sm dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
          Add element to the story
        </button>
        <div class="dropdown-menu">
          <a class="dropdown-item" href="#" @click="addEmptyVueEditor()">New Text field</a>
          <a class="dropdown-item" href="#" @click="uploadFileClicked(isGeomMedia=false)">Upload Media file</a>
          <a class="dropdown-item" href="#" @click="drawGeometry()">Draw map geometry</a>
          <a class="dropdown-item" href="#" @click="reuseGeometry()">Reuse map geometry</a>
        </div>
      </div>

      <div class="row col-md-12 pl-5">
        <draggable v-model="story.storyBodyElements" class="width-inherit" ghost-class="ghost" handle=".handle" @start="dragging = true" @end="dragging = false">
          <div v-for="element in story.storyBodyElements" :key="element.id" class="row mb-2">
            <div class="col-md-11 mt-3">
              <div class="text-center handle">
                <span class="btn btn-sm btn-secondary drag-element handle">
                  Drag me&nbsp;
                  <i><font-awesome-icon icon="arrows-alt" /></i>
                </span>
              </div>
              <div v-if="element.element_type == 'GEOM'">
                <div class="story-elem-geom text-center">
                  <button type="button" class="btn pr-0" title="Zoom to geometry" @click="zoomToGeometry(element)">
                    <i><font-awesome-icon icon="map-marked-alt" class="pointer" />&nbsp;</i>
                  </button>
                  <strong v-show="storyLang === 'eng'">
                    <span v-if="element.geom_attr.name.eng">{{ element.geom_attr.name.eng }}</span>
                    <span v-else class="text-muted font-italic">No name defined in English</span>
                  </strong>
                  <strong v-show="storyLang === 'mao'">
                    <span v-if="element.geom_attr.name.mao">{{ element.geom_attr.name.mao }}</span>
                    <span v-else class="text-muted font-italic">No name defined in Te Reo</span>
                  </strong>
                  <button type="button" class="btn pr-0" title="Edit geometry" @click="editGeometry(element.geom_attr)">
                    <i><font-awesome-icon icon="edit" /></i>
                  </button>
                  <button type="button" class="btn p-0" title="Edit geometry style" @click="editGeometryStyle(element.geom_attr)">
                    <i><font-awesome-icon icon="paint-brush" /></i>
                  </button>
                  <button type="button" class="btn pl-0" title="Manage media about the geometry" @click="manageGeomAttrMedia(element.geom_attr)">
                    <i><font-awesome-icon icon="images" /></i>
                  </button>
                </div>
              </div>
              <div v-if="element.element_type == 'TEXT'">
                <div v-show="storyLang === 'eng'" class="container">
                  <vue-editor v-model="element.texteng" required :editor-toolbar="customToolbar" class="custom-ql-editor" placeholder="Text" />
                </div>
                <div v-show="storyLang === 'mao'" class="container">
                  <vue-editor v-model="element.textmao" :editor-toolbar="customToolbar" class="custom-ql-editor" placeholder="Kuputuhi" />
                </div>
              </div>
              <div class="align-center">
                <img v-if="element.element_type == 'IMG'" :src="mediaRoot + element.mediafile_name" class="story-elem-img img-fluid">
                <video v-if="element.element_type == 'VIDEO'" controls controlsList="nodownload" class="story-elem-video">
                  <source :src="mediaRoot + element.mediafile_name" type="video/mp4">
                  Your browser does not support the video tag.
                </video>
                <audio v-if="element.element_type == 'AUDIO'" controls controlsList="nodownload" class="story-elem-video">
                  <source :src="mediaRoot + element.mediafile_name" type="audio/mpeg">
                  Your browser does not support the audio element.
                </audio>
              </div>
              <!-- <textarea v-if="!['TEXT','GEOM'].includes(element.element_type)" v-model="element.media_description" rows="1" class="form-control form-control-sm mt-1" title="Media description" placeholder="Media description (optional)" /> -->
              <div v-if="element.media_description">
                <div v-show="storyLang === 'eng'" class="container">
                  <textarea v-if="!['TEXT','GEOM'].includes(element.element_type)" v-model="element.media_description.eng" rows="1" class="form-control form-control-sm mt-1" title="Media description" placeholder="Media description (optional)" />
                </div>
                <div v-show="storyLang === 'mao'" class="container">
                  <textarea v-if="!['TEXT','GEOM'].includes(element.element_type)" v-model="element.media_description.mao" rows="1" class="form-control form-control-sm mt-1" title="Media description" placeholder=" Whakaahuatanga pāpāho (kōwhiringa)" />
                </div>
              </div>
            </div>
            <div class="col-md-1 delete-element">
              <font-awesome-icon disabled icon="cog" size="lg" color="grey" class="pointer" title="Settings" @click="settingsElementModal(element)" />
              <font-awesome-icon disabled icon="times-circle" size="lg" color="grey" class="pointer ml-2" title="Delete element" @click="deleteElementModal(element)" />
            </div>
          </div>
        </draggable>
      </div>
    </div>

    <div class="row mr-2">
      <div class="col-md-12">
        <p class="scroll-story-top float-right" @click="scrollStoryTop()">
          Scroll top
        </p>
      </div>
    </div>

    <div v-if="story.id" class="row">
      <div class="col-md-12 ml-3 mb-2">
        <p class="date sub-text-grey mb-0">
          Story added on {{ story.created_date | moment("MMMM Do, YYYY") }}
        </p>
        <p class="date sub-text-grey mb-0">
          Last edit on {{ story.modified_date | moment("MMMM Do, YYYY") }}
        </p>
      </div>
    </div>

    <hr v-if="isStoryViewMode" class="m-0">
    <comments-view v-if="isStoryViewMode" id="comments" />

    <div class="clear" :style="isStoryViewMode? 'background-color:#ffffff;' : ''" />

    <div :class="[getOrientation === 'portrait' ? {'col-md-12 visible':togglePanel, 'col-md-0 invisible':!togglePanel} :{'col-md-5 visible':togglePanel, 'col-md-0 invisible':!togglePanel},'row sidepanel-footer ml-0']">
      <div class="row m-0">
        <div class="col-xs-10">
          <button v-if="story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-sm btn-success" @click="saveStory()">
            Update story
          </button>
          <button v-if="!story.hasOwnProperty('id') && !isStoryViewMode" type="button" class="btn btn-sm btn-success" @click="saveStory()">
            Save story
          </button>
          <button v-if="!isStoryViewMode" type="button" class="btn btn-sm btn-danger ml-2" @click="showCancelStorySavingModal()">
            Cancel
          </button>
          <button v-if="story.hasOwnProperty('id') && isStoryViewMode && (story.owner === username || (user && user.is_superuser) || story.co_authors.indexOf(userPK) >= 0)" type="button" class="btn btn-sm btn-primary" @click="editStory()">
            <font-awesome-icon icon="pen" />
            Edit story
          </button>
          <div v-if="isStoryViewMode && (story.owner === username || (user && user.is_superuser))" class="btn-group btn-group-sm dropup">
            <button type="button" class="btn btn-sm btn-primary dropdown-toggle" data-toggle="dropdown" aria-haspopup="true" aria-expanded="false">
              <font-awesome-icon icon="share-alt" class="mr-2" />
            </button>
            <div v-if="story" class="dropdown-menu">
              <a class="dropdown-item" href="#" @click="inviteCoAuthorOpenModal()">Co-create narrative</a>
              <a class="dropdown-item" href="#" @click="setStoryPublicationOpenModal('submit')">Submit narrative</a>
              <a v-if="publishedGroups && publishedGroups.length >0" class="dropdown-item" href="#" @click="setStoryUnPublicationOpenModal('unpublish')">Unpublish narrative</a>
              <!-- <a class="dropdown-item" href="#" @click="setStoryPublicationOpenModal('publish')">Publish narrative</a> -->
            </div>
          </div>
          <button v-if="story.hasOwnProperty('id') && isStoryViewMode" type="button" class="btn btn-sm btn-primary" @click="printStory(story.title)">
            <font-awesome-icon icon="print" />
            Print
          </button>
          <button v-if="isStoryViewMode" type="button" class="btn btn-sm btn-success" @click="seeComments()">
            <font-awesome-icon icon="comments" />
            Comments
          </button>
          <button v-if="isStoryViewMode" type="button" class="btn btn-sm btn-secondary" @click="closeStory()">
            <font-awesome-icon icon="times" />
            Close
          </button>
        </div>
      </div>
    </div>

    <!-- modals -->
    <div id="uploadFileModal" class="modal" data-backdrop="static">
      <div class="modal-dialog" role="document">
        <div class="modal-content">
          <div class="modal-header">
            <h5 class="modal-title">
              Upload file (video/audio/image)
            </h5>
            <button v-show="!uploadingMedia" type="button" class="close" data-dismiss="modal" aria-label="Close">
              <span aria-hidden="true">&times;</span>
            </button>
          </div>
          <div class="modal-body">
            <form v-if="!uploadError" enctype="multipart/form-data" novalidate>
              <div class="dropbox">
                <input type="file" :name="uploadFieldName" class="input-file" @change="fileChange($event.target.files)">
                <p v-if="!uploadedFile && !uploadingMedia">
                  Click to browse or drop a media file here
                </p>
                <p v-if="uploadedFile && !uploadingMedia">
                  {{ uploadedFile.name }}
                </p>
                <div v-if="uploadingMedia">
                  <p class="uploadmedia-loading p-4 mt-2 mb-0" />
                  <p class="p-0">
                    Uploading media... <span>{{ uploadMediaProgress }}%</span>
                  </p>
                </div>
              </div>
              <h6 class="mb-1 mt-3">
                Media description (optional)
              </h6>
              <div v-show="storyLang === 'eng'" class="container">
                <textarea v-model="tempMediaDescriptionEng" class="form-control form-control-sm" title="Media description" placeholder="Media description (optional)" />
              </div>
              <div v-show="storyLang === 'mao'" class="container">
                <textarea v-model="tempMediaDescriptionMao" class="form-control form-control-sm" title="Media description" placeholder="Whakaahuatanga pāpāho (kōwhiringa)" />
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
            <span v-show="!uploadingMedia" class="btn btn-secondary" data-dismiss="modal" @click="cancelAddMediaElement()">
              <span v-if="!uploadError">Cancel</span>
              <span v-else>Close</span>
            </span>
            <button v-if="!uploadError && !isGeomMedia" :disabled="!uploadedFile" type="button" class="btn btn-primary wait-for-media" data-dismiss="modal" @click="addMediaElement()">
              Add media to story
            </button>
            <button v-if="!uploadError && isGeomMedia" :disabled="!uploadedFile" type="button" class="btn btn-primary wait-for-media" data-dismiss="modal" @click="addGeomAttrMedia()">
              Add media to geometry
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="inviteCoAuthorModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Invite Co-authors</h4>
          </div>
          <div v-if="allOtherUsers" class="modal-body">
            <!-- <div v-if="story.length > 0"> -->
            <h5 v-if="allOtherUsers" class="mb-0">
              Users
            </h5>
            <div v-if="userPK">
              <vue-bootstrap-typeahead ref="usersAutocomplete" v-model="query" :serializer="s => s.username +' - '+ s.first_name +' '+ s.last_name" :data="allOtherUsers.filter(user=>!coAuthors.includes(user.id))" placeholder="Type a co-author's name" @hit="setCoAuthors($event)" />
              <div class="coauthor-box">
                <ul class="coauthor-list">
                  <li v-for="item in coAuthors" :key="item" class="coauthor col-md-12">
                    <div class="col-md-10 center-content-vertically">
                      <div class="user-image">
                        <img v-if="getAuthAvatar(item)" class="img-responsive" :src="mediaRoot + getAuthAvatar(item)" alt="User picture">
                        <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                      </div>
                      <span>{{ getAuthFullName(item) }}</span>
                    </div>
                    <div class="col-md-2 vertical-align-middle">
                      <font-awesome-icon icon="times-circle" size="lg" color="grey" class="float-right" @click="deleteCoAuthorModalOpen(item)" />
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

    <div id="deleteCoAuthorModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content delete-coauthor-modal">
          <div class="modal-header">
            <h5>Remove Co-author</h5>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to remove co-author {{ coauthorToDelete?allOtherUsers.filter(user=>user.id === coauthorToDelete)[0].username:'' }}?</p>
            <p>
              This user will no longer be able to edit your narrative.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="removeCoAuthor(coauthorToDelete)">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="cantdeleteCoauthorWarningModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content modal-margin-top">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <h6>Currently this story is being edited by {{ editor?allUsers.filter(user=>user.id === editor)[0].username:'' }}, so you can't delete now, please come back later.</h6>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Close
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="settingsElementModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Settings</h4>
          </div>
          <div class="modal-body">
            <!-- <div v-if="story.length > 0"> -->
            <h5 v-if="allElementContentTypes" class="mb-0">
              Content Type
            </h5>
            <select v-model="elementContentType" class="form-control form-control-sm">
              <option key="SELECT" value="" selected disabled>
                Select content type
              </option>
              <option v-for="item in allElementContentTypes" :key="item.id" :value="item.id">
                {{ item.type }}
              </option>
            </select>
            <!-- </div> -->
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="setElementContentType()">
              Done
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="deleteElementModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h5>Delete element</h5>
          </div>
          <div class="modal-body">
            <p>Are you sure you want to delete this element?</p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="deleteElement()">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="editingWarningModal" class="modal fade">
      <div class="modal-dialog">
        <div :class="[isDrawMode ? ' modal-margin-top': '', 'modal-content']">
          <div class="modal-header">
            <h5>Attention</h5>
          </div>
          <div class="modal-body text-center">
            <div v-if="isDrawMode">
              <h6>The map drawing interaction is active, please stop drawing before close the story.</h6>
            </div>
            <div v-else>
              <h6>Don't forget to save changes before closing the story panel.</h6>
              <h6>Are you sure you want to cancel editing?</h6>
            </div>
          </div>
          <div class="modal-footer">
            <div v-if="isDrawMode" class="btn btn-secondary btn-ok" data-dismiss="modal">
              Got it!
            </div>
            <div v-else>
              <button type="button" class="btn btn-danger" data-dismiss="modal">
                No
              </button>
              <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="cancelStorySaving()">
                Yes
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="magnifyImageModal" class="modal fade">
      <div class="modal-dialog modal-xl">
        <div class="modal-content">
          <div class="modal-body text-center pt-5 magnify-modal">
            <img v-if="magnifyImageElem" :src="mediaRoot + magnifyImageElem.mediafile_name" class="story-elem-img mb-3" style="width:1000px;">
            <p v-if="magnifyImageElem">
              <span v-show="storyLang === 'eng'">
                {{ magnifyImageElem.media_description.eng }}
              </span>
              <span v-show="storyLang === 'mao'">
                {{ magnifyImageElem.media_description.mao }}
              </span>
            </p>
          </div>
          <div class="modal-footer">
            <div class="btn btn-secondary btn-ok" data-dismiss="modal">
              Close
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="geomsUsageModal" class="modal fade">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h3 class="mb-0">
              Features in Cultural Narratives
              <p class="mb-0 mt-2 modal-header-description">
                Check out the features you clicked on and the related cultural narratives
              </p>
            </h3>
          </div>
          <div class="modal-body pt-0 pb-0 ml-2">
            <div v-for="usage in geomsUsage" :key="usage.geomAttr.id" class="mt-4">
              <h6 title="Feature name">
                <strong><i><font-awesome-icon icon="map-marked-alt" /></i>&nbsp;&nbsp;{{ usage.geomAttr.name.eng }}</strong>
              </h6>
              <div class="row">
                <div class="col-sm-9 geom-usage">
                  <h6 class="text-muted">
                    <span title="Narrative title"><i><font-awesome-icon icon="book-open" /></i>&nbsp;&nbsp;{{ usage.story.title.eng }}</span> &mdash; <small title="Type of Narrative"><i>{{ usage.story.storytype }}</i></small>
                  </h6>
                  <h6 title="Narrative summary" class="ml-4">
                    <i>{{ usage.story.summary.eng }}</i>
                  </h6>
                </div>
                <div class="col-sm-3 text-center">
                  <button type="button" class="btn btn-sm btn-primary" title="Open narrative" @click="openNarrative(usage.story.id, usage.geomAttr)">
                    Open narrative
                  </button>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer mt-3">
            <div class="btn btn-secondary btn-ok" data-dismiss="modal">
              Close
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="setStoryPublicationModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>
              <span v-if="setStoryPublication.action">{{ setStoryPublication.action.charAt(0).toUpperCase() + setStoryPublication.action.slice(1) }} </span>
              your narrative
            </h4>
          </div>
          <div class="modal-body">
            <p class="text-center mb-5">
              <strong>Note: </strong>
              <strong class="text-muted">Narratives submitted into Whānau nests become published immediately, while submissions into wider sectors require validation before publication.</strong>
            </p>
            <!-- v-if="user && user.profile && user.profile.affiliation.length != 0" -->
            <div>
              <form>
                <p>
                  Select the sector in which you want to {{ setStoryPublication.action }} your narrative<br>
                </p>
                <div class="ml-md-5 mr-md-5">
                  <select v-if="sectors" v-model="setStoryPublication.sector" class="selectpicker form-control form-control-sm mb-3" @change="reinitialiseBootstrapSelect()">
                    <option v-for="sector in sectors" :key="sector.id" :value="sector.name">
                      {{ sector.name }}
                    </option>
                  </select>
                </div>

                <div v-if="setStoryPublication.sector">
                  <p>
                    Select the nest(s) you want to {{ setStoryPublication.action }} your narrative<br>
                  </p>
                  <div class="ml-md-5 mr-md-5">
                    <select v-model="setStoryPublication.nests" class="selectpicker form-control form-control-sm mb-3" multiple>
                      <option v-for="affiliatednest in affiliationBySector[setStoryPublication.sector].filter(id=> !publishedGroups.includes(id))" :key="'nest_'+affiliatednest" :value="affiliatednest">
                        {{ nests.filter(x =>x.id === affiliatednest)[0].name }}
                      </option>
                    </select>
                  </div>
                </div>
                <!-- <select class="selectpicker form-control form-control-sm mb-3">
                  <option :value="tatouNestId">
                    Tātou
                  </option>
                </select> -->
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-dismiss="modal" @click="clearSetStoryPublication()">
              Close
            </button>
            <button disabled class="btn btn-success" data-dismiss="modal" @click="sendSetStoryPublication()">
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="setStoryUnPublicationModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>
              <span v-if="setStoryPublication.action">{{ setStoryPublication.action.charAt(0).toUpperCase() + setStoryPublication.action.slice(1) }} </span>
              your narrative
            </h4>
          </div>
          <div class="modal-body">
            <div>
              <form>
                <div v-if="publishedGroups && publishedGroups.length > 0">
                  <p>
                    Select the nest in which you want to {{ setStoryPublication.action }} your narrative<br>
                  </p>
                  <div class="ml-md-5 mr-md-5">
                    <select v-model="nestsToUnpublish" class="selectpicker form-control form-control-sm mb-3" multiple @change="reinitialiseBootstrapSelect()">
                      <option v-for="nest in publishedGroups" :key="nest" :value="nest">
                        {{ nests.filter(x =>x.id === nest)[0].name }}
                      </option>
                    </select>
                  </div>
                </div>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button class="btn btn-secondary" data-dismiss="modal" @click="clearSetStoryPublication()">
              Close
            </button>
            <button disabled class="btn btn-success" data-dismiss="modal" @click="sendSetStoryUnPublication()">
              Submit
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="showNarrativeInfoModal" class="modal fade">
      <div class="modal-dialog modal-lg">
        <div class="modal-content">
          <div class="modal-header">
            <h4>
              Narrative Info
            </h4>
          </div>
          <div class="modal-body">
            <div class="row">
              <div v-if="story && story.title" class="col-sm-12">
                <h6 class="text-muted">
                  <span title="Narrative title"><i><font-awesome-icon icon="book-open" /></i>&nbsp;&nbsp;{{ story.title.eng }}</span> &mdash; <small title="Type of Narrative"><i>{{ story.story_type.type }}</i></small>
                </h6>
                <h6 title="Narrative summary" class="ml-4">
                  <i>{{ story.summary.eng }}</i>
                </h6>
                <p v-if="story.owner != username" class="font-italic ml-4 mb-0">
                  <small>&mdash; Story by {{ story.owner }}</small>
                </p>
                <div class="ml-4 mt-4">
                  <table v-if="storyPublications && storyPublications.length > 0" class="table table-sm table-borderless">
                    <thead>
                      <tr>
                        <th scope="col">
                          Status
                        </th>
                        <th scope="col">
                          Nest
                        </th>
                        <th scope="col">
                          Date
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr v-for="publication in storyPublications" :key="publication.id">
                        <td>
                          <span v-if="publication.status == 'SUBMITTED'" class="badge badge-secondary">{{ publication.status }}</span>
                          <span v-else-if="publication.status == 'PUBLISHED'" class="badge badge-success">{{ publication.status }}</span>
                          <span v-else-if="publication.status == 'UNPUBLISHED'" class="badge badge-dark">{{ publication.status }}</span>
                          <span v-else-if="publication.status == 'REVIEWED'" class="badge badge-warning">{{ publication.status }}</span>
                          <span v-else-if="publication.status == 'ACCEPTED'" class="badge badge-info">{{ publication.status }}</span>
                          <span v-else class="badge badge-light">{{ publication.status }}</span>
                        </td>
                        <td>
                          {{ publication.nest.kinship_sector.name }} {{ publication.nest.name }}
                          <strong v-if="user.profile.affiliation.includes(publication.nest.id)">(You are member)</strong>
                        </td>
                        <td>{{ publication.status_modified_on | moment("MMMM Do, YYYY") }}</td>
                      </tr>
                    </tbody>
                  </table>
                  <table v-else class="table table-sm table-borderless">
                    <thead>
                      <tr>
                        <th scope="col">
                          Status
                        </th>
                      </tr>
                    </thead>
                    <tbody>
                      <tr>
                        <td>
                          <span class="badge badge-secondary">DRAFT</span>
                        </td>
                      </tr>
                    </tbody>
                  </table>
                </div>
              </div>
            </div>
          </div>
          <div class="modal-footer">
            <div class="btn btn-secondary btn-ok" data-dismiss="modal">
              Close
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import draggable from "vuedraggable"
import { VueEditor } from "vue2-editor"
import { imgFormats, videoFormats, audioFormats } from 'utils/objectUtils'
import { some, each, delay, without} from 'underscore'
import { EventBus } from 'store/event-bus'
import { disableEventListenerSingleClick, enableEventListenerSingleClick } from 'utils/mapUtils'
import CommentsView from 'components/Comments'
import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'
import { success as notifySuccess } from 'utils/notify'

export default {
  components: {
    draggable,
    VueEditor,
    CommentsView,
    VueBootstrapTypeahead
  },
  data() {
    return {
      mediaRoot: process.env.API_HOST + '/media/',
      uploadFieldName: 'file',
      uploadError: null,
      uploadedFile: null,
      uploadingMedia: false,
      dragging: false,
      customToolbar: [
        // [{ 'font': [] }],
        // [{ 'header': [false, 1, 2, 3, 4, 5, 6, ] }],
        [{ 'size': ['small', false, 'large', 'huge'] }],
        ['bold', 'italic', 'underline'],
        [{'align': ''}, {'align': 'center'}, {'align': 'right'}, {'align': 'justify'}],
        [{ 'list': 'ordered'}, { 'list': 'bullet' }],
        [{ 'script': 'sub'}, { 'script': 'super' }],
        [{ 'color': [] }, { 'background': [] }]
      ],
      tempMediaDescriptionEng: null,
      tempMediaDescriptionMao: null,
      selectedElement: null,
      magnifyImageElem: null,
      isGeomMedia: false,
      mediaForGeomAttr: null,
      geomsUsage: null,
      elementContentType: null,
      coAuthors: [],
      storyLang: 'eng',
      query: '',
      coauthorToDelete: '',
      editor: null,
      allOtherUsers: [],
      setStoryPublication: {
        action: null,
        sector: null,
        nests: []
      },
      nestsToUnpublish: []
    }
  },
  computed: {
    getOrientation(){
      return this.$store.state.orientation
    },
    togglePanel (){
      return this.$store.state.isPanelOpen
    },
    story() {
      return this.$store.state.storyContent
    },
    isStoryViewMode () {
      return this.$store.state.storyViewMode
    },
    isDrawMode () {
      if (this.$store.state.drawMode) {
        disableEventListenerSingleClick()
        $('#sidePanel :button').prop('disabled', true)
        $('#sidePanel :radio').prop('disabled', true)
      }else {
        enableEventListenerSingleClick()
        $('#sidePanel :button').prop('disabled', false)
        $('#sidePanel .wait-for-media').prop('disabled', true)
        $('#sidePanel :radio').prop('disabled', false)
      }
      return this.$store.state.drawMode
    },
    isGeomMediaMode () {
      if (this.$store.state.geomMediaMode) {
        disableEventListenerSingleClick()
        $('#sidePanel button:not("#uploadFileModalCancel")').prop('disabled', true)
      }else {
        enableEventListenerSingleClick()
        $('#sidePanel :button').prop('disabled', false)
        $('#sidePanel .wait-for-media').prop('disabled', true)
      }
      return this.$store.state.geomMediaMode
    },
    isReuseMode () {
      if (this.$store.state.reuseMode) {
        $('#sidePanel :button').prop('disabled', true)
      }else {
        $('#sidePanel :button').prop('disabled', false)
        $('#sidePanel .wait-for-media').prop('disabled', true)
      }
      return this.$store.state.reuseMode
    },
    allAtuas() {
      return this.$store.state.allAtuas
    },
    allUsers() {
      return this.$store.state.allUsers
    },
    user () {
      return this.$store.state.user
    },
    userPK () {
      var userpk
      if (this.$store.state.user) {
        userpk = this.$store.state.user.id
      }
      return userpk
    },
    username () {
      var username
      if (this.$store.state.user) {
        username = this.$store.state.user.username
      }
      return username
    },
    storyPublications () {
      return this.$store.state.storyPublications
    },
    affiliationBySector () {
      var affiliationBySector = {}

      if (this.sectors && this.nests) {
        var sectors_names = this.sectors.map(x => x.name)
        each(sectors_names, (name) => {
          affiliationBySector[name] = []
        })
      }
      each(this.nests, (nest) => {
        if (this.user && this.user.profile.affiliation.includes(nest.id)) {
          if (affiliationBySector[nest.kinship_sector.name]) {
            affiliationBySector[nest.kinship_sector.name].push(nest.id)
          }
        }
      })
      return affiliationBySector
    },
    allStoryTypes(){
      return this.$store.state.allStoryTypes
    },
    allElementContentTypes(){
      return this.$store.state.allElementContentTypes
    },
    uploadMediaProgress () {
      return this.$store.state.uploadMediaProgress
    },
    storyCoAuthors () {
      var coauthors = []
      each(this.$store.state.allUsers, (auth) => {
        if (this.$store.state.storyContent.co_authors.includes(auth.id)) {
          coauthors.push(auth)
        }
      })
      return coauthors
    },
    nests () {
      return this.$store.state.nests
    },
    sectors () {
      return this.$store.state.sectors
    },
    tatouNestId () {
      var tatouNestId
      if (this.nests) {
        var tatouNest = this.nests.filter(x=>x.name == 'Tātou')[0]
        if (tatouNest) {
          tatouNestId = tatouNest.id
        }
      }
      return tatouNestId
    },
    publishedGroups(){
      var groupids
      if(this.storyPublications) {
        groupids = this.storyPublications.filter(item=>item.status=== 'PUBLISHED').map(item=>item.nest.id)
      }
      return groupids
    }
  },
  watch: {
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
  created () {
    window.addEventListener('beforeunload', this.removeEditor)
  },
  beforeDestroy() {
    window.removeEventListener('beforeunload', this.removeEditor)
  },
  mounted: function () {
    EventBus.$on('addGeometryElement', (geomAttr) => {
      this.story.storyBodyElements.unshift({
        element_type: 'GEOM',
        geom_attr: geomAttr
      })
      EventBus.$emit('addNewStoryGeomToMap', geomAttr)
    })

    EventBus.$on('updateGeometryElement', (geomAttr) => {
      this.story.storyBodyElements.forEach( (elem) => {
        if (elem.element_type === 'GEOM') {
          if (elem.geom_attr.id === geomAttr.id) {
            elem.geom_attr = geomAttr
          }
        }
      })
      EventBus.$emit('replaceStoryGeomToMap', geomAttr)
    })

    EventBus.$on('getStoryGeomInfo', (feature) => {
      var geomAttr
      this.story.storyBodyElements.forEach( (elem) => {
        if (elem.element_type === 'GEOM') {
          if (elem.geom_attr.id == feature.getProperties().name) {
            geomAttr = elem.geom_attr
          }
        }
      })
      EventBus.$emit('showStoryGeomInfo', geomAttr)
    })


    EventBus.$on('addMediaToGeomAttr', (geomAttr) => {
      this.mediaForGeomAttr = geomAttr
      this.uploadFileClicked(this.isGeomMedia=true)
    })


    EventBus.$on('showGeomsUsage', (geomsUsage) => {
      this.geomsUsage = geomsUsage
      $('#geomsUsageModal').modal('show')
    })

    EventBus.$on('closePanel', () => {
      this.closePanel()
    })

    EventBus.$on('scrollStoryTop', () => {
      this.scrollStoryTop()
    })

    EventBus.$on('initialiseBootstrapSelect', () => {
      this.reinitialiseBootstrapSelect()
    })

    EventBus.$on('openNarrative', (story_id) => {
      this.openNarrative(story_id, null)
    })

  },
  methods: {
    onChange (e) {
      this.story.approx_time = {
        type: e.target.value,
        date: null,
        start_time: null,
        end_time: null
      }
    },
    removeEditor(event){
      event.preventDefault()
      if(!this.isStoryViewMode && this.story.id)
      {
        this.$store.dispatch('updateEditor', {'story_id': this.story.id,'editor': this.userPK,"action":"unset"})
      }
    },
    onChangeStoryLang:function(){
      // Update the store with the new Story view language
      this.$store.commit('SET_STORY_VIEW_LANG', this.storyLang)
      EventBus.$emit('addStoryGeomsToMap', this.story.storyBodyElements)
    },
    closePanel () {
      this.$store.commit('SET_PANEL_OPEN', false)
      EventBus.$emit('removeLayer', 'storyGeomsLayer')
      EventBus.$emit('resetDrawnFeature')
      this.$store.commit('RESTORE_ALL_USEDSTORIESGEOMETRIES')
      this.$store.state.allStoriesGeomsLayer.visible = true
    },
    reset () {
      $('input[type="file"]').val(null);
      this.uploadError = null
      this.uploadedFile = null
      this.tempMediaDescriptionEng = null
      this.tempMediaDescriptionMao = null
    },
    addEmptyVueEditor: function () {
      this.story.storyBodyElements.unshift({
        element_type: 'TEXT',
        texteng: null,
        textmao: null
      })
    },
    uploadFileClicked () {
      this.reset()
      $('#uploadFileModal').modal('show')
    },
    fileChange (fileList) {
      this.uploadingMedia = true

      var FileSize = fileList[0].size / 1024 / 1024; // in MB
        if (FileSize > 500) {
          this.uploadError = 'The file size exceeds 500 MB. Please, upload a smaller media file.'
          fileList = ''
          this.uploadingMedia = false
          return
        }

      const formData = new FormData()

      if (!fileList.length) return

      // append the files to FormData
      Array
        .from(Array(fileList.length).keys())
        .map(x => {
          formData.append('file', fileList[x], fileList[x].name)
        })

      this.$store.dispatch('addMedia', formData)
      .then((response) => {
        if (response.ok) {
          if (response.body) {
            this.uploadedFile = response.body
          }
        } else {
          if (response.body[0].indexOf('Request') == -1) {
            this.uploadError = response.body[0]
          } else {
            this.uploadError = response.body.split('Request')[0]
          }
        }
        fileList = ''
        this.uploadingMedia = false
      })
      .catch((err) => {
        console.log(err)
      })
    },
    addMediaElement: function () {
      $('#uploadFileModal').modal('hide')
      this.story.storyBodyElements.unshift({
        element_type: imgFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'IMG' : videoFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'VIDEO' : audioFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'AUDIO' : null,
        mediafile_name: this.uploadedFile.name,
        mediafile: this.uploadedFile.id,
        media_description: {eng:this.tempMediaDescriptionEng,mao:this.tempMediaDescriptionMao}
      })
      this.reset()
    },
    drawGeometry: function () {
      this.$store.commit('SET_DRAW_MODE', true)
      EventBus.$emit('addDrawingLayer')
      EventBus.$emit('resetSelectedFeatures')
    },
    reuseGeometry: function () {
      this.$store.commit('SET_REUSE_MODE', true)
      EventBus.$emit('resetSelectedFeatures')
    },
    saveStory: function () {
      EventBus.$emit('resetDrawnFeature')

      var storyform = document.getElementById(this.story.id + "_storyform")
      let delInstance = this;//To delete the current element ('this' keyword does not work correctly inside loop, so created thisway)

      if (storyform.checkValidity()) {

        let elements = this.story.storyBodyElements
        some(this.story.storyBodyElements, function (el, i) {
          // Remove empty text elements from storyBodyElements array
          if (el.element_type === 'TEXT' && (el.texteng === undefined || el.texteng === null || el.texteng === "") && (el.textmao === undefined || el.textmao === null || el.textmao === "")) {
            if (el.hasOwnProperty('id')) {
              delInstance.$store.dispatch('deleteStoryBodyElement', el)
            }
            elements.splice(i, 1)
            return true
          }

          // Replace empty string by null
          if (el.content_type === "") {
            el.content_type = null
          }
        })

        // Assign the order_position attribute
        each(this.story.storyBodyElements, (elem, index) => {
          elem.order_position = index
        })

        // Create or update
        if (this.story.hasOwnProperty('id')) {
          this.$store.dispatch('saveStoryContent', this.story)
        } else {
          this.$store.dispatch('addStory', this.story)
        }
        this.$store.commit('SET_STORY_VIEW_MODE', true)
        this.$store.commit('SET_GEOM_MEDIA_MODE', false)

        // Remove validated class
        storyform.classList.remove("was-validated")
      }else {
        storyform.classList.add("was-validated")
        $('#sidePanel').animate({ scrollTop: 0 }, 'fast')
      }
    },
    showCancelStorySavingModal: function () {
      if (!this.isStoryViewMode) {
        $('#editingWarningModal').modal('show')
      } else {
        this.cancelStorySaving()
      }
    },
    cancelStorySaving: function () {
      this.cleanUnusedMediaFiles()
      this.cleanUnusedGeomAttrs()
      this.$store.commit('SET_STORY_VIEW_MODE', true)
      this.$store.commit('SET_DRAW_MODE', false)
      this.$store.commit('SET_GEOM_MEDIA_MODE', false)
      this.$store.commit('SET_REUSE_MODE', false)
      if (this.story.hasOwnProperty('id')) {
        this.$store.dispatch('getStoryContent', this.story.id)
        .then((story) => {
          this.$store.dispatch('updateEditor', {'story_id': this.story.id,'editor': this.userPK,"action":"unset"})
          EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)
        })
      } else {
        this.closePanel()
      }
    },
    closeStory: function () {
      if (!this.isStoryViewMode) {
        $('#editingWarningModal').modal('show')
      } else {
        this.$store.dispatch('updateEditor', {'story_id': this.story.id,'editor': this.userPK,"action":"unset"})
        this.closePanel()
        EventBus.$emit("updateMapWidth")
      }
    },
    editStory: function () {
      this.$store.dispatch('getStoryContent', this.story.id)
      .then(() => {
        if (!this.story.being_edited_by || this.story.being_edited_by ==  this.userPK) {
          this.$store.dispatch('updateEditor', {'story_id': this.story.id,'editor': this.userPK,"action":"set"})
          if (this.story.story_type) {
            this.story.story_type_id = this.story.story_type.id
          }
          this.$store.commit('SET_STORY_VIEW_MODE', false)
          this.reinitialiseBootstrapSelect()
          EventBus.$emit('resetDrawnFeature')
          }
        else{
          EventBus.$emit('showStoryIsBeingEditedByWarning',this.story.being_edited_by)
        }
      })
    },
    inviteCoAuthorOpenModal: function () {
      this.$store.dispatch('getEditor', {'story_id': this.story.id})
      .then((response) => {
        this.editor = response.being_edited_by
      })
      if(this.story.co_authors)
      {
        this.coAuthors = this.story.co_authors
      }
      $('#inviteCoAuthorModal').modal('show')
    },
    deleteCoAuthorModalOpen: function (value) {
      if(value == this.editor)
      {
        $('#cantdeleteCoauthorWarningModal').modal('show')
      }
      else {
        this.coauthorToDelete = value
        $('#deleteCoAuthorModal').modal('show')
      }
    },
    setStoryPublicationOpenModal(action) {
      this.reinitialiseBootstrapSelect()
      this.setStoryPublication.action = action
      $('#setStoryPublicationModal').modal('show')
    },
    setStoryUnPublicationOpenModal(action) {
      this.reinitialiseBootstrapSelect()
      this.setStoryPublication.action = action
      $('#setStoryUnPublicationModal').modal('show')
    },
    settingsElementModal: function (element) {
      if (!this.isDrawMode) {
        this.selectedElement = element

        if (element) {
          if (element.hasOwnProperty('content_type')) {
            if (element.content_type && element.content_type.hasOwnProperty('id')) {
              this.elementContentType = element.content_type.id
            } else {
              this.elementContentType = ''
            }
          }
        }

        $('#settingsElementModal').modal('show')
      }
    },
    setElementContentType: function () {
      this.selectedElement.content_type = this.elementContentType
    },
    onClose: function () {
      this.$refs.usersAutocomplete.inputValue = ''
    },
    removeCoAuthor: function (value) {
      this.$refs.usersAutocomplete.inputValue = ''
      if (this.story.hasOwnProperty('id')) {
        this.coAuthors=without(this.coAuthors,value)
        var obj = {
          story_id: this.story.id,
          co_author: this.coAuthors
        }
        this.$store.dispatch('addCoAuthors', obj)
      }
    },
    setCoAuthors: function (value) {
      this.$refs.usersAutocomplete.inputValue = ''
      if (this.story.hasOwnProperty('id')) {
        this.coAuthors.push(value.id)
        var obj = {
          story_id: this.story.id,
          co_author: this.coAuthors
        }
        this.$store.dispatch('addCoAuthors', obj)
      }
    },
    deleteElementModal: function (element) {
      if (!this.isDrawMode) {
        this.selectedElement = element
        $('#deleteElementModal').modal('show')
      }
    },
    deleteElement: function () {
      if (this.selectedElement.hasOwnProperty('id')) {
        this.$store.dispatch('deleteStoryBodyElement', this.selectedElement)
        .then(() => {
          this.clean()
        })
      } else {
        var index = this.story.storyBodyElements.indexOf(this.selectedElement)
        if (index > -1) {
            this.story.storyBodyElements.splice(index, 1)
        }
        this.clean()
      }
    },
    clean: function () {
      if (['IMG', 'VIDEO', 'AUDIO'].includes(this.selectedElement.element_type)) {
        this.cleanUnusedMediaFiles()
      } else if (this.selectedElement.element_type === 'GEOM') {
        this.cleanUnusedGeomAttrs()
        EventBus.$emit('removeStoryGeomFromMap', this.selectedElement.geom_attr)
      }
    },
    cleanUnusedMediaFiles: function () {
      this.$store.dispatch('deleteUnusedMediaFiles')
    },
    cleanUnusedGeomAttrs: function () {
      this.$store.dispatch('deleteUnusedGeomAttrs')
    },
    cancelAddMediaElement: function () {
      this.reset()
      this.cleanUnusedMediaFiles()
    },
    zoomToGeometry (element) {
      EventBus.$emit('zoomToGeometry', element.geom_attr)
      EventBus.$emit('showStoryGeomInfo', element.geom_attr)
    },
    editGeometry (geomAttr) {
      EventBus.$emit('editGeomAttr', geomAttr)
    },
    editGeometryStyle (geomAttr) {
      EventBus.$emit('editGeomStyle', geomAttr)
    },
    magnifyImage (element) {
      this.magnifyImageElem = element
      $('#magnifyImageModal').modal('show')
    },
    manageGeomAttrMedia (geomAttr) {
      this.$store.commit('SET_GEOM_MEDIA_MODE', true)
      this.$store.commit('SET_DRAW_MODE', false)
      EventBus.$emit('zoomToGeometry', geomAttr)
      EventBus.$emit('showStoryGeomInfo', geomAttr)
    },
    addGeomAttrMedia () {
      $('#uploadFileModal').modal('hide')
      var geomAttrMedia = {
        geom_attr: this.mediaForGeomAttr.id,
        media_type: imgFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'IMG' : videoFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'VIDEO' : audioFormats.includes(this.uploadedFile.filetype.toLowerCase()) ? 'AUDIO' : null,
        mediafile_name: this.uploadedFile.name,
        mediafile: this.uploadedFile.id,
        media_description: {eng:this.tempMediaDescriptionEng,mao:this.tempMediaDescriptionMao}
      }

      this.$store.dispatch('addGeometryAttrbMedia', geomAttrMedia)
      .then((response) => {

        this.reset()

        this.story.storyBodyElements.forEach( (elem) => {
          if (elem.element_type === 'GEOM') {
            if (elem.geom_attr.id === this.mediaForGeomAttr.id) {
              // Update this.story
              elem.geom_attr.geomAttribMedia.unshift(response.body)
              // Update drawngeom info
              EventBus.$emit('showStoryGeomInfo', elem.geom_attr)
            }
          }
        })
      })
    },
    openNarrative (story_id, geomAttr) {
      $('#geomsUsageModal').modal('hide')
      if (!this.isStoryViewMode) {
        EventBus.$emit('storyIsBeingEditedWarning')
      } else {
        this.$store.dispatch('getStoryPublications', story_id)
        this.$store.dispatch('getStoryContent', story_id)
        .then((story) => {
          this.$store.commit('SET_STORY_VIEW_MODE', true)
          this.$store.commit('SET_PANEL_OPEN', true)
          EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)

          if (geomAttr) {
            delay(() => {
              EventBus.$emit('zoomToGeometry', geomAttr)
              EventBus.$emit('showStoryGeomInfo', geomAttr)
            }, 10)
          }
        })
      }
    },
    seeComments () {
      $('#sidePanel').animate({
                    scrollTop: $("#comments").offset().top
                }, '1000')
    },
    scrollStoryTop () {
      $('#sidePanel').animate({ scrollTop: 0 }, 'fast')
    },
    showUserManualModal (content) {
      EventBus.$emit('showUserManualModal',content)
    },
    reinitialiseBootstrapSelect () {
      $(function () {
        if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            $('.selectpicker').selectpicker('refresh');
        }
        else {
          $('.selectpicker').removeClass('selectpicker');
        }
      })
    },
    printStory (title) {
      var pdfname = title.eng?title.eng:title.mao
      var currentdate = new Date(Date.now()).toLocaleString().split(',')[0]

      // Get image of the map
      var canvas = document.getElementsByTagName("CANVAS")
      var mapcanvas
      each(canvas, (c) => {
        if (c.className == "ol-unselectable") {
          mapcanvas = c
        }
      })
      var imageURL = mapcanvas.toDataURL()

      let mywindow = window.open('', 'PRINT', 'height=650,width=900,top=100,left=150')
      mywindow.document.write(`<html><head><title>${pdfname}</title>`)

      var css = this.getallcss()
      each(css.hrefs, (href) => {
        mywindow.document.write(`<link href="${href}" rel="stylesheet">`)
      })
      mywindow.document.write(`<style>${css.cssClasses}</style>`)

      mywindow.document.write('</head><body >')

      mywindow.document.write(`<small class="text-muted">Printed on ${currentdate}</small><br />`)
      mywindow.document.write(`<h5><b>CULTURAL NARRATIVES</b></h5><br /><br /><br />`)

      each($(".printme_1"), (elem) => {
        mywindow.document.write(elem.innerHTML)
      })

      mywindow.document.write(`<img style="display: block; margin-left: auto; margin-right: auto; width: 60%; margin-top:40px; margin-bottom:10px; border: solid 2px #595353" src="${imageURL}" >`)
      mywindow.document.write(`<h4 style="text-align:center; margin-bottom:20px;">Locations in the narrative</h4>`)

      each($(".printme_2"), (elem) => {
        mywindow.document.write(elem.innerHTML)
        mywindow.document.write('<br /><br />')
      })

      var geomhtml = ''
      var storyGeoms = this.$store.state.storyContent.storyBodyElements.filter(x => x.element_type == 'GEOM')
      each(storyGeoms, (geom) => {
        var geomattr = geom.geom_attr
        geomhtml += `<p class="mt-3"><b>Geometry name:</b> ${geomattr.name.eng?geomattr.name.eng:geomattr.name.mao}</p>`
        geomhtml += `<p><b>Description:</b> ${geomattr.description.eng?geomattr.description.eng:geomattr.description.mao}</p>`
        each(geomattr.geomAttribMedia, (media) => {
          if (media.media_type == 'IMG') {
            geomhtml += `<img src="${process.env.API_HOST + '/media/' + media.mediafile_name}" alt="" class="geometry-media">`
            geomhtml += `<p class="media-caption">${media.media_description.eng?media.media_description.eng:media.media_description.mao}</p>`
          }
        })
        geomhtml += `<br />`
      })

      mywindow.document.write(geomhtml)

      mywindow.document.write('<h2 class="mt-5 mb-5">Layers Copyrights</h2>')

      // To print internal layers' copyright
      var intlayers = this.$store.state.internalLayers
      each(intlayers, (layer) => {
        if(layer.visible)
        {
          if(layer.assigned_name){
            mywindow.document.write('<p><strong>Layer name: </strong>'+layer.assigned_name+'</p>')
          }
          else {
            mywindow.document.write('<p><strong>Layer name: </strong>'+layer.name+'</p>')
          }
          if(layer.copyright_text){
            mywindow.document.write('<i>'+layer.copyright_text+'</i><br /><br /><br />')
          }
          else {
            mywindow.document.write('<i>Copyright statement not provided.</i><br /><br /><br />')
          }
        }
        })
      // To print external layers' copyright
      var extlayers = this.$store.state.externalLayers
      each(extlayers, (layer) => {
        if(layer.visible)
        {
          mywindow.document.write(layer.attribution+'<br /><br /><br />')
        }
      })
      mywindow.document.write('<p><strong>Basemaps: </strong><i>Map tiles by <a href="https://stamen.com/">Stamen Design</a>, under <a href="https://creativecommons.org/licenses/by/3.0/">CC BY 3.0</a>.© <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a> contributors.</i></p>')

      mywindow.document.write('</body></html>')

      mywindow.document.close(); // necessary for IE >= 10
      mywindow.focus(); // necessary for IE >= 10*/

      delay( () => {
          mywindow.print()
          if (!/Android|webOS|iPhone|iPad|iPod|BlackBerry|IEMobile|Opera Mini/i.test(navigator.userAgent)) {
            mywindow.close()
          }
        }, 700)
    },
    getallcss () {
      var cssClasses = ''
      var hrefs = []
      $.each(document.styleSheets, (sheetIndex, sheet) => {
        if (sheet.href == null) {
          $.each(sheet.cssRules || sheet.rules, (ruleIndex, rule) => {
            cssClasses += rule.cssText
          })
        } else {
          hrefs.push(sheet.href)
        }
      })
      return { 'cssClasses': cssClasses, 'hrefs': hrefs }
    },
    clearSetStoryPublication () {
      this.setStoryPublication = {
        action: null,
        sector: null,
        nests: []
      }
    },
    sendSetStoryPublication () {
      this.setStoryPublication.story = this.story
      this.$store.dispatch('setStoryPublication', this.setStoryPublication)
      .then((response) => {
        if (response.ok) {
          notifySuccess("&nbsp;&nbsp;The narrative was successfully <strong>published</strong> in the selected nests.")
        }
      })
      this.clearSetStoryPublication()
    },
    sendSetStoryUnPublication () {
      this.setStoryPublication.story = this.story
      this.setStoryPublication.nests = this.nestsToUnpublish
      this.$store.dispatch('setStoryPublication', this.setStoryPublication)
      .then((response) => {
        if (response.ok) {
          notifySuccess("&nbsp;&nbsp;The narrative was successfully <strong>unpublished</strong> from the selected nests.")
        }
      })
      this.clearSetStoryPublication()
    },
    showNarrativeInfoOpenModal () {
      $('#showNarrativeInfoModal').modal('show')
    },
    getAuthFullName(item){
      let author = this.allOtherUsers.filter(user=>user.id === item)[0]
      if (author.first_name || author.first_name) {
        return `${author.username} ( ${author.first_name} ${author.last_name} )`
      } else {
        return `${author.username}`
      }
    },
    getAuthAvatar(item){
      let author = this.allOtherUsers.filter(user=>user.id === item)[0]
      if (author.profile.avatar) {
        return author.profile.avatar.split('/media/')[1]
      }
      return
    },
  }
  };
  </script>
