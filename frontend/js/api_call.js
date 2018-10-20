
function get_request(url, callback) {
    var request = new XMLHttpRequest();
    request.open("get", endpoint);
    request.onreadystatechange = callback;
    request.send();
}

function get_simulators(ip, port, callback) {
    var endpoint = "http://" + ip + ":" + port + "/get_simulators?simulator=bouncing_ball";
    get_request(endpoint, callback);
}

function get_param_names(ip, port, callback, simulator) {
    var endpoint = "http://" + ip + ":" + port + "/get_param_names?simulator=" + simulator;
    get_request(endpoint, callback);
}
