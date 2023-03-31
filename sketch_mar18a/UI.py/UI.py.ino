int ledPin = 9;    // broche de la DEL
void setup() {
  pinMode(ledPin, OUTPUT); // configure la broche de la DEL en sortie
  Serial.begin(9600);      // initialise la communication série à 9600 bauds
}

void loop() {
  if (Serial.available() > 0) { // si des données sont disponibles sur le port série
    String input = Serial.readStringUntil('\n'); // lit les données jusqu'à ce qu'un caractère de saut de ligne soit reçu
    if (input.startsWith("LUM")) { // si les données commencent par "LUM"
      int brightness = input.substring(3).toInt(); // extrait la valeur de luminosité et la convertit en entier
      analogWrite(ledPin, brightness); // envoie la valeur de luminosité à la broche de la DEL
      Serial.println("Doing my best gang so let's just test what we will get");
    }
  }
}

