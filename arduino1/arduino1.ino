int i;
int intervalo = 5000;
int inputPin[] = {4,5,9,10,11,12};
int ID[] = {1,-1,2,-2,3,-3};
unsigned long temporizado[sizeof(inputPin)];

void setup() {
  Serial.begin(9600);
  for (i=0; i<(sizeof(inputPin)/sizeof(int)); i++){
      pinMode(inputPin[i], INPUT);
  }
}

void loop(){
  for (i=0; i<(sizeof(inputPin)/sizeof(int)); i++){
    int digital_input = digitalRead(inputPin[i]);
    unsigned long tiempo_actual = millis();
    if (digital_input == HIGH && tiempo_actual-temporizado[i]>=intervalo){
      Serial.println(ID[i]);
      temporizado[i] = millis();
    }
    if (tiempo_actual-temporizado[i]<0){
      temporizado[i] = 0;
    }
  }
}
