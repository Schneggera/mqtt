/*
 * MQTT-WebClient example for Web-IO 4.0
 */
var hostname = "test.mosquitto.org";
var clientId = "mqttJs";
var port = 8081;
clientId += new Date().getUTCMilliseconds();
var subscription = "/$_fluzzy$$cadabra/Nö/Heizung";
var subscription1 = "/$_fluzzy$$cadabra/Nö/WeMos";

mqttClient = new Paho.MQTT.Client(hostname, port, clientId);
mqttClient.onMessageArrived = MessageArrived;
mqttClient.onConnectionLost = ConnectionLost;
Connect();

function Connect() {
  mqttClient.connect({
    onSuccess: Connected,
    onFailure: ConnectionFailed,
    useSSL: true,
  });
}

function Connected() {
  console.log("Connected");
  mqttClient.subscribe(subscription1);
}

function ConnectionFailed(res) {
  console.log("Connect failed:" + res.errorMessage);
}

function ConnectionLost(res) {
  if (res.errorCode !== 0) {
    console.log("Connection lost:" + res.errorMessage);
    Connect();
  }
}

/*Callback for incoming message processing */
function MessageArrived(message) {
  console.log(message.destinationName + " : " + message.payloadString);
  let payloadArray = message.payloadString.split(';');
  let temp = payloadArray[0];
  let heater = payloadArray[1];
  document.getElementById('status').innerHTML = 
  `Status: Current temperature is ${temp} and heater is ${heater}`;
}

function Send() {
  let low = parseInt(document.getElementById("low").value);
  let high = parseInt(document.getElementById("high").value);

  if (low > high) {
    alert("Low higher then High!");
  } else {
    var message = new Paho.MQTT.Message(
      PadZero(low, 2) + ";" + PadZero(high, 2)
    );
    message.destinationName = "/$_fluzzy$$cadabra/Nö/Heizung";
    mqttClient.send(message);
  }
}

function DragEnd() {
  let low = document.getElementById("low").value;
  let high = document.getElementById("high").value;

  document.getElementById("lblLow").innerText = "Low: " + low;
  document.getElementById("lblHigh").innerText = "High: " + high;
}

function PadZero(n, size) {
  let s = n + "";
  while (s.length < size) s = "0" + s;
  return s;
}
