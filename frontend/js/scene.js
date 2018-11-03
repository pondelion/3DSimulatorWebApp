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
    camera.position.y = 20;
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
                if (paramNames[paramName].param_type == "slider_textbox") {
                    controls[paramName] = paramNames[paramName].default;
                    gui.add(controls, paramName)
                        .min(paramNames[paramName].min)
                        .max(paramNames[paramName].max)
                        .step(paramNames[paramName].step)
                        .onChange(function(newValue) {
                            var params = {}
                            for (var paramName in paramNames) {
                                params[this.property] = controls[this.property];
                            }
                            setParams(ip, port, function () {}, controls.simulators, params, 'numeric');
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
                } else if (paramNames[paramName].param_type == "textbox") {
                    controls[paramName] = paramNames[paramName].default;
                    gui.add(controls, paramName)
                        .onChange(function(newValue) {
                        
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
                    var n = 1;
                    objs[object] = {}
                }
                console.log(objects[object].object_type);

                for (var i = 0; i < n; ++i) {

                    if (n == 1) {
                        var nameSuffix = "";
                    } else {
                        var nameSuffix = i;
                    }

                    var objName = object + nameSuffix;

                    pos_x = objects[object].initial_pos_x;
                    pos_y = objects[object].initial_pos_y;
                    pos_z = objects[object].initial_pos_z;
                    objs[objName]['pos_x'] = pos_x;
                    objs[objName]['pos_y'] = pos_y;
                    objs[objName]['pos_z'] = pos_z;

                    if (objects[object].opacity) {
                        objs[objName]['opacity'] = objects[object].opacity;
                    } else {
                        objs[objName]['opacity'] = 1.0;
                    }

                    if (objects[object].object_type == "sphere") {
                        objs[objName]["object_type"] = "sphere";
                        radius = objects[object].initial_radius;
                        objs[objName]['radius'] = radius;
                    } else if (objects[object].object_type == "plane") {
                        objs[objName]["object_type"] = "plane";
                        objs[objName]['rotation_x'] = objects[object].initial_rotation_x;
                        objs[objName]['rotation_y'] = objects[object].initial_rotation_y;
                        objs[objName]['rotation_z'] = objects[object].initial_rotation_z;
                        objs[objName]['size_h'] = objects[object].initial_size_h;
                        objs[objName]['size_w'] = objects[object].initial_size_w;
                    } else if (objects[object].object_type == "arrow") {
                        objs[objName]["object_type"] = "arrow";
                        objs[objName]['rotation_x'] = objects[object].initial_rotation_x;
                        objs[objName]['rotation_y'] = objects[object].initial_rotation_y;
                        objs[objName]['rotation_z'] = objects[object].initial_rotation_z;
                    } else if (objects[object].object_type == "sprite") {
                        objs[objName]["object_type"] = "sprite";
                    } else if (objects[object].object_type == "box") {
                        objs[objName]["object_type"] = "box";
                        objs[objName]['size_x'] = objects[object].initial_size_x;
                        objs[objName]['size_y'] = objects[object].initial_size_y;
                        objs[objName]['size_z'] = objects[object].initial_size_z;
                    } 
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
                        var states = JSON.parse(this.responseText).states;
                        
                        updateStates(states, statesDefinition)
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
            if (object["object_type"] == "sphere") {
                obj = createSphere(object["pos_x"], object["pos_y"], object["pos_z"], object["radius"]);
                objects[objName]['object'] = obj;
                scene.add(obj);
            } else if (object["object_type"] == "plane") {
                obj = createPlane(pos_x=object["pos_x"], pos_y=object["pos_y"], pos_z=object["pos_z"], 
                                        rotation_x=object["rotation_x"], rotation_y=object["rotation_y"], 
                                        rotation_z=object["rotation_z"]);
                objects[objName]['object'] = obj;
                scene.add(obj);
            } else if (object["object_type"] == "arrow") {
                obj = createArrow(name=objName, pos_x=object["pos_x"], pos_y=object["pos_y"], pos_z=object["pos_z"], 
                                rotation_x=object["rotation_x"], rotation_y=object["rotation_y"], rotation_z=object["rotation_z"]);
                objects[objName]['object'] = obj;
                scene.add(obj);
            } else if (object["object_type"] == "sprite") {
                obj = createSprite(pos_x=object["pos_x"], pos_y=object["pos_y"], pos_z=object["pos_z"]);
                objects[objName]['object'] = obj;
                scene.add(obj);
            } else if (object["object_type"] == "box") {
                obj = createBox(pos_x=object["pos_x"], pos_y=object["pos_y"], pos_z=object["pos_z"],
                                size_x=object["size_x"], size_y=object["size_y"], size_z=object["size_z"], 
                                opacity=object["opacity"]);
                objects[objName]['object'] = obj;
                scene.add(obj);
            }
        }
        console.log(objs);
    }

    function updateStates(states, statesDefinition) {
        for (stateName in states) {
            if (stateName in statesDefinition) {
                def = statesDefinition[stateName];
                val = states[stateName];
                if ("object_name" in def) {
                    if ("property" in def) {
                        if (def.list) {
                            for (var i = 0; i < val[0].length; ++i) {
                                object = objs[def["object_name"] + i].object;
                                setObjectProperty(object, def["property"], val[0][i]);
                            }
                        } else {
                            object = objs[def["object_name"]].object;
                            setObjectProperty(object, def["property"], val);
                        }
                    }
                }
            } 
        }
    }

    function setObjectProperty(object, property_type, val) {
        switch(property_type) {
            case "pos_x":
                object.position.x = val;
                break;
            case "pos_y":
                object.position.y = val;
                break;
            case "pos_z":
                object.position.z = val;
                break;
            case "radius":
                object.scale.x = 0.33*val;
                object.scale.y = 0.33*val;
                object.scale.z = 0.33*val;
                break;
            case "position":
                object.position.x = val[0];
                object.position.y = val[1];
                object.position.z = val[2];
                break;
            case "rotation_x":
                object.rotation.x = val;
                break;
            case "rotation_y":
                object.rotation.y = val;
                break;
            case "rotation_z":
                object.rotation.z = val;
                break;
            case "color":
                object.setColor(new THREE.Color(val));
                break;
        } 
    }
}
