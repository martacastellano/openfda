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


# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase. Y los que
# nosotros consideremos los podemos reemplazar por los nuestros
class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    # GET. Este metodo se invoca automaticamente cada vez que hay una
    # peticion GET por HTTP. El recurso que nos solicitan se encuentra
    # en self.path
    def do_GET(self):

        # La primera linea del mensaje de respuesta es el
        # status. Indicamos que OK
        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las
        # cabeceras necesarias para que el cliente entienda el
        # contenido que le enviamos (que sera HTML)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

        # Este es el mensaje que enviamos al cliente: un texto y
        # el recurso solicitado
        message = """<html>

        <body>

        <ol>"""

        message += "<h2>Los nombres de los medicamentos son:</h3>"

        for nombre in medicinas: #Iteramos sobre los elementos de la lista, y los escribimos en forma de lista ordenada (ol) en html

            message += "<li type='disc'>" + nombre + '</li>'

        message += """</ol>

        </body>

        </html>"""

        self.wfile.write(bytes(message,"utf-8"))
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