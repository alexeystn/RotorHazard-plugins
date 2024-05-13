#include <Arduino.h>
#include <FastLED.h>
#include <EEPROM.h>
#include <RTClib.h>

#define LED_STRIP_PIN     A3
#define SERIAL_BAUD_RATE  115200
#define COLOR_ORDER       "GRB" 
#define DEF_BRIGHTNESS    2  
#define DEF_COLOR         CRGB::Red
#define NUM_LEDS          8*40
#define ROW_REVERSE       1   // TODO
#define RX_BUF_SIZE       20
#define NUM_COLORS        8
#define NUM_LEVELS        6

#define KEY_PIN_1         8
#define KEY_PIN_2         9
#define KEY_PIN_3         10
#define BUILTIN_LED_PIN   13

#define EEPROM_ADDRESS    0

uint8_t digits[6];

uint8_t rxBuf[RX_BUF_SIZE];
uint8_t rxBufPnt = 0;

uint8_t digitPositions[] = {0, 6, 14, 20, 28, 34};
CRGB colors[NUM_COLORS] = {CRGB::Red, CRGB::Orange, CRGB::Yellow, CRGB::Green, 
                           CRGB::Cyan, CRGB::Blue, CRGB::Purple, CRGB::White};
uint8_t brightnessLevels[NUM_LEVELS] = {1, 2, 4, 8, 16, 32};

uint8_t configLevel = 0;
uint8_t configColor = 0;
uint8_t configRotated = 0;

uint32_t lastKeyPressedMs[3];
uint32_t keyState[3];
uint8_t keyPin[3] = {KEY_PIN_1, KEY_PIN_2, KEY_PIN_3};

uint8_t configNotSaved = 0;
uint32_t configLastChangeMs = 0;

RTC_DS3231 rtc;

DateTime now, before;

uint8_t font[10][5] = {
  {0x7E, 0x81, 0x81, 0x81, 0x7E}, 
  {0x00, 0x41, 0xFF, 0x01, 0x00}, 
  {0x41, 0x83, 0x85, 0x89, 0x71}, 
  {0x42, 0x81, 0x91, 0x91, 0x6E}, 
  {0x0C, 0x14, 0x24, 0x44, 0xFF}, 
  {0xF2, 0x91, 0x91, 0x91, 0x8E}, 
  {0x3E, 0x51, 0x91, 0x91, 0x0E}, 
  {0x80, 0x83, 0x8C, 0xB0, 0xC0}, 
  {0x6E, 0x91, 0x91, 0x91, 0x6E}, 
  {0x70, 0x89, 0x89, 0x8A, 0x7C},
};

CRGB crgbLedsArr[NUM_LEDS];


void configLoad(void) {
  uint8_t b = 0;
  b = EEPROM.read(EEPROM_ADDRESS);
  configColor = (b & 0xF0) >> 4;
  configLevel = (b & 0x0F) >> 1;
  configRotated = (b & 0x01);
  if (configColor >= NUM_COLORS) {
    configColor = 0;
  }
  if (configLevel >= NUM_LEVELS) {
    configLevel = 0;
  }  
}


void configSave(void) {
  uint8_t b = 0;
  b = (configColor << 4) + (configLevel << 1) + configRotated;
  EEPROM.write(EEPROM_ADDRESS, b);
}


void setup() {
  configLoad();
  Serial.begin(SERIAL_BAUD_RATE);
  while (!Serial) {};

  if (!rtc.begin()) {
    Serial.println("Couldn't find RTC");
    while (1);
  } else {
    Serial.println("RTC found");
  }

  if (rtc.lostPower()) {
    Serial.println("RTC lost power, let's set the time!");
    rtc.adjust(DateTime(2024, 1, 1, 0, 0, 0));
  }

  
  FastLED.addLeds<WS2811, LED_STRIP_PIN, GRB>(crgbLedsArr, NUM_LEDS);
  FastLED.setBrightness(brightnessLevels[configLevel]);
  FastLED.showColor(CRGB::Black);
  for (uint8_t i = 0; i < 3; i++) {
    pinMode(keyPin[i], INPUT);
    digitalWrite(keyPin[i], HIGH);
    keyState[i] = 1;
  }
  pinMode(BUILTIN_LED_PIN, OUTPUT);
}


void putDigit(uint8_t digit, uint8_t pos) {
  uint16_t n;
  for (int x = 0; x < 5; x++) {
    uint8_t b = font[digit][x];
    for (int y = 0; y < 8; y++) {
      uint8_t xx = pos + x;
      if (b & 0x01) {
        if (( !configRotated && (xx % 2 == 1)) || ( configRotated && (xx % 2 == 0)))  {
          n = xx*8 + y;
        } else {
          n = xx*8 + 7 - y;
        }
        if (!configRotated) {
          crgbLedsArr[n] = colors[configColor];
        } else {
          crgbLedsArr[NUM_LEDS - 1 - n] = colors[configColor];
        }
      }
      b /= 2; 
    }
  }
}


void updateClock(void) {
  for (uint16_t i = 0; i < NUM_LEDS; i++) {
    crgbLedsArr[i] = CRGB::Black;
  }
  for (uint8_t i = 0; i < 6; i++) {
    if (digits[i] != 0) {
      putDigit(digits[i]-'0', digitPositions[i]);
    }
  }
  FastLED.show();
}


void updateRtc(void) {
  uint8_t h, m, s;
  uint8_t d[6];
  
  for (uint8_t i = 0; i < 6; i++) {
    d[i] = digits[i]-'0';
  }
  h = d[0] * 10 + d[1];
  m = d[2] * 10 + d[3];
  s = d[4] * 10 + d[5];
  char txt[10];
  rtc.adjust(DateTime(2024, 1, 1, h, m, s));
  sprintf(txt, "%02d:%02d:%02d", h, m, s);
  Serial.print("Time is set to ");
  Serial.println(txt);
}


void displayRtc(void) {

  for (uint16_t i = 0; i < NUM_LEDS; i++) {
    crgbLedsArr[i] = CRGB::Black;
  }
  
  putDigit(now.hour()/10, digitPositions[0]);
  putDigit(now.hour()%10, digitPositions[1]);
  putDigit(now.minute()/10, digitPositions[2]);
  putDigit(now.minute()%10, digitPositions[3]);
  putDigit(now.second()/10, digitPositions[4]);
  putDigit(now.second()%10, digitPositions[5]);
  FastLED.show();
  
}


void processRxBuf() {
  for (uint8_t i = 0; i < 6; i++) {
    digits[i] = 0;
    if (i == rxBufPnt) {
      break;
    }
    if ((rxBuf[i] >= '0') && (rxBuf[i] <= '9')) {
      digits[i] = rxBuf[i];
    }
  }
  updateRtc();
  //updateClock();
}


void doKeyAction(uint8_t key) {
  if (key == 0) {
    configColor++;
    if (configColor == NUM_COLORS) {
      configColor = 0;
    }    
  }
  if (key == 1) {
    configLevel++;
    if (configLevel == NUM_LEVELS) {
      configLevel = 0;
    }
    FastLED.setBrightness(brightnessLevels[configLevel]);    
  }
  if (key == 2) {
    configRotated ^= 1;
  }
  configNotSaved = 1;
  configLastChangeMs = millis();
  //updateClock();
  displayRtc();
}


void processKeys() {  
  for (uint8_t i = 0; i < 3; i++) {
    uint8_t state = digitalRead(keyPin[i]);
    if ((state == 0) && (keyState[i] == 1)) {
      if (millis() - lastKeyPressedMs[i] > 200) {
        doKeyAction(i);
        lastKeyPressedMs[i] = millis();
      }
    }
    keyState[i] = state;
  }
}


void processEeprom(void) {
  if (configNotSaved) {
    if (millis() > (configLastChangeMs + 2000)) {
      configSave();
      for (uint8_t i = 0; i < 3; i++) {
        digitalWrite(BUILTIN_LED_PIN, 1);
        delay(100);
        digitalWrite(BUILTIN_LED_PIN, 0);
        delay(100); 
      }
      configNotSaved = 0;
    } 
  }
}


void loop() {
   
  if (Serial.available() > 0) {
    uint8_t c = Serial.read();
    if (rxBufPnt < RX_BUF_SIZE) {
      rxBuf[rxBufPnt] = c;
      rxBufPnt++;
    }
    if (c == '\n') {
      processRxBuf();
      rxBufPnt = 0;
    }
  }

  now = rtc.now();
  if (now != before) {
    displayRtc();
  }

  before = now;

  
  processKeys();
  processEeprom();
  delay(10);
}
