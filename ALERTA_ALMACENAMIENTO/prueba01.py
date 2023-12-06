import re

def encontrar_ultima_palabra(documento, palabra):
  """
  Encuentra la posición de la última aparición de la palabra en el documento.

  Args:
    documento: El texto del documento.
    palabra: La palabra que se desea encontrar.

  Returns:
    La posición de la última aparición de la palabra en el documento, o -1 si la palabra no se encuentra.
  """

  #coincidencias = re.finditer(palabra, documento)
  #if coincidencias:
  #  coincidencia = coincidencias[-1]
  #  return coincidencia.start()
  #else:
  #  return -1
  coincidencias = None
  lista=[]
  for coincidencias in re.finditer(palabra,documento):pass
  lista.append(coincidencias.start())
  #for i in coincidencias:
  #    print (i.start())
  return lista

documento = open("alertaLog.txt", "r").read()
palabra = "correo"
posicion = encontrar_ultima_palabra(documento, palabra)

print(posicion)