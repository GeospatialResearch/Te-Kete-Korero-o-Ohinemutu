<template>
  <div class="content-info">
    <div class="row p-5">
      <div class="col-lg-12">
        <div class="row mb-4">
          <div class="col-lg-12 settings-title">
            <h2>My Profile</h2>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-4 mb-4">
            <div class="center-content">
              <img v-if="user && user.profile && user.profile.avatar" class="img-responsive img-rounded mb-2 profile-avatar" :src="mediaRoot + user.profile.avatar" alt="User picture">
              <img v-else class="img-responsive img-rounded mb-2 profile-avatar" src="static/img/user.jpg" alt="User picture">
            </div>
            <div class="center-content">
              <button type="button" class="btn btn-primary btn-sm" @click="changePicture()">
                Change picture
              </button>
            </div>
          </div>
          <div class="col-lg-8">
            <div class="profile-section">
              <form>
                <div class="row">
                  <div class="col-lg-6">
                    <div class="form-group">
                      <label for="firstName">First name(s)</label>
                      <input id="firstName" v-model="inputs.first_name" :disabled="!editingProfile" type="text" class="form-control">
                    </div>
                  </div>
                  <div class="col-lg-6">
                    <div class="form-group">
                      <label for="lastName">Last name(s)</label>
                      <input id="lastName" v-model="inputs.last_name" :disabled="!editingProfile" type="text" class="form-control">
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-12">
                    <div class="form-group">
                      <label for="pepeha">Pepeha</label>
                      <textarea id="pepeha" v-model="inputs.pepeha" :disabled="!editingProfile" class="form-control form-control-sm" type="text" rows="8" placeholder="Write your pepeha here..." />
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-12">
                    <div class="form-group">
                      <label for="bio">Bio</label>
                      <textarea id="bio" v-model="inputs.bio" :disabled="!editingProfile" class="form-control form-control-sm" type="text" rows="5" placeholder="Write something about your life, job or hobbies..." />
                    </div>
                  </div>
                </div>
                <div class="row">
                  <div class="col-lg-4">
                    <label for="dateBirth">Date of birth</label>
                    <div id="dateBirth" class="input-group mb-4">
                      <div class="input-group-append">
                        <span class="input-group-text">
                          <i><font-awesome-icon :icon="['far', 'calendar-alt']" /></i>
                        </span>
                      </div>
                      <input v-model="inputs.date_birth" :disabled="!editingProfile" type="date" class="form-control input_pass">
                    </div>
                  </div>
                  <div class="col-lg-8" />
                </div>
                <div class="pull-right">
                  <button v-if="editingProfile" type="button" name="button" class="btn btn-success" @click="saveProfile()">
                    Save Profile
                  </button>
                  <button v-if="editingProfile" type="button" name="button" class="btn btn-secondary" @click="cancelProfile()">
                    Cancel
                  </button>
                  <button v-else type="button" name="button" class="btn btn-primary" @click="editingProfile=true">
                    Edit Profile
                  </button>
                </div>
              </form>
              <div class="row col-lg-12 mt-5">
                <button :disabled="editingProfile" type="button" class="btn btn-success" @click="requestAccess()">
                  Request Access To Wider Nests
                </button>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="avatarModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Change picture
            </h4>
          </div>
          <div class="modal-body">
            <div class="text-center">
              <vue-avatar
                ref="vueavatar"
                :width="200"
                :height="200"
                :rotation="rotation"
                :scale="scale"
                @vue-avatar-editor:image-ready="onImageReady"
              />
              <br>
              <form class="ml-5 mr-5">
                <div class="form-group">
                  <label for="formControlRangeZoom">Zoom : {{ scale }}x</label>
                  <input id="formControlRangeZoom" v-model.number="scale" type="range" min="1" max="3" step="0.02" class="form-control-range">
                </div>
                <div class="form-group">
                  <label for="formControlRangeRotation">Rotation : {{ rotation }}°</label>
                  <input id="formControlRangeRotation" v-model.number="rotation" type="range" min="0" max="360" step="1" class="form-control-range">
                </div>
              </form>
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button class="btn btn-success btn-ok" data-dismiss="modal" @click="saveClicked">
              Save picture
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="RequestAccessModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Request access to wider nests
            </h4>
          </div>
          <div class="modal-body">
            <p v-if="isDisabled">
              <code>{{ bgdetailError }}</code>
            </p>
            <p else>
              Please insert your phone number and a brief summary about your connections and select your whakapapa using the select boxes below
            </p>

            <label for="background_info"><strong>Explain your connections</strong></label>
            <div class="input-group mb-4">
              <textarea v-model="background_info" class="form-control form-control-sm" type="text" rows="5" placeholder="Explain your connections..." required />
            </div>
            <label for="phone_number"><strong>Phone number</strong></label>
            <div class="input-group mb-4">
              <input v-model="phone_number" value="" type="number" name="" class="form-control input_pass" placeholder="Phone number" required>
            </div>
            <affiliation-form v-if="user" :key="user.useraccessrequests.length" :access-requests="user.useraccessrequests" :user-profile="user.profile" prefix="profile" @childToParentAffiliation="getAffiliation($event)" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelRequest()">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" @click="sendRequest()">
              Send request
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { VueAvatar } from 'vue-avatar-editor-improved'
import { each } from 'underscore'
import AffiliationForm from 'components/AffiliationForm'
import { success as notifySuccess } from 'utils/notify'


export default {
  components: {
    VueAvatar,
    AffiliationForm
  },
  data () {
    return {
      rotation: 0,
      scale: 1,
      mediaRoot: process.env.API_HOST,
      editingProfile: false,
      inputs: {
        first_name: '',
        last_name: '',
        date_birth: '',
        pepeha: '',
        bio: ''
      },
      background_info: '',
      phone_number: '',
      selected_affiliationBySector: {},
      bgdetailError: ''
    }
  },
  computed: {
    user () {
      return this.$store.state.user
    },
    sectors () {
      var sectors = this.$store.state.sectors
      var sorted_sectors = []
      if (sectors) {
        sorted_sectors = sectors.sort((a,b) => (a.id > b.id) ? 1 : ((b.id > a.id) ? -1 : 0))
      }
      return sorted_sectors
    },
    nests () {
      return this.$store.state.nests
    },
    nestsBySector () {
      var nestsBySector = {}

      if (this.sectors && this.nests) {
        var sectors_names = this.sectors.filter(x=>x.name !== 'Tātou' && x.name !== 'Whānau').map(x => x.name)
        each(sectors_names, (name) => {
          nestsBySector[name] = []
        })
        each(this.nests, (nest) => {
          if (nest.kinship_sector) {
            if (nestsBySector[nest.kinship_sector.name]) {
              nestsBySector[nest.kinship_sector.name].push(nest)
            }
          }
        })
      }
      return nestsBySector
    },
    affiliationBySector () {
      var affiliationBySector = {}

      if (this.sectors && this.nests) {
        var sectors_names = this.sectors.filter(x=>x.name !== 'Tātou' && x.name !== 'Whānau').map(x => x.name)
        each(sectors_names, (name) => {
          affiliationBySector[name] = []
        })
      }
      each(this.nests, (nest) => {
        if (this.user.profile && this.user.profile.affiliation.includes(nest.id)) {
          if (affiliationBySector[nest.kinship_sector.name]) {
            affiliationBySector[nest.kinship_sector.name].push(nest.id)
          }
        }
      })
      return affiliationBySector
    }
  },
  watch: {
    user: {
      deep: true,
      handler: function (newVal) {
        this.inputs.first_name = newVal.first_name
        this.inputs.last_name = newVal.last_name
        if (newVal.profile) {
          this.inputs.date_birth = newVal.profile.birth_date
          this.inputs.pepeha = newVal.profile.pepeha
          this.inputs.bio = newVal.profile.bio
          this.background_info = newVal.profile.background_info
          this.phone_number = newVal.profile.phone_number
        }
      }
    },
  },
  mounted: function () {
    this.inputs = {
      first_name: this.user.first_name,
      last_name: this.user.last_name,
      date_birth: this.user.profile.birth_date,
      pepeha: this.user.profile.pepeha,
      bio: this.user.profile.bio
    }
    this.background_info = this.user.profile.background_info
    this.phone_number = this.user.profile.phone_number
  },
  methods: {
    changePicture () {
      $('#avatarModal').modal('show')
    },
    saveClicked () {
      var img = this.$refs.vueavatar.getImageScaled()
      // this.$refs.image.src = img.toDataURL()
      this.$store.dispatch('changeAvatar', img.toDataURL())
    },
    onImageReady () {
      this.scale = 1
      this.rotation = 0
    },
    saveProfile () {
      this.$store.dispatch('saveProfile', this.inputs)
      this.editingProfile = false
    },
    cancelProfile () {
      this.editingProfile = false
      this.inputs = {
        first_name: this.user.first_name,
        last_name: this.user.last_name,
        date_birth: this.user.profile.birth_date,
        pepeha: this.user.profile.pepeha,
        bio: this.user.profile.bio
      }
    },
    requestAccess () {
      this.reinitialiseBootstrapSelect()
      $('#RequestAccessModal').modal('show')
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
    cancelRequest() {
      this.selected_affiliationBySector = null
      this.bgdetailError = null
      this.background_info = this.user.profile.background_info
      this.phone_number = this.user.profile.phone_number
    },
    gatherSelectedAffiliation()
    {
      let affiliation = []
      // Save affiliation
      if (this.selected_affiliationBySector && Object.keys(this.selected_affiliationBySector).length > 0) {

        each(this.selected_affiliationBySector, (value) => {
          if(!this.user.useraccessrequests.map(item=>item.nest_id).includes(value[0])){
            affiliation.push(...value)
          }
        })

      }
      return affiliation
    },
    isDisabled() {
      let affiliation = this.gatherSelectedAffiliation()

      //validation
      if(this.background_info == '' || this.phone_number == '' || (affiliation.length == 0 && !this.noMoreWiderNests()))
      {
        this.bgdetailError = 'Please insert'
        if(this.background_info == '')
          this.bgdetailError = this.bgdetailError + ' a brief summary about your connections'
        if(this.phone_number == '')
         this.bgdetailError = this.bgdetailError + ' - your phone number'
        if(affiliation.length == 0 && !this.noMoreWiderNests())
          this.bgdetailError = this.bgdetailError + ' - at least one nest in dropdown'
        return true;
      }
      else{
        return false;
      }
    },
    sendRequest () {
      if(!this.isDisabled())
      {
        let affiliation = this.gatherSelectedAffiliation()
        // Saves affiliation requests in WiderGroupAccessRequest table
        if(affiliation.length > 0){
          this.$store.dispatch('saveRequest', {'user': this.user.id, 'affiliation': affiliation, 'background_info': this.background_info,'phone_number': this.phone_number})
        }
        else{
          // Saves the background_info,phone no details in the profile table
          this.$store.dispatch('saveUserbackgroundInfo', {'user': this.user.id, 'affiliation': affiliation, 'background_info': this.background_info,'phone_number': this.phone_number})
        }
        this.bgdetailError = null
        $('#RequestAccessModal').modal('hide')
        notifySuccess("&nbsp;&nbsp;Your request to access wider group(s) was sent.")
      }
      else {
        return false
      }
    },
    getAffiliation (value) {
      this.selected_affiliationBySector = value
    },
    noMoreWiderNests(){
        let result = true
          each(this.nestsBySector, (sector,sectorkey) => {
            if(sector.length > 0 && sector.filter(item=>!this.affiliationBySector[sectorkey].includes(item.id) && !this.user.useraccessrequests.map(item=>item.nest_id).includes(item.id)).length > 0){
              result = false
            }
          })
        return result
    },
  }
}
</script>
