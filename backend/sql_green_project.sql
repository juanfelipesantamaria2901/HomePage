--
-- Base de datos: `pibd`
--

-- --------------------------------------------------------

CREATE DATABASE pibd;

USE pibd;

--
-- Estructura de tabla para la tabla `a`
--

CREATE TABLE `a` (
  `id` int(100) NOT NULL,
  `id_usuario` int(50) NOT NULL,
  `id_tipo_usuario` int(50) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `avance`
--

CREATE TABLE `avance` (
  `id` int(100) NOT NULL,
  `url_imagen` varchar(200) NOT NULL,
  `titulo_avance` text NOT NULL,
  `descripcion_avance` text NOT NULL,
  `id_proyecto` int(100) NOT NULL,
  `fecha_avance` date NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `donaciones_monetaria`
--

CREATE TABLE `donaciones_monetaria` (
  `id` int(50) NOT NULL,
  `id_usuario` int(100) NOT NULL,
  `id_proyecto` int(10) NOT NULL,
  `cantidad_donacion` double(100,0) NOT NULL,
  `origen_donacion` double(100,0) NOT NULL,
  `fecha_realizada` datetime(6) NOT NULL,
  `numero_autorizacion` int(50) NOT NULL,
  `moneda` varchar(50) NOT NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `donacion_recursos`
--

CREATE TABLE `donacion_recursos` (
  `id` int(10) NOT NULL,
  `id_usuario` int(50) NOT NULL,
  `id_recurso` int(50) NOT NULL,
  `cantidad_recurso` int(50) NOT NULL,
  `fecha_donativo` datetime(6) NOT NULL);

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `participante_proyecto`
--

CREATE TABLE `participante_proyecto` (
  `id` int(100) NOT NULL,
  `id_usuario` int(100) NOT NULL,
  `id_proyecto` int(100) NOT NULL,
  `id_perfil` int(100) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `perfil`
--

CREATE TABLE `perfil` (
  `id` int(11) NOT NULL,
  `nombre_perfil` varchar(200) NOT NULL,
  `cantidad_participantes` text NOT NULL,
  `id_proyecto` int(100) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `proyecto`
--

CREATE TABLE `proyecto` (
  `id` int(11) NOT NULL,
  `nombre_proyecto` varchar(50) NOT NULL,
  `descripcion` text NOT NULL,
  `justificacion` text NOT NULL,
  `impacto` varchar(100) NOT NULL,
  `alineacion_ods` varchar(100) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `fecha_finalizacion` date NOT NULL,
  `estado` varchar(50) NOT NULL,
  `tipo_proyecto` varchar(50) NOT NULL,
  `url_video` varchar(200) NOT NULL,
  `url_imagen` varchar(200) NOT NULL,
  `ciudad` varchar(100) NOT NULL,
  `perfil_colaborador` varchar(100) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `recursos`
--

CREATE TABLE `recursos` (
  `id` int(100) NOT NULL,
  `nombre_recurso` varchar(50) NOT NULL,
  `cantidad_recurso` int(100) NOT NULL,
  `id_proyecto` int(10) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `tipo_usuario`
--

CREATE TABLE `tipo_usuario` (
  `id` int(100) NOT NULL,
  `nombre_tipo_usuario` varchar(50) NOT NULL,
  `fecha_creacion` datetime(6) NOT NULL
) ;

-- --------------------------------------------------------

--
-- Estructura de tabla para la tabla `usuario`
--

CREATE TABLE `usuario` (
  `id` int(10) NOT NULL,
  `nombre` varchar(50) NOT NULL,
  `apellido` varchar(50) NOT NULL,
  `edad` int(3) NOT NULL,
  `sexo` varchar(20) NOT NULL,
  `identificacion` int(15) NOT NULL,
  `direccion_residencia` varchar(100) NOT NULL,
  `ocupacion` varchar(100) NOT NULL,
  `numero_telefonico` varchar(15) NOT NULL,
  `correo_electronico` varchar(100) NOT NULL,
  `contrasena` varchar(100) NOT NULL,
  `fecha_creacion` date NOT NULL,
  `estado_usuario` tinyint(1) NOT NULL,
  `nacionalidad` varchar(50) NOT NULL,
  `ciudad` varchar(50) NOT NULL
) ;

--
-- Índices para tablas volcadas
--

--
-- Indices de la tabla `a`
--
ALTER TABLE `a`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_tipo_usuario` (`id_tipo_usuario`);

--
-- Indices de la tabla `avance`
--
ALTER TABLE `avance`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_proyecto` (`id_proyecto`);

--
-- Indices de la tabla `donaciones_monetaria`
--
ALTER TABLE `donaciones_monetaria`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_proyecto` (`id_proyecto`);

--
-- Indices de la tabla `donacion_recursos`
--
ALTER TABLE `donacion_recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_recurso` (`id_recurso`);

--
-- Indices de la tabla `participante_proyecto`
--
ALTER TABLE `participante_proyecto`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_usuario` (`id_usuario`),
  ADD KEY `id_proyecto` (`id_proyecto`),
  ADD KEY `id_perfil` (`id_perfil`);

--
-- Indices de la tabla `perfil`
--
ALTER TABLE `perfil`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_proyecto` (`id_proyecto`);

--
-- Indices de la tabla `proyecto`
--
ALTER TABLE `proyecto`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `recursos`
--
ALTER TABLE `recursos`
  ADD PRIMARY KEY (`id`),
  ADD KEY `id_proyecto` (`id_proyecto`);

--
-- Indices de la tabla `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
  ADD PRIMARY KEY (`id`);

--
-- Indices de la tabla `usuario`
--
ALTER TABLE `usuario`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT de las tablas volcadas
--

--
-- AUTO_INCREMENT de la tabla `a`
--
ALTER TABLE `a`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `avance`
--
ALTER TABLE `avance`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `donaciones_monetaria`
--
ALTER TABLE `donaciones_monetaria`
  MODIFY `id` int(50) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `donacion_recursos`
--
ALTER TABLE `donacion_recursos`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `participante_proyecto`
--
ALTER TABLE `participante_proyecto`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `perfil`
--
ALTER TABLE `perfil`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `proyecto`
--
ALTER TABLE `proyecto`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `recursos`
--
ALTER TABLE `recursos`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `tipo_usuario`
--
ALTER TABLE `tipo_usuario`
  MODIFY `id` int(100) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT de la tabla `usuario`
--
ALTER TABLE `usuario`
  MODIFY `id` int(10) NOT NULL AUTO_INCREMENT;

--
-- Restricciones para tablas volcadas
--

--
-- Filtros para la tabla `a`
--
ALTER TABLE `a`
  ADD CONSTRAINT `a_ibfk_1` FOREIGN KEY (`id_tipo_usuario`) REFERENCES `tipo_usuario` (`id`),
  ADD CONSTRAINT `a_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `avance`
--
ALTER TABLE `avance`
  ADD CONSTRAINT `avance_ibfk_1` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`);

--
-- Filtros para la tabla `donaciones_monetaria`
--
ALTER TABLE `donaciones_monetaria`
  ADD CONSTRAINT `donaciones_monetaria_ibfk_1` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`),
  ADD CONSTRAINT `donaciones_monetaria_ibfk_2` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `donacion_recursos`
--
ALTER TABLE `donacion_recursos`
  ADD CONSTRAINT `donacion_recursos_ibfk_1` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`),
  ADD CONSTRAINT `donacion_recursos_ibfk_2` FOREIGN KEY (`id_recurso`) REFERENCES `recursos` (`id`);

--
-- Filtros para la tabla `participante_proyecto`
--
ALTER TABLE `participante_proyecto`
  ADD CONSTRAINT `participante_proyecto_ibfk_1` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`),
  ADD CONSTRAINT `participante_proyecto_ibfk_2` FOREIGN KEY (`id_perfil`) REFERENCES `perfil` (`id`),
  ADD CONSTRAINT `participante_proyecto_ibfk_3` FOREIGN KEY (`id_usuario`) REFERENCES `usuario` (`id`);

--
-- Filtros para la tabla `perfil`
--
ALTER TABLE `perfil`
  ADD CONSTRAINT `perfil_ibfk_1` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`);

--
-- Filtros para la tabla `recursos`
--
ALTER TABLE `recursos`
  ADD CONSTRAINT `recursos_ibfk_1` FOREIGN KEY (`id_proyecto`) REFERENCES `proyecto` (`id`);
COMMIT;
