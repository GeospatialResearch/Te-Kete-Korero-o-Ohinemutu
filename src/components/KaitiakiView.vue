<template>
  <div class="content-info">
    <div class="row p-5">
      <div class="col-lg-12 mt-3 mb-3">
        <h4>Submitted narratives</h4>
        <div v-if="nests && allPublications.length > 0">
          <div>
            <table class="table table-hover table-borderless">
              <thead>
                <tr>
                  <th scope="col" class="fit" colspan="2">
                    User
                  </th>
                  <th scope="col" class="fit">
                    Narrative title
                  </th>
                  <th scope="col" class="fit">
                    Narrative status
                  </th>
                  <th scope="col" class="fit">
                    Status modified date
                  </th>
                  <th scope="col" class="fit">
                    Nest
                  </th>
                  <th scope="col" class="fit">
                    Reviewed by
                  </th>
                </tr>
              </thead>
              <tbody v-for="item in allPublications" :key="item.id">
                <td scope="col" class="fit" colspan="2">
                  {{ getAuthFullName(item.story.owner) }}
                </td>
                <td>
                  <span v-if="item.story.title.eng">{{ item.story.title.eng }}</span>
                  <span v-else>{{ item.story.title.mao }}</span>
                </td>
                <td>
                  {{ item.status }}
                </td>
                <td>
                  {{ item.status_modified_on | moment("MMMM Do, YYYY") }}
                </td>
                <td>
                  {{ item.nest.kinship_sector.name }} {{ item.nest.name }}
                </td>
                <td v-if="reviews">
                  {{ getAuthFullName(reviews.filter(x => x.publication.id == item.id).map(y => y.reviewer_id)[0]) }}
                </td>
                <td v-if="item.story.owner !== user.id">
                  <button type="button" class="btn btn-sm btn-primary" title="open story" @click="openNarrative(item.story.id, item)">
                    Open narrative
                  </button>
                </td>
              </tbody>
            </table>
          </div>
        </div>
        <p v-else class="text-muted">
          No publications available
        </p>
      </div>
      <hr>
    </div>
  </div>
</template>

<script>
import { EventBus } from 'store/event-bus'
// import { delay } from 'underscore'

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
    allUsers() {
      return this.$store.state.allUsers
    },
    allPublications(){
      return this.$store.state.publications.filter(pub => pub.nest.kaitiaki.map(item => item.id).includes(this.user.id)).filter(x => x.status !== "DRAFT").reverse()
    },
    reviews(){
      return this.$store.state.reviews
    }
  },
  methods: {
    getAuthFullName(userid){
      if(userid)
      {
        let author = this.allUsers.filter(user=>user.id === userid)[0]
        return `${author.username} ( ${author.first_name} ${author.last_name} )`
      }
      else {
        return
      }

    },
    openNarrative(story_id, publication){
      this.$store.commit('TOGGLE_CONTENT', 'map')
      if(publication && publication.status == 'SUBMITTED')
      {
        this.$store.commit('SET_SUBMITTED_PUB', publication)
      }
      this.$store.dispatch('getStoryContent', story_id)
      .then((story) => {
        this.$store.commit('SET_STORY_VIEW_MODE', true)
        this.$store.commit('SET_PANEL_OPEN', true)
        EventBus.$emit('addStoryGeomsToMap', story.storyBodyElements)
      })
    }
  }
}
</script>
