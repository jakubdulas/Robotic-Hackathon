#include <WiFi.h>

const char *ssid = "hackathon_2024";
const char *password = "hackathon_2024";

WiFiServer server(80);

#define M_L1 5
#define M_L2 6
#define M_R1 9
#define M_R2 10

int pwm;
int inkey;

void setup()
{
  Serial.begin(9600);
  while (!Serial)
    delay(10);

  pinMode(M_L1, OUTPUT);
  pinMode(M_L2, OUTPUT);
  pinMode(M_R1, OUTPUT);
  pinMode(M_R2, OUTPUT);

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
          else if (c == 'z')
          {
            Moter_Control(0, 0, 0, 0); // stop
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
