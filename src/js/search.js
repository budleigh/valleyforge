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
            if (this.ss.searching) {
                this.socket.close();
                // close before opening a new mone
            }
            this.openSearchSocket();
        },

        stop: function () {
            this.socket.close();
        },

        openSearchSocket: function () {
            this.$dispatch('start-searching');
            this.socket = new WebSocket(this.socketURI);

            this.socket.onopen = () => {
                this.socket.send(this.words);
            };

            this.socket.onmessage = (event) => {
                this.$dispatch('new-anagram', event.data);
            };

            this.socket.onclose = () => {
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