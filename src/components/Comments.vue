<template>
  <div id="comments" class="row">
    <div class="col-md-12 pl-4 pr-4" style="background-color:#ffffff;">
      <div class="detail-box">
        <div class="title-box">
          <font-awesome-icon icon="comments" class="mr-2" />
          <label>{{ translationObj.comments[lang] }}
            <span v-if="story.comments">
              ({{ story.comments.length }})
            </span>
          </label>
        </div>
        <div v-if="authenticated" class="comment-box">
          <form class="form-inline" role="form">
            <div class="form-group pr-3">
              <textarea v-model="comment" class="form-control form-control-sm" type="text" placeholder="Your comment" />
            </div>
            <div class="form-group">
              <font-awesome-icon v-if="isLoadingComment" icon="spinner" spin size="lg" />
              <button v-else class="btn btn-sm btn-success float-right" @click="addComment()">
                {{ translationObj.add[lang] }}
              </button>
            </div>
          </form>
        </div>
        <div class="action-box">
          <ul class="comment-list">
            <li v-if="story.comments && story.comments.length==0" class="text-center text-muted">
              <p>
                There are no comments
              </p>
            </li>
            <li v-for="comm in story.comments" v-else :key="comm.id">
              <div class="commenter-image">
                <img src="static/img/user.jpg">
              </div>
              <div class="comment-text">
                <p>
                  {{ comm.comment }}
                </p>
                <span class="sub-text">{{ comm.user }}</span>
                <span class="date sub-text-grey">on {{ comm.date | moment("MMMM Do, YYYY") }} ({{ comm.date | moment('from', 'now') }})</span>
              </div>
            </li>
          </ul>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { langObj } from 'utils/initialTranslObj'
export default {
  data () {
    return {
      comment: null,
      isLoadingComment: false
    }
  },
  computed: {
    story() {
      return this.$store.state.storyContent
    },
    authenticated () {
      return this.$store.state.authenticated
    },
    user () {
      return this.$store.state.user
    },
    lang () {
      return this.$store.state.lang
    },
    translationObj () {
      if (this.$store.state.websiteTranslObj) {
        return this.$store.state.websiteTranslObj
      } else {
        return langObj
      }
    }
  },
  methods: {
    addComment () {
      this.isLoadingComment = true
      var comment = {
        'comment': this.comment,
        'story': this.story.id,
      }
      this.$store.dispatch('addComment', comment)
      .then(() => {
        this.comment = null
        this.isLoadingComment = false
      })
    }
  }
}
</script>
