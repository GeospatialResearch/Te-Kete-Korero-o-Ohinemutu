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
                <button type="button" class="btn btn-success" @click="requestTribalVerification()">
                  Request Tribal Membership verification
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

    <div id="tribalMemberVerificationModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Request Tribal Membership verification
            </h4>
          </div>
          <div class="modal-body">
            <p class="text-center">
              <b>Functionality under development...</b>
            </p>
            <p>
              Please insert your tribal register number and select your whakapapa using the select boxes below
            </p>
            <div class="input-group mb-4">
              <div class="input-group-append">
                <span class="input-group-text">
                  <i><font-awesome-icon icon="fingerprint" /></i>
                </span>
              </div>
              <input v-model="membership_number" value="" type="text" name="" class="form-control input_pass" placeholder="Tribal register number">
            </div>
            <affiliation-form v-if="user" :user-profile="user.profile" prefix="profile" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelRequest()">
              Cancel
            </button>
            <button disabled class="btn btn-danger btn-ok" data-dismiss="modal" @click="sendRequest()">
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
// import { each } from 'underscore'
import AffiliationForm from 'components/AffiliationForm'

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
      membership_number: null
    }
  },
  computed: {
    user () {
      return this.$store.state.user
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
        }
      }
    }
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
    requestTribalVerification () {
      $('#tribalMemberVerificationModal').modal('show')
      this.reinitialiseBootstrapSelect()
    },
    reinitialiseBootstrapSelect () {
      $(function () {
        $('.selectpicker').selectpicker('refresh')
      })
    },
    cancelRequest() {
      // this.affiliationBySector = null
    },
    sendRequest () {
    }
  }
}
</script>
