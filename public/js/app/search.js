/**
 * Search bar component. This will fire a socket at the
 * server, and the server will run the non-blocking
 * anagram computations, streaming results back here.
 */
Vue.component('search', {
    template: '#search',
    data: function () {
        return {
            words: '',
            socket: undefined
        }
    },
    methods: {
        search: function () {
            this.$dispatch('start-searching');
            // bind an event dispatcher to handle the new anagrams
            // coming into the SearchSocket handler. also set up a
            // 'socket-close' handler, indicating the search is finished
            var newAnagramCB = this.$dispatch.bind(this, 'new-anagram');
            var socketCloseCB = this.$dispatch.bind(this, 'stop-searching');
            this.socket = new SearchSocket(this.words, newAnagramCB, socketCloseCB);
        }
    }
});