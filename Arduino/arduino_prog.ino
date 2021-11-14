// #include <WiFi.h>
// #include <HTTPClient.h>

// const char* ssid = "LRKSPR";
// const char* password = "honeybear";

// const int sensePin = 34;
// const int ledPinGreen = 12;
// const int ledPinRed = 13;
// const int ledPinRequest = 2;

// const int threshold = 600; // ≈200 = lights OFF | ≈1000 lights ON
// const int mask = 2000; // Retrigger mask

// bool lastState = false; //Default ligths OFF
// bool currentState;


// void blinkRequest(int t, int s) {
//   for (int i = 0; i <= t - 1; i++) {
//     digitalWrite(ledPinRequest, HIGH);
//     delay(s);
//     digitalWrite(ledPinRequest, LOW);
//     delay(s);
//   }
// }


// void setup() {
//   pinMode(ledPinGreen, OUTPUT);
//   pinMode(ledPinRed, OUTPUT);
//   pinMode(ledPinRequest, OUTPUT);
//   digitalWrite(ledPinGreen, HIGH);
//   digitalWrite(ledPinRed, LOW);
  
//   Serial.begin(9600);

//   WiFi.begin(ssid, password);

//   while (WiFi.status() != WL_CONNECTED) {
//     Serial.println("Connecting to WiFi...");
//     blinkRequest(5, 200);
//   }

//   Serial.println("ESP32 successfully connected to the WiFi network");
//   blinkRequest(2, 100);
// }


// void loop() {
//   int ldrVal = analogRead(sensePin);

//   if (ldrVal > threshold) { 
//     currentState = true; //Lights are ON
//   }
//   else if (ldrVal < threshold) { 
//     currentState = false; //Lights are OFF
//   }

//   //Serial.println(ldrVal);
  
//   if (currentState != lastState) {
//     if (currentState == true) {
//       digitalWrite(ledPinGreen, LOW);
//       digitalWrite(ledPinRed, HIGH);
//       Serial.println("Lights was turned ON");
//       if (WiFi.status() != WL_CONNECTED) {
//         Serial.println("WiFi problem!");
//         blinkRequest(20, 100);
//       }
//       else {
//         HTTPClient http;
//         http.begin("http://gladibad.pythonanywhere.com/changestate/True/");
//         int httpCode = http.GET();
//         //Serial.println(httpCode);
//         if (httpCode == 200) {
//           Serial.println("DB succesfully updated");
//           blinkRequest(2, 100); 
//         }
//         http.end();
//       }
//     }
//     else {
//       digitalWrite(ledPinGreen, HIGH);
//       digitalWrite(ledPinRed, LOW);
//       Serial.println("Lights was turned OFF");
//       if (WiFi.status() != WL_CONNECTED) {
//         Serial.println("WiFi problem!");
//         blinkRequest(20, 100);
//       }
//       else {
//         HTTPClient http;
//         http.begin("http://gladibad.pythonanywhere.com/changestate/False/");
//         int httpCode = http.GET();
//         //Serial.println(httpCode);
//         if (httpCode == 200) {
//           Serial.println("DB succesfully updated");
//           blinkRequest(2, 100);
//         }
//         http.end();
//       }
//     }
//     lastState = currentState;
//     delay(mask);
//   }
// }


#include <WiFi.h>
#include <HTTPClient.h>

const char* ssid = "";      // Wifi name
const char* password = "";

const int sensePin = 34;
const int ledPinGreen = 12;
const int ledPinRed = 13;
const int ledPinRequest = 2;

const int threshold = 600; // ≈200 = lights OFF | ≈1000 lights ON
const int mask = 2000; // Retrigger mask

bool lastState; //Default ligths OFF
bool currentState;


void blinkRequest(int t, int s) {
  for (int i = 0; i <= t - 1; i++) {
    digitalWrite(ledPinRequest, HIGH);
    delay(s);
    digitalWrite(ledPinRequest, LOW);
    delay(s);
  }
}


void connectToWiFi() {
  WiFi.begin(ssid, password);

  while (WiFi.status() != WL_CONNECTED) {
    Serial.println("Connecting to WiFi...");
    blinkRequest(5, 200);
  }

  Serial.println("ESP32 successfully connected to the WiFi network");
  blinkRequest(2, 100);
}

void updateDB() {
  int ldrVal = analogRead(sensePin);

  if (ldrVal > threshold) { 
    digitalWrite(ledPinGreen, LOW);
    digitalWrite(ledPinRed, HIGH);
    lastState = true;
      
    HTTPClient http;
    http.begin("http://gladibad.pythonanywhere.com/changestate/True/");
    int httpCode = http.GET();
    Serial.println("Http Response Code: " + String(httpCode));
    if (httpCode == 200) {
      Serial.println("DB succesfully updated\n");
      blinkRequest(2, 100); 
    }
    http.end();
  }
  
  else if (ldrVal < threshold) { 
    digitalWrite(ledPinGreen, HIGH);
    digitalWrite(ledPinRed, LOW);
    lastState = false;
    
    HTTPClient http;
    http.begin("http://gladibad.pythonanywhere.com/changestate/False/");
    int httpCode = http.GET();
    Serial.println("Http Response Code: " + String(httpCode));
    if (httpCode == 200) {
      Serial.println("DB succesfully updated\n");
      blinkRequest(2, 100);
    }
    http.end();
  }
}

void setup() {
  pinMode(ledPinGreen, OUTPUT);
  pinMode(ledPinRed, OUTPUT);
  pinMode(ledPinRequest, OUTPUT);
  digitalWrite(ledPinGreen, HIGH);
  digitalWrite(ledPinRed, LOW);
  
  Serial.begin(9600);

  connectToWiFi();

  updateDB();
}


void loop() {
  int ldrVal = analogRead(sensePin);

  if (ldrVal > threshold) { 
    currentState = true; //Lights are ON
  }
  else if (ldrVal < threshold) { 
    currentState = false; //Lights are OFF
  }

  //Serial.println(ldrVal);
  
  if (currentState != lastState) {
    if (currentState == true) {
      digitalWrite(ledPinGreen, LOW);
      digitalWrite(ledPinRed, HIGH);
      Serial.println("Lights was turned ON");
      if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi problem!");
        blinkRequest(10, 100);
        connectToWiFi();
        updateDB();
      }
      else {
        HTTPClient http;
        http.begin("http://gladibad.pythonanywhere.com/changestate/True/");
        int httpCode = http.GET();
        Serial.println("Http Response Code: " + String(httpCode));
        if (httpCode == 200) {
          Serial.println("DB succesfully updated\n");
          blinkRequest(2, 100); 
          http.end();
        }
        else {
          http.end();
          updateDB();
        }
      }
    }
    else {
      digitalWrite(ledPinGreen, HIGH);
      digitalWrite(ledPinRed, LOW);
      Serial.println("Lights was turned OFF");
      if (WiFi.status() != WL_CONNECTED) {
        Serial.println("WiFi problem!");
        blinkRequest(10, 100);
        connectToWiFi();
        updateDB();
      }
      else {
        HTTPClient http;
        http.begin("http://gladibad.pythonanywhere.com/changestate/False/");
        int httpCode = http.GET();
        Serial.println("Http Response Code: " + String(httpCode));
        if (httpCode == 200) {
          Serial.println("DB succesfully updated\n");
          blinkRequest(2, 100);
          http.end();
        }
        else {
          http.end();
          updateDB();
        }
      }
    }
    lastState = currentState;
    delay(mask);
  }
}