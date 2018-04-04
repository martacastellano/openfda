#la API REST que utilizaremos es: https://api.fda.gov/drug/label.json
#seguimos el modelo del ejercicio 10 del L7
#importamos 'http.client' para establecer conexión con FDA y 'json' para obtener la información en formato python

import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")  #establecemos conexión con el servidor
conn.request("GET", "/drug/label.json", None, headers)  #enviamos un mensaje de solicitud usando el verbo GET

r1 = conn.getresponse()  #lectura del mensaje
print(r1.status, r1.reason)  #comprobación de la respuesta --> status: 200 y reason: OK

repos_raw = r1.read().decode("utf-8")  #lectura del contenido en json y transformación en cadena
conn.close()

repos = json.loads(repos_raw)  #pasamos el fichero a un formato más sencillo para obtener los datos requeridos (diccionario, lista)

info=repos['results'][0]
print('El medicamento cuyo identificador es '+info['id']+', es de uso recomendado en caso de '+info['purpose'][0]+' y es fabricado por ' +info['openfda']['manufacturer_name'][0]+'.')