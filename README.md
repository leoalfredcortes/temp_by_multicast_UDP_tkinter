# Sistema de alertas de Temperatura 
Sistema de Alertas Multicast por UDP escrito en Python3

El sistema lee datos de un dispositivo sensor realizado con Arduino
este los envia al programa Emisor por puerto serial 
el Emisor envia de froma multicast a traves del protocolo UDP las alertas.

El programa Emisor lee constantemente la temperatura recibida

Para que el programa emisor empiece a mandar alerta es necesario configurar el rango 
en el cual este empezara amandar alertas.

El programa Receptor recibira las Alertas programadas en el Programa Emisor
