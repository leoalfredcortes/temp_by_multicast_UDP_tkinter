# Servidor MULTICAST UDP
import serial, time
import socket
import struct

message =  'nuevo mensaje'
arduino = serial.Serial('/dev/ttyUSB0', 9600)
time.sleep(2)
#Direccion IP multicast desde 224.0.0.0 hasta 239.255.255.255
multicast_addr = '224.0.0.1'
port = 6000

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
#Define el Time to Live
#Establece el tiempo de vida de los mensajes en 1
#para que no pasen del segmento de red local.
ttl = struct.pack('b', 1)
rawString = arduino.readline()
print (rawString)

#Para ayudarnos a manipular el buffer la libreria socket de Python
#nos ofrece el metodo setsockopt(), el cual debemos aplicar sobre una instancia
#de la clase socket. 
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, ttl)
#sock.sendto(str.encode(rawString), (multicast_addr, port))
sock.sendto((rawString), (multicast_addr, port))
sock.close()
