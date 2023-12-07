import smtplib
from email.mime.text import MIMEText

def envio_email(mensaje):
    # Se define los datos del correo electrónico
    remitente = "<costos@mayaprin.com>"
    destinatario = "<ampablojose@gmail.com>"
    msg = MIMEText(mensaje)
    msg['Subject'] = 'ALERTA DE ALMACENAMIENTO SERVIDOR SAP'
    msg['From'] = "MONITOREO SAP"
    msg['To'] = destinatario
   
    # Se crea una conexión al servidor SMTP
    servidor = smtplib.SMTP("smtp.gmail.com", 587)

    # Se inicia la conexión con el servidor
    servidor.starttls()

    # Autenticamos al servidor
    servidor.login("costos@mayaprin.com", "Mayaprin100%")

    # Enviamos el correo electrónico
    servidor.sendmail(remitente, destinatario, msg.as_string())

    # Cerramos la conexión con el servidor
    servidor.quit()
