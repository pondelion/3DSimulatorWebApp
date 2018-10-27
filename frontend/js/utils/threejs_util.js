
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