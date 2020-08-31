<template>
  <div class="content-info">
    <div class="row p-5">
      <div class="col-lg-12 settings-title">
        <h2>Nests settings</h2>
      </div>
      <div class="col-lg-12 mt-3">
        <button class="btn btn-primary float-right" @click="addNewNestOpenModal()">
          <font-awesome-icon icon="plus" size="lg" />
          Add new nest
        </button>
      </div>
      <div class="col-lg-12 pt-4 pt-lg-5 nests-table">
        <table class="table table-hover">
          <thead>
            <tr>
              <th scope="col">
                Name
              </th>
              <th scope="col">
                Unit
              </th>
              <th scope="col">
                Kaitiaki
              </th>
              <th scope="col" />
            </tr>
          </thead>
          <tbody v-for="(sectornests, sectorkey) in nestsBySector" :key="sectorkey">
            <tr v-for="(nest, nestkey) in sectornests" :key="'nest'+nestkey">
              <td class="nest-name">
                {{ nest.name }}
              </td>
              <td v-if="nest.kinship_sector">
                <span>{{ nest.kinship_sector.name }}</span>
              </td>
              <td>
                <span v-for="(k, key) in nest.kaitiaki" :key="key">
                  {{ k.username }}<span v-if="key != nest.kaitiaki.length - 1">,</span>
                </span>
              </td>
              <td v-if="nest.kinship_sector.name == 'Iwi'">
                <a href="#" type="button" class="btn btn-sm btn-primary" title="Edit nest" @click="editNest(nest)">
                  <i><font-awesome-icon icon="pen" /></i>
                </a>
                <a v-if="user && user.is_superuser" href="#" type="button" class="btn btn-sm btn-danger" title="Delete nest" @click="deleteNestOpenModal(nest)">
                  <i><font-awesome-icon icon="trash" /></i>
                </a>
              </td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
    <div id="editNestModal" class="modal fade" data-backdrop="static">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4 class="mb-0">
              Nest settings
            </h4>
          </div>
          <div class="modal-body">
            <form>
              <div class="form-group">
                <label for="nestName">Name</label>
                <input id="nestName" v-model="nestToEdit.name" type="text" class="form-control">
              </div>
              <div>
                <label for="kinshipSector">Unit</label>
                <span>
                  <font-awesome-icon icon="info-circle" size="lg" color="grey" title="The users create their own whanau nests" />
                </span>
                <select v-if="sectors" id="kinshipSector" v-model="nestToEdit.kinship_sector_id" class="selectpicker form-control form-control-sm mb-3" title="Select one political unit">
                  <!-- <option v-for="sector in sectors.filter(x=>x.name !== 'Whānau')" :key="sector.id" :value="sector.id"> -->
                  <option v-for="sector in sectors.filter(x=>x.name == 'Iwi')" :key="sector.id" :value="sector.id">
                    {{ sector.name }}
                  </option>
                </select>
              </div>
              <div>
                <label for="kaitiaki">Kaitiaki</label>
                <select id="kaitiaki" v-model="nestToEdit.kaitiaki" class="selectpicker form-control form-control-sm mb-3" multiple title="Select one or more kaitiaki">
                  <option v-for="a_user in allUsers.filter(x => x.username !== 'admin')" :key="a_user.id" :value="a_user.id">
                    {{ getAuthFullName(a_user.id) }}
                  </option>
                  <!-- Only nest members (not allUsers) are listed here below to be picked as kaitiaki   -->
                  <!-- <option v-for="a_user in nestToEdit.members" :key="a_user.user_id" :value="a_user.user_id">
                    {{ getAuthFullName(a_user.user_id) }}
                  </option> -->
                </select>
              </div>
            </form>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal" @click="cancelNest()">
              Cancel
            </button>
            <button class="btn btn-danger btn-ok" data-dismiss="modal" @click="saveNest()">
              Save
            </button>
          </div>
        </div>
      </div>
    </div>
    <div id="deleteNestModal" class="modal fade">
      <div class="modal-dialog">
        <div class="modal-content">
          <div class="modal-header">
            <h4>Delete nest</h4>
          </div>
          <div v-if="nestToDelete" class="modal-body">
            <p>
              Are you sure you want to delete the nest {{ nestToDelete.name }}?
            </p>
            <p>
              NOTE: The narratives published in this nest will become unpublished and only their authors will be able to access them.<br>
            </p>
          </div>
          <div class="modal-footer">
            <button type="button" class="btn btn-secondary" data-dismiss="modal">
              Cancel
            </button>
            <button type="button" class="btn btn-danger" data-dismiss="modal" @click="deleteNest()">
              Delete
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
      nestToEdit: {
        name: null,
        kinship_sector_id: null,
        kaitiaki: [],
        members: []
      },
      nestToDelete: null
    }
  },
  computed: {
    user () {
      return this.$store.state.user
    },
    sectors () {
      return this.$store.state.sectors
    },
    nests () {
      return this.$store.state.nests
    },
    nestsBySector () {
      var nestsBySector = {}
      var sectors_names

      if (this.sectors && this.nests) {
        if (this.user && this.user.is_superuser) {
          sectors_names = this.sectors.map(x => x.name)
        } else {
          // sectors_names = this.sectors.filter(x=>x.name !== 'Whānau').map(x => x.name)
          // To have only ngati whakaue where the kaitiaki can be assigned
          sectors_names = this.sectors.filter(x=>x.name == 'Iwi').map(x => x.name)
        }
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
    allUsers() {
      return this.$store.state.allUsers
    }
  },
  methods: {
    editNest (nest) {
      this.reinitialiseBootstrapSelect()
      this.nestToEdit.id = nest.id
      this.nestToEdit.name = nest.name
      this.nestToEdit.kinship_sector_id = nest.kinship_sector.id
      this.nestToEdit.kaitiaki = nest.kaitiaki.map(x => x.id)
      this.nestToEdit.members = nest.members
      $('#editNestModal').modal('show')
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
    saveNest () {
      if (this.nestToEdit.id) {
        this.$store.dispatch('updateNest', $.extend(true, {}, this.nestToEdit))
      } else {
        this.$store.dispatch('addNest', $.extend(true, {}, this.nestToEdit))
      }
    },
    cancelNest () {
      this.nestToEdit = {
        name: null,
        kinship_sector_id: null,
        kaitiaki: []
      }
    },
    deleteNest () {
      this.$store.dispatch('deleteNest', $.extend(true, {}, this.nestToDelete))
      this.nestToDelete = null
    },
    deleteNestOpenModal (nest) {
      this.nestToDelete = nest
      $('#deleteNestModal').modal('show')
    },
    addNewNestOpenModal () {
      this.reinitialiseBootstrapSelect()
      this.cancelNest()
      $('#editNestModal').modal('show')
    },
    getAuthFullName(userid){
      let author = this.allUsers.filter(user=>user.id === userid)[0]
      return `${author.username} ( ${author.first_name} ${author.last_name} )`
    }
  }
}
</script>
