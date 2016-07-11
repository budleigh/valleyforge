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

class SearchSocket {
    constructor (words) {
        this.socket = new WebSocket(constructWSURI());
        this.socket.onopen = () => {
            console.log('open');
        };
        this.socket.onmessage = (event) => {
            console.log(event.data);
        };
        this.socket.onclose = () => {
            console.log('closed');
        }
    }
}