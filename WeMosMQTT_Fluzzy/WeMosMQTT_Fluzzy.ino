
/******
   https://www.baldengineer.com/mqtt-tutorial.html
   WeMosMQTTSubPub_Projekt5.ino

   it works 1911031140

*/

#include <EEPROM.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <Wire.h>

const char* ssid = "AP-MN";
const char* password = "Martin#123";
//const char* mqtt_server = "mqtt.eclipse.org";     // :-)
const char* mqtt_server = "test.mosquitto.org";     // :-)
//const char* mqtt_server = "172.20.10.5";          // :-)
const char* topic0 = "/$_fluzzy$$cadabra/Nö/Heizung/";
const char* topic1 = "/$_fluzzy$$cadabra/Nö/Temperature/";
String clientId = "WeMos_";
char* clientID_c_str = "1234567890123456789012345678";

char msg[50];
int value = 0;
long lastMsg = 0;
long lastLoop = 0;
long lastReconnect = 0;

// Connect to the WiFi
WiFiClient espClient;
PubSubClient client(espClient);

const byte ledPin = 14; // Pin with LED on Adafruit Huzzah

void setup() {
  Serial.begin(115200);
  setup_wifi();
  client.setServer(mqtt_server, 1883);
  client.setCallback(callback);
  pinMode(ledPin, OUTPUT);
  pinMode(BUILTIN_LED, OUTPUT);     // Initialize the BUILTIN_LED pin as an output
  composeClientID() ;
}

void setup_wifi() {
  delay(10);

  // We start by connecting to a WiFi network
  Serial.println();
  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("");
  Serial.println("WiFi connected");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message arrived [");
  Serial.print(topic);
  Serial.print("] ");
  for (int i = 0; i < length; i++) {
    Serial.print((char)payload[i]);
  }
  Serial.println();

  // Switch on the LED if an 1 was received as first character
  if ((char)payload[0] == '1') {
    digitalWrite(BUILTIN_LED, LOW);   // Turn the LED on (Note that LOW is the voltage level
    // but actually the LED is on; this is because
    // it is acive low on the ESP-01)
  } else if ((char)payload[0] == '0') {
    digitalWrite(BUILTIN_LED, HIGH);  // Turn the LED off by making the voltage HIGH
  }
}
void reconnect() {
  // Loop until we're reconnected
  while (!client.connected()) {
    Serial.print("Attempting MQTT connection...");
    // Attempt to connect
    if (client.connect(clientID_c_str)) {
      Serial.print("connected as ");
      //Serial.println(clientId);
      Serial.println(clientID_c_str);
      // Once connected, publish an announcement...
      client.publish(topic1, "hello world");
      // ... and resubscribe
      client.subscribe(topic0);
    } else {
      Serial.print("failed, rc=");
      Serial.print(client.state());
      Serial.println(" try again in 5 seconds");
      // Wait 5 seconds before retrying
      delay(5000);
    }
  }
}

void loop() {

  long now = millis();
  if (now - lastLoop > 1000) {
    lastLoop = now;
    client.loop();
  }

  if (now - lastReconnect > 333) {
    lastReconnect = now;
    if (!client.connected()) {
      reconnect();
    }
  }


//  if (now - lastMsg > 5000) {
//    lastMsg = now;
//    ++value;
//    snprintf (msg, 75, "WeMos Meldung #%ld", value); // http://www.cplusplus.com/reference/cstdio/snprintf/
//    Serial.print("Publish message: ");
//    Serial.println(msg);
//    client.publish(topic1, msg);
//  }
}

void composeClientID() {
  uint8_t mac[6];
  WiFi.macAddress(mac);
  clientId += macToStr(mac);
  strcpy(clientID_c_str, clientId.c_str());
}

String macToStr(const uint8_t* mac) {
  String result;
  for (int i = 0; i < 6; ++i) {
    result += String(mac[i], 16);
    if (i < 5)
      result += ':';
  }
  return result;
}
