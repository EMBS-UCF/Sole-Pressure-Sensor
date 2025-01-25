void setup() {
  Serial.begin(9600);
  for (int i = A0; i <= A2; i++) {
    pinMode(i, OUTPUT);
  }
  for (int i = A3; i <= A7; i++) {
    pinMode(i, INPUT);
  }
}

void loop() {
  String data = "";
  
  for (int row = A0; row <= A2; row++) {
    digitalWrite(row, HIGH);
    delay(10);  // Allow the current to stabilize
    
    for (int col = A3; col <= A7; col++) {
      float value = analogRead(col);
      float mapped = value / 4092 * 5;
      data += String(mapped);
      if (col < A7) {
        data += ",";
      }
    }
    digitalWrite(row, LOW);
    if (row < A2) {
      data += ";";
    }
  }

  Serial.println(data);
  delay(100);  // Slight delay before the next reading
}
