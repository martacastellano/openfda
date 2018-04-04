# Partimos del mismo codigo del programa1
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?limit=10", None, headers)  # Como buscamos informacion de
                                                                 #10 medicamentos ponemos limit=10
r1 = conn.getresponse()
print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")
conn.close()

repos = json.loads(repos_raw)

# Itero con un bucle for para acceder a la informacion de los 10 medicamentos
for medicamento in range(10):
    datos= repos['results'][medicamento]
    print('El medicamento', medicamento+1,' tiene como id: ',datos['id'])