/**
 * The main app object, that 'contains' all components
 * and listens to their events, such that the events
 * trigger changes in the state object. All state changes
 * go through this object, no child component should be
 * allowed to directly manipulate the state.
 * @type {Vue}
 */
var app = new Vue({
    el: '#app',
    events: {
        'start-searching': function () {
            this.ss.searching = true;
        }
    }
});