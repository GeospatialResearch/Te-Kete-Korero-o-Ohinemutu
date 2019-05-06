import Vue from 'vue'
export const EventBus = new Vue()

// This is how you use it:
// Import: import { EventBus } from '../store/event-bus.js'
// Send event: EventBus.$emit('refresh-map')
// OR
// Subscribe: EventBus.$on('refresh-map', this.handleResize)

// Note that this is just for events, and for shared state, use the store.
