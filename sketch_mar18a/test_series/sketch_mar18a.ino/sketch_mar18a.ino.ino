int frequence = 255;
int consigne;
#define pin 9
#define relayMode
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(pin, 11);
  analogWrite(pin, frequence);

}

void loop() {
    if (Serial.available() > 0) { // si des données sont disponibles sur le port série
    String input = Serial.readStringUntil('\n'); // lit les données jusqu'à ce qu'un caractère de saut de ligne soit reçu
    /*if (input.startsWith("LUM")) { // si les données commencent par "LUM"
      int brightness = input.substring(3).toInt(); // extrait la valeur de luminosité et la convertit en entier
      analogWrite(ledPin, brightness); // envoie la valeur de luminosité à la broche de la DEL
      
    }*/
    if (input.startsWith("FRE")){
      Serial.println(frequence);
    }else if(input.startsWith("CON")){
      frequence = input.substring(3).toInt();
      analogWrite(pin, frequence);
    }
  }
}
