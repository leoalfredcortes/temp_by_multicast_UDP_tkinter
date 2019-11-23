#include "LiquidCrystal_I2C.h" // Libreria para utulizar LCD con adaptador i2c
#include "Adafruit_Sensor.h" // Libreria necesaria para LiquidCrystal_I2C
#include "Wire.h" // Libreria para utilizar i2c
#include "DHT.h" // Libreria para leer sensor DHT22 u DHT11

// Constructor de la librería de LCD 16x2
// Aqui se configuran los pines asignados a la pantalla del PCF8574
LiquidCrystal_I2C lcd (0x3F, 2, 1, 0, 4, 5, 6, 7, 3, POSITIVE);

#define DHTTYPE DHT22   // Definimos el sensor DHT22 o DHT11 
#define DHTPIN 2     // Definimos el Pin al que se conecto el sensor DHT
DHT dht(DHTPIN, DHTTYPE); // Cargamos la configuracion del Pin de lectura y el Tipo de DHT

void setup() {
  lcd.begin(16, 2); // Indica a la libreria que tenemos conectada una pantalla de 16x2
  lcd.home (); // Movemos el cursor a la primera posición de la pantalla (0, 0)
  lcd.print("Bienvenido"); // Mostramos un mensage en LCD al Iniciar
  Serial.begin(9600); // Inicialisa la interfas serial a 9600 baudios
  dht.begin(); //Inicialisa la lectura del sensor DHT
}

void loop() {
  delay(2000); // Tiempo de espera entre lecturas

  float h = dht.readHumidity(); // leemos humedad y asignamos valor a variable
  float t = dht.readTemperature(); // leemos temperatura y asignamos valor a varialbe 
  float f = dht.readTemperature(true); // leemos temperatura en Farenheit y asignamos valor a varialbe 

  if (isnan(h) || isnan(t)) { //comprovamos que las lecturas tengan algun valor
    Serial.println(F("Error al leer sensor DHT!")); // Si ocurrio algun error en la lectura mostramos mensaje por puerto serial
    lcd.clear(); // Limpiamos pantalla de LCD
    lcd.home (); // Movemos el cursor a la primera posición de la pantalla (0, 0)
    lcd.print("Error sensor DHT"); //Si ocurrio algun error en la lectura mostramos en pantalla LCD mensaje de error 
    return; // Al finalisar el envio de mensaje volvemos a intentar leer el sensor hasta conseguir algun valor aceptable
  }

  //Serial.print(F("Humedad: ")); //mandamos por puerto serial menseje de Humedad
  //Serial.print(h); //seguido mandamos por puerto serial el valor de la humedad relativa
  //Serial.print("% \n"); //seguido el simbolo de porciento y un salto de linea
  
  lcd.setCursor(0,1); //ponemos el cursor al principio de la segunda linea de la LCD
  lcd.print("Hmd: "); // seguido enviamos el texto refrente al a la Humedad a la pantalla LCD
  lcd.print(h); // seguido el valor de la Humedad relativa

  //Serial.print(F("Temperatura: ")); //mandamos por puerto serial menseje de Temperatura
  Serial.print(t); //seguido mandamos por puerto serial el valor de la Temperatura 
  //Serial.print(F("°C \n")); //seguido el simbolo de grados centigrados y un salto de linea

  lcd.setCursor(0,0); // ponemos el cursor al principio de la primer linea de la LCD
  lcd.print("Temp: "); // seguido enviamos el texto refrente al a la Temperatura a la pantalla LCD
  lcd.print(t); // seguido el valor de la Temperatura 

}
