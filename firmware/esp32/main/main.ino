#include <WiFi.h>
#include <WebServer.h>

const char* ssid = "ctk";
const char* password = "Wi1df1ower";
#define RELAY_ON  HIGH
#define RELAY_OFF LOW

WebServer server(80);

// Use valid GPIOs
const int relayPins[4] = {A0, A2, A4, A6};

// LOW = ON (relay is active low)
void setRelay(int zone, bool on) {
  if (zone < 1 || zone > 4) return;
  digitalWrite(relayPins[zone - 1], on ? RELAY_OFF : RELAY_ON);
}

bool getRelayState(int zone) {
  if (zone < 1 || zone > 4) return false;
  return digitalRead(relayPins[zone - 1]) == RELAY_OFF;
}

// ----------- HTTP handlers -----------

void handleZone() {
  String uri = server.uri();  // /zone/1/on

  int zone = uri.substring(6, 7).toInt();
  bool turnOn = uri.endsWith("/on");

  setRelay(zone, turnOn);

  server.send(200, "text/plain",
    "Zone " + String(zone) + (turnOn ? " ON" : " OFF"));
}

void handleStatus() {
  String json = "{";
  for (int i = 1; i <= 4; i++) {
    json += "\"zone" + String(i) + "\":";
    json += getRelayState(i) ? "true" : "false";
    if (i < 4) json += ",";
  }
  json += "}";

  server.send(200, "application/json", json);
}

void handleRoot() {
  server.send(200, "text/plain",
    "ESP32 Irrigation Controller\n"
    "/zone/{1-4}/on\n"
    "/zone/{1-4}/off\n"
    "/status\n");
}

// ----------- setup -----------

void setup() {
  // #define RELAY_ON  HIGH
  // #define RELAY_OFF LOW
  Serial.begin(115200);

  const int* relays = relayPins;
  for (int i = 0; i < 4; i++) {
    pinMode(relays[i], OUTPUT);
    digitalWrite(relays[i], RELAY_OFF);  // OFF for HIGH-trigger relay
  }

  delay(1000);  // give USB time to come up
  Serial.println("BOOTED");

  // 🔒 HARDENED INIT: prevent relay chatter
  for (int i = 0; i < 4; i++) {
    pinMode(relayPins[i], INPUT_PULLUP); // ensure HIGH via pull-up
  }

  delay(50); // let lines settle

  for (int i = 0; i < 4; i++) {
    pinMode(relayPins[i], OUTPUT);
    digitalWrite(relayPins[i], RELAY_ON); // OFF
  }

  Serial.println("BOOTING...");

  // WiFi
  WiFi.begin(ssid, password);
  Serial.print("Connecting");

  int attempts = 0;
  while (WiFi.status() != WL_CONNECTED && attempts < 40) {
    delay(500);
    Serial.print(".");
    attempts++;
  }

  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nConnected!");
    Serial.print("IP: ");
    Serial.println(WiFi.localIP());
    Serial.print("MAC:");
    Serial.println(WiFi.macAddress());
  } else {
    Serial.println("\nWiFi FAILED");
  }

  // Routes
  server.on("/", handleRoot);

  server.on("/zone/1/on", handleZone);
  server.on("/zone/1/off", handleZone);
  server.on("/zone/2/on", handleZone);
  server.on("/zone/2/off", handleZone);
  server.on("/zone/3/on", handleZone);
  server.on("/zone/3/off", handleZone);
  server.on("/zone/4/on", handleZone);
  server.on("/zone/4/off", handleZone);

  server.on("/status", handleStatus);

  server.begin();
  Serial.println("Server started");
}

// ----------- loop -----------

void loop() {
  server.handleClient();
}
