/**
section:CMPUT 274 A2
Project Title: Snake Game Arduino
Team members: Irene(Zihan) Gao and Gaoping Zhou
referencce:https:Arduino library--
(//www.arduino.cc/en/Tutorial/JoystickMouseControl)
(https://www.arduino.cc/en/Reference/TFTLibrary)
*/

#include <Arduino.h>
#include <Adafruit_GFX.h>    // Core graphics library
#include <Adafruit_ST7735.h> // Hardware-specific library
#include <SPI.h>
#include <SD.h>
#include "lcd_image.h"       // copy corresponding files from the Parrot folder

// ==========standard U of A library settings, assuming Atmel Mega SPI pins=====
#define SD_CS    5  // Chip select line for SD card
#define TFT_CS   6  // Chip select line for TFT display
#define TFT_DC   7  // Data/command line for TFT
#define TFT_RST  8  // Reset line for TFT (or connect to +5V)

// define tft display (use Adafruit library)
Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);

// ===================Joystick definations=======================================
#define VERT  0   // Analog input A0 - vertical
#define HORIZ 1   // Analog input A1 - horizontal
#define SEL 9  // Digital input pin 9 - select

//=====================LEDs definations==========================================
#define LED_1 2
#define LED_2 3
#define LED_3 4

//=====================pushbutton definations====================================
#define PUSH 10 // reset the game button

//==================== Variables=================================================
const int16_t screen_height = 160;//screen height
const int16_t screen_width = 128;//screen width
//int mapgrid[800];
int select;//joystick button input
int push;// push button input
int game_speed1 = 10;
int game_speed2 = 20;

// socres are representing the pirces of food tha snake eats in each mode
int score1;
int score2;
int score3;
//====================snake variables=============================================
int initial_snakelength = 15;
int snake_body_widith = 6;
int snake_max_length = 500;
int snakelength = initial_snakelength;
int delta_vert;
int delta_horiz;
int vertical;
int horizontal;

int old_snake_x;// old joystick position
int old_snake_y;

int snake_x;// joystck position
int snake_y;

int init_vertical;// initial joystick
int init_horizontal;
//====================food variables==============================================
int foodX;
int foodY;
int food_size = 3;

//===================set up joystick button=======================================
void selection_init() {
    // setup the botton at joystick
    pinMode(SEL,INPUT);
    digitalWrite(SEL,HIGH);
}
//==================set up LEDs===================================================
void led_init(){
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(LED_3, OUTPUT);
}
//=================set up pushbuttons=============================================
void push_button_init(){
  // initialize the pushbutton pin as an input:
 pinMode(PUSH,INPUT);
 digitalWrite(PUSH, HIGH);
}
//=================forward declarations===========================================
// state the functions in order to have problems like
//   " xxx is not declared at this scope."
void start_game_page();
void game_over();
void restart();
void update_Food();
void update_snake();
void snake_move();
void eat_food1();
void eat_food2();
void eat_food_final();
void eat_tail();
void touch_the_wall();
void mode0();
void mode1();
void mode2();
void playthegame();

//==================start the game display========================================
void start_game_page(){
  tft.fillScreen(ST7735_BLACK);//make the background black

  tft.setTextSize(3);
  tft.setTextColor(ST7735_WHITE);
  tft.setCursor(20,10);
  tft.print("Snake");

  tft.setTextSize(1);
  tft.setCursor(50,25);
  tft.println("");
  tft.println("   Created by ");
  tft.println("Irene Gao");
  tft.println("and");
  tft.println("Gaoping Zhou.");

  tft.setTextColor(ST7735_YELLOW);
  tft.setCursor(100,100);
  tft.println(" ");
  tft.println(" Press joystick to start.");
}

//================game over page==================================================
void game_over(){
  tft.fillScreen(ST7735_BLACK);//make the background black

  tft.setTextSize(3);
  tft.setTextColor(ST7735_WHITE);
  tft.setCursor(20,10);
  tft.print("Game Over");

  tft.setTextSize(4);
  tft.setTextColor(ST7735_YELLOW);
  tft.setCursor(50,10);
  tft.print("your score is: ");
  tft.println(score1 + score2 +score3);

  tft.setTextSize(3);
  tft.setTextColor(ST7735_WHITE);
  tft.setCursor(80,10);
  tft.print("press the restartbutton to restart ");


 // pinMode(PUSH,INPUT);  //new

  while(true){
    push = digitalRead(PUSH);
    if (push == 0){
      // if the restart button is pressed, go to restart the game
      restart();
      playthegame();
      Serial.print("game restart");
    }
   }
  }

//================reset the game==================================================
void restart(){
  // initialize the food pisition
  foodX = 50;
  foodY = 50;

  // // initialize the snake position
  snake_x = 20;
  snake_y = 20;

  // initialize the score
  score1 = 0;
  score2 = 0;
  score3 = 0;

}

//===============update food=====================================================
void update_Food() {
  // the food appers in the screen radomly
	food_size =3;
  foodX = random(10,125);
  foodY = random(10,150);
  tft.fillCircle(foodX, foodY,food_size, ST7735_YELLOW);
}
//===============update snake=====================================================
void update_snake(){
   snake_body_widith = 6;
   tft.fillRect(snake_x,snake_y,snake_body_widith,snakelength, ST7735_GREEN);
   Serial.print("snake_x value is: ");
   Serial.println(snake_x);
   Serial.print("snake_y value is: ");
   Serial.println(snake_y);
   Serial.print("snakelength value is: ");
   Serial.println(snakelength);


 }
// TODO:move the snake and make the new cursor replace the old cursor
//==============update snake's movement===========================================
void snake_move(){

snake_body_widith;
select;
snake_x, snake_y;
old_snake_x,old_snake_y;
vertical,horizontal;
init_vertical,init_horizontal;
delta_vert,delta_horiz;

vertical = analogRead(VERT);
horizontal = analogRead(HORIZ);

delta_vert = vertical - init_vertical;     // vertical change
delta_horiz = horizontal - init_horizontal; // horizontal change

// store old position of the tank
old_snake_x = snake_x;
old_snake_y = snake_y;

snake_x = snake_x - delta_horiz / 200;     // left and right movement of cursor
snake_y = snake_y - delta_vert / 200;     // change of initialVelocity
touch_the_wall();                       //new
if ( snake_x != old_snake_x || snake_y != old_snake_y){
  update_snake(); // redraw the snake
}

}



// TODO: how to write the this function correctly??
//===============snake eat the food===============================================
void eat_food1(){

  while(score1 < 5){
    update_snake();
    snake_move();
  if (snake_x == foodX && snake_y == foodY){
    snakelength += 3;

    update_Food();
    update_snake();
    snake_move();
    score1 ++;
    }
  }
  delay(800);// speed

}
 void eat_food2(){
   for (int score2 = 0; score2 < 5; score2 ++){
   if (snake_x == foodX && snake_y == foodY){
     snakelength += 7;

     update_Food();
     update_snake();
     snake_move();
     score2 ++;
    }
   }
   delay(500);// speed
  }

void eat_food_final(){
	int snake_max_length;
  for (int score3 = 0 ; score3 < snake_max_length; score3 ++){
  if (snake_x == foodX && snake_y == foodY){
    snakelength += 3;

    update_Food();
    update_snake();
    snake_move();
    score3 ++;
    }
  }
  delay(100);// speed
}

//===============snake eats its tail=================================================
void eat_tail(){
if (snake_x == snake_x && snake_y == snake_y){
  game_over();
  }
}

//==============snake touch the wall================================================
void touch_the_wall(){
  if ((snake_x < 0) || (snake_x > screen_width)){
    game_over();
  }
if ((snake_y < 0) || (snake_y > screen_height)){
  game_over();
  }
}
//===============mode0===============================================================
void mode0(){
  pinMode(LED_1,INPUT);
  digitalWrite(LED_1, HIGH);
  delay(200);
  pinMode(LED_2,INPUT);
  digitalWrite(LED_2, LOW);
  pinMode(LED_3,INPUT);
  digitalWrite(LED_3, LOW);
  Serial.println(foodX);
  Serial.println(foodY);

  foodX = 50;
  foodY = 50;
  if (foodX == 50 && foodY == 50){
    update_Food();
    eat_food1();
    eat_tail();
    touch_the_wall();
    Serial.print("foodX is right\n");
	}
  else{
    Serial.print("foodX is wrong\n");

  }
}
//==============mode1===============================================================

void mode1(){
  pinMode(LED_1,INPUT);
  digitalWrite(LED_1, LOW);
  pinMode(LED_2,INPUT);
  digitalWrite(LED_2, HIGH);
  delay(200);
  pinMode(LED_3,INPUT);
  digitalWrite(LED_3, LOW);
  Serial.println(foodX);
  Serial.println(foodY);

  foodX = 70;
  foodY = 70;
  if (foodX == 70 && foodY == 70){
    update_Food();
    eat_food2();
    eat_tail();
    touch_the_wall();
    Serial.print("everything is ok!\n");
  }
  else{
    Serial.print("some thing is wring\n");
  }
}
//===============mode2===============================================================
  void mode2(){
  pinMode(LED_1,INPUT);
  digitalWrite(LED_1, LOW);
  pinMode(LED_2,INPUT);
  digitalWrite(LED_2, LOW);
  pinMode(LED_3,INPUT);
  digitalWrite(LED_3, HIGH);
  delay(200);
  Serial.println(foodX);
  Serial.println(foodY);
  foodX = 50;
  foodY = 20;
  if (foodX == 50 && foodY == 20){
    update_Food();
    eat_food_final();
    eat_tail();
    touch_the_wall();
    Serial.print("ok hhh\n");
  }
  else{
    Serial.print("not okay\n");
  }
}

// TODO: how to write this function correctly? how to connect the functions together
// how to organize the funcitons?
//===============playthegame==========================================================
void playthegame(){
  //init();
  //show the main background of the game site
  tft.fillScreen(ST7735_BLACK);
  // fisrt mode
  if (score1 == 0){
    mode0();
    Serial.print("it's time for mode0");
    if(score1 == 4){
      mode1();
      Serial.print("it's time for mode1");
      if (score2 == 4){
        mode2();
        Serial.print("it's time for mode2");
      }
    }
  }
}
//==============main===================================================================
int main(){

  init();
    // Attach USB for applicable processors
    #ifdef USBCON
        USBDevice.attach();
    #endif
    tft.initR(INITR_BLACKTAB);
    // customize initilization
    // serial start
    Serial.begin(9600);

    selection_init();
    led_init();
    //push_button_init();
    // initialize the food position
    foodX = 50;
    foodY = 50;

    // // initialize the snake position
    snake_x = 20;
    snake_y = 20;

    score1 = 0;
    score2 = 0;
    score3 = 0;

    snakelength = initial_snakelength;

    while(true){
      start_game_page();
      select = digitalRead(SEL);
      Serial.print("strat game is running ");
      // if the joystick button is pressed
      if (select == 0){
        playthegame();
        Serial.print("game is playing");
      }
      start_game_page();
      Serial.print("there is a loop");
  }
  // end the Project
  Serial.end();
  return 0;
}
