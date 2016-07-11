Vue.config.delimiters = ['[[', ']]']; // clashes with template {}

/**
 * Create a 'global state' fluxy-type thing that stores
 * variables you know multiple components may want to
 * read/write to - but only allow writing via events
 * listened to by the parent app, which is the delegate
 * manager of this state.
 */
var state = {
    anagrams: [],
    searching: false
};

/**
 * this registers a 'global mixin' - that is, EVERY vue component
 * receives the provided structure. this is usually bad but ok to
 * implement fluxy-type stuff.
 */
Vue.mixin({
    data: function () {
        return {
            ss: state
        }
    }
});