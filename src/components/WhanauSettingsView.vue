<template>
  <div class="content-info">
    <div class="row p-5">
      <div class="col-lg-12">
        <div class="row mb-4">
          <div class="col-lg-12 settings-title">
            <h2>My Whānau groups</h2>
          </div>
        </div>
        <div class="row">
          <div class="col-lg-12 mb-3">
            <h6>
              This page allows you to create your whānau groups and invite members to be part of them.
            </h6>
            <h6>
              You can also receive invitations, which you must accept if you wish to be part of the specific whānau/group you were invited to.
            </h6>
            <h6>
              This way you can easily access and publish narratives into these nests and preserve the knowledge within the whānau.
            </h6>
          </div>
          <div class="col-lg-12 mt-3 mb-3">
            <h4>Pending invitations</h4>
            <div v-if="user && user.invitations && user.invitations.filter(inv => inv.accepted==null).length > 0">
              <div>
                <table class="table table-hover table-borderless">
                  <thead>
                    <tr>
                      <th scope="col" class="fit" colspan="2">
                        Inviter
                      </th>
                      <th scope="col" class="fit">
                        Whānau
                      </th>
                      <th scope="col" class="fit">
                        Sent on
                      </th>
                      <th scope="col" />
                    </tr>
                  </thead>
                  <tbody>
                    <tr v-for="invitation in user.invitations.filter(inv => inv.accepted==null)" :key="'invite'+invitation.id">
                      <td class="fit pr-0">
                        <div class="user-image">
                          <img v-if="invitation.nest.created_by.profile.avatar" class="img-responsive" :src="mediaRoot + invitation.nest.created_by.profile.avatar" alt="User picture">
                          <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                        </div>
                      </td>
                      <td class="fit pl-0 vertical-align-middle">
                        {{ invitation.nest.created_by.username }}
                      </td>
                      <td class="fit vertical-align-middle">
                        {{ invitation.nest.name }}
                      </td>
                      <td class="fit vertical-align-middle">
                        {{ invitation.sent_on | moment("MMMM Do, YYYY") }} <span class="date-extra-info">({{ invitation.sent_on | moment('from', 'now') }})</span>
                      </td>
                      <td class="ml-auto">
                        <a href="#" class="btn btn-primary" @click="acceptInvitation(invitation.id)">Accept</a>
                        <a href="#" class="btn btn-danger" @click="declineInvitation(invitation.id)">Decline</a>
                      </td>
                    </tr>
                  </tbody>
                </table>
              </div>
            </div>
            <p v-else class="text-muted">
              You don't have pending invitations
            </p>
          </div>
        </div>
        <hr>
        <div class="row">
          <div class="col-lg-6 mb-5">
            <div class="input-group">
              <div class="input-group-prepend">
                <span class="input-group-text">New</span>
              </div>
              <input v-model="newWhanauName" type="text" class="form-control" placeholder="Name of the whānau or group">
              <div class="input-group-append">
                <button :disabled="!newWhanauName" class="btn btn-primary" type="button" @click="addWhanau()">
                  Add
                </button>
              </div>
            </div>
          </div>
        </div>
        <!-- Cards -->
        <div class="row">
          <div class="col-lg-12 card-group center-content-horizontally">
            <!-- Owned nests -->
            <div v-for="(nest, nkey) in nests" :key="'ownednests_'+nkey">
              <div v-if="nest.created_by && nest.created_by.id == userPK" class="card whanau-card m-3">
                <div class="card-body d-flex flex-row">
                  <div>
                    <h4 class="card-title font-weight-bold mb-2">
                      {{ nest.name }}
                    </h4>
                    <p class="card-text" title="Created on">
                      <i class="far fa-clock pr-2" />
                      {{ nest.created_on | moment("MMMM Do, YYYY") }}
                    </p>
                  </div>
                </div>
                <!-- <img src="..." class="card-img" alt="..."> -->
                <div class="card-body pt-0">
                  <!-- <p class="card-text">Some text about the group</p> -->
                  <p class="card-text">
                    <strong>Members</strong>
                  </p>
                  <div class="col-md-12 p-0 mb-2">
                    <div class="col-md-12 center-content-vertically">
                      <div class="user-image">
                        <img v-if="user.profile.avatar" class="img-responsive" :src="mediaRoot + user.profile.avatar" alt="User picture">
                        <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                      </div>
                      <span>You</span>
                      <div class="ml-auto" title="Group administrator">
                        <font-awesome-icon icon="user-shield" size="lg" color="dark-grey" />
                      </div>
                    </div>
                  </div>
                  <div v-for="(member, mkey) in nest.members" :key="'member_'+mkey" class="col-md-12 p-0 mb-2">
                    <div v-if="member.user_id != userPK">
                      <div class="col-md-12 center-content-vertically">
                        <div class="user-image">
                          <img v-if="member.avatar" class="img-responsive" :src="mediaRoot + member.avatar" alt="User picture">
                          <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                        </div>
                        <span v-if="allUsersObj[member.user_id]">{{ allUsersObj[member.user_id].username }}</span>
                        <div class="ml-auto pointer" title="Remove user from the group">
                          <font-awesome-icon icon="user-times" size="lg" color="grey" @click="removeUserFromWhanauOpenModal(member, nest)" />
                        </div>
                      </div>
                    </div>
                  </div>
                  <div v-for="(invitation, ikey) in nest.invitations.filter(inv => inv.accepted==null)" :key="'invitee'+ikey" class="col-md-12 p-0 mb-2">
                    <div v-if="allUsersObj[invitation.invitee.id]">
                      <div class="col-md-12 center-content-vertically">
                        <div class="user-image">
                          <img v-if="allUsersObj[invitation.invitee.id].profile && allUsersObj[invitation.invitee.id].profile.avatar" class="img-responsive" :src="mediaRoot + allUsersObj[invitation.invitee.id].profile.avatar" alt="User picture">
                          <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                        </div>
                        <span>{{ allUsersObj[invitation.invitee.id].username }}</span>
                        <div class="ml-auto">
                          <font-awesome-icon icon="hourglass-half" size="lg" color="grey" title="Invitation sent. Pending acceptance" />
                        </div>
                      </div>
                    </div>
                  </div>
                </div>
                <p class="text-center">
                  <small>No. of Published narratives: <strong>{{ nest.publications }}</strong></small>
                </p>
                <div class="card-footer">
                  <a href="#" class="btn btn-primary" @click="inviteMember(nest)">Invite member</a>
                  <a href="#" class="btn btn-danger float-right" title="Delete group" @click="deleteWhanauOpenModal(nest)"><font-awesome-icon icon="trash-alt" /></a>
                </div>
              </div>
            </div>
            <!-- Member but not owned nests -->
            <div v-for="(nest, nkey) in nests" :key="'membernest'+nkey">
              <div v-if="nest.members.map(member => member.user_id).includes(userPK) && nest.created_by && nest.created_by.id != userPK" class="card whanau-card m-3">
                <div class="card-body d-flex flex-row">
                  <div>
                    <h4 class="card-title font-weight-bold mb-2">
                      {{ nest.name }}
                    </h4>
                    <p class="card-text" title="Created on">
                      <i class="far fa-clock pr-2" />
                      {{ nest.created_on | moment("MMMM Do, YYYY") }}
                    </p>
                  </div>
                </div>
                <div class="card-body pt-0">
                  <p class="card-text">
                    <strong>Members</strong>
                  </p>
                  <div class="col-md-12 p-0 mb-2">
                    <div class="col-md-12 center-content-vertically">
                      <div class="user-image">
                        <img v-if="nest.created_by && nest.created_by.profile && nest.created_by.profile.avatar" class="img-responsive" :src="mediaRoot + nest.created_by.profile.avatar" alt="User picture">
                        <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                      </div>
                      <span>{{ nest.created_by.username }}</span>
                      <div class="ml-auto" title="Group administrator">
                        <font-awesome-icon icon="user-shield" size="lg" color="dark-grey" />
                      </div>
                    </div>
                  </div>
                  <div v-for="(member, mkey) in nest.members" :key="'member_'+mkey" class="col-md-12 p-0 mb-2">
                    <div v-if="member.user_id != nest.created_by.id">
                      <div v-if="member.user_id != userPK" class="col-md-12 center-content-vertically">
                        <div class="user-image">
                          <img v-if="member.avatar" class="img-responsive" :src="mediaRoot + member.avatar" alt="User picture">
                          <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                        </div>
                        <span>{{ allUsersObj[member.user_id].username }}</span>
                      </div>
                      <div v-else class="col-md-12 center-content-vertically">
                        <div class="user-image">
                          <img v-if="user.profile.avatar" class="img-responsive" :src="mediaRoot + user.profile.avatar" alt="User picture">
                          <img v-else class="img-responsive" src="static/img/user.jpg" alt="User picture">
                        </div>
                        <span>You</span>
                      </div>
                    </div>
                  </div>
                </div>
                <p class="text-center">
                  <small>No. of Published narratives: <strong>{{ nest.publications }}</strong></small>
                </p>
                <div class="card-footer" />
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <div id="inviteMemberModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Invite member</h4>
          </div>
          <div v-if="allOtherUsers" class="modal-body">
            <h5 v-if="allOtherUsers" class="mb-0">
              Users
            </h5>
            <div v-if="userPK && inviteToNest.nest && inviteToNest.nest.members">
              <vue-bootstrap-typeahead ref="inviteMemberAutocomplete" v-model="usersquery" :serializer="s => s.username +' - '+ s.first_name +' '+ s.last_name" :data="allOtherUsers.filter(user=>!inviteToNest.nest.members.map(member => member.user_id).includes(user.id) && !inviteToNest.nest.invitations.filter(inv => inv.accepted==null).map(member => member.invitee_id).includes(user.id))" placeholder="Type a username" @hit="setWhanauMember($event)" />
            </div>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button :disabled="!inviteToNest.invitee" type="button" class="btn btn-success" data-dismiss="modal" @click="sendInvite()">
              Send invite
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="removeUserFromWhanauModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Remove user</h4>
          </div>
          <div v-if="userToRemoveFromWhanau.user && userToRemoveFromWhanau.nest" class="modal-body">
            Are you sure you want to delete the user {{ userToRemoveFromWhanau.user.username }} from whānau/group {{ userToRemoveFromWhanau.nest.name }}?
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button type="button" class="btn btn-danger" data-dismiss="modal" @click="removeUserFromWhanau()">
              Remove
            </button>
          </div>
        </div>
      </div>
    </div>

    <div id="deleteWhanauModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Delete Whānau/group</h4>
          </div>
          <div v-if="whanauToDelete" class="modal-body">
            <p>
              Are you sure you want to delete the whānau/group {{ whanauToDelete.name }}?
            </p>
            <p>
              NOTE: The narratives published in this nest will become unpublished and only their authors will be able to access them.
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button type="button" class="btn btn-danger" data-dismiss="modal" @click="deleteWhanau()">
              Delete
            </button>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import VueBootstrapTypeahead from 'vue-bootstrap-typeahead'
import { each } from 'underscore'

export default {
  components: {
    VueBootstrapTypeahead
  },
  data () {
    return {
      mediaRoot: process.env.API_HOST,
      allOtherUsers: [],
      usersquery: '',
      newWhanauName: null,
      inviteToNest: {
        invitee: null,
        nest: null
      },
      userToRemoveFromWhanau: {
        user: null,
        nest: null
      },
      whanauToDelete: null
    }
  },
  computed: {
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
    sectors () {
      return this.$store.state.sectors
    },
    nests () {
      var whanauNests
      if (this.$store.state.nests) {
        whanauNests = this.$store.state.nests.filter(x=>x.kinship_sector.name === 'Whānau')
      }
      return whanauNests
    },
    allUsersObj () {
      var allUsersObj = {}
      each(this.$store.state.allUsers, (user) => {
        allUsersObj[user.id] = user
      })
      return allUsersObj
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
  methods: {
    addWhanau () {
      var kinship_sector_id = this.sectors.filter(x=>x.name === 'Whānau')[0].id
      if (kinship_sector_id) {
        var nest = {
          name: this.newWhanauName,
          kinship_sector_id: kinship_sector_id
        }
        this.$store.dispatch('addNest', nest)
        .then((response) => {
          if (response.body.id) {
            this.$store.dispatch('saveAffiliation', {'user': this.userPK, 'affiliation': [response.body.id], 'isWhanauOrGroup': true})
          }
        })
      }
      this.newWhanauName = null
    },
    deleteWhanauOpenModal (nest) {
      this.whanauToDelete = nest
      $('#deleteWhanauModal').modal('show')
    },
    deleteWhanau () {
      this.$store.dispatch('deleteNest', this.whanauToDelete)
      .then(() => {
        // TODO: Unpublish stories published on this nest
      })
    },
    inviteMember (nest) {
      this.inviteToNest.invitee = null
      if (this.$refs.inviteMemberAutocomplete) {
        this.$refs.inviteMemberAutocomplete.inputValue = ''
      }
      this.inviteToNest.nest = nest
      $('#inviteMemberModal').modal('show')
    },
    setWhanauMember (value) {
      this.inviteToNest.invitee = value
    },
    sendInvite () {
      console.log("addWhanauInvitation ");
      if (this.inviteToNest.invitee) {
        this.$store.dispatch('addWhanauInvitation', {'nest_id':  this.inviteToNest.nest.id, 'invitee_id':  this.inviteToNest.invitee.id})
      }
    },
    acceptInvitation (invitationId) {
      this.$store.dispatch('acceptWhanauInvitation', {'id': invitationId, 'accepted': true})
    },
    declineInvitation (invitationId) {
      this.$store.dispatch('declineWhanauInvitation', {'id': invitationId, 'accepted': false})
    },
    removeUserFromWhanauOpenModal (user, nest) {
      this.userToRemoveFromWhanau.user = user
      this.userToRemoveFromWhanau.nest = nest
      $('#removeUserFromWhanauModal').modal('show')
    },
    removeUserFromWhanau () {
      this.$store.dispatch('removeUserFromWhanau', {'user': this.userToRemoveFromWhanau.user.user_id, 'nest': this.userToRemoveFromWhanau.nest.id})
    }
  }
}
</script>
