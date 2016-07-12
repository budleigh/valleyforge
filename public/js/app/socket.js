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