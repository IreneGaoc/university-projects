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

// ==========standard U of A library settings, assuming Atmel Mega SPI pins==================================
#define SD_CS    5  // Chip select line for SD card
#define TFT_CS   6  // Chip select line for TFT display
#define TFT_DC   7  // Data/command line for TFT
#define TFT_RST  8  // Reset line for TFT (or connect to +5V)

Adafruit_ST7735 tft = Adafruit_ST7735(TFT_CS, TFT_DC, TFT_RST);// define tft display (use Adafruit library)

// ===================Joystick definations===================================================================
#define VERT  0   // Analog input A0 - vertical
#define HORIZ 1   // Analog input A1 - horizontal
#define SEL 9  // Digital input pin 9 - select
//=======================DIRECT=============================================
#define UP 9
#define DOWN 7
#define LEFT 8
#define RIGHT 6

//=====================LEDs definations======================================================================
#define LED_1 2
#define LED_2 3
#define LED_3 4

//=====================pushbutton definations================================================================
#define PUSH 10 // reset the game button

//==================== Variables=============================================================================
const int16_t screen_height = 160;//screen height
const int16_t screen_width = 128;//screen width
int select;//joystick button input
int push;// push button input
int game_speed1 = 10;
int game_speed2 = 20;

// socres are representing the pirces of food tha snake eats in each mode
int score;
//====================snake variables=========================================================================
int initial_snakelength = 35;        //snake initial lenth         2015//28
int snake_body_width = 4;          //snake width                 2015//28
int snake_max_length = 500;        //snake max length              2015//28
int snakelength = initial_snakelength;
int snake_x[300];                 //snake x point
int snake_y[300];                 //snake y ponit
int delta_vert;
int delta_horiz;
int vertical;
int horizontal;
int snake_dir ; //snake head direct

int init_vertical ; // initial joystick
int init_horizontal;
//====================food variables=========================================================================
int foodX;
int foodY;
int food_size = 4;

//===================set up joystick button==================================================================
void selection_init() {
    // setup the botton at joystick
    pinMode(SEL,INPUT);
    digitalWrite(SEL,HIGH);
    pinMode(VERT,INPUT);
    pinMode(HORIZ,INPUT);
}
//==================set up LEDs==============================================================================
void led_init(){
  pinMode(LED_1, OUTPUT);
  pinMode(LED_2, OUTPUT);
  pinMode(LED_3, OUTPUT);
}
//=================set up pushbuttons=========================================================================
void push_button_init(){
// initialize the pushbutton pin as an input:
 pinMode(PUSH,INPUT);
 digitalWrite(PUSH, HIGH);
}
//=================forward declarations=======================================================================
// state the functions in order to have problems like
//   " xxx is not declared at this scope."
void start_game_page();
void game_over1();
void game_over2();
void init_snake_food(); //restart rename init_snake_food()
void update_Food();
void update_snake();
void snake_move();
int eat_food(int);
void eat_tail(int );
void touch_the_wall(int);
void mode0();
void mode1();
void mode2();
void playthegame();
int snake_direct(int,int,int,int);
void move_position(int ) ;
void eat_position(int);
void game_over_page1();
void game_over_page2();

//==================start the game display====================================================================
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

//================game over page================================================================================
void game_over_page1(){
tft.fillScreen(ST7735_BLACK);//make the background black

tft.setTextSize(3);
tft.setTextColor(ST7735_WHITE);
tft.setCursor(20,10);
tft.print("Game  ");
tft.print(" Over");

tft.setTextSize(1);
tft.setTextColor(ST7735_YELLOW);
tft.setCursor(10,60);
tft.print("your score is: ");
tft.println(score);

tft.setTextSize(1);
tft.setTextColor(ST7735_YELLOW);
tft.setCursor(10,90);
tft.print("you touched the wall! ");

tft.setTextSize(1);
tft.setTextColor(ST7735_WHITE);
tft.setCursor(10,140);
tft.print("press the restartbutton to restart ");
}


void game_over_page2(){
  tft.fillScreen(ST7735_BLACK);//make the background black

  tft.setTextSize(3);
  tft.setTextColor(ST7735_WHITE);
  tft.setCursor(20,10);
  tft.print("Game  ");
  tft.print(" Over");

  tft.setTextSize(1);
  tft.setTextColor(ST7735_YELLOW);
  tft.setCursor(10,60);
  tft.print("your score is: ");
  tft.println(score);
  tft.setTextSize(1);
  tft.setTextColor(ST7735_YELLOW);
  tft.setCursor(10,90);
  tft.print("you ate your tail!  ");

  tft.setTextSize(1);
  tft.setTextColor(ST7735_WHITE);
  tft.setCursor(10,140);
  tft.print("press the restartbutton to restart ");
}
//================game over======================================================
void game_over1(){

  push_button_init();

  game_over_page1();

 // pinMode(PUSH,INPUT);  //new

  while(true){
    game_over_page1();
    Serial.print("game_over_page");
    while (true){
      delay(100);
      if(digitalRead(PUSH) == 0){// if the restart button is pressed, go to restart the game
        playthegame();
        Serial.print("game restart");
        }
      }
      game_over_page1();
      Serial.print("there is another loop");
    }
   }
void game_over2(){

   push_button_init();

   game_over_page2();

  // pinMode(PUSH,INPUT);  //new

 while(true){
   game_over_page2();
   Serial.print("game_over_page");
   while (true){
     delay(100);
     if(digitalRead(PUSH) == 0){// if the restart button is pressed, go to restart the game
       playthegame();
       Serial.print("game restart");
      }
     }
    game_over_page2();
    Serial.print("there is another loop");
  }
}


//================reset the game================================================================================
void init_snake_food(){

  // // initialize the snake position
  snake_x[0] = 20;            // snake head init x
  snake_y[0] = 20;            // snake head init y
  for ( int i=1;i<snakelength ; i++)          //snake baody x,y
    {
      snake_x[i]=snake_x[i-1]+1;
      snake_y[i]=snake_y[i-1];
    }
  snake_dir = LEFT ; //initialize LEFT
  // initialize the score
  score = 0;
  //get orginal joystick x and y
  init_vertical = analogRead(VERT);
  init_horizontal = analogRead(HORIZ);


}

//===============update food====================================================================================
void update_Food() {
  int flag =1 ;
  while (flag)                   //food posistion not in snake position
  {
   foodX = random(10,screen_width);
   foodY = random(10,screen_height);
    for (int i = 0; i < snakelength; i++)
    {
        if((foodX==snake_x[i])&&(foodY==snake_y[i]))
        {
          break;
        }
        flag=0;
    }
  }
  Serial.println("FOODX");
  Serial.println(foodX);
   Serial.println("FOODY");
  Serial.println(foodY);
  tft.fillCircle(foodX, foodY,food_size, ST7735_YELLOW);
}
//===============update snake===================================================================================
void update_snake(){
    for (int i = 0; i < snakelength; i++)  //display snake
    {
      if(i==0)
      {

        tft.fillCircle(snake_x[i],snake_y[i],snake_body_width, ST7735_RED);  //snake head
        Serial.print(snake_x[i]);Serial.print(snake_y[i]);
      }
      else
      {
        tft.drawCircle(snake_x[i],snake_y[i],snake_body_width, ST7735_GREEN); //snake body
      Serial.println(snake_x[i]+snake_body_width+1);Serial.println(snake_y[i]+snake_body_width+1);
      }
    }

   Serial.print("snake_x value is: ");
   Serial.println(snake_x[0]);
   Serial.print("snake_y value is: ");
   Serial.println(snake_y[0]);
   Serial.print("snakelength value is: ");
   Serial.println(snakelength);


 }
 //===============snake move direct=============================================================================
 int snake_direct(int currentX,int initX,int currentY ,int initY){
 int DIRECT ;
 if ( currentX <initX-10){
    DIRECT = LEFT ;
    return DIRECT ;
 }
 if ( currentX  > initX+10 ){
    DIRECT = RIGHT ;
    return DIRECT ;
 }
 if (currentY > initY +10){
     DIRECT = DOWN  ;
     return DIRECT ;
 }
 if (currentY < initY -10){
     DIRECT = UP  ;
     return DIRECT ;
 }
       return 0 ;
 }

//==============update snake's movement==========================================================================
void snake_move(){

snake_body_width;
select;
snake_x, snake_y;

vertical,horizontal;

delta_vert,delta_horiz;

vertical = analogRead(VERT);
horizontal = analogRead(HORIZ);


int direct =snake_direct(horizontal,init_horizontal,vertical,init_vertical);

if(direct != 0 ) {
   switch(direct)
    {
      case UP:
        if(snake_dir!=DOWN)
        {
          snake_dir=UP;
          break;
        }
      case DOWN:
        if(snake_dir!=UP)
        {
          snake_dir=DOWN;
          break;
        }
        case LEFT:
        if(snake_dir!=RIGHT)
        {
          snake_dir=LEFT;
          break;
        }
        case RIGHT:
        if(snake_dir!=LEFT)
        {
          snake_dir=RIGHT;
          break;
        }
        default:break;
    }
    Serial.println("M");
    if(eat_food(snake_dir)==1){
      update_Food();
      score++;
    }
    else {
       touch_the_wall(snake_dir);
       eat_tail(snake_dir);
       move_position(snake_dir);
    }

  update_snake(); // redraw the snake
  }

}
//========================snake move position ===================================================================
void move_position(int DIR){
  int temp_x[snakelength+2];
  int temp_y[snakelength+2];
  for(int i=0;i<snakelength-1;i++)
  {
    temp_x[i]=snake_x[i];
    temp_y[i]=snake_y[i];
  }
  switch(DIR)
  {
    case RIGHT: {snake_x[0]+=1;break;}
    case LEFT: {snake_x[0]-=1;break;}
    case UP: {snake_y[0]-=1;break;}
    case DOWN: {snake_y[0]+=1;break;}
  }
  tft.fillCircle(snake_x[snakelength-1],snake_y[snakelength-1],snake_body_width, ST7735_BLACK); //snake body
  for(int i=1;i<snakelength;i++)
  {
    snake_x[i]=temp_x[i-1];
    snake_y[i]=temp_y[i-1];
  }

}
//============================ eat food position is changed================================================================
void eat_position(){
  int temp_x[snakelength+2];
  int temp_y[snakelength+2];
  for(int i=0;i<snakelength-1;i++)
  {
    temp_x[i]=snake_x[i];
    temp_y[i]=snake_y[i];
  }
  snake_x[0]=foodX;
  snake_y[0]=foodY;
  for(int i=1;i<snakelength;i++)
  {
    snake_x[i]=temp_x[i-1];
    snake_y[i]=temp_y[i-1];
  }
}


// TODO: how to write the this function correctly??
//===============snake eat the food==============================================================================
int eat_food( int dir ){

  int x_temp=snake_x[0];
  int y_temp=snake_y[0];
  switch(dir)
  {
    case UP :y_temp-=1;break;
    case DOWN :y_temp+=1;break;
    case LEFT :x_temp-=1;break;
    case RIGHT :x_temp+=1;break;
  }
  if((x_temp==foodX)&&(y_temp==foodY))
  {
      snakelength+=3;               //snake body incremnt 3
      eat_position();
      return 1;
  }
  else
  {
    return 0;
  }
}

//===============snake eats its tail===============================================================================
void eat_tail(int dir){
  int x_temp=snake_x[0];
  int y_temp=snake_y[0];
  switch(dir)
  {
    case UP :y_temp-=1;break;
    case DOWN :y_temp+=1;break;
    case LEFT :x_temp-=1;break;
    case RIGHT :x_temp+=1;break;
  }
  for(int i=1;i<snakelength;i++)
  {
    if((snake_x[0]==snake_x[i])&&(snake_y[0]==snake_y[i]))
    {
     game_over2();
    }
  }
}

//==============snake touch the wall==============================================================================
void  touch_the_wall(int dir){
   int x_temp=snake_x[0];
   int y_temp=snake_y[0];
  switch(dir)
  {
    case UP :y_temp-=1;break;
    case DOWN :y_temp+=1;break;
    case LEFT :x_temp-=1;break;
    case RIGHT :x_temp+=1;break;
  }
  if(x_temp<1||x_temp>screen_width-1)
  {
    Serial.println("DEAD1");
    game_over1();
  }
  if(y_temp<1||y_temp>screen_height-1)
  {
  Serial.println("DEAD2");
  game_over1();
  }
}
//===============mode0============================================================================================
void mode0(){
  pinMode(LED_1,INPUT);
  digitalWrite(LED_1, HIGH);
  delay(200);
  pinMode(LED_2,INPUT);
  digitalWrite(LED_2, LOW);
  pinMode(LED_3,INPUT);
  digitalWrite(LED_3, LOW);

  update_Food();
  update_snake();
  while(score<2){
    snake_move();
    delay(0);// speed

  }
}
//==============mode1============================================================================================

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

  update_Food();
  update_snake();
   while(score<3){
    snake_move();
    delay(20);

  }

}
//===============mode2==========================================================================================
  void mode2(){
  pinMode(LED_1,INPUT);
  digitalWrite(LED_1, LOW);
  pinMode(LED_2,INPUT);
  digitalWrite(LED_2, LOW);
  pinMode(LED_3,INPUT);
  digitalWrite(LED_3, HIGH);
  delay(200);
  foodX = 50;
  foodY = 20;

  Serial.println(foodX);
  Serial.println(foodY);
  update_Food();
  update_snake();
  while(score>2){
    snake_move();
    delay(5);// speed

  }
}

//===============playthegame======================================================================================
void playthegame(){
  //init();
  //show the main background of the game site
  tft.fillScreen(ST7735_BLACK);
  init_snake_food();
  // fisrt mode
  score = 0;
 update_snake();
  if (score < 4 ){
     mode0();
  }else {
    if(score > 4 && score<8){
      mode1();
    }else
     {
        mode2();
       }
    }

}
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
    //initialize the food and snake
    init_snake_food();


    score = 0;

    init_vertical = analogRead(VERT);
    init_horizontal = analogRead(HORIZ);

    snakelength = initial_snakelength;

    while(true){
      start_game_page();
      Serial.print("strat game is running ");
      // if the joystick button is pressed
      while (true) {
        delay(100);
        if (digitalRead(SEL) == 0){
          playthegame();
          Serial.print("game is playing");
        }
      }
      start_game_page();
      Serial.print("there is a loop");
  }
  // end the Project
  Serial.end();
  return 0;
}
