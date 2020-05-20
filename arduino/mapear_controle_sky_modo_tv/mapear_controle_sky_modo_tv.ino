#include <IRremote.h>

const char key_0[]  PROGMEM = "TV VIDEO";
const char key_2[]  PROGMEM = "ON";  
const char key_3[]  PROGMEM = "OFF";
const char key_8[]  PROGMEM = "SETA CIMA";  
const char key_9[]  PROGMEM = "SETA ESQ";  
const char key_11[]  PROGMEM = "SETA DIR";  
const char key_12[]  PROGMEM = "SETA BAIX";
const char key_14[]  PROGMEM = "MENU";
const char key_20[]  PROGMEM = "VOL +";
const char key_21[]  PROGMEM = "VOL -";  
const char key_22[]  PROGMEM = "(MUTE)";  
const char key_23[]  PROGMEM = "RET CH";  
const char key_24[]  PROGMEM = "CH +";  
const char key_25[]  PROGMEM = "CH -";  
const char key_26[]  PROGMEM = "1"; 
const char key_27[]  PROGMEM = "2";  
const char key_28[]  PROGMEM = "3";  
const char key_29[]  PROGMEM = "4";  
const char key_30[]  PROGMEM = "5";
const char key_31[]  PROGMEM = "6";  
const char key_32[]  PROGMEM = "7"; 
const char key_33[]  PROGMEM = "8";  
const char key_34[]  PROGMEM = "9";   
const char key_36[]  PROGMEM = "0";  

const char *const key_table[]  PROGMEM = {
  key_36, key_34, key_33, key_32, key_31, key_30, key_29, key_28, key_27, 
  key_26, key_25, key_24, key_23, key_22, key_21, key_20, key_14, key_12, key_11, key_9,  key_8, key_3,  key_2,  key_0
};

/* Variáveis */
int cont = 23;

String res = "";
String last = "";
boolean nextKey = true;

int RECV_PIN = 7;
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup() {
  Serial.begin(9600);
  Serial.println("Enabling IRin");

  irrecv.enableIRIn(); // Start the receiver

  Serial.println("Enabled IRin");
}


char buffer[15];
char v = 0;

void loop() {
  if (nextKey) {
    strcpy_P(buffer, (char *) pgm_read_word(&(key_table[cont--])));  // Necessary casts and dereferencing, just copy.
    Serial.print(buffer);

    for(v = 0; v < (15 - String(buffer).length()); v++)
      Serial.print(" ");
    
    delay(500);
    nextKey = false;
  }


  if (irrecv.decode(&results)) {
    res = String(results.value, HEX);
    res.toUpperCase();

    if (!res.equals("E3DC5833") && !res.equals("FFFFFFFF") && !res.equals(last)) {
      last = res;
      nextKey = true;

      Serial.println(" " + res);
    }

    irrecv.resume(); // Receive the next value
  }

  delay(100);
}
