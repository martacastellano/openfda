import http.server
import socketserver
import http.client
import json

PORT = 1999  # Puerto donde lanzamos el servidor

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=10", None, headers)  # Podemos como limite 10 medicamentos en la busqueda
r1 = conn.getresponse()
print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")
conn.close()

medicinas = []  # Se crea una lista para almacenar los nombres genericos de los medicamentos

datos = json.loads(repos_raw)

for med in range(len(datos)):
    medicinas.append(datos['results'][med]['openfda']['generic_name'][0])

print(medicinas)
