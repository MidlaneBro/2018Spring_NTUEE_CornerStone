#include<SoftwareSerial.h>

// TODO: return the direction based on the command you read
char ask_direction(){
  while(1){
    if(BT.available()){
      char c=BT.read();
      return c;
    } 
  }
}

// TODO: send the id back by BT
void send_byte(byte *id, byte idSize){
  for(int i=0;i<idSize;i++){
    BT.write(id[i]);
  }
}
