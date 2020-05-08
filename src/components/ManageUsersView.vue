<template>
  <div class="content-info">
    <div class="row p-5">
      <div class="col-lg-12 settings-title">
        <h2>Users settings</h2>
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
              <th scope="col" />
            </tr>
          </thead>
          <tbody>
            <tr v-for="(user, userkey) in allUsers" :key="userkey">
              <td class="user-name">
                {{ user.username }}
              </td>
              <td class="user-name">
                {{ user.first_name }}
              </td>
              <td class="user-name">
                {{ user.last_name }}
              </td>
              <td>
                <div v-if="Object.keys(profilesObj).length > 0 && Object.keys(nestsObj).length > 0">
                  <p v-for="nestid in profilesObj[user.id].affiliation" :key="nestid" class="mb-0">
                    <span>{{ nestsObj[nestid.toString()].name }}</span>
                  </p>
                </div>
              </td>
              <td><a href="#" @click="editUser(user)">Edit</a></td>
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
            <h5 class="mb-3">
              User affiliation
            </h5>
            <form class="p-2">
              <div v-for="(sector, sectorkey) in nestsBySector" :key="sectorkey">
                <label :for="sectorkey"><strong>{{ sectorkey }}</strong></label>
                <select v-if="sector.length > 0" :id="sectorkey" v-model="affiliationBySector[sectorkey]" class="selectpicker form-control form-control-sm mb-3" multiple :title="'Select one or more ' + sectorkey">
                  <option v-for="nest in sector" :key="nest.id" :value="nest.id">
                    {{ nest.name }}
                  </option>
                </select>
                <p v-else class="text-muted">
                  There are no {{ sectorkey }} nests defined yet
                </p>
              </div>
            </form>
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
  </div>
</template>

<script>
import { each } from 'underscore'

export default {
  data () {
    return {
      userToEdit: null,
      mediaRoot: process.env.API_HOST,
      nestsBySector: {},
      affiliationBySector: {}
    }
  },
  computed: {
    sectors () {
      return this.$store.state.sectors
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
        nestsObj[nest.id] = nest
      })
      return nestsObj
    },
    profilesObj () {
      var profilesObj = {}
      each(this.$store.state.allProfiles, (profile) => {
        profilesObj[profile.user] = profile
      })
      return profilesObj
    },
  },
  watch: {
    nests: {
      deep: true,
      handler: function (newNests) {
        if (this.sectors) {
          var sectors_names = this.sectors.filter(x=>x.name !== 'Tātou').map(x => x.name)
          each(sectors_names, (name) => {
            this.nestsBySector[name] = []
            this.affiliationBySector[name] = []
          })
          each(newNests, (nest) => {
            if (nest.kinship_sector) {
              if (this.nestsBySector[nest.kinship_sector.name]) {
                this.nestsBySector[nest.kinship_sector.name].push(nest)
              }
            }
          })
        }
      }
    },
    sectors: {
      deep: true,
      handler: function (newSectors) {
        if (this.nests) {
          var sectors_names = newSectors.filter(x=>x.name !== 'Tātou').map(x => x.name)
          each(sectors_names, (name) => {
            this.nestsBySector[name] = []
            this.affiliationBySector[name] = []
          })
          each(this.nests, (nest) => {
            if (nest.kinship_sector) {
              if (this.nestsBySector[nest.kinship_sector.name]) {
                this.nestsBySector[nest.kinship_sector.name].push(nest)
              }
            }
          })
        }
      }
    }
  },
  methods: {
    editUser (user) {
      this.userToEdit = user
      this.userToEdit.profile = this.allProfiles.filter(x=>x.user == user.id)[0]

      each(this.nests, (nest) => {
        if (this.userToEdit.profile.affiliation.includes(nest.id)) {
          this.affiliationBySector[nest.kinship_sector.name].push(nest.id)
        }
      })

      $('#editUserModal').modal('show')
      this.reinitialiseBootstrapSelect()
    },
    saveUser () {
      var affiliation = []
      each(this.affiliationBySector, (value) => {
        affiliation.push(...value)
      })
      this.$store.dispatch('saveAffiliation', {'user': this.userToEdit.id, 'affiliation': affiliation})
    },
    cancelUser () {
      this.userToEdit = null
    },
    reinitialiseBootstrapSelect () {
      $(function () {
        $('.selectpicker').selectpicker()
      })
    },
  }
}
</script>
