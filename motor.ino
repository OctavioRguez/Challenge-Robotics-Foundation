//Import Basic Libraries
#include <ros.h>
#include <std_msgs/Float32.h>

//Declare ROS node
ros::NodeHandle nh;

//Declare variables and GPIO
const int PinM1 = 2;
const int PinM2 = 4;

const int PinA1 = 15;
const int PinB1 = 18;
const int PinA2 = 14;
const int PinB2 = 13;

const int Channel = 0;
const int freq = 980;
const int resolution = 8;

float pwm = 0.0;
bool reverse = false;
int counter = 0;

//Callback function for the subscription
void callback(const std_msgs::Float32& msg){
  pwm = msg.data * 100;
  if (pwm < 0){
    reverse = true;
    pwm *= (-1);
  }
  else{
    reverse = false;
  }
}

//Publisher & Subscribers
ros::Subscriber<std_msgs::Float32> sub("cmd_pwm", &callback);

void setup()
{
  Serial.begin(115200);

  pinMode(PinA1, OUTPUT); 
  pinMode(PinB1, OUTPUT);
  pinMode(PinA2, OUTPUT); 
  pinMode(PinB2, OUTPUT);

  //Initialize the pwm
  ledcSetup(Channel, freq, resolution);
  ledcAttachPin(PinM1, Channel);
  ledcAttachPin(PinM2, Channel);

  //Manage ROS node
  nh.initNode();
  nh.subscribe(sub);

}

void loop()
{
  //Call functions
  pwm_duty_cycle();
  directions();
  
  nh.spinOnce();
  delay(10);
}

void pwm_duty_cycle()
{
  //Map the received pwm
  pwm = 0.15*100;
  int dutyCycle = map(pwm, 0.0, 100.0, 0, 255);
  ledcWrite(Channel, dutyCycle);
}

void directions()
{
  //Control the direction for the encoders
  if (reverse){
    //cw
    digitalWrite(PinA1, LOW);
    digitalWrite(PinB1, HIGH);

    //ccw
    digitalWrite(PinA2, HIGH);
    digitalWrite(PinB2, LOW);
  }
  else{
    //ccw
    digitalWrite(PinA1, HIGH);
    digitalWrite(PinB1, LOW);
    
    //cw
    digitalWrite(PinA2, LOW);
    digitalWrite(PinB2, HIGH);
  }
}
