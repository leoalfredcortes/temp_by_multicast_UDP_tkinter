######################################################################################
# Instituto Tecnológico de Colima - División de Estudios de Posgrado e Investigación #
# Maestría en Sistemas Computacionales - Materia: Tecnologías de Internet            #
#                                                                                    #
# Código Fuente para Cliente (receptor) UDP, con interfáz tkinter el cual obtiene    #
# alertas si la temperatura pasa los rangos establesidos en el servidor (emisor)     #
#                                                                                    #
# Realizado por:                                                                     #
# Osvaldo Vladimir Rodríguez Leal                                                    #
# José Alfredo Cortés Quiroz                                                         #
# Villa de Álvarez, Col 21/10/19                                                     #
######################################################################################

from tkinter import *                         # Importamos libreria gráfica Tkinter
from tkinter import scrolledtext              # Importamos el elemento scrolledtext de la libreria Tkinter
import threading                              # Importamos libreria para manejar Hilos
import socket                                 # Importamos Libreria para manejar comunicación por Sockets 
import struct                                 # Importamos Librearia para convertir cadenas de bytes

multicast_addr = '224.0.0.1'                  # Definimos la dirección (grupo) Multicast al que pertenece la interfaz
bind_addr = '0.0.0.0'                         # Definimos la IP Host al cual se conectara  
port = 6000                                   # Definimos el puerto por el cual se establesera la comunicación

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)                     # Configuramos el socket para establecer comunicación por protocolo UDP
membership = socket.inet_aton(multicast_addr) + socket.inet_aton(bind_addr) # Configuramos el grupo al que pertenecerá el receptor 

sock.setsockopt(socket.IPPROTO_IP, socket.IP_ADD_MEMBERSHIP, membership)    # Cargamos la configuración del grupo multicast al socket
sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)                  # terminamos con la configuración del socket para el enlace

sock.bind((bind_addr, port))                  # Realizamos en enlace                                          

window = Tk()                                 # Inicializamos interfaz gráfica Tkinter 
window.title("..::Receptor Aletas de Temperatura UDP::..")                  # Asignamos un titulo a la ventana creada            
window.geometry('425x450')                                                  # Definimos el tamaño de la ventana
area_conversation = scrolledtext.ScrolledText(window,width=50,height=20)    # creamos un control tipo scrolledtext y determinamos el largo y ancho
area_conversation.grid(column=1, row=0)                                     # situamos el scrolledtext en la ventana
falg_start = 0                                                              # variable para utilizar como bandera

def get_alerts():                                                           # función para recibir las alertas
    falg_start = 1                                                          # cambiamos el estatus de nuestra bandera a 1    
    while(falg_start==1):                                                   # Iniciamos un siclo hasta que nuestra bandera cambie
        message, address = sock.recvfrom(255)                               # cargamos la alerta recibida en la variable message
        area_conversation.insert(INSERT,message)                            # Insertamos en scrolledtext la alerta recibida 
        area_conversation.insert(INSERT,'\n')                               # Insertamos en scrolledtext un salto de linea
        
def clean_text():                                                           # Función para limpiar scrolledtext
    area_conversation.delete('1.0', END)                                    # Borramos contenido de scrolledtext    
    
def ini_prog():                                                             # Función que inicia la recepción de alertas
    area_conversation.insert(INSERT,"Iniciando sistema de Alertas...")      # Introducimos mensaje de inicio en scrolledtext
    tread1 = threading.Thread(target = get_alerts)                          # Iniciamos la función de recibir alertas a hilos
    tread1.start()                                                          # Iniciamos hilos    
    
btn = Button(window, text="Start", bg="blue", fg="white", command=ini_prog) # Creamos Botón, asignamos texto, ponemos azul el color de fondo y lo asociamos con la funcion para inicio de alertas
btn.grid(column=1, row=2)                                                   # Situamos el Botón en la ventana    

btn = Button(window, text="Clear", bg="blue", fg="white", command=clean_text) # Creamos Botón, asignamos texto, ponemos azul el color de fondo y lo asociamos con la funcion para limpiar scrolledtext
btn.grid(column=1, row=3)                                                   # Situamos el Botón en la ventana

window.mainloop()                               # Ponemos en un siclo infinito la Interfaz creada en espera de algún evento.
