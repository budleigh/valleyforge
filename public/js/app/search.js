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
            // coming into the SearchSocket handler
            var newAnagramCB = this.$dispatch.bind(this, 'new-anagram');
            this.socket = new SearchSocket(this.words, newAnagramCB);
        }
    }
});