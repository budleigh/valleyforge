/**
 * Created by budleigh on 7/11/16.
 */

Vue.config.delimiters = ['[[', ']]']; // clashes with template {}

/**
 * Create a 'global state' fluxy-type thing that stores
 * variables you know multiple components may want to
 * read/write to - but only allow writing via events
 * listened to by the parent app, which is the delegate
 * manager of this state.
 */
var state = {
    anagrams: []
};

// this registers a 'global mixin' - that is, EVERY vue
// component receives the provided structure. this is
// usually bad but ok to implement fluxy-type stuff.
Vue.mixin({
    data: function () {
        return {
            ss: state,
            ps: {}
        }
    }
});

/**
 * Search bar component. This will fire a socket at the
 * server, and the server will run the non-blocking
 * anagram computations, streaming results back here.
 */
Vue.component('search', {
    template: '#search',
    data: function () {
        return {
            words: ''
        }
    }
});

/**
 * Anagram list component. Listens to changes in the
 * anagrams variable in the global state and renders
 * them to a well list.
 */
Vue.component('anagrams', {
    template: '#anagrams',
    data: function () {
        return {
            anagrams: []
        }
    }
});

/**
 * The main app object, that 'contains' all components
 * and listens to their events, such that the events
 * trigger changes in the state object. All state changes
 * go through this object, no child component should be
 * allowed to directly manipulate the state.
 * @type {Vue}
 */
var app = new Vue({
    el: '#app'
});