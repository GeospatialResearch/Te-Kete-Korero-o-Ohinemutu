// var _ = require('underscore')
import { library } from '@fortawesome/fontawesome-svg-core'
import { faCoffee } from '@fortawesome/free-solid-svg-icons/faCoffee'
import { faChevronRight } from '@fortawesome/free-solid-svg-icons/faChevronRight'
import { faChevronLeft } from '@fortawesome/free-solid-svg-icons/faChevronLeft'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'

library.add(
  faCoffee, faChevronRight, faChevronLeft
)

export {
  FontAwesomeIcon
}
