import MySQLdb
import requests
import re


def connection():
    conn = MySQLdb.connect(host= "localhost",
                           user="root",
                           passwd="",
                           db="eatbot")
                           
    return conn

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

    query = "CREATE TABLE RestauranteProducto(idRestaurante int,idProducto int,PRIMARY KEY (idRestaurante, idProducto),FOREIGN KEY (idRestaurante) REFERENCES Restaurante (idRestaurante),FOREIGN KEY (idProducto) REFERENCES Producto (idProducto)) ;"

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








