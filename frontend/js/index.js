var request = new XMLHttpRequest();
request.open("get", "http://127.0.0.1:5000/get_param_names?simulator=bouncing_ball");

request.onreadystatechange = function() {
  console.log("Ready state: " + this.readyState);
  if (this.readyState == 4) {
    console.log(this.status);
    console.log(this.responseText);
  }
};
request.send();

console.log("Request senda.");