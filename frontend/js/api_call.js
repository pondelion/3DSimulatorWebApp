
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

function runSimulation(ip, port, callback, simulator) {
    var endpoint = "http://" + ip + ":" + port + "/run_simulation?simulator=" + simulator;
    getRequest(endpoint, callback);
}

function stopSimulation(ip, port, callback, simulator) {
    var endpoint = "http://" + ip + ":" + port + "/stop_simulation?simulator=" + simulator;
    getRequest(endpoint, callback);
}

function getStates(ip, port, callback, simulator, n=1) {
    var endpoint = "http://" + ip + ":" + port + "/get_states?simulator=" + simulator + '&n=' + n;
    getRequest(endpoint, callback);
}

function initSimulation(ip, port, callback, simulator) {
    var endpoint = "http://" + ip + ":" + port + "/init_simulation?simulator=" + simulator;
    getRequest(endpoint, callback);
}
