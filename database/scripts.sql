CREATE DATABASE IF NOT EXISTS umami;
USE umami;

-- Tabla de usuarios
CREATE TABLE IF NOT EXISTS users (
 id smallint unsigned NOT NULL AUTO_INCREMENT,
 email varchar(30) NOT NULL,
 password char(102) NOT NULL,
 fullname varchar(50),
 usertype tinyint NOT NULL,
 PRIMARY KEY (id)
) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci



DELIMITER //
CREATE PROCEDURE sp_AddUser(IN pEmail VARCHAR(30), IN pPassword VARCHAR(102), IN pFullName
VARCHAR(50), in pUserType tinyint)
BEGIN
 DECLARE hashedPassword VARCHAR(255);
 SET hashedPassword = SHA2(pPassword, 256);
 INSERT INTO users (email, password, fullname, usertype )
 VALUES (pEmail, hashedPassword, pFullName, pUserType);
END //
DELIMITER ;


DELIMITER //
CREATE PROCEDURE sp_UpdateUser( IN pId SMALLINT, IN pEmail VARCHAR(30), IN pPassword VARCHAR(102), IN pFullName VARCHAR(50))
BEGIN
    DECLARE hashedPassword VARCHAR(255);
    
    
    IF pPassword IS NOT NULL AND pPassword != '' THEN
        SET hashedPassword = SHA2(pPassword, 256);
    ELSE
        SELECT password INTO hashedPassword FROM users WHERE id = pId;
    END IF;
    
    -- Actualizar solo los campos necesarios
    UPDATE users 
    SET 
        email = pEmail,
        password = hashedPassword,
        fullname = pFullName
    WHERE id = pId;
END //
DELIMITER ;



DELIMITER //
CREATE PROCEDURE sp_verifyIdentity(IN pEmail VARCHAR(30), IN pPlainTextPassword VARCHAR(20))
BEGIN
 DECLARE storedPassword VARCHAR(255);

 SELECT password INTO storedPassword FROM users
 WHERE email = pEmail COLLATE utf8mb4_unicode_ci;

 IF storedPassword IS NOT NULL AND storedPassword = SHA2(pPlainTextPassword, 256) THEN
 SELECT id, email, storedPassword, fullname, usertype FROM users
 WHERE email = pEmail COLLATE utf8mb4_unicode_ci;
 ELSE
 SELECT NULL;
END IF;
END //
DELIMITER ;




-- Tabla de platillos
CREATE TABLE platillos (
    id_platillo INT AUTO_INCREMENT PRIMARY KEY,
    nombre VARCHAR(50),
    descripcion TEXT,
    precio DECIMAL(10,2)
);










CREATE TABLE carrito (
    id_carrito INT AUTO_INCREMENT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_repartidor INT,
    fecha DATETIME,
    estatus ENUM('Entregado', 'Pagado'),
    FOREIGN KEY (id_cliente) REFERENCES usuarios(id_usuario),
    FOREIGN KEY (id_repartidor) REFERENCES usuarios(id_usuario)
);


CREATE TABLE DetalleCarrito (
    id_detalle INT AUTO_INCREMENT PRIMARY KEY,
    id_carrito INT NOT NULL,
    id_platillo INT NOT NULL,
    cantidad INT,
    FOREIGN KEY (id_carrito) REFERENCES carrito(id_carrito),
    FOREIGN KEY (id_platillo) REFERENCES platillos(id_platillo)
);

