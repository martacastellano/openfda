# La API REST que utilizaremos es: https://api.fda.gov/drug/label.json
# Seguimos el modelo del ejercicio 10 del L7
# Importamos los modulos necesarios para completar el codigo

import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")   # Establecemos conexion con el servidor
conn.request("GET", "/drug/label.json", None, headers)  # Enviamos un mensaje de solicitud usando el verbo GET

r1 = conn.getresponse()  # lectura del mensaje
print(r1.status, r1.reason)  # Comprobacion de la respuesta --> status: 200 y reason: OK

medicina_raw = r1.read().decode("utf-8")  # Lectura del contenido en json y transformacion en cadena
conn.close()

medicina = json.loads(medicina_raw)     # Pasamos el fichero a un formato mas sencillo para obtener
                                        # los datos requeridos (diccionario, lista)
info = medicina['results'][0]

print('El medicamento cuyo identificador es ' + info['id'] + ', es de uso recomendado en caso de '
      + info['purpose'][0] + ' y es fabricado por ' + info['openfda']['manufacturer_name'][0] + '.')
