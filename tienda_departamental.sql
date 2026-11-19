-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 27-10-2026 a las 15:20:09
-- Versión del servidor: 10.4.32-MariaDB
-- Versión de PHP: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Base de datos: `tienda_departamental`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `clientes`
--

CREATE TABLE `clientes` (
  `id_cliente` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `email` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `fecha_registro` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `clientes`
--

INSERT INTO `clientes` (`id_cliente`, `nombre`, `apellido`, `email`, `telefono`, `direccion`, `fecha_registro`) VALUES
(1, 'Ana', 'García', 'ana.garcia@mail.com', '5551234567', 'Av. Reforma 101, CDMX', '2023-01-15'),
(2, 'Luis', 'Martínez', 'luis.mtz@mail.com', '5559876543', 'Calle Juárez 45, Guadalajara', '2023-02-20'),
(3, 'María', 'López', 'maria.lopez@mail.com', '5554567890', 'Insurgentes 300, CDMX', '2023-03-10'),
(4, 'Carlos', 'Hernández', 'carlos.hdz@mail.com', '5552345678', 'Reforma 55, Monterrey', '2023-04-05'),
(5, 'Sofía', 'Ramírez', 'sofia.ram@mail.com', '5558765432', 'Patriotismo 88, CDMX', '2023-05-22'),
(6, 'Jorge', 'Torres', 'jorge.torres@mail.com', '5553456789', 'Chapultepec 12, Puebla', '2023-06-30');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `departamentos`
--

CREATE TABLE `departamentos` (
  `id_departamento` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `descripcion` varchar(200) DEFAULT NULL,
  `piso` int(11) DEFAULT NULL,
  `encargado` varchar(150) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `estado` varchar(20) DEFAULT 'Activo'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `departamentos`
--

INSERT INTO `departamentos` (`id_departamento`, `nombre`, `descripcion`, `piso`, `encargado`, `telefono`, `estado`) VALUES
(1, 'Ropa Dama', 'Moda femenina', 1, 'Laura Díaz', '5551112233', 'Activo'),
(2, 'Ropa Caballero', 'Moda masculina', 1, 'Miguel Ruiz', '5551112244', 'Activo'),
(3, 'Electrónica', 'Televisores y audio', 2, 'Pedro Sánchez', '5551112255', 'Activo'),
(4, 'Perfumería', 'Fragancias y cuidado', 1, 'Daniela Cruz', '5551112266', 'Activo'),
(5, 'Hogar', 'Muebles y blancos', 3, 'Raúl Morales', '5551112277', 'Activo'),
(6, 'Juguetería', 'Juguetes infantiles', 2, 'Patricia Vega', '5551112288', 'Activo');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `detalle_venta`
--

CREATE TABLE `detalle_venta` (
  `id_detalle` int(11) NOT NULL,
  `id_venta` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `cantidad` int(11) NOT NULL,
  `precio_unitario` decimal(10,2) NOT NULL,
  `subtotal` decimal(10,2) NOT NULL,
  `descuento` decimal(10,2) DEFAULT 0.00
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `detalle_venta`
--

INSERT INTO `detalle_venta` (`id_detalle`, `id_venta`, `id_producto`, `cantidad`, `precio_unitario`, `subtotal`, `descuento`) VALUES
(1, 1, 1, 1, 499.00, 499.00, 0.00),
(2, 2, 2, 1, 1299.00, 1299.00, 0.00),
(3, 3, 3, 1, 12999.00, 12999.00, 500.00),
(4, 4, 4, 1, 1850.00, 1850.00, 0.00),
(5, 5, 5, 1, 899.00, 899.00, 0.00),
(6, 6, 6, 1, 650.00, 650.00, 50.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `empleados`
--

CREATE TABLE `empleados` (
  `id_empleado` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `apellido` varchar(100) NOT NULL,
  `puesto` varchar(80) NOT NULL,
  `salario` decimal(10,2) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `fecha_ingreso` date NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `empleados`
--

INSERT INTO `empleados` (`id_empleado`, `nombre`, `apellido`, `puesto`, `salario`, `email`, `fecha_ingreso`) VALUES
(1, 'Pedro', 'Sánchez', 'Cajero', 8500.00, 'pedro.s@liverpool.com', '2020-03-01'),
(2, 'Laura', 'Díaz', 'Supervisora', 15000.00, 'laura.d@liverpool.com', '2019-07-15'),
(3, 'Miguel', 'Ruiz', 'Gerente', 25000.00, 'miguel.r@liverpool.com', '2018-01-10'),
(4, 'Daniela', 'Cruz', 'Vendedora', 9200.00, 'daniela.c@liverpool.com', '2021-09-20'),
(5, 'Raúl', 'Morales', 'Almacenista', 7800.00, 'raul.m@liverpool.com', '2022-02-14'),
(6, 'Patricia', 'Vega', 'Cajera', 8500.00, 'patricia.v@liverpool.com', '2021-05-05');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `inventario`
--

CREATE TABLE `inventario` (
  `id_inventario` int(11) NOT NULL,
  `id_producto` int(11) NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  `stock` int(11) NOT NULL,
  `stock_minimo` int(11) DEFAULT 5,
  `ubicacion` varchar(100) DEFAULT NULL,
  `ultima_entrada` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `inventario`
--

INSERT INTO `inventario` (`id_inventario`, `id_producto`, `id_sucursal`, `stock`, `stock_minimo`, `ubicacion`, `ultima_entrada`) VALUES
(1, 1, 1, 50, 10, 'Pasillo A-01', '2024-01-05'),
(2, 2, 2, 30, 10, 'Pasillo B-02', '2024-01-06'),
(3, 3, 1, 15, 5, 'Bodega E-01', '2024-01-08'),
(4, 4, 3, 40, 15, 'Pasillo P-01', '2024-01-09'),
(5, 5, 4, 20, 8, 'Bodega H-02', '2024-01-10'),
(6, 6, 5, 60, 20, 'Pasillo J-01', '2024-01-11');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `pagos`
--

CREATE TABLE `pagos` (
  `id_pago` int(11) NOT NULL,
  `id_venta` int(11) NOT NULL,
  `metodo_pago` varchar(50) NOT NULL,
  `monto` decimal(10,2) NOT NULL,
  `fecha_pago` datetime NOT NULL,
  `referencia` varchar(100) DEFAULT NULL,
  `banco` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `pagos`
--

INSERT INTO `pagos` (`id_pago`, `id_venta`, `metodo_pago`, `monto`, `fecha_pago`, `referencia`, `banco`) VALUES
(1, 1, 'Tarjeta de Crédito', 499.00, '2024-01-10 11:32:00', 'TC-001', 'BBVA'),
(2, 2, 'Efectivo', 1299.00, '2024-01-11 16:47:00', 'EF-002', NULL),
(3, 3, 'Tarjeta Débito', 12499.00, '2024-01-12 13:17:00', 'TD-003', 'Banorte'),
(4, 4, 'Transferencia', 1850.00, '2024-01-13 10:05:00', 'TR-004', 'Santander'),
(5, 5, 'Tarjeta de Crédito', 899.00, '2024-01-14 18:22:00', 'TC-005', 'HSBC'),
(6, 6, 'Efectivo', 600.00, '2024-01-15 12:12:00', 'EF-006', NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `productos`
--

CREATE TABLE `productos` (
  `id_producto` int(11) NOT NULL,
  `nombre` varchar(150) NOT NULL,
  `marca` varchar(80) DEFAULT NULL,
  `precio` decimal(10,2) NOT NULL,
  `categoria` varchar(80) DEFAULT NULL,
  `id_proveedor` int(11) DEFAULT NULL,
  `id_departamento` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `productos`
--

INSERT INTO `productos` (`id_producto`, `nombre`, `marca`, `precio`, `categoria`, `id_proveedor`, `id_departamento`) VALUES
(1, 'Blusa Casual', 'Zara', 499.00, 'Ropa Dama', 1, 1),
(2, 'Camisa Formal', 'Hugo Boss', 1299.00, 'Ropa Caballero', 1, 2),
(3, 'Smart TV 55\"', 'Samsung', 12999.00, 'Electrónica', 2, 3),
(4, 'Perfume EDT 100ml', 'Carolina H.', 1850.00, 'Perfumería', 3, 4),
(5, 'Juego de Sábanas', 'Spring Air', 899.00, 'Hogar', 4, 5),
(6, 'Peluche Gigante', 'MundoFeliz', 650.00, 'Juguetería', 5, 6);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proveedores`
--

CREATE TABLE `proveedores` (
  `id_proveedor` int(11) NOT NULL,
  `razon_social` varchar(150) NOT NULL,
  `contacto` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `email` varchar(150) DEFAULT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `pais` varchar(80) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `proveedores`
--

INSERT INTO `proveedores` (`id_proveedor`, `razon_social`, `contacto`, `telefono`, `email`, `direccion`, `pais`) VALUES
(1, 'Textiles del Norte SA', 'Juan Pérez', '8181234567', 'ventas@textinorte.com', 'Monterrey, NL', 'México'),
(2, 'ElectroWorld SA de CV', 'Elena Ríos', '5552345678', 'contacto@electroworld.mx', 'CDMX', 'México'),
(3, 'Fragancias Globales', 'Marco Solís', '5553456789', 'info@fragglobal.com', 'Guadalajara, JAL', 'México'),
(4, 'Muebles Finos SA', 'Lucía Vidal', '5554567890', 'ventas@mueblesfinos.mx', 'Puebla, PUE', 'México'),
(5, 'Juguetería MundoFeliz', 'Hugo Lara', '5555678901', 'pedidos@mundofeliz.com', 'CDMX', 'México'),
(6, 'Importadora Andina', 'Carla Méndez', '5556789012', 'ventas@andina.com', 'Lima', 'Perú');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `sucursales`
--

CREATE TABLE `sucursales` (
  `id_sucursal` int(11) NOT NULL,
  `nombre` varchar(100) NOT NULL,
  `direccion` varchar(200) DEFAULT NULL,
  `ciudad` varchar(100) DEFAULT NULL,
  `telefono` varchar(20) DEFAULT NULL,
  `gerente` varchar(150) DEFAULT NULL,
  `fecha_apertura` date DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `sucursales`
--

INSERT INTO `sucursales` (`id_sucursal`, `nombre`, `direccion`, `ciudad`, `telefono`, `gerente`, `fecha_apertura`) VALUES
(1, 'Liverpool Reforma', 'Av. Reforma 222', 'CDMX', '5551234001', 'Roberto Núñez', '2010-05-10'),
(2, 'Liverpool Polanco', 'Av. Presidente Masaryk 100', 'CDMX', '5551234002', 'Silvia Ortega', '2012-08-15'),
(3, 'Liverpool Galerías', 'Av. Vallarta 2000', 'Guadalajara', '3331234003', 'Andrés Luna', '2015-03-20'),
(4, 'Liverpool Monterrey', 'Av. Constitución 500', 'Monterrey', '8181234004', 'Mónica Ríos', '2016-11-01'),
(5, 'Liverpool Puebla', 'Blvd. Atlixco 300', 'Puebla', '2221234005', 'Iván Castro', '2018-06-12'),
(6, 'Liverpool Cancún', 'Av. Kukulcán 55', 'Cancún', '9981234006', 'Gabriela Peña', '2020-09-25');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `ventas`
--

CREATE TABLE `ventas` (
  `id_venta` int(11) NOT NULL,
  `id_cliente` int(11) NOT NULL,
  `id_empleado` int(11) NOT NULL,
  `id_sucursal` int(11) NOT NULL,
  `fecha_venta` datetime NOT NULL,
  `total` decimal(10,2) NOT NULL,
  `estado` varchar(30) DEFAULT 'Pagada'
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `ventas`
--

INSERT INTO `ventas` (`id_venta`, `id_cliente`, `id_empleado`, `id_sucursal`, `fecha_venta`, `total`, `estado`) VALUES
(1, 1, 1, 1, '2024-01-10 11:30:00', 499.00, 'Pagada'),
(2, 2, 4, 2, '2024-01-11 16:45:00', 1299.00, 'Pagada'),
(3, 3, 1, 1, '2024-01-12 13:15:00', 12999.00, 'Pagada'),
(4, 4, 6, 3, '2024-01-13 10:00:00', 1850.00, 'Pagada'),
(5, 5, 4, 4, '2024-01-14 18:20:00', 899.00, 'Pendiente'),
(6, 6, 1, 5, '2024-01-15 12:10:00', 650.00, 'Pagada');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `clientes`
--
ALTER TABLE `clientes`
  ADD PRIMARY KEY (`id_cliente`),
  ADD UNIQUE KEY `email` (`email`);

--
-- Indices de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  ADD PRIMARY KEY (`id_departamento`);

--
-- Indices de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD PRIMARY KEY (`id_detalle`),
  ADD KEY `id_venta` (`id_venta`),
  ADD KEY `id_producto` (`id_producto`);

--
-- Indices de la tabla `empleados`
--
ALTER TABLE `empleados`
  ADD PRIMARY KEY (`id_empleado`);

--
-- Indices de la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD PRIMARY KEY (`id_inventario`),
  ADD KEY `id_producto` (`id_producto`),
  ADD KEY `id_sucursal` (`id_sucursal`);

--
-- Indices de la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD PRIMARY KEY (`id_pago`),
  ADD KEY `id_venta` (`id_venta`);

--
-- Indices de la tabla `productos`
--
ALTER TABLE `productos`
  ADD PRIMARY KEY (`id_producto`),
  ADD KEY `id_proveedor` (`id_proveedor`),
  ADD KEY `id_departamento` (`id_departamento`);

--
-- Indices de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  ADD PRIMARY KEY (`id_proveedor`);

--
-- Indices de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  ADD PRIMARY KEY (`id_sucursal`);

--
-- Indices de la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD PRIMARY KEY (`id_venta`),
  ADD KEY `id_cliente` (`id_cliente`),
  ADD KEY `id_empleado` (`id_empleado`),
  ADD KEY `id_sucursal` (`id_sucursal`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `clientes`
--
ALTER TABLE `clientes`
  MODIFY `id_cliente` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `departamentos`
--
ALTER TABLE `departamentos`
  MODIFY `id_departamento` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  MODIFY `id_detalle` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `empleados`
--
ALTER TABLE `empleados`
  MODIFY `id_empleado` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `inventario`
--
ALTER TABLE `inventario`
  MODIFY `id_inventario` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `pagos`
--
ALTER TABLE `pagos`
  MODIFY `id_pago` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `productos`
--
ALTER TABLE `productos`
  MODIFY `id_producto` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `proveedores`
--
ALTER TABLE `proveedores`
  MODIFY `id_proveedor` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `sucursales`
--
ALTER TABLE `sucursales`
  MODIFY `id_sucursal` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT de la tabla `ventas`
--
ALTER TABLE `ventas`
  MODIFY `id_venta` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `detalle_venta`
--
ALTER TABLE `detalle_venta`
  ADD CONSTRAINT `detalle_venta_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`),
  ADD CONSTRAINT `detalle_venta_ibfk_2` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`);

--
-- Filtros para la tabla `inventario`
--
ALTER TABLE `inventario`
  ADD CONSTRAINT `inventario_ibfk_1` FOREIGN KEY (`id_producto`) REFERENCES `productos` (`id_producto`),
  ADD CONSTRAINT `inventario_ibfk_2` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursales` (`id_sucursal`);

--
-- Filtros para la tabla `pagos`
--
ALTER TABLE `pagos`
  ADD CONSTRAINT `pagos_ibfk_1` FOREIGN KEY (`id_venta`) REFERENCES `ventas` (`id_venta`);

--
-- Filtros para la tabla `productos`
--
ALTER TABLE `productos`
  ADD CONSTRAINT `productos_ibfk_1` FOREIGN KEY (`id_proveedor`) REFERENCES `proveedores` (`id_proveedor`),
  ADD CONSTRAINT `productos_ibfk_2` FOREIGN KEY (`id_departamento`) REFERENCES `departamentos` (`id_departamento`);

--
-- Filtros para la tabla `ventas`
--
ALTER TABLE `ventas`
  ADD CONSTRAINT `ventas_ibfk_1` FOREIGN KEY (`id_cliente`) REFERENCES `clientes` (`id_cliente`),
  ADD CONSTRAINT `ventas_ibfk_2` FOREIGN KEY (`id_empleado`) REFERENCES `empleados` (`id_empleado`),
  ADD CONSTRAINT `ventas_ibfk_3` FOREIGN KEY (`id_sucursal`) REFERENCES `sucursales` (`id_sucursal`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
