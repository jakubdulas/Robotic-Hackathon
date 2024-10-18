#include <WiFi.h>
#include <Servo.h> // Include the Servo library

const char *ssid = "hackathon_2024";
const char *password = "hackathon_2024";

// Define static IP, gateway, and subnet
IPAddress ip(192, 168, 0, 199);
IPAddress gateway(192,168,0,1);
IPAddress subnet(255, 255, 255, 0);
IPAddress dns(192, 168, 1, 254); //primaryDNS


WiFiServer server(80);

#define HEAD 3  // Pin for head servo
#define TAIL 11 // Pin for tail servo
#define M_L1 5  // Going towards, left front, right back
#define M_L2 6  // Going backwards, left front, right back
#define M_R1 9  // Going towards, left back, right front
#define M_R2 10 // Going backwards, left back, right front
#define V 70
#define HT_V 1

Servo headServo; // Create Servo object for head
Servo tailServo; // Create Servo object for tail

int pwm;
int inkey;
int tail_pos = 0;
int head_pos = 90;             // Initial head position
bool head_moving_right = true; // Direction of head movement
bool tail_moving_right = true; // Direction of tail movement

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
  WiFi.config(ip, dns, gateway, subnet); 

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
}

void Tail_Move(int val)
{
  // Ensure the value is within the servo's limits
  tail_pos = constrain(val, 0, 180);
  tailServo.write(tail_pos); // Move the tail servo
}

void moveHeadAndTail()
{
  // Move head
  if (head_moving_right)
  {
    head_pos += HT_V; // Move right
    if (head_pos >= 180)
    {
      head_pos = 180;            // Limit to max position
      head_moving_right = false; // Change direction
    }
  }
  else
  {
    head_pos -= HT_V; // Move left
    if (head_pos <= 0)
    {
      head_pos = 0;             // Limit to min position
      head_moving_right = true; // Change direction
    }
  }
  Head_Move(head_pos);

  // Move tail
  if (tail_moving_right)
  {
    tail_pos += HT_V; // Move right
    if (tail_pos >= 70)
    {
      tail_pos = 70;             // Limit to max position
      tail_moving_right = false; // Change direction
    }
  }
  else
  {
    tail_pos -= HT_V; // Move left
    if (tail_pos <= 0)
    {
      tail_pos = 0;             // Limit to min position
      tail_moving_right = true; // Change direction
    }
  }
  Tail_Move(tail_pos);
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
            Moter_Control(V, 0, V, 0); // front
          }
          else if (c == 's')
          {
            Moter_Control(0, V, 0, V); // back
          }
          else if (c == 'd')
          {
            Moter_Control(0, 0, V, 0);
          }
          else if (c == 'a')
          {
            Moter_Control(V, 0, 0, 0); // left
          }
          else if (c == 'z')
          {
            Moter_Control(0, 0, 0, 0); // stop
          }
          else if (c == 'q')
          {
            Moter_Control(V, 0, 0, V); // left
          }
          else if (c == 'e')
          {
            Moter_Control(0, V, V, 0); // right
          }
        }
        else
        {
          currentLine = "";
        }
      }
      moveHeadAndTail();
    }
    request = "";
    Moter_Control(0, 0, 0, 0); // stop
    client.stop();
    Serial.println("Client disconnected.");
    Serial.println("");
  }
}
