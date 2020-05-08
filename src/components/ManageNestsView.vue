<template>
  <div class="content-info">
    <div class="row p-5">
      <div class="col-lg-12 settings-title">
        <h2>Nests settings</h2>
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
          <tbody>
            <tr v-for="(nest, nestkey) in nests" :key="nestkey">
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
              <td><a href="#" @click="editNest(nest)">Edit</a></td>
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
            <form v-if="nestToEdit.name">
              <div class="form-group">
                <label for="nestName">Name</label>
                <input id="nestName" v-model="nestToEdit.name" type="text" class="form-control">
              </div>
              <div>
                <label for="kinshipSector">Unit</label>
                <select id="kinshipSector" v-model="nestToEdit.kinship_sector_id" class="selectpicker form-control form-control-sm mb-3" placeholder="Select one political unit">
                  <option v-for="sector in sectors" :key="sector.id" :value="sector.id">
                    {{ sector.name }}
                  </option>
                </select>
              </div>
              <div>
                <label for="kaitiaki">Kaitiaki</label>
                <select id="kaitiaki" v-model="nestToEdit.kaitiaki" class="selectpicker form-control form-control-sm mb-3" multiple title="Select one or more kaitiaki">
                  <option v-for="user in allUsers" :key="user.id" :value="user.id">
                    {{ user.username }}
                  </option>
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
  </div>
</template>

<script>

export default {
  data () {
    return {
      nestToEdit: {
        name: null,
        kinship_sector_id: null,
        kaitiaki: []
      }
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
    }
  },
  methods: {
    editNest (nest) {
      this.reinitialiseBootstrapSelect()
      this.nestToEdit.id = nest.id
      this.nestToEdit.name = nest.name
      this.nestToEdit.kinship_sector_id = nest.kinship_sector.id
      this.nestToEdit.kaitiaki = nest.kaitiaki.map(x => x.id)
      $('#editNestModal').modal('show')
    },
    reinitialiseBootstrapSelect () {
      $(function () {
        $('.selectpicker').selectpicker()
      })
    },
    saveNest () {
      this.$store.dispatch('updateNest', $.extend(true, {}, this.nestToEdit))
    },
    cancelNest () {
      this.nestToEdit = {
        name: null,
        kinship_sector_id: null,
        kaitiaki: []
      }
    }
  }
}
</script>
