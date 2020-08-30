<template>
  <div :id="prefix + '_affiliationForm'">
    <form v-if="affiliationBySector" class="p-2">
      <div v-if="formPrefix == 'profile'">
        <div v-for="(sector, sectorkey) in nestsBySector" :key="prefix+'_sector'+sectorkey">
          <div v-if="sector.length > 0 && sector.filter(item=>!affiliationBySector[sectorkey].includes(item.id) && !Requests.map(item=>item.nest_id).includes(item.id)).length > 0">
            <label :for="sectorkey"><strong>{{ sectorkey }}</strong></label>
            <select v-model="affiliationBySector[sectorkey]" class="selectpicker form-control form-control-sm mb-3" multiple :title="'Select one or more ' + sectorkey" @change="sendAffiliation()">
              <option v-for="nest in sector.filter(item=>!affiliationBySector[sectorkey].includes(item.id) && !Requests.map(item=>item.nest_id).includes(item.id))" :key="prefix+'_nest'+nest.id" :value="nest.id">
                {{ nest.name }}
              </option>
            </select>
          </div>
          <!-- <p v-else class="text-muted">
            There are no {{ sectorkey }} nests defined yet
          </p> -->
        </div>
      </div>
      <div v-else>
        <div v-for="(sector, sectorkey) in nestsBySector" :key="prefix+'_sector'+sectorkey">
          <label :for="sectorkey"><strong>{{ sectorkey }}</strong></label>
          <select v-if="sector.length > 0" v-model="affiliationBySector[sectorkey]" class="selectpicker form-control form-control-sm mb-3" multiple :title="'Select one or more ' + sectorkey" @change="sendAffiliation()">
            <option v-for="nest in sector" :key="prefix+'_nest'+nest.id" :value="nest.id">
              {{ nest.name }}
            </option>
          </select>
          <p v-else class="text-muted">
            There are no {{ sectorkey }} nests defined yet
          </p>
        </div>
      </div>
    </form>
    <div v-if="formPrefix == 'manageuser_'+profile.user">
      <h5>Other settings</h5>
      <div class="form-check">
        <input id="staffSetting" v-model="isStaff" type="checkbox" class="form-check-input" @change="sendStaffSetting()">
        <label class="form-check-label" for="staffSetting">Is Tool Manager</label><br>
        <small>(capable of accessing and modifying Users Settings and Nests Settings pages)</small>
      </div>
    </div>
  </div>
</template>

<script>

import { each } from 'underscore'

export default {
  props: {
    userProfile: {
      default: function () { return {} },
      type: Object
    },
    staff: {
      default: false,
      type: Boolean
    },
    prefix: {
      default: '',
      type: String
    },
    accessRequests: {
      default:  function () { return [] },
      type: Array
    }
  },
  data () {
    return {
      profile: this.userProfile,
      formPrefix: this.prefix,
      isStaff: this.staff,
      Requests:this.accessRequests
    }
  },
  computed: {
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
        var sectors_names = this.sectors.filter(x=>x.name !== 'Tātou' && x.name !== 'Whānau' && x.name !== 'Koromatua Hapū' && x.name !== 'Hapū').map(x => x.name)
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
        var sectors_names = this.sectors.filter(x=>x.name !== 'Tātou' && x.name !== 'Whānau' && x.name !== 'Koromatua Hapū' && x.name !== 'Hapū').map(x => x.name)
        each(sectors_names, (name) => {
          affiliationBySector[name] = []
        })
      }
      each(this.nests, (nest) => {
        if (this.profile && this.profile.affiliation.includes(nest.id)) {
          if (affiliationBySector[nest.kinship_sector.name]) {
            affiliationBySector[nest.kinship_sector.name].push(nest.id)
          }
        }
      })
      return affiliationBySector
    }
  },
  methods: {
    sendAffiliation () {
      this.$emit('childToParentAffiliation', this.affiliationBySector)
    },
    sendStaffSetting () {
      this.$emit('childToParentStaffSetting', this.isStaff)
    }
  }
}
</script>
