#include <Servo.h>
#include <PID_v1.h>
#include <LiquidCrystal.h>

// GPIOs
const int            freqMeas      =  53;
const int            motorPin      =  2;  // TODO change pin
const int            relayPin      =  52;

// LCD
const int btnsPin = A0;
int btnsVal = 0;

// LCD init
LiquidCrystal lcd(8, 9, 4, 5, 6, 7);

int currentPage   = 0;
int consigne      = 100;
int autoAccord    = 0;

//Enums
enum {
  BUTTON_NONE,
  BUTTON_UP,
  BUTTON_DOWN,
  BUTTON_LEFT,
  BUTTON_RIGHT,
  BUTTON_SELECT,
};

// Moteur
Servo                servoMoteur;

// Variables du compteur de fréquence
int                  pulseHigh, pulseLow;
float                pulseTime, pulseTotal, frequency, correctionFactor;
int                  relayState = LOW;

// PID
double        Input, Output, Setpoint;
double        Kp = 0.15;
double        Ki = 4;
double        Kd = 0.025;

// Init PID
PID controleMoteur (&Input, &Output, &Setpoint, Kp, Ki, Kd, P_ON_M, REVERSE);

void setup() {
  
  // init serial com avec un baudrate de 115 200
  Serial.begin(115200);

  // init Moteur  
  pinMode(motorPin, OUTPUT);
  servoMoteur.attach(motorPin);
  
  // position neutre pour avoir 100 Hz.
  servoMoteur.write(127);

  // PID init
  controleMoteur.SetMode(AUTOMATIC);
  controleMoteur.SetSampleTime(500); // taux de refresh du moteur à 200 ms.

  // LCD welcom message
  lcd.begin(16, 2);
  lcd.print(F("Electro Beatz  !"));
  delay(2000);

  // GPIO configs
  pinMode(freqMeas, INPUT);
  pinMode(relayPin, OUTPUT);

  //mode de la corde
  digitalWrite(relayPin, HIGH); 
  
}

void loop() {
  
  // LCD update
  btnListener(getBtnPressed());
  displayPage();

  // frequency measure update
  pulseHigh  = pulseIn(freqMeas, HIGH);
  pulseLow   = pulseIn(freqMeas, LOW);
  pulseTotal = pulseHigh + pulseLow; // Time period of the pulse in microseconds
  frequency  = 1000000/pulseTotal; // Frequency in Hertz (Hz)
  Serial.print("Frequency: ");
  Serial.println(int(frequency));   // DEBUG
  
  // delay avant le PID
  delay(150);

  // PID update si le mode auto accord est activé
  Setpoint = consigne;
  if (Serial.available()){
    String cmd = Serial.readStringUntil('\n');
    if (if cmd.startsWith("FRE")){
      Serial.println(freqency);
    }else if (cmd.startsWith("CON")){
      consigne = cmd.substring(3).toInt();
    }else if (cmd.startsWith("MOD")){
      if (cmd.substring(3).toInt() == 2){
       modeChange();
    }

  }
  pidUpdate();
}

void modeChange(void){
  // écrire ici ce qui se passe quand on change de mode
  if (relayState == LOW){
    relayState = HIGH;
    digitalWrite(relayPin, LOW);
    consigne = 200;    
    }
  else{
    relayState = LOW;
    digitalWrite(relayPin, HIGH);
    consigne = 100;
    }
}

void pidUpdate(void){
  if (autoAccord == 1){
    Input = int(frequency);
    controleMoteur.Compute()
    ;
    servoMoteur.write(Output);
  }
}

void btnListener(byte btnStatus) { /* function btnListener */
  //// Get button value when pressed
  switch (btnStatus) {
    case BUTTON_UP:
      if (currentPage == 2){
        consigneUp();
      }
      break;

    case BUTTON_DOWN:
      if (currentPage == 2){
        consigneDown();        
      }
      break;

    case BUTTON_LEFT:
      pageDown();
      break;

    case BUTTON_RIGHT:
      pageUp();
      break;

    case BUTTON_SELECT:
      if (currentPage == 0) {
        modeChange();
      }

      else if (currentPage == 2){
        if (autoAccord == 0) {
          autoAccord = 1;
        } 
        else {  
          autoAccord = 0;                  
        }        
      }
      break;

    default:  //case BUTTON_NONE:
      //lcd.print(F("       "));
      break;
  }
  // delay(150);
}

void pageDown(void) {
  if (currentPage == 0) {
    currentPage = 2;
  } else {
    currentPage -= 1;
  }
}

void pageUp(void) {
  if (currentPage == 2) {
    currentPage = 0;
  } else {
    currentPage += 1;
  }
}

void consigneUp(void) {
  
  if (relayState == 0){
    if (consigne == 120) {
      consigne = 90;
    }
    else {
    consigne += 1;
    }
  }
  else if (relayState == 1){
      if (consigne == 235) {
      consigne = 185;
    }
    else {
    consigne += 1;
    }
  }  
}

void consigneDown(void) {
  if (relayState == 0){
    if (consigne == 90) {
    consigne = 120;
    } 
    else {
    consigne -= 1;
    }
  }
  else if (relayState == 1){
    if (consigne == 235) {
      consigne = 185;
    }
    else {
      consigne -= 1;
    }
  }
}

void displayPage(void) {
  
  lcd.clear();  
  if (currentPage == 0) {
    lcd.setCursor(0, 0);
    lcd.print(F("Harmonique : "));
    lcd.setCursor(0, 1);
    if (relayState == 0) {
      lcd.print(F("Premiere"));
    } 
    else if (relayState == 1) {
      lcd.print(F("Deuxieme"));
    }
  }
  else if (currentPage == 1){
    lcd.setCursor(0, 0);
    lcd.print(F("Frequence : "));
    lcd.setCursor(0, 1);
    lcd.print(frequency);
    lcd.print("  Hz");
  }

  else if (currentPage == 2){
    lcd.setCursor(0, 0);
    lcd.print(F("Consigne: "));
    lcd.print(consigne);
    lcd.print(" Hz");    
    lcd.setCursor(0, 1);

    if (autoAccord == 0){
      lcd.print(F("Appuyez sur SEL!"));
    }
    
    else if(autoAccord == 1){
      lcd.print(F("Auto-accord ON !"));
    }
    
    lcd.print("Appuyez sur SEL!");
  }
}

byte getBtnPressed() {
  //// Get button value when pressed
  btnsVal = analogRead(btnsPin);
  if (btnsVal < 50)
    return BUTTON_RIGHT;
  else if (btnsVal < 250)
    return BUTTON_UP;
  else if (btnsVal < 350)
    return BUTTON_DOWN;
  else if (btnsVal < 450)
    return BUTTON_LEFT;
  else if (btnsVal < 650)
    return BUTTON_SELECT;
  else
    return BUTTON_NONE;
}
