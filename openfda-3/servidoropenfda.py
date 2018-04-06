import socketserver
import http.server
import http.client
import json

PORT = 1999  # Puerto donde lanzamos el servidor

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")  # Establecemos conexion con el servidor
conn.request("GET", "/drug/label.json?&limit=10", None, headers)  # Podemos como limite 10 medicamentos en la busqueda

r1 = conn.getresponse()  # Obtenemos la informacion requerida
print(r1.status, r1.reason)  # Comprobamos status y razon (200, OK)

info_raw = r1.read().decode("utf-8")  # Lectura en json y transformacion en cadena
conn.close()

medicinas = []  # Se crea una lista para almacenar los nombres genericos de los medicamentos

datos = json.loads(info_raw)  # Pasamos la informacion a un formato que facilite su lectura en python

# Iteramos sobre cada producto, para comprobar mediante un condicional si tiene nombre generico o no,
# Para anadirlo a la lista previamente creada
for med in range(len(datos['results'])):
    if datos['results'][med]['openfda']:
        medicinas.append(datos['results'][med]['openfda']['generic_name'][0])
    else:
        medicinas.append('Nombre no identificado')



# Partimos del server2 del L6
# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase, usamos herencia
class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)  # Respuesta del status (OK)

        self.send_header('Content-type', 'text/html')  # Aclaraciones para que el cliente entienda el mensaje (en HTML)
        self.end_headers()

        # Este es el mensaje que enviamos al cliente
        message = """<html><body>"""

        message += "<h2>Los nombres de los medicamentos obtenidos son:</h3>"  # En negrita

        # Iteramos sobre los elementos de la lista de medicinas previamente creada, y se une al documento html
        for nombre in medicinas:
            message += "<li type='square'>" + nombre + '</li>'  # En una lista

        self.wfile.write(bytes(message, "utf-8"))  # Ecribimos el mensaje HTML
        return


# El servidor comienza a aqui
# Establecemos como manejador nuestra propia clase
Handler = TestHTTPRequestHandler

# Configurar el socket del servidor, para esperar conexiones de clientes
httpd = socketserver.TCPServer(("", PORT), Handler)
print("serving at port", PORT)

# Entrar en el bucle principal
# Las peticiones se atienden desde nuestro manejador
# Cada vez que se ocurra un "GET" se invoca al metodo do_GET de
# nuestro manejador
try:
    httpd.serve_forever()
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
