import MySQLdb

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
            print(query)
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

        query = "INSERT IGNORE INTO Restaurante (nombreRestaurante) VALUES ('{0}');".format(restaurante)

        try:
            print(query)
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
    query = "DROP TABLE RestauranteProducto; DROP TABLE Producto; DROP TABLE Restaurante;"

    try:
        print(query)
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

    query = "CREATE TABLE Producto(idProducto int NOT NULL AUTO_INCREMENT,nombreProducto varchar(100), UNIQUE(nombreProducto),PRIMARY KEY (idProducto)) ; CREATE TABLE Restaurante(idRestaurante int NOT NULL AUTO_INCREMENT,nombreRestaurante varchar(100),PRIMARY KEY (idRestaurante),UNIQUE(nombreRestaurante)) ;CREATE TABLE RestauranteProducto(idRestaurante int,idProducto int,PRIMARY KEY (idRestaurante, idProducto),FOREIGN KEY (idRestaurante) REFERENCES Restaurante (idRestaurante),FOREIGN KEY (idProducto) REFERENCES Producto (idProducto)) ;"

    try:
        print(query)
        x.execute(query)
    except MySQLdb.ProgrammingError:
        print("Fallo:%s" % query + '\n')
    print("Tablas creadas")

    conn.commit()
    x.close()
    conn.close()












