#include <Servo.h>
Servo myservo; // 建立Servo物件，控制伺服馬達
Servo myservo2;
int trigPin = 11;      // trig pin of HC-SR04
int echoPin = 10;     // Echo pin of HC-SR04
int control_trig = 6; //伺服馬達

int revleft = 4;       //REVerse motion of Left motor
int fwdleft = 7;       //ForWarD motion of Left motor
int revright = 8;      //REVerse motion of Right motor(white black (4,7))
int fwdright = 12;      //ForWarD motion of Right motor(purple gray(8,12))
int scratch= 9;        //scratch (5 orange)

int ena = 3; //右輪
int enb = 5; //左輪
long duration, distance;

int motor_speed_left=120; 
int motor_speed_right=88;



int pyorder = -1;
int bottle = 0;
int bottle_direction = 0; // 1:左；-1:右
int motor_delay = 100 ;


int detectOn;
int count=0;

void setup() {
  myservo.attach(scratch);  
  myservo2.attach(control_trig);
  Serial.begin(115200);
  pinMode(revleft, OUTPUT);      // set Motor pins as output
  pinMode(fwdleft, OUTPUT);
  pinMode(revright, OUTPUT);
  pinMode(fwdright, OUTPUT);
  pinMode(ena, OUTPUT);
  pinMode(enb, OUTPUT);
  pinMode(trigPin, OUTPUT);         // set trig pin as output
  pinMode(echoPin, INPUT);          //set echo pin as input to capture reflected waves
  myservo2.write(90);
  myservo.write(115);
  detectOn = 0;
}


class Move{
  public: void stoprun(){
      analogWrite(ena, motor_speed_right);
      analogWrite(enb, motor_speed_left);
      digitalWrite(fwdright, LOW);  //Stop
      digitalWrite(revright, LOW);
      digitalWrite(fwdleft, LOW);
      digitalWrite(revleft, LOW);
    };
  public: void backward(){
      analogWrite(ena, motor_speed_right);
      analogWrite(enb, motor_speed_left);
      digitalWrite(fwdright, LOW);     
      digitalWrite(revright, HIGH);
      digitalWrite(fwdleft, LOW);
      digitalWrite(revleft, HIGH);
    };
  public: void forward(){
      analogWrite(ena, motor_speed_right);
      analogWrite(enb, motor_speed_left-10);
      digitalWrite(fwdright, HIGH);                 
      digitalWrite(revright, LOW);
      digitalWrite(fwdleft, HIGH);
      digitalWrite(revleft, LOW);
  };
  public: void left(){
      analogWrite(ena, motor_speed_right);
      analogWrite(enb, motor_speed_left);
      digitalWrite(fwdright, LOW);                
      digitalWrite(revright, LOW);
      digitalWrite(fwdleft, HIGH);
      digitalWrite(revleft, LOW);
  };
  public: void right(){
      analogWrite(ena, motor_speed_right);
      analogWrite(enb, motor_speed_left+8);
      digitalWrite(fwdright, HIGH);                  
      digitalWrite(revright, LOW);
      digitalWrite(fwdleft, LOW);
      digitalWrite(revleft, LOW);
  };
  public: void forright(){
      analogWrite(ena, motor_speed_right-30);
      analogWrite(enb, motor_speed_left+10);
      digitalWrite(fwdright, HIGH);                    
      digitalWrite(revright, LOW);
      digitalWrite(fwdleft, HIGH);
      digitalWrite(revleft, LOW);
  };
  public: void forleft(){
      analogWrite(ena, motor_speed_right+10);
      analogWrite(enb, motor_speed_left-10);
      digitalWrite(fwdright, HIGH);               
      digitalWrite(revright, LOW);
      digitalWrite(fwdleft, HIGH);
      digitalWrite(revleft, LOW);
  };
  public: void bacright(){
      analogWrite(ena, motor_speed_right-30);
      analogWrite(enb, motor_speed_left+10);
      digitalWrite(fwdright, LOW);               
      digitalWrite(revright, HIGH);
      digitalWrite(fwdleft, LOW);
      digitalWrite(revleft, HIGH);
  };
  public: void bacleft(){
      analogWrite(ena, motor_speed_right+10);
      analogWrite(enb, motor_speed_left-10);
      digitalWrite(fwdright, LOW);            
      digitalWrite(revright, HIGH);
      digitalWrite(fwdleft, LOW);
      digitalWrite(revleft, HIGH);
  };
};
int measure_distance(){
  digitalWrite(trigPin, LOW);
  delayMicroseconds(2);
  digitalWrite(trigPin, HIGH);     // send waves for 10 us
  delayMicroseconds(10);
    
  duration = pulseIn(echoPin, HIGH); // receive reflected waves
  distance = duration / 58.2;   // convert to distance
  return distance;
}

void obstacle_detect(){
  int distance = measure_distance();
  
  ////Serial.println(distance);
  // If you dont get proper movements of your robot then alter the pin numbers
  if (distance>10)
  {
    bottle = 0;
  }else{
    bottle = 1;
  }
}

void scratch_close(){
  for(int i=115;i>=-45;i--){
    myservo.write(i);
    delay(20);
  }
}
void scratch_open(){
  for(int i=-45;i<=115;i++){
    myservo.write(115);
    delay(20);
  } 
}

void key_pressed_control(){
Move move;
  if (Serial.available()) {
      while(Serial.available()){
        pyorder = Serial.read();
        if (pyorder == 117 ){ //u
          detectOn=1;
          Serial.println("detectOn"); 
            
        }
        if (pyorder == 106 ){ //j
          detectOn=0; 
          Serial.println("detectoff");
            
        }
      }
      //pyorder = Serial.read();
      
      if (bottle == 0){
        
        if (pyorder == 115 ){
          move.backward();
          delay(motor_delay);
          //Serial.println("backward");   
        }
        else if (pyorder == 119) {
          move.forward();
          delay(motor_delay);
          //Serial.println("forward");
        } 
        
        else if (pyorder == 97){
          move.left();
          delay(motor_delay);
          //Serial.println("turnLeft");
        }
        else if (pyorder == 100){
          move.right();
          delay(motor_delay);
          //Serial.println("turnRight");
        }
        else if(pyorder==114){
          scratch_close();
          delay(motor_delay);
          //Serial.println("scratch_close");
          //detectOn=1;
        }
        else if(pyorder==102){
          scratch_open();
          delay(motor_delay);
          //Serial.println("scratch_open");
        }
        else if(pyorder==101){
          move.forright();
          delay(motor_delay);
          //Serial.println("forRight");
        }
        else if(pyorder==113){
          move.forleft();
          delay(motor_delay);
          //Serial.println("forLeft");
        }
        else if(pyorder==99){
          move.bacright();
          delay(motor_delay);
          //Serial.println("bacRight");
        }
        else if(pyorder==122){
          move.bacleft();
          delay(motor_delay);
          //Serial.println("bacLeft");
        }
        else{
          move.stoprun();
        }      
      }else{
          while(bottle == 1){
            move.backward();
            delay(motor_delay*10);
            //Serial.println("bottle");
            
            myservo2.write(125);
            delay(100);
            int left_distance = measure_distance();
            myservo2.write(55);
            delay(100);
            int right_distance = measure_distance();
            
            if (left_distance>right_distance){
              bottle_direction = 1;
              move.left();
              delay(motor_delay*4);
              myservo2.write(90);
              obstacle_detect();
            }else{
              bottle_direction = -1;
              move.right();
              delay(motor_delay*4);
              myservo2.write(90);
              obstacle_detect();
            }
          }
//          move.forward();
//          delay(motor_delay*15);
//          if (count>=2){
//            detectOn=0;
//          }
          
//          if(bottle_direction==1){
//            move.right();
//            delay(motor_delay*5);
//          }else{
//            
//            move.left();
//            delay(motor_delay*5);
//          }
          count += 1;
          
      }
      
  }  
  move.stoprun();
}

void loop() {
  
  if(detectOn){
    obstacle_detect();
  }
  key_pressed_control();
  bottle = 0;
}
