import psutil
import ALERTA02_05122023
import io
import datetime

def get_disk_info():
    
    #listas que almacenarán discos, ocupación y discos en peligro
    storage = []
    alert=[]
    correo_verificacion=""
      
    #Se extrae la información en cada uno de los discos
    for disk in psutil.disk_partitions():
        usage = psutil.disk_usage(disk.mountpoint)
        storage.append(disk.mountpoint[0])
        storage.append(usage.percent)
        
    #Bandera 1 en la cual verificamos discos y % de ocupación
    print(storage)
    
    #Se verifica ocupación de los discos según límite definido    
    for i in range(len(storage)):
        correo_verificacion="verificacion"
        if type(storage[i])==float:
            
            if storage[i]>=50:
                a=i-1
                alert.append(storage[a])
                medidaAlmacenamiento = str(storage[i])
                correo_verificacion="correo"
                #Envío de correo con la información necesaria
                ALERTA02_05122023.envio_email(storage[a],medidaAlmacenamiento)
                   
            #Se imprime en el registro la acción realizada envío de correo/solamente verificación
            registro_log(correo_verificacion,storage)            
    #Bandera 2 en la cual se verifica discos con problema 
    print(alert)
    
def registro_log(correo_verificacion,estado_actual):
    #Se abre el archivo en modo de escritura
    archivo = io.open("alertaLog.txt", "a")

    #Se obtiene la fecha y hora actual
    fecha_y_hora_actual = datetime.datetime.now()

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
    
if __name__ == "__main__":
    get_disk_info()
