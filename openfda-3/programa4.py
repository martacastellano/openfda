import socketserver
import json
import http.server

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

for med in range(10):
    try:
        medicinas.append(datos['results'][med]['openfda']['generic_name'][0])
    except KeyError:
        continue


class testHTTPRequestHandler (http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)

        # En las siguientes lineas de la respuesta colocamos las cabeceras necesarias
        # para que el cliente entienda el contenido que le enviamos (en HTML)

        self.send_header('Content-type', 'text/html')

        self.end_headers()

        # Aqui escribiremos el mensaje que queremos mostrar en html

        message = """<html>

                <body>

                <ol>"""

        message += "<h2>Los medicamentos son:</h3>"

        for elem in medicamentos:  # Iteramos sobre los elementos de la lista
                                   # y los escribimos en forma de lista ordenada (ol) en html
            message += "<li type='disc'>" + elem + '</li>'
        message += """</ol>

                </body>

                </html>"""

        self.wfile.write(bytes(message, "utf8"))

        return

    # El servidor comienza aqui
    # Establecemos como manejador nuestra propia clase

    Handler = testHTTPRequestHandler
    # Se configura el socket del servidor, para esperar conexiones de clientes

    with socketserver.TCPServer(("", PORT), Handler) as httpd:

        print("serving at port", PORT)

        # Entra en el bucle principal

        # Las peticiones se atienden desde nuestro manejador

        # Cada vez que se ocurra un "GET" se invoca al metodo do_GET del manejador

        try:

            httpd.serve_forever()

        except KeyboardInterrupt:

            print("")

            print("Interrumpido por el usuario")

    print("")

    print("Servidor parado")