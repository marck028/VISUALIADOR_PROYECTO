------ PARA SUCURSAL
CREATE TABLE Dim_Paises (
    id_pais SERIAL PRIMARY KEY,
    nombre_pais VARCHAR(50) NOT NULL
);

CREATE TABLE Dim_Ciudades (
    id_ciudad SERIAL PRIMARY KEY,
    nombre_ciudad VARCHAR(50) NOT NULL,
    id_pais INT NOT NULL,
    FOREIGN KEY (id_pais) REFERENCES Dim_Paises(id_pais)
);

CREATE TABLE Dim_Ubicacion_Sucursales (
    id_ubicacion SERIAL PRIMARY KEY,
    id_ciudad INT NOT NULL,
    latitud DECIMAL(9, 6),
    longitud DECIMAL(9, 6),
    descripcion VARCHAR(255),  -- Nueva columna para detalles de la ubicación
    FOREIGN KEY (id_ciudad) REFERENCES Dim_Ciudades(id_ciudad)
);

CREATE TABLE Dim_Sucursales (
    id_sucursal SERIAL PRIMARY KEY,
    id_ubicacion INT NOT NULL,
    nombre VARCHAR(50) NOT NULL,
    direccion VARCHAR(255) NOT NULL,
    cajas INT NOT NULL,
    FOREIGN KEY (id_ubicacion) REFERENCES Dim_Ubicacion_Sucursales(id_ubicacion)
);

------ PARA PRODUCTO
CREATE TABLE Dim_Categorias (
    id_categoria SERIAL PRIMARY KEY,
    nombre VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255)
);

CREATE TABLE Dim_Subcategorias (
    id_subcategoria INT PRIMARY KEY,
    id_categoria INT NOT NULL,
    nombre_subcategoria VARCHAR(50) NOT NULL,
    descripcion VARCHAR(255),
    FOREIGN KEY (id_categoria) REFERENCES Dim_Categorias(id_categoria)
);

CREATE TABLE Dim_Productos (
    id_producto SERIAL PRIMARY KEY,
    id_subcategoria INT NOT NULL,
    nombre VARCHAR(100) NOT NULL,
    precio DECIMAL(10, 2) NOT NULL,
    perecedero BOOLEAN NOT NULL,
    FOREIGN KEY (id_subcategoria) REFERENCES Dim_Subcategorias(id_subcategoria)
);

------- PARA CLIENTE
CREATE TABLE Dim_Genero (
    id_genero SERIAL PRIMARY KEY,
    genero VARCHAR(20) NOT NULL
);

CREATE TABLE Dim_Clientes (
    id_cliente SERIAL PRIMARY KEY,
    nombre VARCHAR(100) NOT NULL,
    apellido VARCHAR(100) NOT NULL,
    email VARCHAR(100),
    telefono VARCHAR(20),
    id_genero INT,
    FOREIGN KEY (id_genero) REFERENCES Dim_Genero(id_genero)
);

---- PARA FECHA
CREATE TABLE Dim_Fecha (
    id_fecha DATE PRIMARY KEY,
    dia INT NOT NULL,
    mes INT NOT NULL,
    anio INT NOT NULL,
    dia_semana VARCHAR(20),
    trimestre INT
);

------ PARA PAGO
CREATE TABLE Dim_Metodos_Pago (
    id_metodo_pago SERIAL PRIMARY KEY,
    metodo_pago VARCHAR(50) NOT NULL UNIQUE -- Métodos de pago disponibles
);

CREATE TABLE Hechos_Ventas (
    id_venta SERIAL PRIMARY KEY,
    id_sucursal INT NOT NULL,
    id_producto INT NOT NULL,
    id_cliente INT NOT NULL,
    id_fecha DATE NOT NULL,
    id_metodo_pago INT NOT NULL,
    cantidad INT NOT NULL,
    total DECIMAL(10, 2) NOT NULL,
    FOREIGN KEY (id_sucursal) REFERENCES Dim_Sucursales(id_sucursal),
    FOREIGN KEY (id_producto) REFERENCES Dim_Productos(id_producto),
    FOREIGN KEY (id_cliente) REFERENCES Dim_Clientes(id_cliente),
    FOREIGN KEY (id_fecha) REFERENCES Dim_Fecha(id_fecha),
    FOREIGN KEY (id_metodo_pago) REFERENCES Dim_Metodos_Pago(id_metodo_pago)
); 


-- Insertar país
INSERT INTO Dim_Paises (nombre_pais) VALUES ('Bolivia');

-- Insertar ciudades
INSERT INTO Dim_Ciudades (nombre_ciudad, id_pais) VALUES
('Cochabamba', 1),
('La Paz', 1),
('Santa Cruz', 1);

-- Insertar ubicaciones de sucursales con descripción
INSERT INTO Dim_Ubicacion_Sucursales (id_ciudad, latitud, longitud, descripcion) VALUES
(1, -17.3964, -66.1575, 'Centro Histórico, Cochabamba'),  -- Cochabamba Centro
(1, -17.3700, -66.1550, 'Zona Sur, Cochabamba'),           -- Cochabamba Sur
(2, -16.5000, -68.1193, 'Centro Histórico, La Paz'),       -- La Paz Centro
(2, -16.5200, -68.1400, 'Zona Sur, La Paz'),               -- La Paz Sur
(3, -17.7845, -63.1820, 'Centro Histórico, Santa Cruz'),    -- Santa Cruz Centro
(3, -17.8000, -63.1800, 'Zona Norte, Santa Cruz');         -- Santa Cruz Norte

-- Insertar sucursales
INSERT INTO Dim_Sucursales (id_ubicacion, nombre, direccion, cajas) VALUES
(1, 'Sucursal Cochabamba Centro', 'Av. San Martín 1234, Cochabamba', 2),
(2, 'Sucursal Cochabamba Sur', 'Calle 4 de Noviembre, Cochabamba', 2),
(3, 'Sucursal La Paz Centro', 'Calle Comercio 567, La Paz', 2),
(4, 'Sucursal La Paz Sur', 'Av. 6 de Agosto, La Paz', 2),
(5, 'Sucursal Santa Cruz Centro', 'Calle Monseñor Rivero, Santa Cruz', 2),
(6, 'Sucursal Santa Cruz Norte', 'Av. Cristo Redentor, Santa Cruz', 2);

-- Insertar categorías
INSERT INTO Dim_Categorias (nombre, descripcion) VALUES
('Pollo', 'Productos derivados de pollo.'),
('Bebidas', 'Variedad de bebidas, tanto alcohólicas como no alcohólicas.');

-- Insertar subcategorías
INSERT INTO Dim_Subcategorias (id_subcategoria, id_categoria, nombre_subcategoria, descripcion) VALUES
(1, 1, 'Pipocas de pollo', 'Pipocas de pollo, enmarinado con huevo y harina.'),
(2, 1, 'Alitas', 'Muslo y punta de la ala.'),
(3, 1, 'Filetes', 'Filetes de pollo sin hueso.'),
(4, 2, 'Bebidas Sin Alcohol', 'Bebidas refrescantes y no alcohólicas.'),
(5, 2, 'Bebidas Alcohólicas', 'Bebidas que contienen alcohol.');

-- Insertar productos de pollo
INSERT INTO Dim_Productos (id_subcategoria, nombre, precio, perecedero) VALUES
(1, 'Pipoca pequeña', 20.00, TRUE),
(1, 'Pipoca grande', 25.00, TRUE),
(2, 'Alitas de Pollo 6 und.', 29.00, TRUE),
(2, 'Alitas de Pollo 10 und.', 36.00, TRUE),
(3, 'Filetes 3 und.', 29.00, TRUE),
(3, 'Filetes 5 und.', 36.00, TRUE);

-- Insertar bebidas
INSERT INTO Dim_Productos (id_subcategoria, nombre, precio, perecedero) VALUES
(4, 'Gaseosa Cola', 5.00, TRUE),
(4, 'Agua Mineral', 3.00, TRUE),
(5, 'Cerveza', 10.00, TRUE),
(5, 'Vino Tinto', 15.00, TRUE); 

-- Insertar géneros
INSERT INTO Dim_Genero (genero) VALUES
('Masculino'),
('Femenino');

-- Insertar 50 clientes
INSERT INTO Dim_Clientes (nombre, apellido, email, telefono, id_genero) VALUES
('Juan', 'Pérez', 'juan.perez@example.com', '720-123456', 1),
('Ana', 'Gómez', 'ana.gomez@example.com', '720-123457', 2),
('Luis', 'Martínez', 'luis.martinez@example.com', '720-123458', 1),
('María', 'López', 'maria.lopez@example.com', '720-123459', 2),
('Carlos', 'Hernández', 'carlos.hernandez@example.com', '720-123460', 1),
('Laura', 'González', 'laura.gonzalez@example.com', '720-123461', 2),
('Javier', 'Ramírez', 'javier.ramirez@example.com', '720-123462', 1),
('Sofía', 'Torres', 'sofia.torres@example.com', '720-123463', 2),
('Andrés', 'Díaz', 'andres.diaz@example.com', '720-123464', 1),
('Isabel', 'Flores', 'isabel.flores@example.com', '720-123465', 2),
('Diego', 'Rojas', 'diego.rojas@example.com', '720-123466', 1),
('Carmen', 'Mendoza', 'carmen.mendoza@example.com', '720-123467', 2),
('Fernando', 'Castillo', 'fernando.castillo@example.com', '720-123468', 1),
('Natalia', 'Salazar', 'natalia.salazar@example.com', '720-123469', 2),
('Roberto', 'Núñez', 'roberto.nunez@example.com', '720-123470', 1),
('Verónica', 'Castro', 'veronica.castro@example.com', '720-123471', 2),
('Hugo', 'Serrano', 'hugo.serrano@example.com', '720-123472', 1),
('Patricia', 'Paredes', 'patricia.paredes@example.com', '720-123473', 2),
('Raúl', 'Vásquez', 'raul.vasquez@example.com', '720-123474', 1),
('Luisa', 'Cáceres', 'luisa.caceres@example.com', '720-123475', 2),
('Cristian', 'Bermúdez', 'cristian.bermudez@example.com', '720-123476', 1),
('Rocío', 'Benítez', 'rocio.benitez@example.com', '720-123477', 2),
('Eduardo', 'Aguirre', 'eduardo.aguirre@example.com', '720-123478', 1),
('Patricia', 'Aguilar', 'patricia.aguilar@example.com', '720-123479', 2),
('Francisco', 'Márquez', 'francisco.marquez@example.com', '720-123480', 1),
('Marisol', 'Córdova', 'marisol.cordova@example.com', '720-123481', 2),
('Pedro', 'Cruz', 'pedro.cruz@example.com', '720-123482', 1),
('Silvia', 'Soto', 'silvia.soto@example.com', '720-123483', 2),
('Raúl', 'Reyes', 'raul.reyes@example.com', '720-123484', 1),
('Yolanda', 'Acosta', 'yolanda.acosta@example.com', '720-123485', 2),
('Gustavo', 'Moreno', 'gustavo.moreno@example.com', '720-123486', 1),
('Cecilia', 'Alvarez', 'cecilia.alvarez@example.com', '720-123487', 2),
('Arturo', 'Sánchez', 'arturo.sanchez@example.com', '720-123488', 1),
('Lucía', 'Ramírez', 'lucia.ramirez@example.com', '720-123489', 2),
('Daniel', 'Ceballos', 'daniel.ceballos@example.com', '720-123490', 1),
('Monica', 'Lima', 'monica.lima@example.com', '720-123491', 2),
('Felipe', 'Salas', 'felipe.salas@example.com', '720-123492', 1),
('Adriana', 'Téllez', 'adriana.tellez@example.com', '720-123493', 2),
('Oscar', 'Zapata', 'oscar.zapata@example.com', '720-123494', 1),
('Claudia', 'Peña', 'claudia.pena@example.com', '720-123495', 2),
('Victor', 'Valdez', 'victor.valdez@example.com', '720-123496', 1),
('Angela', 'Cisneros', 'angela.cisneros@example.com', '720-123497', 2),
('Jorge', 'Paz', 'jorge.paz@example.com', '720-123498', 1),
('Marina', 'Figueroa', 'marina.figueroa@example.com', '720-123499', 2),
('Salvador', 'Cordero', 'salvador.cordero@example.com', '720-123500', 1),
('Carolina', 'Cifuentes', 'carolina.cifuentes@example.com', '720-123501', 2),
('Eduardo', 'Arriaga', 'eduardo.arriaga@example.com', '720-123502', 1),
('Veronica', 'Soto', 'veronica.soto@example.com', '720-123503', 2),
('Pablo', 'Rivas', 'pablo.rivas@example.com', '720-123504', 1),
('Margarita', 'Ocampo', 'margarita.ocampo@example.com', '720-123505', 2);

-- Insertar fechas para el mes de octubre de 2024
INSERT INTO Dim_Fecha (id_fecha, dia, mes, anio, dia_semana, trimestre) VALUES
('2024-10-01', 1, 10, 2024, 'Martes', 4),
('2024-10-02', 2, 10, 2024, 'Miércoles', 4),
('2024-10-03', 3, 10, 2024, 'Jueves', 4),
('2024-10-04', 4, 10, 2024, 'Viernes', 4),
('2024-10-05', 5, 10, 2024, 'Sábado', 4),
('2024-10-06', 6, 10, 2024, 'Domingo', 4),
('2024-10-07', 7, 10, 2024, 'Lunes', 4),
('2024-10-08', 8, 10, 2024, 'Martes', 4),
('2024-10-09', 9, 10, 2024, 'Miércoles', 4),
('2024-10-10', 10, 10, 2024, 'Jueves', 4),
('2024-10-11', 11, 10, 2024, 'Viernes', 4),
('2024-10-12', 12, 10, 2024, 'Sábado', 4),
('2024-10-13', 13, 10, 2024, 'Domingo', 4),
('2024-10-14', 14, 10, 2024, 'Lunes', 4),
('2024-10-15', 15, 10, 2024, 'Martes', 4),
('2024-10-16', 16, 10, 2024, 'Miércoles', 4),
('2024-10-17', 17, 10, 2024, 'Jueves', 4),
('2024-10-18', 18, 10, 2024, 'Viernes', 4),
('2024-10-19', 19, 10, 2024, 'Sábado', 4),
('2024-10-20', 20, 10, 2024, 'Domingo', 4),
('2024-10-21', 21, 10, 2024, 'Lunes', 4),
('2024-10-22', 22, 10, 2024, 'Martes', 4),
('2024-10-23', 23, 10, 2024, 'Miércoles', 4),
('2024-10-24', 24, 10, 2024, 'Jueves', 4),
('2024-10-25', 25, 10, 2024, 'Viernes', 4),
('2024-10-26', 26, 10, 2024, 'Sábado', 4),
('2024-10-27', 27, 10, 2024, 'Domingo', 4),
('2024-10-28', 28, 10, 2024, 'Lunes', 4),
('2024-10-29', 29, 10, 2024, 'Martes', 4),
('2024-10-30', 30, 10, 2024, 'Miércoles', 4),
('2024-10-31', 31, 10, 2024, 'Jueves', 4); 

-- Insertar métodos de pago
INSERT INTO Dim_Metodos_Pago (metodo_pago) VALUES
('Efectivo'),
('Tarjeta de Crédito'); 


select * from hechos_ventas hv ;


select * from dim_sucursales ds ;

