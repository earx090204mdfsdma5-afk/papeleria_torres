-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Servidor: 127.0.0.1
-- Tiempo de generación: 24-09-2026 a las 15:45:28
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
-- Base de datos: `cecytemz`
--

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `alumnos`
--

CREATE TABLE `alumnos` (
  `id_alumno` int(11) NOT NULL,
  `id_grupo` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `alumnos`
--

INSERT INTO `alumnos` (`id_alumno`, `id_grupo`, `nombre`) VALUES
(1, 1, 'María González'),
(2, 1, 'José Ramírez'),
(3, 2, 'Ana López'),
(4, 2, 'Luis Martínez'),
(5, 3, 'Carla Sánchez'),
(6, 3, 'Pedro Flores'),
(7, 4, 'Lucía Díaz'),
(8, 4, 'Jorge Morales'),
(9, 5, 'Elena Torres'),
(10, 5, 'Carlos Rivera');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `aulas`
--

CREATE TABLE `aulas` (
  `id_aula` int(11) NOT NULL,
  `numero` varchar(10) DEFAULT NULL,
  `edificio` varchar(20) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `aulas`
--

INSERT INTO `aulas` (`id_aula`, `numero`, `edificio`) VALUES
(1, 'A101', 'Norte'),
(2, 'A102', 'Norte'),
(3, 'B201', 'Sur'),
(4, 'B202', 'Sur'),
(5, 'C301', 'Oriente'),
(6, 'C302', 'Oriente'),
(7, 'D401', 'Poniente'),
(8, 'D402', 'Poniente'),
(9, 'E501', 'Central'),
(10, 'E502', 'Central');

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `calificaciones`
--

CREATE TABLE `calificaciones` (
  `id_calificacion` int(11) NOT NULL,
  `id_alumno` int(11) DEFAULT NULL,
  `id_materia` int(11) DEFAULT NULL,
  `calificacion` decimal(4,2) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `calificaciones`
--

INSERT INTO `calificaciones` (`id_calificacion`, `id_alumno`, `id_materia`, `calificacion`) VALUES
(1, 1, 1, 8.50),
(2, 2, 2, 9.00),
(3, 3, 3, 7.50),
(4, 4, 4, 8.00),
(5, 5, 5, 9.50),
(6, 6, 6, 6.00),
(7, 7, 7, 8.50),
(8, 8, 8, 7.00),
(9, 9, 9, 9.00),
(10, 10, 10, 8.00);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `grupos`
--

CREATE TABLE `grupos` (
  `id_grupo` int(11) NOT NULL,
  `nombre` varchar(10) DEFAULT NULL,
  `id_profesor` int(11) DEFAULT NULL,
  `id_materia` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `grupos`
--

INSERT INTO `grupos` (`id_grupo`, `nombre`, `id_profesor`, `id_materia`) VALUES
(1, 'G01', 1, 1),
(2, 'G02', 2, 2),
(3, 'G03', 3, 3),
(4, 'G04', 4, 4),
(5, 'G05', 5, 5),
(6, 'G06', 6, 6),
(7, 'G07', 7, 7),
(8, 'G08', 8, 8),
(9, 'G09', 9, 9),
(10, 'G10', 10, 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `horarios`
--

CREATE TABLE `horarios` (
  `id_horario` int(11) NOT NULL,
  `dia` varchar(15) DEFAULT NULL,
  `hora` time DEFAULT NULL,
  `id_aula` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `horarios`
--

INSERT INTO `horarios` (`id_horario`, `dia`, `hora`, `id_aula`) VALUES
(1, 'Lunes', '08:00:00', 1),
(2, 'Lunes', '09:00:00', 2),
(3, 'Martes', '08:00:00', 3),
(4, 'Martes', '09:00:00', 4),
(5, 'Miércoles', '08:00:00', 5),
(6, 'Miércoles', '09:00:00', 6),
(7, 'Jueves', '08:00:00', 7),
(8, 'Jueves', '09:00:00', 8),
(9, 'Viernes', '08:00:00', 9),
(10, 'Viernes', '09:00:00', 10);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `materias`
--

CREATE TABLE `materias` (
  `id_materia` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL,
  `creditos` int(11) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `materias`
--

INSERT INTO `materias` (`id_materia`, `nombre`, `creditos`) VALUES
(1, 'Álgebra', 5),
(2, 'Física I', 6),
(3, 'Química', 5),
(4, 'Biología', 4),
(5, 'Historia Universal', 4),
(6, 'Literatura', 3),
(7, 'Inglés', 4),
(8, 'Artes', 3),
(9, 'Música', 2),
(10, 'Ética', 3);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `profesores`
--

CREATE TABLE `profesores` (
  `id_profesor` int(11) NOT NULL,
  `id_departamento` int(11) NOT NULL,
  `nombre` varchar(50) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Volcado de datos para la tabla `profesores`
--

INSERT INTO `profesores` (`id_profesor`, `id_departamento`, `nombre`) VALUES
(1, 1, 'Roberto Martínez'),
(2, 1, 'Patricia Gómez'),
(3, 2, 'Miguel Sánchez'),
(4, 2, 'Sofía López'),
(5, 3, 'Andrés Pérez'),
(6, 3, 'Laura Fernández'),
(7, 4, 'Fernando Ruiz'),
(8, 4, 'Carmen Díaz'),
(9, 5, 'Ricardo Mora'),
(10, 5, 'Gabriela Castro');

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `alumnos`
--
ALTER TABLE `alumnos`
  ADD PRIMARY KEY (`id_alumno`,`id_grupo`);

--
-- Indices de la tabla `aulas`
--
ALTER TABLE `aulas`
  ADD PRIMARY KEY (`id_aula`);

--
-- Indices de la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD PRIMARY KEY (`id_calificacion`),
  ADD KEY `id_alumno` (`id_alumno`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD PRIMARY KEY (`id_grupo`),
  ADD KEY `id_profesor` (`id_profesor`),
  ADD KEY `id_materia` (`id_materia`);

--
-- Indices de la tabla `horarios`
--
ALTER TABLE `horarios`
  ADD PRIMARY KEY (`id_horario`),
  ADD KEY `id_aula` (`id_aula`);

--
-- Indices de la tabla `materias`
--
ALTER TABLE `materias`
  ADD PRIMARY KEY (`id_materia`);

--
-- Indices de la tabla `profesores`
--
ALTER TABLE `profesores`
  ADD PRIMARY KEY (`id_profesor`,`id_departamento`);

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `calificaciones`
--
ALTER TABLE `calificaciones`
  ADD CONSTRAINT `calificaciones_ibfk_1` FOREIGN KEY (`id_alumno`) REFERENCES `alumnos` (`id_alumno`),
  ADD CONSTRAINT `calificaciones_ibfk_2` FOREIGN KEY (`id_materia`) REFERENCES `materias` (`id_materia`);

--
-- Filtros para la tabla `grupos`
--
ALTER TABLE `grupos`
  ADD CONSTRAINT `grupos_ibfk_1` FOREIGN KEY (`id_profesor`) REFERENCES `profesores` (`id_profesor`),
  ADD CONSTRAINT `grupos_ibfk_2` FOREIGN KEY (`id_materia`) REFERENCES `materias` (`id_materia`);

--
-- Filtros para la tabla `horarios`
--
ALTER TABLE `horarios`
  ADD CONSTRAINT `horarios_ibfk_1` FOREIGN KEY (`id_aula`) REFERENCES `aulas` (`id_aula`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
