import random
import psycopg2
from datetime import datetime, timedelta

def obtener_datos():
    usuario = input('Ingresar usuario de postgres: ')
    contrasena = input(f'Ingresar contraseña de {usuario}: ')
    nombre_db = input('Nombre de la base de datos: ')
    return usuario, contrasena, nombre_db

def connect(usuario, contrasena, nombre_bd):
    try:
        connection = psycopg2.connect(
                host = "localhost",
                user = usuario,
                password = contrasena,
                database = nombre_bd)
        
        print('Conexión exitosa')
        return connection
    
    except psycopg2.Error as e:
        print("Error al conectar a la base de datos:", e)
        return None

usuario, contraseña, nombre_bd = obtener_datos()                    #nombre y usuario de la base de datos
connection = connect(usuario, contraseña, nombre_bd)                #se crea la conexion a la base de datos
    
cursor = connection.cursor()
random.seed(1)

if connection is None:
    print('No se pudo conectar a la base de datos')
    exit()

def crear_tablas():
        
    #Tabla 1 - Clientes
    cursor.execute("""
              CREATE TABLE clientes (
                rut_cliente VARCHAR(12) PRIMARY KEY,
                nombre_cliente VARCHAR(50) NOT NULL,
                correo VARCHAR(50) NOT NULL,
                numero_personas INT NOT NULL CHECK (numero_personas > 0),
                telefono VARCHAR(20) NOT NULL UNIQUE);
            """)

    #Tabla 2 - Empleados
    cursor.execute("""
              CREATE TABLE empleados (
                rut_empleado VARCHAR(12) PRIMARY KEY,
                nombre_empleado VARCHAR(50) NOT NULL,
                cargo VARCHAR(50) NOT NULL,
                contacto VARCHAR(20) NOT NULL);
            """)
    
    #Tabla 3 - Habitaciones
    cursor.execute("""
              CREATE TABLE habitaciones (
                numero SERIAL PRIMARY KEY,
                estado VARCHAR(30) NOT NULL,
                cantidad_camas INT CHECK (cantidad_camas > 0),
                precio INT NOT NULL CHECK (precio > 0));
            """)

    #Tabla 4 - Reservas
    cursor.execute("""
              CREATE TABLE reservas (
                id_reserva SERIAL PRIMARY KEY,
                habitacion_asociada INT NOT NULL,
                cliente_asociado VARCHAR(12) NOT NULL,
                estado VARCHAR(30) NOT NULL,
                fecha_llegada DATE NOT NULL,
                fecha_ida DATE NOT NULL,
                FOREIGN KEY (habitacion_asociada) REFERENCES habitaciones(numero),                                 
                FOREIGN KEY (cliente_asociado) REFERENCES clientes(rut_cliente),
                CHECK (fecha_ida > fecha_llegada) );
            """)

    #Tabla 5 - Servicios extras
    cursor.execute("""
              CREATE TABLE servicios_extras (
                id_servicio SERIAL PRIMARY KEY,
                nombre_servicio VARCHAR(50) NOT NULL,
                precio INT NOT NULL CHECK (precio > 0),
                descripcion VARCHAR(100));
            """)

    connection.commit() 
    print('Tablas creadas correctamente!')
            
def tabla_clientes():

    ruts = ["17.107.374-K", "11.235.488-3", "21.590.469-5", "6.400.944-3", "13.948.731-1", "8.826.640-4", "11.319.041-8", "13.444.517-3", 
            "11.576.243-5", "24.407.348-4", "19.941.955-2", "8.784.970-8", "8.027.100-K", "13.658.243-7", "5.023.916-0", "11.285.585-8", 
            "9.762.112-8", "5.065.712-4", "6.050.888-7", "19.453.599-6", "20.334.250-0", "18.198.266-7", "9.710.797-1", "19.309.693-K", 
            "14.052.417-4", "17.912.088-7", "16.901.303-9", "19.545.204-0", "14.759.587-5","19.529.864-5"]

    nombres = ['Juan', 'María', 'Pedro', 'Ana', 'Carlos', 'Laura', 'Luis', 'Sofía', 'Javier', 'Elena',
                'Miguel', 'Carmen', 'Diego', 'Isabel', 'Pablo', 'Lucía', 'José', 'Marta', 'Fernando', 'Clara',
                'Antonio', 'Valentina', 'Daniel', 'Raquel', 'Manuel', 'Paula', 'Jorge', 'Silvia', 'Rubén', 'Natalia']

    apellidos = ['García', 'Martínez', 'López', 'González', 'Rodríguez', 'Hernández', 'Pérez', 'Sánchez', 'Romero', 'Díaz',
                'Martín', 'Jiménez', 'Ruiz', 'Torres', 'Fernández', 'Gómez', 'Vázquez', 'Serrano', 'Ramos', 'Molina',
                'Ortega', 'Delgado', 'Castro', 'Navarro', 'Guerrero', 'Flores', 'Santiago', 'Morales', 'Iglesias', 'León']
    
    numeros = ['123456789', '890123456', '543210987', '654321098', '432109876', '876543210', '789012345', '765432109', 
               '456789012', '678901234', '987654321', '102345678', '234567890', '321098765', '567890123', '210987654', 
               '901234567', '876543211', '543210981', '321092765', '789012342', '432109871', '985654321', '654321092', 
               '890123452', '456789212', '678101234', '765432106', '234597890', '210987454']
 

    #AGREGAR DATOS A LA TABLA CLIENTE
    for i in range(30):  
        
        rut = ruts[i]                                                                                       #rut_cliente
        
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        nombre_completo = f'{nombre} {apellido}'                                                            #nombre_cliente                                                 
        
        correo = f'{nombre.lower()}.{apellido.lower()}@gmail.com'                                           #correo                                 
        
        cantidad_personas = random.randint(1,5)                                                             #numero_personas                                                
        
        telefono = numeros[i]                                                                               #telefono                      
        
        cursor.execute('''INSERT INTO clientes (rut_cliente, nombre_cliente, correo, numero_personas, telefono)
                            VALUES (%s, %s, %s, %s, %s);
                            ''', (rut, nombre_completo, correo, cantidad_personas, telefono))
        
    connection.commit()
    print('Datos agregados a la tabla clientes de manera exitosa')        

def tabla_empleados():
    
    ruts =["8164980-4", "18646317-K", "18786603-0", "13006624-0", "7980182-8",
            "22732693-K", "7796974-8", "16670800-1", "23814595-3", "17683813-2",
            "14695325-5", "21603177-6", "6244117-8", "13814737-1", "24536048-7"]
        
    nombres = ['Juan', 'María', 'Pedro', 'Ana', 'Carlos', 'Laura', 'Luis', 'Sofía', 'Javier', 'Elena',
                'Miguel', 'Carmen', 'Diego', 'Isabel', 'Pablo', 'Lucía', 'José', 'Marta', 'Fernando', 'Clara',
                'Antonio', 'Valentina', 'Daniel', 'Raquel', 'Manuel', 'Paula', 'Jorge', 'Silvia', 'Rubén', 'Natalia']

    apellidos = ['García', 'Martínez', 'López', 'González', 'Rodríguez', 'Hernández', 'Pérez', 'Sánchez', 'Romero', 'Díaz',
                'Martín', 'Jiménez', 'Ruiz', 'Torres', 'Fernández', 'Gómez', 'Vázquez', 'Serrano', 'Ramos', 'Molina',
                'Ortega', 'Delgado', 'Castro', 'Navarro', 'Guerrero', 'Flores', 'Santiago', 'Morales', 'Iglesias', 'León']

    cargos = ['Recepcionista', 'Cocinero', 'Lavandero', 'Encargado de Reservas', 'Encargado de Seguridad', 'Auxiliar de Limpieza',
              'Recepcionista', 'Cocinero', 'Lavandero', 'Encargado de Reservas', 'Encargado de Seguridad', 'Auxiliar de Limpieza',
              'Cocinero', 'Encargado de Reservas', 'Auxiliar de Limpieza']

    numeros_telefonos = ['555-123-4567', '555-234-5678', '555-345-6789', '555-456-7890', '555-567-8901',
                         '555-678-9012', '555-789-0123', '555-890-1234', '555-901-2345', '555-012-3456',
                         '555-111-2233', '555-222-3344', '555-333-4455', '555-444-5566', '555-555-6677']
        
    random.shuffle(numeros_telefonos)
        
    for i in range(15):
            
        rut = ruts[i]                                                                       #rut_empleado
            
        nombre = random.choice(nombres)
        apellido = random.choice(apellidos)
        nombre_completo = f'{nombre} {apellido}'                                            #nombre_empleado         
            
        cargo = cargos[i]                                                                   #cargo
            
        telefono = numeros_telefonos[i]                                                     #telefono
        
        cursor.execute("""INSERT INTO empleados (rut_empleado, nombre_empleado, cargo, contacto)
                            VALUES (%s, %s, %s, %s);
                            """, (rut, nombre_completo, cargo, telefono))
            
    connection.commit()
    print('Datos agregados a la tabla empleados de manera exitosa')    

def tabla_habitaciones():
    
    estados = ["Disponible", "Ocupada", "Reservada", "Limpieza en Proceso", "Mantenimiento", "No Disponible"]    
        
    for i in range(30):
        
        estado_habitacion = random.choice(estados)                          #estado
        
        camas = random.randint(1,5)                                         #cantidad_camas

        if camas == 1:                                                      #precio
            precio = 25000                                                  
        elif camas == 2:
            precio = 40000
        elif camas == 3:
            precio = 65000
        elif camas == 4:
            precio = 85000
        else:
            precio = 100000
        
        cursor.execute("""INSERT INTO habitaciones (estado, cantidad_camas, precio)
                            VALUES ( %s, %s, %s);
                            """, (estado_habitacion, camas, precio))
        
    connection.commit()
    print('Datos agregados a la tabla habitaciones de manera exitosa')   

def tabla_reservas():
    #Obtener numero de las habitaciones
    cursor.execute('SELECT numero FROM habitaciones')
    numeros = cursor.fetchall()
    habitaciones = []                                   #lista con los numeros de las habitaciones

    for numero in numeros:
        habitaciones.append(numero[0])
        
    #Obtener rut de los clientes
    cursor.execute('SELECT rut_cliente FROM clientes')
    rut = cursor.fetchall()
    clientes = []                                       #lista con los rut de los clientes

    for rut in rut:
        clientes.append(rut[0])

    estados = ["confirmada", "pendiente", "cancelada", "confirmada", 'deshabilitada', 'ocupada']

    for i in range(30):
        
        estado = random.choice(estados)                                                                             #estado
        
        start_date = datetime(2024, 5, 20)                                  #year - month - day
        end_date = datetime(2024, 12, 31)
        random_date = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
        fecha_llegada = random_date.strftime("%d/%m/%Y")                                                            #fecha_llegada
        random_date_llegada = datetime.strptime(fecha_llegada, "%d/%m/%Y")

        dias_estancia = random.randint(1, 30)
        fecha_ida = random_date_llegada + timedelta(days=dias_estancia)
        fecha_ida_formateada = fecha_ida.strftime("%d/%m/%Y")                                                       #fecha_ida

        habitacion = habitaciones[i]                                                                                #habitacion_asociada

        id_cliente = clientes[i]                                                                                    #cliente_asociado

        cursor.execute("""INSERT INTO reservas (habitacion_asociada, cliente_asociado, estado, fecha_llegada, fecha_ida)
                        VALUES (%s, %s, %s, %s, %s);
                        """, (habitacion, id_cliente, estado, fecha_llegada, fecha_ida_formateada))
        
    connection.commit()
    print('Datos agregados a la tabla reservas de manera exitosa')   

def tabla_servicios_extras():
    
    servicios = ["Desayuno", "Servicio de habitaciones 24 horas", "Spa y masajes", "Gimnasio", "Piscina", 
                 "Conexión Wi-Fi", "Estacionamiento", "Restaurante gourmet", "Bar en la azotea", "Mini bar",] 

    precios = {'Desayuno': 15000, 
            'Servicio de habitaciones 24 horas': 30000,
            'Spa y masajes': 25000,
            'Gimnasio': 10000,
            'Piscina': 15000,
            'Conexión Wi-Fi': 5000,
            'Estacionamiento': 15000,
            'Restaurante gourmet': 45000,
            'Bar en la azotea': 35000,
            'Mini bar': 10000}

    descripcion = {
        'Desayuno': "Desayuno buffet con variedad de productos frescos y de temporada",
        'Servicio de habitaciones 24 horas': "Servicio de habitaciones 24 horas con atención personalizada y atención al detalle",
        'Spa y masajes': "Spa y masajes con productos de alta calidad y atención personalizada",
        'Gimnasio': "Gimnasio con equipamiento de alta calidad y atención personalizada",
        'Piscina': "Piscina con atención personalizada y atención al detalle",
        'Conexión Wi-Fi': "Conexión Wi-Fi con velocidad de alta calidad y atención personalizada",
        'Estacionamiento': "Estacionamiento con atención personalizada y atención al detalle",
        'Restaurante gourmet': "Restaurante gourmet con atención personalizada y atención al detalle",
        'Bar en la azotea': "Bar en la azotea con atención personalizada y atención al detalle",
        'Mini bar': "Mini bar con atención personalizada y atención al detalle"}

    for i in range(len(servicios)):
        nombre_servicio = servicios[i]
        
        precio_servicio = precios[nombre_servicio]
        
        descripcion_servicio = descripcion[nombre_servicio]
        
        cursor.execute("""INSERT INTO servicios_extras (nombre_servicio, precio, descripcion)
                            VALUES (%s, %s, %s);
                            """, (nombre_servicio, precio_servicio, descripcion_servicio))
        
    connection.commit()
    print('Datos agregados a la tabla reservas de manera exitosa')   

def cerrar_conexiones()          :
    # Cerrar cursor y conexión al final del código
    if cursor:
        cursor.close()
    if connection:
        connection.close()
          
def main():
    
    crear_tablas()
    tabla_clientes()
    tabla_empleados()
    tabla_habitaciones()
    tabla_reservas()
    tabla_servicios_extras()
    cerrar_conexiones() 
    
if __name__ == '__main__':
    main()