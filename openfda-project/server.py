import http.server
import http.client
import socketserver
import json

PORT = 8000
socketserver.TCPServer.allow_reuse_address = True    # Esta linea de codigo permite mantener siempre el mismo puerto  


# Clase con nuestro manejador. Es una clase derivada de BaseHTTPRequestHandler
# Esto significa que "hereda" todos los metodos de esta clase, usamos herencia
class TestHTTPRequestHandler(http.server.BaseHTTPRequestHandler):

    def get_conection(self, limit=10, search="", name=""): 
    # Utilizaremos esta funcion para obtener la informacion de la API de openFDA

        headers = {'User-Agent': 'http-client'}
        Request = "/drug/label.json?limit={}".format(limit)

        # Utilizamos un condicional para añadir la informacion solicitada a la peticion
        if search != "":
            Request += '&search=' + search + ':' + name

        print("Requested resource: " + Request)

        # Establecemos conexion y solicitamos la informacion
        conn = http.client.HTTPSConnection("api.fda.gov")
        conn.request("GET", Request, None, headers)

        r1 = conn.getresponse()

        # Chequeamos el status del programa, si da error se aborta
        if r1.status == 404:
            print("ERROR. Recurso no encontrado")
            exit(1)
        else:
            print(r1.status, r1.reason)

        info = json.loads(r1.read().decode("utf-8"))
        conn.close()

        return info
    
    

    def get_indice(self):    # Diseñamos el contenido html de la pagina principal del formulario
        info_api = '''
            <html>
                <head>
                    <title>OpenFDA</title>
                </head>
                <body style='background: lightpink'>
            <p><h3>MEDICAMENTOS:</h3></p>
            <p><form action="listDrugs" method="get">
                  Cantidad de medicamentos a obtener:<input type="text" name='limit' value="">
                  <input type="submit" value="Buscar">
            </form>
            <p><h3>BUSQUEDA DE MEDICAMENTOS:</h3></p>
            <form action = "searchDrug" method="get">
                  Principio activo*: <input type="text" name="active_ingredient" value="Glycerin">
                  Limite de medicamentos: <input type="text" name="limit" value="">
                  <input type="submit" value="Buscar">
                  <br><br>
                  <td>*Recuerde que debe buscar previamente el principio activo en el listado de medicamentos</td>
            </form>
            <p><h3>EMPRESAS:</h3></p>
            <form action = "listCompanies" method="get">
                  Cantidad de empresas a obtener: <input type="text" name="limit" value="">
                  <input type="submit" value="Buscar">
            </form>
            <p><h3>BUSQUEDA DE EMPRESAS:</h3></p>
            <form action = "searchCompany" method="get">
                  Empresa**: <input type="text" name="company" value="Apotheca Company">
                  Limite de medicamentos: <input type="text" name="limit" value="">
                  <input type="submit" value="Buscar">
                  <br><br>
                  <td>**Recuerde que debe buscar el nombre de la empresa que desee en el listado de empresas</td>
            </form>
            <p><h3>USOS Y PRECAUCIONES:</h3></p>
            <form action = "listWarnings" method="get">
                  Introduzca la cantidad de medicamentos de los que desee obtener precauciones: <input type="text" name="limit" value="">
                  <input type="submit" value="Buscar">
            </form>
            '''

        return info_api
    
    

    def get_listDrugs(self, limit):    # Diseñamos el contenido html para el listado de medicamentos
        info = self.get_conection(limit)    # Establecemos conexion con la API

        info_api = (' <!DOCTYPE html>\n'
                    '<html lang="es">\n'
                    '<head>\n'
                    '    <meta charset="UTF-8">\n'
                    '    <title>API</title>\n'
                    '</head>\n'
                    '<body style="background: lightblue">\n'
                    '<h1>Lista de medicamentos:</h2>\n'
                    '\n'
                    )

        
        # Iteramos sobre la informacion del API para obtener la lista
        for i in range(len(info["results"])): 
            id = info["results"][i]["id"]

            # Comprobamos que los datos que queremos mostrar existen, sino mandamos un mensaje de desconocido
            if "active_ingredient" in info["results"][i].keys():
                principio_activo = info["results"][i]['active_ingredient'][0]
            else:
                principio_activo = "Desconocido"

            if info["results"][i]["openfda"]:
                nombre = info["results"][i]["openfda"]["generic_name"][0]
            else:
                nombre = 'Desconocido'

            # Añadimos la informacion de cada elemento al codigo html           
            info_api += '<li type="square"><td> Nombre del medicamento: ' + nombre + '</td></li>\n'
            info_api += '<li type="square"><td> Identificador del medicamento: ' + id + '</td></li>\n'
            info_api += '<li type="square"><td> Principio activo del medicamento: ' + principio_activo + '</td></li>\n'
            info_api += '<br>'

        return info_api

    
    
    def get_searchDrug(self, limit, search, name):    # Diseñamos el contenido referente a la busqueda de medicamentos
                                                        # en funcion de su principio activo
        info = self.get_conection(limit, search, name)

        info_api = (' <!DOCTYPE html>\n'
                    '<html lang="es">\n'
                    '<head>\n'
                    '    <meta charset="UTF-8">\n'
                    '    <title>API</title>\n'
                    '</head>\n'
                    '<body style="background: orange">\n'
                    '<h1>Medicamentos encontrados:</h2>\n'
                    '\n'
                    )

        # Iteramos sobre la informacion del API para obtener la lista
        for i in range(len(info["results"])):
            id = info["results"][i]["id"]

            # Comprobamos la existencia de los datos
            if info["results"][i]["openfda"]:
                nombre = info["results"][i]["openfda"]["generic_name"][0]
            else:
                nombre = 'Desconocido'

            # Añadimos la informacion de cada elemento al codigo html
            info_api += '<li type="square"><td>' + nombre + ' (ID: ' + id + ') <td></li>\n'

        return info_api


    
    def get_listCompanies(self, limit):    # Diseñamos el contenido referente al listado de las empresas 
        info = self.get_conection(limit)

        info_api = (' <!DOCTYPE html>\n'
                    '<html lang="es">\n'
                    '<head>\n'
                    '    <meta charset="UTF-8">\n'
                    '    <title>API</title>\n'
                    '</head>\n'
                    '<body style="background: lightgreen">\n'
                    '<h1>Lista de empresas proveedoras:</h2>\n'
                    '\n'
                    )

        
        
        # Iteramos sobre la informacion del API para obtener la lista
        for i in range(len(info["results"])):
            id = info["results"][i]["id"]

            
            # Comprobamos que los datos que queremos mostrar existen, sino mandamos un mensaje de desconocido
            if info["results"][i]["openfda"]:
                nombre = info["results"][i]["openfda"]["generic_name"][0]
                empresa = info["results"][i]["openfda"]["manufacturer_name"][0]
            else:
                nombre = 'Desconocido'
                empresa = 'Desconocida'

            # Añadimos la informacion de cada elemento al codigo html
            info_api += '<li type="square"><td> Nombre del medicamento: ' + nombre + ' </td></li>\n'
            info_api += '<li type="square"><td> Identificador del medicamento: ' + id + '</td></li>\n'
            info_api += '<li type="square"><td> Empresa proveedora del medicamento: ' + empresa + '</td></li>\n'
            info_api += '<br>'

        return info_api

    
    
    def get_searchCompany(self, limit, search, name):    # Diseñamos el contenido referente a la busqueda de medicamentos en 
                                                         # Funcion de su fabricante
        info = self.get_conection(limit, search, name)

        info_api = (' <!DOCTYPE html>\n'
                    '<html lang="es">\n'
                    '<head>\n'
                    '    <meta charset="UTF-8">\n'
                    '    <title>API</title>\n'
                    '</head>\n'
                    '<body style="background:violet">\n'
                    '<h1>Medicamentos encontrados:</h2>\n'
                    '\n'
                    )
        
        
        # Iteramos sobre la informacion del API para obtener la lista
        for i in range(len(info["results"])):
            id = info["results"][i]["id"]
            
            
            # Comprobamos que los datos que queremos mostrar existen, sino mandamos un mensaje de desconocido
            if info["results"][i]["openfda"]:
                nombre = info["results"][i]["openfda"]["generic_name"][0]
            else:
                nombre = 'Desconocido'

            # Añadimos la informacion de cada elemento al codigo html
            info_api += '<li type="square"><td>' + nombre + ' (id: ' + id + ') </td></li>\n'

        return info_api

    
    
    def get_listWarnings(self, limit):    # Diseñamos el contenido referente al listado de usos y advertencias de los medicamentos
        info = self.get_conection(limit)

        info_api = (' <!DOCTYPE html>\n'
                    '<html lang="es">\n'
                    '<head>\n'
                    '    <meta charset="UTF-8">\n'
                    '    <title>API</title>\n'
                    '</head>\n'
                    '<body style="background: yellow">\n'
                    '<h1>Lista de usos y precauciones:</h2>\n'
                    '\n'
                    )
        
        
        # Iteramos sobre la informacion del API para obtener la lista
        for i in range(len(info["results"])):
            id = info["results"][i]["id"]
            
            
            # Comprobamos que los datos que queremos mostrar existen, sino mandamos un mensaje de desconocido
            if "purpose" in info["results"][i].keys():
                usos = info["results"][i]['purpose'][0]
            else:
                usos = 'Desconocido'

            if "warnings" in info["results"][i].keys():
                precauciones = info["results"][i]['warnings'][0]
            else:
                precauciones ='Desconocido'

            if info["results"][i]["openfda"]:
                nombre = info["results"][i]["openfda"]["generic_name"][0]
            else:
                nombre = 'Desconocido'

            # Añadimos la informacion de cada elemento al codigo html
            info_api += '<li type="square"><td> Nombre del medicamento: ' + nombre + ' </td></li>\n'
            info_api += '<li type="square"><td> Identificador del medicamento: ' + id + '</td></li>\n'
            info_api += '<li type="square"><td> Utilidad del medicamento: ' + usos + '</td></li>\n'
            info_api += '<li type="square"><td> Precauciones antes de tomar el medicamento: ' + precauciones + '</td></li>\n'
            info_api += '<br>'

        return info_api
    
    

    
    def do_GET(self):    # Este metodo es el principal, con el llamamos al resto de metodos y nos ayuda a obtener la informacion requerida.
                        # Almacena la informacion en self.path
        path =self.path
        if '&' in path:
            path = path.replace('&', '?')    # Sustituimos estos caracteres para simplificar
                                                  # La busqueda de informacion
                
        if '%3C' in path:    #Eliminamos los caracteres que aparecen como consecuencia de los signos <>
            path=path.replace("%3C", "").replace("%3E", "") 
            print(path)                                     


        if '?' in path:    # Si encontramos este caracter en la url, hemos añadido algun parametro
            parametros = path.split("?")[1:]    # Parametros de busqueda, por ejemplo un limit
            solicitud = path.split("?")[0]    # Señala el recurso que queremos
            print("Request:", solicitud)

            
            # Iteramos sobre la cantidad de parametros 
            for i in range(len(parametros)):
                parameters = parametros[i].split("=")    # Separa los parametros
                if parameters[0] == 'limit':    # Si es un limite, almacena el valor que se le asigna
                    limit = parameters[1]
                    print("Number:", limit)

                else:    # En caso de que no se haga referencia al limite, le añadimos un valor por defecto
                    limit = 10

                if parameters[0] == "company":    # Igual que con el limite pero con el dato del fabricante
                    name = parameters[1]
                    search = "manufacturer_name"
                    print("Name:", name)
                    print("Search:", search)

                if parameters[0] == 'active_ingredient':    # Sucede igual con el dato del principio activo
                    name = parameters[1]
                    search = parameters[0]
                    print("Name:", name)
                    print("Search:", search)


        else:    # Valor por defecto en caso de que no hayan parametros
            limit = 10
            solicitud = ""

        print('Numero de recursos solicitados:', limit)

        
        
        if path == "/" or path == "":    # Si no hay ningun parametro 
            vista = self.get_indice()   # Te muestra la pagina del formulario (html indice)
            self.send_response(200)    # Status
            self.send_header('Content-type', 'text/html')    # Informamos que el texto devuelto sera html
            self.end_headers()
            self.wfile.write(bytes(vista, "utf8"))    # Enviamos el mensaje


        elif path == '/listDrugs' or self.path == '/listDrugs?limit={}'.format(limit):    # Si el parametro hace referencia 
                                                                                         # Al listado de medicamentos
            vista = self.get_listDrugs(limit)    # Nos muestra el contenido html diseñado en el metodo listDrugs
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(vista, "utf8"))

        elif solicitud == "/searchDrug":    # Si nos encontramos con la busqueda de medicamentos
            vista = self.get_searchDrug(limit, search, name)    # Nos muestra la informacion del metodo SearchDrug
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(vista, "utf8"))

        elif path == '/listCompanies' or path == '/listCompanies?limit={}'.format(limit):    
            vista = self.get_listCompanies(limit)    # Contenido html del listado de los fabricantes
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(vista, "utf8"))

        elif solicitud == "/searchCompany":
            vista = self.get_searchCompany(limit, search, name)    # Busqueda de medicamentos en funcion de su fabricante
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(vista, "utf8"))

        elif path == '/listWarnings' or path == '/listWarnings?limit={}'.format(limit):
            vista = self.get_listWarnings(limit)    # Lista de usos y advertencias de los medicamentos
            self.send_response(200)
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(bytes(vista, "utf8"))


        else:    # Si no se identifica la peticion se devuelve error
            self.send_error(404)
            self.send_header('Content-type', 'text/plain; charset=utf-8')
            self.end_headers()
            self.wfile.write("I don't know '{}'.".format(path).encode())

        print('List sent')

        return



# Establecemos nuestra propia clase como manejador
Handler = TestHTTPRequestHandler

httpd = socketserver.TCPServer(("", PORT), Handler)
print("Serving at port", PORT)

try:
    httpd.serve_forever()  # Permite que el servidor no se cierre y este disponible para una nueva busqueda
except KeyboardInterrupt:
    print("")
    print("Interrumpido por el usuario")

print("")
print("Servidor parado")
