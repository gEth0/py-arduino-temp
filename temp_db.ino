#include <dht11.h>
dht11 DHT11;
#define DHT11PIN 6
void setup(void)
{
  Serial.begin(9600);
}
void loop(void)
{
  DHT11.read(DHT11PIN);
  Serial.print(DHT11.temperature);
  Serial.print(' ');
  Serial.println(DHT11.humidity);

  delay(1800000);//Set the temperature measurement frequency here (milliseconds)
}
//gEth0