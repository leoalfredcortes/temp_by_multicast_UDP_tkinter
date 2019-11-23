######################################################################################
# Instituto Tecnológico de Colima - División de Estudios de Posgrado e Investigación #
# Maestría en Sistemas Computacionales - Materia: Tecnologías de Internet            #
#                                                                                    #
# Código Fuente para Servidor UDP, con interfaz tkinter el cual lee datos            #
# del puerto serial (temperatura) si la temperatura excede de los rangos establecidos#
# el programa emitirá una alerta a los clientes conectados a este                    #
#                                                                                    #
# Realizado por:                                                                     #
# Osvaldo Vladimir Rodríguez Leal                                                    #
# José Alfredo Cortés Quiroz                                                         #
# Villa de Álvarez, Col 21/10/19                                                     #
######################################################################################

from tkinter import *   #libreria gráfica Tkinter 
import tk_tools         #libreria gráfica para el acelerometro
import serial, time     #libreria para el puerto serial
import threading        #libreria para manejar hilos
import socket           #libreria para manejar la comunicación por sockets
import struct           #libreria para manejar estructuras

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)         # configuramos el socket para transmitir por el protocolo UDP
sock.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 1)  # añadimos la opción de envío por IP de forma Multicast con tiempo de vida 1
arduino = serial.Serial('/dev/ttyUSB0', 9600)                   # definimos la dirección del puerto serial y a que frecuencia se utilizara
mensage = '!Alerta temperatura elevada!'                        # mensaje que se enviara al momento que se produzca una alerta
multicast_addr = '224.0.0.1'                                    # definimos las dirección IP multicast que puede ser desde 224.0.0.0 hasta 239.255.255.255
port = 6000                                                     # definimos el puerto por el cual se transmitirá
temp1 = ""                                                      # variable para el 1er valor donde empezaran las alertas
temp2 = ""                                                      # variable para 2do valor hasta donde se enviaran las alertas

window = Tk()                                                   # instrucción para inicializar Tkinter
window.title("::Monitor UDP::")                                 # definimos el titulo de la ventana
window.geometry('230x260')                                      # definimos el tamaño de la ventana

tk_title = Label(window,text="Temperature Monitor")             # mostramos una etiqueta de tipo Label 
tk_title.grid(column=1,row=0)                                   # definimos la ubicación del Label dentro de la ventana 

gauge = tk_tools.Gauge(window, max_value=50.0,
    label='Temperature', unit='°C')                             # llamamos el tool gauge y configuramos valores máximos, mínimos y el titulo
gauge.grid(column=1, row=1)                                     # definimos la ubicación del tool gauge dentro de la ventana                          

tk_tex_intruction = Label(window,text="Rango para Alertas")     # mostramos una etiqueta de tipo Label
tk_tex_intruction.grid(column=1,row=3)                          # definimos la ubicación del Label dentro de la ventana 

tk_label= Label(window,text="De:")                              # mostramos una etiqueta de tipo Label
tk_label.grid(column=1,row=4)                                   # definimos la ubicación del Label dentro de la ventana

txt_in = Entry(window,width=15)                                 # creamos una entrada para el 1er valor del rango para las alertas
txt_in.grid(column=1, row=5)                                    # definimos la ubicación de la entrada de texto dentro de la ventana

tk_label2= Label(window,text="A:")                              # mostramos una etiqueta de tipo Label
tk_label2.grid(column=1,row=6)                                  # definimos la ubicación del Label dentro de la ventana

txt_in2 = Entry(window,width=15)                                # creamos otra entrada para el 2do valor del rango para las alertas
txt_in2.grid(column=1, row=7)                                   # definimos la ubicación de la entrada de texto dentro de la ventana

def read_serial():                                              # Función donde se leerá datos del puerto seria y se enviaran por UDP alertas si estos valores exeden del rango estabelicido
    while(True):                                                # Iniciamos un siclo infinito
        rawString = arduino.readline()                          # Leemos puerto serial hasta un salto de linea y asignamos datos a una variable
        gauge.set_value(float(rawString))                       # Convertimos a flotante (decimales) el valor leído y lo colocamos en el gráfico 
        cadena = rawString.decode("utf-8")                      # Convertimos a string (cadena) el valor leído por serial
        temp1 = float(txt_in.get())                             # Convertimos a flotante el primer valor para el rango de alertas y lo asignamos a una variable
        temp2 = float(txt_in2.get())                            # Convertimos a flotante el segundo valor para el rango de alertas y lo asignamos a una variable
        if (float(cadena) >= temp1 and float(cadena)<= temp2):  # Convertimos a flotante los valores de la cadena y comparamos con los valores del rango establecido
            sock.sendto((str.encode(cadena + "°C" + mensage )), # Si los valores leidos están en el rango de alertas, qui enviamos el mensaje de alerta junto el valor que la activo
             (multicast_addr, port))

def iniciar():                                                  # Función que manda a llamar la función de leer datos por puerto serial
    tread1 = threading.Thread(target = read_serial)             # Colocamos en hilos la función de leer datos por puerto serial
    tread1.start()                                              # Iniciamos los hilos

btn = Button(window, text="Star Alerts", bg="blue", fg="white", # Creamos Botón que manda a llamar la función iniciar
    command=iniciar)
btn.grid(column=1, row=8)                                       # Situamos el Botón dentro de la ventana

window.mainloop()                                               # Ponemos en un siclo la Interfaz creada en espera de algún evento
