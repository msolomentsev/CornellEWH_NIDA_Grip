void setup() {
  // put your setup code here, to run once:
  int Vout1 = A1;
  int Vout2 = A2;
  int Vout3 = A3;
  float Vin = 1024; // 3.3V in units of V, assumed to the same for all of the FSRs
  float R1 = 5.1e3; // in units of Ohms, same for all FSRs
  int FSR_1 = 0;
  int FSR_2 = 0;
  int FSR_3 = 0;
  float a = 9622;
  float b = -1.357;
  int force1 = 0;
  int force2 = 0;
  int force3 = 0;
}

void loop() {
  // put your main code here, to run repeatedly:
  // For FSR 1
  FSR_1 = (R1*Vout1/Vin)/(1-Vout1/Vin);
  force1 = a*FSR_1^b;
  // For FSR 2 
  FSR_2 = (R1*Vout2/Vin)/(1-Vout2/Vin);
  force2 = a*FSR_2^b;
  // For FSR 3
  FSR_3 = (R1*Vout3/Vin)/(1-Vout3/Vin);
  force3 = a*FSR_3^b;
}