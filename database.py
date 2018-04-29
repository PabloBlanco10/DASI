import MySQLdb
import requests
import re


def connection():
    conn = MySQLdb.connect(host= "localhost",
                           user="root",
                           passwd="",
                           db="eatbot")
                           
    return conn

def insertarUsuario(listaUsuario):

    conn = connection()
    x = conn.cursor()

    for usuario in listaUsuario:

        idUsuario = usuario[0]
        nombreUsuario = usuario[1]

        query = "INSERT IGNORE INTO Usuario (idUsuario, nombreUsuario) VALUES ('{0}', '{1}');".format(usuario[0], usuario[1])

        try:
            x.execute(query)
        except MySQLdb.ProgrammingError:
            print("La siguiente query ha fallado:%s" % query + '\n')
        print("El usuario " + str(nombreUsuario) + " ha sido añadido")

    conn.commit()
    x.close()
    conn.close()

def cargarPedido(listaUsuario):

    conn = connection()
    x = conn.cursor()

    for usuario in listaUsuario:

        idUsuario = usuario[0]
        nombreUsuario = usuario[1]

        query = "INSERT IGNORE INTO Pedido (idUsuario, nombreUsuario) VALUES ('{0}', '{1}');".format(usuario[0], usuario[1])

        try:
            x.execute(query)
        except MySQLdb.ProgrammingError:
            print("La siguiente query ha fallado:%s" % query + '\n')
        print("El usuario " + str(nombreUsuario) + " ha sido añadido")

    conn.commit()
    x.close()
    conn.close()

def cargarProductosBBDD(listaProductos):
    conn = connection()
    x = conn.cursor()

    for producto in listaProductos:

        query = "INSERT IGNORE INTO Producto (nombreProducto) VALUES ('{0}');" .format(producto)
        
        try:
            x.execute(query)
        except MySQLdb.ProgrammingError:
            print("La siguiente query ha fallado:%s" % query + '\n')
        print("El producto " + str(producto) + " ha sido añadido")

    conn.commit()
    x.close()
    conn.close()


def cargarRestaurantesBBDD(listaRestaurantes):
    conn = connection()
    x = conn.cursor()

    for restaurante in listaRestaurantes:
        nombreRestaurante = restaurante[0]
        tipoRestaurante = restaurante[1]

        query = "INSERT IGNORE INTO Restaurante (nombreRestaurante, tipoRestaurante) VALUES ('{0}', '{1}');".format(restaurante[0], restaurante[1])

        try:
            x.execute(query)
        except MySQLdb.ProgrammingError:
            print("La siguiente query ha fallado:%s" % query + '\n')
        print("El restaurante " + str(restaurante) + " ha sido añadido")

    conn.commit()
    x.close()
    conn.close()

def cargarRestaurantesProductosBBDD(listaProductosRestaurantes):
    conn = connection()
    x = conn.cursor()

    for restauranteProducto in listaProductosRestaurantes:

        query = "INSERT IGNORE INTO RestauranteProducto (idRestaurante, idProducto) VALUES ('{0}', '{1}');".format(
            restauranteProducto[0], restauranteProducto[1])

        try:
            x.execute(query)
        except MySQLdb.ProgrammingError:
            print("La siguiente query ha fallado:%s" % query + '\n')
        print("El restaurante " + str(restauranteProducto) + " ha sido añadido")

    conn.commit()
    x.close()
    conn.close()

def borrarBBDD():
    conn = connection()
    x = conn.cursor()
    query = "DROP TABLE IF EXISTS RestauranteProducto;" # IF EXISTS(SELECT * FROM  dbo.Producto) DROP TABLE Producto; IF EXISTS(SELECT * FROM  dbo.Restaurante) DROP TABLE Restaurante;"

    try:
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("Fallo:%s" % query + '\n')

    conn.commit()

    query = "DROP TABLE IF EXISTS Producto;"  # IF EXISTS(SELECT * FROM  dbo.Producto) DROP TABLE Producto; IF EXISTS(SELECT * FROM  dbo.Restaurante) DROP TABLE Restaurante;"

    try:
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("Fallo:%s" % query + '\n')

    conn.commit()

    query = "DROP TABLE IF EXISTS Restaurante;"  # IF EXISTS(SELECT * FROM  dbo.Producto) DROP TABLE Producto; IF EXISTS(SELECT * FROM  dbo.Restaurante) DROP TABLE Restaurante;"

    try:
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("Fallo:%s" % query + '\n')
    print("Tablas borradas")

    conn.commit()

    query = "DROP TABLE IF EXISTS Usuario;"  # IF EXISTS(SELECT * FROM  dbo.Producto) DROP TABLE Producto; IF EXISTS(SELECT * FROM  dbo.Restaurante) DROP TABLE Restaurante;"

    try:
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("Fallo:%s" % query + '\n')
    print("Tablas borradas")

    conn.commit()

    query = "DROP TABLE IF EXISTS Pedido;"  # IF EXISTS(SELECT * FROM  dbo.Producto) DROP TABLE Producto; IF EXISTS(SELECT * FROM  dbo.Restaurante) DROP TABLE Restaurante;"

    try:
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("Fallo:%s" % query + '\n')
    print("Tablas borradas")

    conn.commit()

    query = "DROP TABLE IF EXISTS PedidoProducto;"  # IF EXISTS(SELECT * FROM  dbo.Producto) DROP TABLE Producto; IF EXISTS(SELECT * FROM  dbo.Restaurante) DROP TABLE Restaurante;"

    try:
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("Fallo:%s" % query + '\n')
    print("Tablas borradas")

    conn.commit()

    x.close()
    conn.close()


def crearTablas():
    conn = connection()
    x = conn.cursor()

    query = "CREATE TABLE Producto(idProducto int NOT NULL AUTO_INCREMENT,nombreProducto varchar(100), UNIQUE(nombreProducto),PRIMARY KEY (idProducto)) ; "

    try:
        x.execute(query)
    except MySQLdb.Warning:
        print("Fallo:%s" % query + '\n')

    conn.commit()

    query = "CREATE TABLE Restaurante(idRestaurante int NOT NULL AUTO_INCREMENT,nombreRestaurante varchar(100), tipoRestaurante varchar(100), PRIMARY KEY (idRestaurante),UNIQUE(nombreRestaurante)) ; "

    try:
        x.execute(query)
    except MySQLdb.Warning:
        print("Fallo:%s" % query + '\n')

    conn.commit()

    query = "CREATE TABLE RestauranteProducto(idRestaurante int, idProducto int, PRIMARY KEY (idRestaurante, idProducto),FOREIGN KEY (idRestaurante) REFERENCES Restaurante (idRestaurante),FOREIGN KEY (idProducto) REFERENCES Producto (idProducto)) ;"

    try:
        x.execute(query)
    except MySQLdb.Warning:
        print("Fallo:%s" % query + '\n')
    print("Tablas creadas")

    conn.commit()

    query = "CREATE TABLE Usuario( idUsuario int, nombreUsuario varchar(100), PRIMARY KEY(idUsuario))";

    try:
        x.execute(query)
    except MySQLdb.Warning:
        print("Fallo:%s" % query + '\n')
    print("Tablas creadas")

    conn.commit()

    query = "CREATE TABLE Pedido( idPedido int NOT NULL AUTO_INCREMENT, idUsuario int , idRestaurante int PRIMARY KEY(idPedido), FOREIGN KEY (idRestaurante) REFERENCES Restaurante (idRestaurante))" \
            "FOREIGN KEY (idUsuario) REFERENCES Usuario (idUsuario)";

    try:
        x.execute(query)
    except MySQLdb.Warning:
        print("Fallo:%s" % query + '\n')
    print("Tablas creadas")

    conn.commit()

    query = "CREATE TABLE PedidoProducto( idPedido int, idProducto int, PRIMARY KEY(idPedido, idProducto), FOREIGN KEY (idPedido) REFERENCES Pedido (idPedido))" \
            "FOREIGN KEY (idProducto) REFERENCES Producto (idProducto)";

    try:
        x.execute(query)
    except MySQLdb.Warning:
        print("Fallo:%s" % query + '\n')
    print("Tablas creadas")

    conn.commit()

    x.close()
    conn.close()

def buscarTiposRestaurante():
    conn = connection()
    x = conn.cursor()
    listaTiposRestaurante = []

    query = "SELECT DISTINCT tipoRestaurante FROM Restaurante ;".format(str)

    try:
        x.execute(query)

    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')

    for line in x:
        listaTiposRestaurante.append(line[0])
    conn.commit()
    x.close()
    conn.close()
    return listaTiposRestaurante


def buscarRestaurantesDelTipo(tipoRestaurante):
    conn = connection()
    x = conn.cursor()
    listaRestaurantes = []
    escaped = re.escape(tipoRestaurante)

    query = "SELECT DISTINCT nombreRestaurante FROM Restaurante WHERE tipoRestaurante = '{0}' ;".format(escaped)

    try:
        x.execute(query)

    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')

    for line in x:
        listaRestaurantes.append(line[0])
    conn.commit()
    x.close()
    conn.close()
    return listaRestaurantes

def buscarProductosDelRestaurante(nombreRestaurante):
    conn = connection()
    x = conn.cursor()
    listaProductos = []
    escaped = re.escape(nombreRestaurante)

    query = "SELECT DISTINCT nombreProducto FROM Producto NATURAL JOIN RestauranteProducto NATURAL JOIN" \
            " Restaurante WHERE nombreRestaurante = '{0}' ;".format(escaped)

    try:
        x.execute(query)

    except MySQLdb.ProgrammingError:
        print("La siguiente query ha fallado: " + query + '\n')

    for line in x:
        listaProductos.append(line[0])
    conn.commit()
    x.close()
    conn.close()
    return listaProductos



# def cargarRestaurantesProductosBBDD(listaProductosRestaurantes):
#     conn = connection()
#     x = conn.cursor()
#
#     for restauranteProducto in listaProductosRestaurantes:
#         nombreRestaurante = restauranteProducto[0]
#         nombreProducto = restauranteProducto[1]
#
#         x.execute("SELECT idRestaurante FROM Restaurante WHERE nombreRestaurante = '{0}' ;".format(restauranteProducto[0]))
#
#         idRestaurante = rows = x.fetchall()[0][0]
#         print(idRestaurante)
#
#         x.execute("SELECT idProducto FROM Producto WHERE nombreProducto = '{0}' ;".format(restauranteProducto[1]))
#
#         idProducto = rows = x.fetchall()[0][0]
#         print(idProducto)
#
#         query = "INSERT IGNORE INTO RestauranteProducto (idRestaurante, nombreRestaurante, idProducto, nombreProducto) VALUES ('{0}', '{1}', '{2}', '{3}');".format(
#             idRestaurante, restauranteProducto[0], idProducto, restauranteProducto[1])
#
#         try:
#             x.execute(query)
#         except MySQLdb.ProgrammingError:
#             print("La siguiente query ha fallado:%s" % query + '\n')
#         print("El restaurante " + str(restauranteProducto) + " ha sido añadido")
#
#     conn.commit()
#     x.close()
#     conn.close()




