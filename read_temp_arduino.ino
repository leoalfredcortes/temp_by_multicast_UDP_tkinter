#include "LiquidCrystal_I2C.h"
#include "Adafruit_Sensor.h"
#include "Wire.h"
#include "DHT.h"

// Constructor de la librería de LCD 16x2
// Aqui se configuran los pines asignados a la pantalla del PCF8574
LiquidCrystal_I2C lcd (0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

#define DHTPIN 2     // Pin al que se conecto el sensor DHT

#define DHTTYPE DHT22   // DHT 22  (AM2302), AM2321

DHT dht(DHTPIN, DHTTYPE);

void setup() {
  lcd.begin(16, 2); // Indicar a la libreria que tenemos conectada una pantalla de 16x2
  lcd.home (); // Mover el cursor a la primera posición de la pantalla (0, 0)
  lcd.print("Bienvenido");
  Serial.begin(9600); // Inicialisa la interfas serial
  dht.begin(); //inicialisa la lectura del sensor DHT
}

void loop() {
  delay(2000); // Tiempo de espera entre lecturas

  float h = dht.readHumidity(); //leemos humedad y asignamos valor a variable
  float t = dht.readTemperature(); // leemos temperatura y asignamos valor a varialbe
 
  //float f = dht.readTemperature(true); // temperatura en Farenheit

  if (isnan(h) || isnan(t)) { //comprovamos que las lecturas tengan algun valor
    Serial.println(F("Error al leer sensor DHT!"));
    lcd.clear(); //limpiamos pantalla
    lcd.home ();
    lcd.print("Error sensor DHT");
    return;
  }

  Serial.print(F("Humedad: "));
  Serial.print(h);
  Serial.print("% \n");
  lcd.setCursor(0,1);
  lcd.print("Hmd: ");
  lcd.print(h);
  Serial.print(F("Temperatura: "));
  Serial.print(t);
  Serial.print(F("°C "));
  Serial.print("\n");
  lcd.setCursor(0,0);
  lcd.print("Temp: ");
  lcd.print(t);

}
