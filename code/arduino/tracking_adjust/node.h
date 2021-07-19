// dir = 0 : read RFID & stop forever 
// dir = 1 : go straight
// dir = 2 : turn right
// dir = 3 : trun left
// dir = 4 : read RFID & go back
// dir = 5 : stop a while

// TODO: determine the behavior of each port when occuring a node(here represented as an integer)

void node(char );
void MotorWriting(double ,double) ;
void MotorInverter(int , bool& );

void node(char dir){
  if(dir=='0'){
    MotorWriting(0,0);
    byte idSize=0;
    byte* id;
    while(idSize==0){
      id=rfid(&idSize);
    }
    send_byte(id,idSize);
    while(1){
      
    }
  }
  if (dir=='1'){  // go straight
    if(!_reversing){
       MotorWriting(179.2, 128);
    }
    else{
      MotorWriting(-128, -128);
    }
    delay(500);
    while(digitalRead(L2)+digitalRead(L1)+digitalRead(M)+digitalRead(R1)+digitalRead(R2)>=3){
      delay(1);
    }
  }
  else if (dir=='2'){ // turn right
    if (_reversing){
      int a[5];
      MotorWriting(179.2,128);
      delay(80);
      MotorWriting(0,0);
      delay(250);
      MotorWriting(-64,64);
      delay(650);
      a[1]=digitalRead(L1);
      a[2]=digitalRead(M);
      a[3]=digitalRead(R1);
      while(a[1]==0||a[2]==0||a[3]==0){
        a[1]=digitalRead(L1);
        a[2]=digitalRead(M);
        a[3]=digitalRead(R1);
        if((a[1]==1&&a[2]==1)||(a[2]==1&&a[3]==1)){
          break;
        }
        delay(1);
      }
    }
    else {
      MotorWriting(179.2,128);
      delay(120);
      MotorWriting(0,0);
      delay(250);
      int a[5]={digitalRead(L2),digitalRead(L1),digitalRead(M),digitalRead(R1),digitalRead(R2)};
      /*
      MotorWriting(64,-64);
      if(a[1]+a[2]+a[3]==0){//T or L
        while(a[1]==0||a[2]==0){
          a[1]=digitalRead(L1);
          a[2]=digitalRead(M);
          delay(1);
        }
      }
      else{//十字路口
        delay(650);
        while(a[1]==0){
          a[1]=digitalRead(L1);
          delay(1);
        }
      }
      */
      
      MotorWriting(64,-64);
      delay(650);
      a[1]=digitalRead(L1);
      a[2]=digitalRead(M);
      a[3]=digitalRead(R1);
      while(a[1]==0||a[2]==0||a[3]==0){
        a[1]=digitalRead(L1);
        a[2]=digitalRead(M);
        a[3]=digitalRead(R1);
        if((a[1]==1&&a[2]==1)||(a[2]==1&&a[3]==1)){
          break;
        }
        delay(1);
      }
      MotorWriting(0,0);
      delay(250);
      
    }
    MotorWriting(0,0);
    delay(250);
    _reversing=false;
    MotorWriting(179.2, 128);
    delay (400);
  }
  else if(dir=='3'){  // trun left
    if (_reversing==true){  
      int a[5];
      MotorWriting(179.2,128);
      delay(80);
      MotorWriting(0,0);
      delay(250);
      MotorWriting(64,-64);
      delay(650);
      a[1]=digitalRead(L1);
      a[2]=digitalRead(M);
      a[3]=digitalRead(R1);
      while(a[1]==0||a[2]==0||a[3]==0){
        a[1]=digitalRead(L1);
        a[2]=digitalRead(M);
        a[3]=digitalRead(R1);
        if((a[1]==1&&a[2]==1)||(a[2]==1&&a[3]==1)){
          break;
        }
        delay(1);
      }
    }
    else {
      MotorWriting(179.2,128);
      delay(135);
      MotorWriting(0,0);
      delay(250);
      int a[5]={digitalRead(L2),digitalRead(L1),digitalRead(M),digitalRead(R1),digitalRead(R2)};
      /*
      MotorWriting(-64,64);
      if(a[1]+a[2]+a[3]==0){//T or L
        while(a[3]==0||a[2]==0){
          a[3]=digitalRead(R1);
          a[2]=digitalRead(M);
          delay(1);
        }
      }
      else{//十字路口
        delay(700);
        while(a[3]==0){
          a[3]=digitalRead(R1);
          delay(1);
        }
      }
      */
      
      MotorWriting(-64,64);
      delay(650);
      a[1]=digitalRead(L1);
      a[2]=digitalRead(M);
      a[3]=digitalRead(R1);
      while(a[1]==0||a[2]==0||a[3]==0){
        a[1]=digitalRead(L1);
        a[2]=digitalRead(M);
        a[3]=digitalRead(R1);
        if((a[1]==1&&a[2]==1)||(a[2]==1&&a[3]==1)){
          break;
        }
        delay(1);
      }
      
    }
    MotorWriting(0,0);
    delay (250);
    _reversing=false;
    MotorWriting(179.2,128);
    delay (400);
  }
  else if (dir=='4'){  // read RFID & go back
    byte idSize=0;
    byte* id;
    if(_reversing==true){
       MotorWriting(-128,-128);
       delay(150);
    }
    while(idSize==0){
      id=rfid(&idSize);
    }
    send_byte(id,idSize);
    if (_reversing==true){
      _reversing=false;
      MotorWriting(128*1.4,128);
      delay(500);
    }
    else{
      _reversing=true;
      MotorWriting(-128, -128);
      delay(300);
    }
  }
  else if(dir=='5'){
    MotorWriting(0,0);
    delay(1000);
  }
}

void MotorWriting(double vR, double vL) {
   if(vR<0){
      if(R_dir){
          MotorInverter(MotorR_PWMR, R_dir);
      }   
      analogWrite(MotorR_PWMR,-vR);
   }
   else if(vR>=0){
      if(!R_dir){
          MotorInverter(MotorR_PWMR, R_dir);      
      }
      analogWrite(MotorR_PWMR,vR);
   }

   if(vL<0){
      if(L_dir){
          MotorInverter(MotorL_PWML, L_dir);
      }
      analogWrite(MotorL_PWML,-vL);
   }
   else if (vL>=0){
      if(!L_dir){
          MotorInverter(MotorL_PWML, L_dir);
      }
      analogWrite(MotorL_PWML,vL);
   } 
}

void MotorInverter(int motor, bool& dir) {
   if(motor == MotorR_PWMR){
      if(dir){
        digitalWrite(MotorR_I1, LOW);
        digitalWrite(MotorR_I2, HIGH);
        dir=false;
      }
      else{
        digitalWrite(MotorR_I1, HIGH);
        digitalWrite(MotorR_I2, LOW);
        dir=true;
      }
  }
  if(motor == MotorL_PWML){
    if(dir){
        digitalWrite(MotorL_I3, LOW);
        digitalWrite(MotorL_I4, HIGH);
        dir=false;
      }
    else{
        digitalWrite(MotorL_I3, HIGH);
        digitalWrite(MotorL_I4, LOW);
        dir=true;
    }
  }
}

