import psutil
import ALERTA02_05122023
import io
import os
import re
from operator import itemgetter
from datetime import datetime, timedelta

alert=[]

def get_disk_info():
    #Función que devolverá la unidad de disco y su % de ocupación
    
    #listas que almacenarán discos, ocupación y discos en peligro
    discos_almacenamiento = []
    
      
    #Se extrae la información en cada uno de los discos
    for disk in psutil.disk_partitions():
        usage = psutil.disk_usage(disk.mountpoint)
        discos_almacenamiento.append(disk.mountpoint[0])
        discos_almacenamiento.append(usage.percent)
        
    #Bandera 1 en la cual verificamos discos y % de ocupación
    print(discos_almacenamiento)
    return(discos_almacenamiento)
    
def obtener_archivos_mas_grandes_y_antiguos(ruta_directorio):
    #Función con la cual obtenemos los archivos más grandes y pesados de los discos
    
    # Obtener lista de archivos en el directorio
    archivos = [(nombre, os.path.getsize(os.path.join(ruta_directorio, nombre)), os.path.getctime(os.path.join(ruta_directorio, nombre))) for nombre in os.listdir(ruta_directorio) if os.path.isfile(os.path.join(ruta_directorio, nombre))]

    # Obtener los 3 archivos más grandes
    archivos_mas_grandes = sorted(archivos, key=itemgetter(1), reverse=True)[:3]

    # Obtener los 3 archivos más antiguos
    archivos_mas_antiguos = sorted(archivos, key=itemgetter(2))[:3]

    return archivos_mas_grandes, archivos_mas_antiguos

def formatear_fecha(fecha_creacion):
    #Función con la cual cambiamos formato para que fecha pueda ser entendida
    
    return datetime.fromtimestamp(fecha_creacion).strftime('%Y/%m/%d')

def obtener_estado_memoria():
    # Obtener información sobre el uso de la memoria
    memoria = psutil.virtual_memory()

    # Obtener el porcentaje de uso de la memoria RAM
    porcentaje_uso = memoria.percent

    return porcentaje_uso

def encontrar_ultima_palabra():
      
  documento = open("alertaLog.txt", "r").read()
  palabra = "correo"
  coincidencias = None
  lista =[]
  for coincidencias in re.finditer(palabra,documento):pass
  
  lista.append(coincidencias.start())
  lista.append(coincidencias.end())
  print(lista)
  
  lista.append(documento[(lista[0]+19):(lista[1]+15)])
  lista.append(documento[(lista[0]+22):(lista[1]+18)])
  return (int(lista[2]),int(lista[3]))

def tiempo_transcurrido(hora,minutos):

    # Obtener la hora y minutos actuales
    hora_actual = datetime.now().hour
    minutos_actuales = datetime.now().minute

    # Crear un objeto datetime para la hora dada
    hora_dada_objeto = datetime(datetime.now().year, datetime.now().month, datetime.now().day, hora, minutos)

    # Calcular la diferencia de tiempo
    diferencia_tiempo = datetime.now() - hora_dada_objeto

    # Si han pasado más de 58 minutos, levantar la bandera
    if diferencia_tiempo > timedelta(minutes=58):
        bandera = True
    else:
        bandera = False
        
    # Mostrar el resultado
    print(f"Hora actual: {hora_actual}:{minutos_actuales}")
    print(f"Hora y minutos dados: {hora}:{minutos}")
    print(f"Ha pasado más de 58 minutos: {bandera}")
    return bandera

    
def registro_log(correo_verificacion,estado_actual):
    #Se abre el archivo en modo de escritura
    archivo = io.open("alertaLog.txt", "a")

    #Se obtiene la fecha y hora actual
    fecha_y_hora_actual = datetime.now()

    #Se borra la fecha y hora actual
    fecha_y_hora_formateada = fecha_y_hora_actual.strftime("%Y-%m-%d %H:%M:%S")

    #Se escribe el texto y la fecha y hora actual en el archivo
    archivo.write(correo_verificacion)
    archivo.write(f": {fecha_y_hora_formateada}\n")
    
    #Se escribe en el documento de logs el registro de la finalización de la revisión
    for i in range(len(estado_actual)):
        a=str(estado_actual[i])
        archivo.write(a+",")
    archivo.write("**************************************\n")
    
    # Cerramos el archivo
    archivo.close()
    
    
    
    
    
    
discos_almacenamiento = get_disk_info()

#Se verifica ocupación de los discos según límite definido    
for i in range(len(discos_almacenamiento)):
    correo_verificacion="verificacion"
    
    #se evalúa solamente los datos correspondientes a la ocupación
    if type(discos_almacenamiento[i])==float:
        
        
        if discos_almacenamiento[i]>=70:
            
            a=i-1
            alert.append(discos_almacenamiento[a])
            medidaAlmacenamiento = str(discos_almacenamiento[i])
            correo_verificacion="correo"
            
            # Ruta del directorio a analizar
            directorio_a_analizar = discos_almacenamiento[a]+':'
            mensaje_ocupacion_disco = ("\nEl disco "+ discos_almacenamiento[a] +" se encuentra al "+ medidaAlmacenamiento+"%\n\n")
            
            # Obtenemos los archivos mas pesados y los más antiguos
            archivos_grandes, archivos_antiguos = obtener_archivos_mas_grandes_y_antiguos(directorio_a_analizar)
            
            #los almacenamos en variables provisionales
            resultados_grandes = "\n".join([f"{nombre}: {tamano} bytes" for nombre, tamano, _ in archivos_grandes])
            resultados_antiguos = "\n".join([f"{nombre}: {formatear_fecha(fecha_creacion)}" for nombre, _, fecha_creacion in archivos_antiguos])
            
            #concretmaos en un mensaje unitario
            mensaje=(f"Los 3 archivos más grandes:\n{resultados_grandes}\n\nLos 3 archivos más antiguos:\n{resultados_antiguos}")
            
            # Obtener el estado de la memoria
            estado_memoria = obtener_estado_memoria()

            # Mostrar el resultado
            mensaje_memoria_ram = (f"La memoria RAM se encuentra al {estado_memoria}%.")
            
            mensaje= mensaje_ocupacion_disco+mensaje_memoria_ram+"\n\n"+mensaje
            print(alert)
            print(mensaje)
            
            hora,minutos = encontrar_ultima_palabra()
            bandera = tiempo_transcurrido(hora,minutos)
            
            if bandera != False:
                #Envío de correo con la información necesaria
                ALERTA02_05122023.envio_email(mensaje)
             
        #Se imprime en el registro la acción realizada envío de correo/solamente verificación
        registro_log(correo_verificacion,discos_almacenamiento)
                    
#Bandera 2 en la cual se verifica discos con problema 
print(alert)