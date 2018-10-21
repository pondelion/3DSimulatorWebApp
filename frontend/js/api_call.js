
function getRequest(url, callback) {
    var request = new XMLHttpRequest();
    request.open("get", url);
    request.onreadystatechange = callback;
    request.send();
}

function getSimulators(ip, port, callback) {
    var endpoint = "http://" + ip + ":" + port + "/get_simulators?simulator=bouncing_ball";
    getRequest(endpoint, callback);
}

function getParamNames(ip, port, callback, simulator) {
    var endpoint = "http://" + ip + ":" + port + "/get_param_names?simulator=" + simulator;
    getRequest(endpoint, callback);
}

function setSimulator(ip, port, callback, simulator) {
    var endpoint = "http://" + ip + ":" + port + "/set_simulator?simulator=" + simulator;
    getRequest(endpoint, callback);
}

function getObjects(ip, port, callback, simulator) {
  var endpoint = "http://" + ip + ":" + port + "/get_objects?simulator=" + simulator;
  getRequest(endpoint, callback);
}
