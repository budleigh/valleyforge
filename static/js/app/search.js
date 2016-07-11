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
            socket: undefined,
            socketURI: constructWSURI()
        }
    },
    methods: {
        search: function () {
            this.$dispatch('start-searching');
            this.socket = new WebSocket(this.socketURI);
            this.socket.onopen = () => {
                console.log('socket open');
            }
        }
    }
});