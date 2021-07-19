#include <SoftwareSerial.h>
#include <SPI.h>
#include <MFRC522.h>
#include <Wire.h> 
#define DEBUG

// App Controller State
// L298N 馬達驅動板
// 宣告 MotorR 為右邊
// 宣告 MotorL 為左邊
#define MotorR_I1     5  //定義 I1 接腳
#define MotorR_I2     4  //定義 I2 接腳
#define MotorL_I3     6 //定義 I3 接腳
#define MotorL_I4     1 //定義 I4 接腳
#define MotorR_PWMR    3  //定義 ENA (PWM調速) 接腳
#define MotorL_PWML    9  //
#define TxPin 8         // RxD of HC-05

// 循線模組/定義 ENB (PWM調速) 接腳
#define RST_PIN      2        // RFID resetpin
#define SS_PIN       10        // RFID selection pin
#define RxPin 7          // TxD of HC
#define R2  A0  // Define Second Right Sensor Pin
#define R1  A1  // Define First Right Sensor Pin
#define M   A2  // Define Middle Sensor Pin
#define L1  A3  // Define First Left Sensor Pin
#define L2  A4  // Define Second Leftt Sensor Pin

MFRC522 mfrc522(SS_PIN, RST_PIN);  // MFRC522 object declaration
SoftwareSerial BT (RxPin, TxPin);

bool R_dir = true;                  // if dir == ture, mean right-motor is forwarding. On the other hand, backwarding.
bool L_dir = true;                  // if dir == ture, mean Left-motor is forwarding. On the other hand, backwarding.
double _w2=16;                         // Weight Value for the Outer Sensor
double _w1=_w2/2;                         // Weight Value for the Inner Sensor
double _Tp=128;                         // Velocity of Car
double _Kp=24;                         // _Kp Parameter
double _Kd=6.4;                         // _Kd Parameter
double _Ki=0.0004;                         // _Ki Parameter
double _Kalpha=0.72;                         // _Kalpha
int i=0;
double _sumError=0;
double _dError=0;
double _lastError=0;                  // Error in Last Stage
double _dV=0;
double _lastV=0;
bool _reversing = false;

void setup()
{
    //Serial.begin(9600);
    BT.begin(9600); //bluetooth initialization
    
    SPI.begin();         //RFID initialization
    mfrc522.PCD_Init();

     pinMode(MotorR_I1,   OUTPUT);
     pinMode(MotorR_I2,   OUTPUT);
     pinMode(MotorL_I3,   OUTPUT);
     pinMode(MotorL_I4,   OUTPUT);
     pinMode(MotorR_PWMR, OUTPUT);
     pinMode(MotorL_PWML, OUTPUT);
     pinMode(R1, INPUT); 
     pinMode(R2, INPUT);
     pinMode(M,  INPUT);
     pinMode(L1, INPUT);
     pinMode(L2, INPUT);
     digitalWrite(MotorR_I1, HIGH);
     digitalWrite(MotorR_I2, LOW);
     digitalWrite(MotorL_I3, HIGH);
     digitalWrite(MotorL_I4, LOW);
}

#include "track.h"

void loop()
{
    track();
}

