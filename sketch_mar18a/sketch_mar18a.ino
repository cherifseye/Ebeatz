void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(13, OUTPUT);
}

void loop() {
  // put your main code here, to run repeatedly:
  if (Serial.available()){
    String cmd = Serial.readStringUntil('\n');
    if (cmd == "High"){
      digitalWrite(13, 1);
    }else if (cmd == "Low"){
      digitalWrite(13, 0);
      Serial.println("Doing our best");
    }
    
  }

}
