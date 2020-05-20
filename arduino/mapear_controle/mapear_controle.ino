#include <IRremote.h>

// Nome das teclas para gerar uma fácil visualização (max. 15 caracteres -- alterar buffer caso queira maior)
const char key_0[]  PROGMEM = "TV VIDEO";
const char key_1[]  PROGMEM = "TELA TV";
const char key_2[]  PROGMEM = "ON";  
const char key_3[]  PROGMEM = "OFF";
const char key_4[]  PROGMEM = "GUIA";  
const char key_5[]  PROGMEM = "(QUADRADO)";  
const char key_6[]  PROGMEM = "LISTA";  
const char key_7[]  PROGMEM = "SAIR";
const char key_8[]  PROGMEM = "SETA CIMA";  
const char key_9[]  PROGMEM = "SETA ESQ";  
const char key_10[]  PROGMEM = "CONFIRMA";  
const char key_11[]  PROGMEM = "SETA DIR";  
const char key_12[]  PROGMEM = "SETA BAIX";  
const char key_13[]  PROGMEM = "(RETORNO)";
const char key_14[]  PROGMEM = "MENU";  
const char key_15[]  PROGMEM = "?INFO";  
const char key_16[]  PROGMEM = "(VERMELHO)";  
const char key_17[]  PROGMEM = "(VERDE)";  
const char key_18[]  PROGMEM = "(AMARELO)";  
const char key_19[]  PROGMEM = "(AZUL)";  
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
const char key_35[]  PROGMEM = "DASH";  
const char key_36[]  PROGMEM = "0";  
const char key_37[]  PROGMEM = "i";

// Mapa das teclas gravada na flash (necessário para não saturar a memória do Arduino)
const char *const key_table[]  PROGMEM = {
  key_37, key_36, key_35, key_34, key_33, key_32, key_31, key_30, key_29, key_28, key_27, 
  key_26, key_25, key_24, key_23, key_22, key_21, key_20, key_19, key_18, key_17, 
  key_16, key_15, key_14, key_13, key_12, key_11, key_10, key_9,  key_8,  key_7,  
  key_6,  key_5,  key_4,  key_3,  key_2,  key_1,  key_0
};

// Tamanho da tabela (Quantidade de teclas para testar)
int cont = 37;

/* Variáveis */
char buffer[15]; // buffer para leitura dos nomes (limitado à 15 caracteres)
char v = 0;
String res = "";
String last = "";
boolean nextKey = true;

/* Configurações da biblioteca */
int RECV_PIN = 7;       // Pino de leitura do sensor
IRrecv irrecv(RECV_PIN);
decode_results results;

void setup() {
  Serial.begin(9600);
  Serial.println("Habilitando a leitura...");

  irrecv.enableIRIn(); // Start the receiver

  Serial.println("Leitura habilitada!");
}

void loop() {
  if (nextKey) {
    // Carrega o nome da tecla no serial
    strcpy_P(buffer, (char *) pgm_read_word(&(key_table[cont--])));
    Serial.print(buffer);

    // Completar com espaços o restante da palavra
    for(v = 0; v < (15 - String(buffer).length()); v++)
      Serial.print(" ");

    nextKey = false;
  }


  if (irrecv.decode(&results)) {
    res = String(results.value, HEX);
    res.toUpperCase();

    // E3DC5833 é o código de fim de linha para o controle testado.
    // FFFFFFFF é o código para quando uma tecla fica pressionada
    if (!res.equals("E3DC5833") && !res.equals("FFFFFFFF") && !res.equals(last)) {
      last = res;         // Evita que leia a mesma tecla várias vezes (caso tenha uma tecla repetida, não irá lê)
      nextKey = true;     // Desbloqueiar a leitura da próxima tecla
      
      Serial.println(" " + res); // exibe o código hex. da tecla
    }

    irrecv.resume(); // Receive the next value
  }

  delay(100);
}
