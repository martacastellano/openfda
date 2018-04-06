# Partimos del codigo de programa1
import http.client
import json

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json/?search=active_ingredient:acetylsalicylic&limit=100", None, headers)
# Llevamos a cabo la busqueda a partir del principio activo, poniento un limite de 100 medicamentos

r1 = conn.getresponse()
print(r1.status, r1.reason)

aspirinas_raw = r1.read().decode("utf-8")
conn.close()

aspirinas = json.loads(aspirinas_raw)
datos = aspirinas['results']

# Iteramos con un bucle for sobre los distintos medicamentos contenedores de aspirina obtenidos tras nuestra busqueda
for asp in range(len(datos)):
    if datos[asp]['openfda']:
        print('El medicamento cuyo identificador es: ', datos[asp]['id'], 'es fabricado por: ',
              datos[asp]['openfda']['manufacturer_name'][0], '.')
    else:
        print('El medicamento cuyo identificador es: ', datos[asp]['id'], 'no tiene un fabricante reconocible.')
