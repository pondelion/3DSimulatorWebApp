function init() {
    var isSimulating = false;
    var ip = "127.0.0.1";
    var port = "5000";
    var paramNames = {};
    var objs = {};  // {オブジェクト名: オブジェクトインスタンス}の辞書
    var paramObjs = {};  // {パラメータ名: {'object': オブジェクトインスタンス, 'param}}
    var statesDefinition = {};
    var rotateCamera = false;

    var scene = new THREE.Scene();
    var camera = new THREE.PerspectiveCamera(45, window.innerWidth / window.innerHeight, 0.1, 1000);
    scene.add(camera);

    var renderer = new THREE.WebGLRenderer();

    renderer.setClearColor(new THREE.Color(0x222222));
    renderer.setSize(window.innerWidth, window.innerHeight);
    renderer.shadowMap.enabled = true;

    camera.position.x = -30;
    camera.position.y = 40;
    camera.position.z = 40;
    camera.lookAt(scene.position);

    var ambientLight = new THREE.AmbientLight(0x0c0c0c);
    scene.add(ambientLight);

    var spotLight = new THREE.SpotLight(0xffffff);
    spotLight.position.set(-20, 30, -5);
    spotLight.castShadow = true;
    scene.add(spotLight);

    var sphere;

    gui = new dat.GUI();
    
    var controls = new function () {
        this.ip = ip;
        this.port = port;
        this.simulators = "";
        this.rotate_camera = false;
        this.run = false;
        this.init = function(){ initSimulation(ip, port, function () {}, controls.simulators);};
    };

    gui.add(controls, "ip").onChange(function(newIP) {
        ip = newIP;
    });
    gui.add(controls, "port").onChange(function(newPORT) {
        port = newPORT;
    });
    gui.add(controls, "rotate_camera").onChange(function() {
        rotateCamera = !rotateCamera;
    });

    getParamNamesCallback = function() {
        if (this.readyState == 4) {
            console.log(this.responseText);
            paramNames = JSON.parse(this.responseText).param_names;
            for (var paramName in paramNames) {
                if (paramNames[paramName].param_type == "textbox") {
                    controls[paramName] = paramNames[paramName].default;
                    gui.add(controls, paramName)
                        .min(paramNames[paramName].min)
                        .max(paramNames[paramName].max)
                        .step(paramNames[paramName].step)
                        .onChange(function(newValue) {
                            //console.log(this);
                            var params = {}
                            for (var paramName in paramNames) {
                                params[this.property] = controls[this.property];
                            }
                            setParams(ip, port, function () {}, controls.simulators, params, 'numeric');
                            //console.log("paramObjs : " + JSON.stringify(paramObjs));
                            if (paramObjs[this.property]) {
                                if (objs[paramObjs[this.property].object_name]) {
                                    setObjectProperty(
                                        objs[paramObjs[this.property].object_name].object,
                                        paramObjs[this.property].property,
                                        controls[this.property]
                                    );
                                }
                            }
                        });
                } else if (paramNames[paramName].param_type == "button") {
                    controls[paramName] = function() {};
                    gui.add(controls, paramName)
                } else if (paramNames[paramName].param_type == "checkbox") {
                    controls[paramName] = paramNames[paramName].default
                    gui.add(controls, paramName)
                }

                if (paramNames[paramName].object_name) {
                    paramObjs[paramName] = {}
                    paramObjs[paramName]['object_name'] = paramNames[paramName].object_name
                }

                if (paramNames[paramName].object_property) {
                    paramObjs[paramName]['property'] = paramNames[paramName].object_property;
                }
            }

            gui.add(controls, 'run').onChange(function(checked) {
                if (checked) {
                    runSimulation(ip, port, function () {}, controls.simulators);
                } else {
                    stopSimulation(ip, port, function () {}, controls.simulators);
                }
            });
            gui.add(controls, 'init');
        }
    };

    setSimulatorCallback = function() {
        // var url = "http://" + ip + ":" + port + "/get_states_streaming?simulator=" + controls.simulators;
        // fetch(url)
        //     .then((response) => response.body.getReader())
        //     .then((reader) => {
        //         for (var i = 0; i < 10; ++i) {
        //             reader.read().then(({done, value}) => {
        //                 console.log(JSON.parse(value));
        //             });
                    
        //         }
        //     });
    };

    getObjectsCallback = function() {
        if (this.readyState == 4) {
            console.log(this.responseText);
            var objects = JSON.parse(this.responseText).objects;
            for (var object in objects) {
                if (objects[object].num) {
                    var n = objects[object].num;
                    for (var i = 0; i < n; ++i) {
                        objs[object + i] = {};
                    }
                } else {
                    objs[object] = {}
                }
                console.log(objects[object].object_type);
                pos_x = objects[object].initial_pos_x;
                pos_y = objects[object].initial_pos_y;
                pos_z = objects[object].initial_pos_z;
                objs[object]['pos_x'] = pos_x;
                objs[object]['pos_y'] = pos_y;
                objs[object]['pos_z'] = pos_z;

                if (objects[object].object_type == "sphere") {
                    objs[object]["object_type"] = "sphere";
                    radius = objects[object].initial_radius;
                    //sphere = addSphere(scene, pos_x, pos_y, pos_z, radius);
                    objs[object]['radius'] = radius;
                } else if (objects[object].object_type == "plane") {
                    objs[object]["object_type"] = "plane";
                    objs[object]['rotation_x'] = objects[object].initial_rotation_x;
                    objs[object]['rotation_y'] = objects[object].initial_rotation_y;
                    objs[object]['rotation_z'] = objects[object].initial_rotation_z;
                    objs[object]['size_h'] = objects[object].initial_size_h;
                    objs[object]['size_w'] = objects[object].initial_size_w;
                } else if (objects[object].object_type == "arrow") {
                    objs[object]["object_type"] = "arrow";
                    objs[object]['rotation_x'] = objects[object].initial_rotation_x;
                    objs[object]['rotation_y'] = objects[object].initial_rotation_y;
                    objs[object]['rotation_z'] = objects[object].initial_rotation_z;
                }
            }
            initObjects(scene, objs);
        };
    };

    getStatesDefinitionCallback = function() {
        if (this.readyState == 4) {
            console.log(this.responseText);
            statesDefinition = JSON.parse(this.responseText).states_definition;
        }
    };
    
    getSimulatorsCallback = function() {
        if (this.readyState == 4) {
            console.log(this.responseText);
            gui.add(controls, "simulators")
                .options(JSON.parse(this.responseText).simulators)
                .onChange(function(selectedSimulator) {
                    setSimulator(ip, port, setSimulatorCallback, selectedSimulator);
                    getParamNames(ip, port, getParamNamesCallback, selectedSimulator);
                    getObjects(ip, port, getObjectsCallback, selectedSimulator);
                    getStatesDefinition(ip, port, getStatesDefinitionCallback, selectedSimulator);
                });
        }
    };
    getSimulators(ip, port, getSimulatorsCallback);

    document.getElementById("3DScene").appendChild(renderer.domElement);

    render();
    var count = 0;

    function render() {
        count += 1;
        if (rotateCamera) {
            camera.position.x = 40 * Math.cos(count*0.01);
            camera.position.z = 40 * Math.sin(count*0.01);
            camera.lookAt(new THREE.Vector3(0, 0, 0))
        }

        if (controls.simulators != "") {
            if (count % 3 == 0) {
                getStatesCallback = function() {
                    if (this.readyState == 4) {
                        //console.log(this.responseText);
                        var states = JSON.parse(this.responseText).states;
                        
                        updateStates(states, statesDefinition)
                        //sphere.position.y = states.height;
                        //console.log(objs);
                    }
                }
                getStates(ip, port, getStatesCallback, controls.simulators);
            }
        }

        requestAnimationFrame(render);
        renderer.render(scene, camera);
    }

    function initObjects(scene, objects) {
        for (objName in objects) {
            object = objects[objName];
            console.log(object);
            if (object["object_type"] == "sphere") {
                obj = createSphere(object["pos_x"], object["pos_y"], object["pos_z"], object["radius"]);
                objects[objName]['object'] = obj;
                console.log(objects);
                scene.add(obj);
            } else if (object["object_type"] == "plane") {
                obj = createPlane(pos_x=object["pos_x"], pos_y=object["pos_y"], pos_z=object["pos_z"], 
                                        rotation_x=object["rotation_x"], rotation_y=object["rotation_y"], 
                                        rotation_z=object["rotation_z"]);
                objects[objName]['object'] = obj;
                console.log(objects);
                scene.add(obj);
            } else if (object["object_type"] == "arrow") {
                obj = createArrow(name="arrow"+i, pos_x=object["pos_x"], pos_y=object["pos_y"], pos_z=object["pos_z"], 
                                rotation_x=object["rotation_x"], rotation_y=object["rotation_y"], rotation_z=object["rotation_z"]);
                objects[objName]['object'] = obj;
                console.log(objects);
                scene.add(obj);
            }
        }
    }

    function updateStates(states, statesDefinition) {
        for (stateName in states) {
            //console.log("stateName : " + stateName);
            if (stateName in statesDefinition) {
                def = statesDefinition[stateName];
                //console.log("def : " + JSON.stringify(def));
                val = states[stateName];
                if ("object_name" in def) {
                    console.log("objs : " + JSON.stringify(objs));
                    object = objs[def["object_name"]].object;
                    if ("property" in def) {
                        setObjectProperty(object, def["property"], val)
                    }
                }
            } 
        }
    }

    function setObjectProperty(object, property_type, val) {
        if (property_type == "pos_x") {
            object.position.x = val;
        } else if (property_type == "pos_y") {
            object.position.y = val;
        } else if (property_type == "pos_z") {
            object.position.z = val;
        } else if (property_type == "radius") {
            object.scale.x = 0.33*val;
            object.scale.y = 0.33*val;
            object.scale.z = 0.33*val;
        }
    }
}
