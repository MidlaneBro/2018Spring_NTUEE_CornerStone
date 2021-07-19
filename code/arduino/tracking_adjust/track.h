#include <SoftwareSerial.h>
#include "RFID.h"
#include "bluetooth.h"
#include "node.h"

void track(){
  char dir[100];
  for(int j=0;j<100;j++){
    dir[j]=ask_direction();
    if(dir[j]=='0'){
      break;
    }
  }
  int n=0;
  while(1){
    int l2,l1,m,r1,r2;
    if(_reversing){
      l2 = digitalRead(L2);
      l1 = digitalRead(L1);
      m = digitalRead(M);
      r1 = digitalRead(R1);
      r2 = digitalRead(R2);
    }
    else{
      l2 = digitalRead(R2);
      l1 = digitalRead(R1);
      m = digitalRead(M);
      r1 = digitalRead(L1);
      r2 = digitalRead(L2);
    }
    
    if(l2+l1+m+r1+r2==1||l2+l1+m+r1+r2==2){
      double error = r2*(_w2)+r1*(_w1)+l1*(-_w1)+l2*(-_w2);                     // Total error from sensor output  
      if ((r2==0 && r1==0) || (r1==0 && m==0) || (m==0 && l1==0) || (l1==0 && l2==0)){
        error=error/2.0;
      }
      _sumError+=error;
      if (i%100==0){
        if (i!=0){
          _dError=error-_lastError;
        }
        _lastError=error;
      }
      double power;
      if (!_reversing){
        power=_dError*(_Kd)+error*(_Kp)+_dV*(_Kalpha)+_sumError*(_Ki);
      }
      else {
        power=_dError*(0.3*_Kd)+error*(0.3*_Kp)+_dV*(0.3*_Kalpha)+_sumError*(0.3*_Ki);
      }
      double vR,vL;
      if (!_reversing){
        vR=_Tp+power/2;                       
        vL=_Tp-power/2; 
      }
      else {
        vR=-_Tp+power/2;                       
        vL=-_Tp-power/2; 
      }
      if (vR>255) vR=255;
      if (vL>255) vL=255;
      if (vR<-255) vR=-255;
      if (vL<-255) vL=-255;
      if (i%100==0){
        if (i!=0){
          _dV=vR-_lastV;
        }
        _lastV=vR;
      }
      if (_reversing==false) MotorWriting (vR*1.4, vL);
      else MotorWriting (vR,vL);
      i++;
      delay(1);
    }

    else if(l2+l1+m+r1+r2==0){
      delay(100);
      if(digitalRead(L2)+digitalRead(L1)+digitalRead(M)+digitalRead(R1)+digitalRead(R2)==0){
        node('5');
      }
    }
    else if(l2+l1+m+r1+r2>=3){
      MotorWriting(0,0);
      node(dir[n]);
      n++;
      _sumError=0;
      _lastError=0;
      _lastV=0;
      i=0;
    }
  }
}
