#include <WiFi.h>
#include <Servo.h> // Include the Servo library

const char *ssid = "hackathon_2024";
const char *password = "hackathon_2024";

WiFiServer server(80);

#define HEAD 3  // Pin for head servo
#define TAIL 11 // Pin for tail servo
#define M_L1 5  // Going towards, left front, right back
#define M_L2 6  // Going backwards, left front, right back
#define M_R1 9  // Going towards, left back, right front
#define M_R2 10 // Going backwards, left back, right front

Servo headServo; // Create Servo object for head
Servo tailServo; // Create Servo object for tail

int pwm;
int inkey;
int tail_pos = 0;
int head_pos = 90; // Initial head position

void setup()
{
  Serial.begin(9600);
  while (!Serial)
    delay(10);

  pinMode(M_L1, OUTPUT);
  pinMode(M_L2, OUTPUT);
  pinMode(M_R1, OUTPUT);
  pinMode(M_R2, OUTPUT);

  // Attach servos to their respective pins
  headServo.attach(HEAD);
  tailServo.attach(TAIL);

  // Set initial positions for servos
  headServo.write(head_pos);
  tailServo.write(tail_pos);

  Serial.print("Connecting to ");
  Serial.println(ssid);
  WiFi.begin(ssid, password);
  while (WiFi.status() != WL_CONNECTED)
  {
    delay(500);
    Serial.print(".");
  }
  Serial.println("");
  Serial.println("WiFi connected.");
  Serial.println("IP address: ");
  Serial.println(WiFi.localIP());
  server.begin();
}

void Moter_Control(int L1, int L2, int R1, int R2)
{
  int pwm_L1 = L1;
  int pwm_L2 = L2;
  int pwm_R1 = R1;
  int pwm_R2 = R2;
  analogWrite(M_L1, pwm_L1);
  analogWrite(M_L2, pwm_L2);
  analogWrite(M_R1, pwm_R1);
  analogWrite(M_R2, pwm_R2);
}

void Head_Move(int val)
{
  // Ensure the value is within the servo's limits
  head_pos = constrain(val, 0, 180);
  headServo.write(head_pos); // Move the head servo
  Serial.print("Head mozed to position: ");
  Serial.println(head_pos);
}

void Tail_Move(int val)
{
  // Ensure the value is within the servo's limits
  tail_pos = constrain(val, 0, 180);
  tailServo.write(tail_pos); // Move the tail servo
  Serial.print("Tail moved to position: ");
  Serial.println(tail_pos);
}

void loop()
{
  WiFiClient client = server.available();
  if (client)
  {
    Serial.println("New Client.");
    String request = client.readStringUntil('\r');
    Serial.println("\nrequest:\n");
    Serial.println(request);

    String currentLine = "";
    while (client.connected())
    {
      if (client.available())
      {
        char c = client.read();
        Serial.println("\nc:\n");

        Serial.write(c);
        request += c;
        if (currentLine.length() == 0)
        {
          client.println("HTTP/1.1 200 OK");
          client.println("Content-type:text/html");
          client.println("Connection: close");
          client.println();

          Serial.println(request.indexOf("w"));
          if (c == 'w')
          {
            Moter_Control(50, 0, 50, 0); // front
          }
          else if (c == 's')
          {
            Moter_Control(0, 50, 0, 50); // back
          }
          else if (c == 'd')
          {
            Moter_Control(0, 50, 50, 0); // right
          }
          else if (c == 'a')
          {
            Moter_Control(50, 0, 0, 50); // left
          }
          else if (c == 'q')
          {
            Moter_Control(50, 0, 0, 50); // left 360
          }
          else if (c == 'e')
          {
            Moter_Control(50, 0, 0, 50); // right 36z0
          }
          else if (c == 'z')
          {
            Moter_Control(0, 0, 0, 0); // stop
          }
          else if (c == 'k')
          {
            head_pos += 10;
            Head_Move(head_pos);
          }
          else if (c == 'l')
          {
            head_pos -= 10;
            Head_Move(head_pos);
          }
          else if (c == 'n') // Control tail movement
          {
            tail_pos += 10;
            Tail_Move(tail_pos);
          }
          else if (c == 'm')
          {
            tail_pos -= 10;
            Tail_Move(tail_pos);
          }
          else if (c == '1')
          {
            Moter_Control(50, 0, 0, 0);
          }
          else if (c == '2')
          {
            Moter_Control(0, 50, 0, 0);
          }
          else if (c == '3')
          {
            Moter_Control(0, 0, 50, 0);
          }
          else if (c == '4')
          {
            Moter_Control(0, 0, 0, 50);
          }
        }
        else
        {
          currentLine = "";
        }
      }
    }
    request = "";
    Moter_Control(0, 0, 0, 0); // stop
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
