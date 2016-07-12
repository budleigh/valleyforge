/**
 * The main app object, that 'contains' all components
 * and listens to their events, such that the events
 * trigger changes in the state object. All state changes
 * go through this object, no child component should be
 * allowed to directly manipulate the state.
 */
var app = new Vue({
    el: '#app',
    events: {
        // these all bubble up from child components
        'start-searching': function () {
            this.ss.anagrams = [];
            this.ss.searching = true;
        },

        'stop-searching': function () {
            this.ss.searching = false;
        },

        'new-anagram': function (anagram) {
            this.ss.anagrams.push(anagram);
        }
    }
});