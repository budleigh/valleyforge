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
            // how many permutations the server has checked
            // IN TOTAL, so this will get fairly large
            permutations: 0,
            socket: undefined,
            // relative URI, see util func below
            socketURI: constructWSURI()
        }
    },
    methods: {
        search: function () {
            if (this.ss.searching) {
                this.socket.close();
                // close before opening a new mone
            }
            this.openSearchSocket();
        },

        stop: function () {
            // close dispatches stop-searching
            this.socket.close();
        },

        openSearchSocket: function () {
            /**
             * Each search gets its own socket. the
             * previous socket is killed for each new
             * one so we don't get overlapping results.
             */
            this.$dispatch('start-searching');
            this.permutations = 0;
            this.socket = new WebSocket(this.socketURI);

            this.socket.onopen = () => {
                // this is done once, and this initializes
                // the worker thread on the server to start
                // processing and sending back results
                this.socket.send(this.words);
            };

            this.socket.onmessage = (event) => {
                if (event.data.indexOf('---') !== -1) {
                    // this is a ping coming from the server
                    // it keeps heroku alive and we get a
                    // permutation count from it
                    this.permutations = parseInt(event.data.split(' ')[1]);
                } else {
                    this.$dispatch('new-anagram', event.data);
                }
            };

            this.socket.onclose = () => {
                // if we start a new search, the new one might
                // open before the old one closes, so we need
                // to monitor 'this.socket' as it changes so
                // we dont do anything silly with the UI
                if (this.socket.readyState === this.socket.CLOSED) {
                    this.$dispatch('stop-searching');
                }
            }
        }
    }
});

/**
* constructs a 'relative' websocket URI path
* is also sensitive to the protocol the pagewas
* grabbed - https = wss, http = ws
*/
function constructWSURI () {
    var loc = window.location, uri;
    if (loc.protocol === "https:") {
        uri = "wss:";
    } else {
        uri = "ws:";
    }
    uri += "//" + loc.host;
    return uri += loc.pathname + "socket/";
}