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

/**
 * Handles communication with the permutation
 * processor thread on the server via a socket.
 * Takes a 'phrase' to send to the permutation
 * processing thread, takes results, then calls
 * whatever the newmessage handler callback is
 * (makes no expectations about binded-ness)
 */
class SearchSocket {
    constructor (words, messageCallback, closeCallback) {
        this.socket = new WebSocket(constructWSURI());

        this.socket.onmessage = (event) => {
            messageCallback(event.data);
        };

        this.socket.onclose = () => {
            closeCallback();
        }
    }
}