
function createSphere(pos_x, pos_y, pos_z, radius, color=0x22DD22) {
    var sphereRadius = radius;
    var sphereGeometry = new THREE.SphereGeometry(sphereRadius, 20, 20);
    var sphereMaterial = new THREE.MeshLambertMaterial({color: color});
    var sphere = new THREE.Mesh(sphereGeometry, sphereMaterial);

    sphere.position.x = pos_x;
    sphere.position.y = pos_y;
    sphere.position.z = pos_z;
    sphere.castShadow = true;

    return sphere;
}

function createBox(pos_x=0, pos_y=0, pos_z=0, size_x=5, size_y=5, size_z=5, opacity=1.0, color=0xff0000) {
    box = new THREE.Mesh(
        new THREE.BoxGeometry(size_x, size_y, size_z),
        new THREE.MeshLambertMaterial({color: color, opacity: opacity, transparent: true, side: THREE.DoubleSide, depthWrite: false})
    );
    box.position.set(pos_x, pos_y, pos_z);
    return box;
}

function createPlane(pos_x=0, pos_y=0, pos_z=0, rotation_x=-0.5*Math.PI, 
                        rotation_y=0, rotation_z=0, color=0xff0000, size_h=50, size_w=50) {
    var planeGeometry = new THREE.PlaneGeometry(size_w, size_h, 1, 1);
    var planeMaterial = new THREE.MeshLambertMaterial({color: color});
    var plane = new THREE.Mesh(planeGeometry, planeMaterial);
    plane.receiveShadow = true;

    plane.rotation.x = rotation_x;
    plane.rotation.y = rotation_y;
    plane.rotation.z = rotation_z;
    plane.position.x = pos_x;
    plane.position.y = pos_y;
    plane.position.z = pos_z;

    return plane;
}

function createArrow(name, dir_x=0, dir_y=1, dir_z=0, pos_x=0, pos_y=0, pos_z=0, rotation_x=-Math.PI, 
                        rotation_y=0, rotation_z=0, length=5, color=0x00ff00, headWidth=2, headLength=1) {
    var dir = new THREE.Vector3(dir_x, dir_y, dir_z);
    var pos = new THREE.Vector3(pos_x, pos_y, pos_z);
    var arrowHelper = new THREE.ArrowHelper(dir, pos, length, color, 
                                            headWidth=headWidth, headLength=headLength);
    arrowHelper.name = name;
    arrowHelper.rotation.x = rotation_x;
    arrowHelper.rotation.y = rotation_y;
    arrowHelper.rotation.z = rotation_z;
    
    return arrowHelper;
}

function createSprite(pos_x=0, pos_y=0, pos_z=0, scale=0.2) {
    // var material = new THREE.SpriteMaterial({
    //     map: new THREE.TextureLoader().load("img/sprite.png")
    // });
    var material = new THREE.SpriteMaterial({color: 0x0000ee});
    var sprite = new THREE.Sprite(material);
    sprite.scale.x = scale;
    sprite.scale.y = scale;
    sprite.scale.z = scale;
    return sprite;
}
