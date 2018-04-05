import http.server
import socketserver
import http.client
import json

PORT = 8001  # Puerto donde lanzamos el servidor

headers = {'User-Agent': 'http-client'}

conn = http.client.HTTPSConnection("api.fda.gov")
conn.request("GET", "/drug/label.json?&limit=10", None, headers)  # Podemos como limite 10 medicamentos en la busqueda

r1 = conn.getresponse()
print(r1.status, r1.reason)

repos_raw = r1.read().decode("utf-8")
conn.close()

medicinas = []  # Se crea una lista para almacenar los nombres genericos de los medicamentos

datos = json.loads(repos_raw)

for med in range(10):
    # Usamos try-excep para evitar el error en caso de que no exista el nombre de algun medicamento (KeyError)
    try:
        medicinas.append(datos['results'][med]['openfda']['generic_name'][0])
    except KeyError:
        continue


# Partimos del servidor2 del L6
class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def do_GET(self):
        self.send_response(200)  # Muestra el status (OK)

        self.send_header('Content-type', 'text/html')  # Aclaraciones del contenido para el cliente (en HTML)
        self.end_headers()

        message = """<html><body>"""
        message += "<h2>Los nombres de los medicamentos son:</h3>"  # En negrita

        # Iteramos sobre los elementos de la lista de medicinas previamente creada, y se une al documento html
        for nombre in medicinas:
            message += "<li type='disc'>" + nombre + '</li>'  # En una lista

        self.wfile.write(bytes(message, "utf8"))  # Mensaje enviado al cliente
        return


# El servidor comienza a aqui
# Establecemos como manejador nuestra propia clase
Handler = TestHTTPRequestHandler

# -- Configurar el socket del servidor, para esperar conexiones de clientes
with socketserver.TCPServer(("", PORT), Handler) as httpd:
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
