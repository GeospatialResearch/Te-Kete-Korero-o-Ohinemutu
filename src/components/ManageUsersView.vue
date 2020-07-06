<template>
  <div class="content-info">
    <div class="row p-5">
      <div class="col-lg-12 mt-3 mb-3">
        <h4>Pending Access Requests</h4>
        <div v-if="user && user.accessrequests && user.accessrequests.filter(req => req.accepted==null).length > 0">
          <div>
            <table class="table table-hover table-borderless">
              <thead>
                <tr>
                  <th scope="col" class="fit" colspan="2">
                    User
                  </th>
                  <th scope="col" class="fit">
                    Nest
                  </th>
                  <th scope="col" class="fit">
                    Sent on
                  </th>
                  <th scope="col" />
                </tr>
              </thead>
              <tbody>
                <tr v-for="accessrequest in user.accessrequests.filter(req => req.accepted==null)" :key="'req'+accessrequest.id">
                  <td class="fit pr-0">
                    <div class="user-image">
                      <img v-if="accessrequest.user.profile.avatar" class="img-responsive" :src="mediaRoot + accessrequest.user.profile.avatar" alt="User picture">
                      <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                    </div>
                  </td>
                  <td class="fit pl-0 vertical-align-middle">
                    {{ accessrequest.user.username }}
                  </td>
                  <td class="fit vertical-align-middle">
                    {{ accessrequest.nest.kinship_sector.name }} {{ accessrequest.nest.name }}
                  </td>
                  <td class="fit vertical-align-middle">
                    {{ accessrequest.sent_on | moment("MMMM Do, YYYY") }} <span class="date-extra-info">({{ accessrequest.sent_on | moment('from', 'now') }})</span>
                  </td>
                  <td class="ml-auto">
                    <a href="#" class="btn btn-info" title="User details" @click="showUserDetailModal(accessrequest.user.profile.background_info,accessrequest.user.profile.phone_number)"><i class="fa fa-id-card" aria-hidden="true" /></a>
                    <a href="#" class="btn btn-primary" @click="acceptRequest(accessrequest.id)">Accept</a>
                    <a href="#" class="btn btn-danger" @click="declineRequest(accessrequest.id)">Decline</a>
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
        <p v-else class="text-muted">
          You don't have pending access requests
        </p>
      </div>
      <hr>

      <div class="col-lg-12 settings-title">
        <h4>Users settings</h4>
      </div>

      <div class="col-lg-12 pt-4 pt-lg-5 nests-table">
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">
                Username
              </th>
              <th scope="col">
                First name(s)
              </th>
              <th scope="col">
                Last name(s)
              </th>
              <th scope="col">
                Affiliation
              </th>
              <th scope="col">
                Is Tool Manager
              </th>
              <th scope="col" />
            </tr>
          </thead>
          <tbody>
            <tr v-for="(a_user, userkey) in allUsers.filter(x=>!x.is_superuser)" :key="userkey">
              <td class="user-name">
                {{ a_user.username }}
                <strong v-if="a_user.id==user.id"> (You)</strong>
              </td>
              <td class="user-name">
                {{ a_user.first_name }}
              </td>
              <td class="user-name">
                {{ a_user.last_name }}
              </td>
              <td>
                <div v-if="Object.keys(profilesObj).length > 0 && Object.keys(nestsObj).length > 0">
                  <div v-if="profilesObj[a_user.id] && profilesObj[a_user.id].affiliation">
                    <p v-for="nestid in profilesObj[a_user.id].affiliation" :key="nestid" class="mb-0">
                      <span v-if="nestsObj[nestid.toString()]" :title="nestsObj[nestid.toString()].kinship_sector.name">{{ nestsObj[nestid.toString()].name }}</span>
                    </p>
                  </div>
                </div>
              </td>
              <td>
                <span v-if="a_user.is_staff">Yes</span>
                <span v-else>No</span>
              </td>
              <td>
                <a href="#" @click="editUser(a_user)">Edit</a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div id="editUserModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              User settings
            </h4>
          </div>
          <div v-if="userToEdit" class="modal-body">
            <div class="text-center">
              <div class="user-pic-settings">
                <img v-if="userToEdit.profile.avatar" class="img-responsive img-rounded profile-avatar" :src="mediaRoot + userToEdit.profile.avatar" alt="User picture">
                <img v-else class="img-responsive img-rounded profile-avatar" src="static/img/user.jpg" alt="User picture">
              </div>
              <p>
                {{ userToEdit.username }}
              </p>
            </div>
            <affiliation-form v-if="userToEdit" :user-profile="userToEdit.profile" :prefix="'manageuser_' + userToEdit.id" :staff="userToEdit.is_staff" @childToParentAffiliation="getAffiliation($event)" @childToParentStaffSetting="getStaffSetting($event)" />
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelUser()">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="saveUser()">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="staffWarningModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Attention
            </h4>
          </div>
          <div class="modal-body text-center">
            {{ staffWarningMessage }}
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Got it!
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="UserDetailModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              User Details
            </h4>
          </div>
          <div class="modal-body">
            <label for="requestorBackgroundInfo"><strong>Connections</strong></label>
            <div class="input-group mb-4">
              <textarea v-model="requestorBackgroundInfo" disabled class="form-control form-control-sm" type="text" rows="5" placeholder="Explain your connections..." />
            </div>
            <label for="requestorPhoneNo"><strong>Phone number</strong></label>
            <div class="input-group mb-4">
              <input v-model="requestorPhoneNo" disabled value="" type="text" name="" class="form-control input_pass" placeholder="Phone number">
            </div>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { each } from 'underscore'
import AffiliationForm from 'components/AffiliationForm'

export default {
  components: {
    AffiliationForm
  },
  data () {
    return {
      userToEdit: null,
      mediaRoot: process.env.API_HOST,
      affiliationBySector: {},
      isStaff: null,
      staffWarningMessage: '',
      requestorPhoneNo: '',
      requestorBackgroundInfo: ''
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
    allUsers() {
      return this.$store.state.allUsers
    },
    allProfiles() {
      return this.$store.state.allProfiles
    },
    nestsObj () {
      var nestsObj = {}
      each(this.$store.state.nests, (nest) => {
        if (this.user && this.user.is_superuser) {
          nestsObj[nest.id] = nest
        } else {
          if (nest.kinship_sector.name!='Whānau') {
            nestsObj[nest.id] = nest
          }
        }
      })
      return nestsObj
    },
    profilesObj () {
      var profilesObj = {}
      each(this.$store.state.allProfiles, (profile) => {
        profilesObj[profile.user] = profile
      })
      return profilesObj
    }
  },
  methods: {
    editUser (user) {
      this.reinitialiseBootstrapSelect()
      this.userToEdit = user
      this.userToEdit.profile = this.allProfiles.filter(x=>x.user == user.id)[0]
      $('#editUserModal').modal('show')
    },
    saveUser () {
      // Save affiliation
      if (Object.keys(this.affiliationBySector).length > 0) {
        var affiliation = []
        each(this.affiliationBySector, (value) => {
          affiliation.push(...value)
        })
        this.$store.dispatch('saveAffiliation', {'user': this.userToEdit.id, 'affiliation': affiliation})
      }

      // Save other settings
      if (this.isStaff != null && this.isStaff != this.userToEdit.is_staff) {
        this.$store.dispatch('setAsStaff', {'user': this.userToEdit.id, 'is_staff': this.isStaff})
        .then((response) => {
          if (!response.ok) {
            this.staffWarningMessage = response.body[0]
            $('#staffWarningModal').modal('show')
          }
        })
      }

      this.userToEdit = null
      this.isStaff = null
    },
    cancelUser () {
      this.userToEdit = null
      this.isStaff = null
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
    getAffiliation (value) {
      this.affiliationBySector = value
    },
    getStaffSetting (value) {
      this.isStaff = value
    },
    acceptRequest (requestId) {
      this.$store.dispatch('acceptRequestToWiderGroup', {'id': requestId, 'accepted': true, 'accepted_by_id': this.user.id})
    },
    declineRequest (requestId) {
      this.$store.dispatch('declineRequestToWiderGroup', {'id': requestId, 'accepted': false, 'accepted_by_id': this.user.id})
    },
    showUserDetailModal(requestorBackgroundInfo,requestorPhoneNo){
      this.requestorBackgroundInfo = requestorBackgroundInfo
      this.requestorPhoneNo = requestorPhoneNo
      $('#UserDetailModal').modal('show')
    }
  }
}
</script>
