CREATE DATABASE IF NOT EXISTS umami;
USE umami;

-- Users table
CREATE TABLE IF NOT EXISTS users (
    id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    email VARCHAR(100) NOT NULL UNIQUE,
    password VARCHAR(255) NOT NULL, 
    fullname VARCHAR(100),
    usertype TINYINT NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Dishes table
CREATE TABLE IF NOT EXISTS dishes (
    dish_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    price DECIMAL(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Shopping cart table
CREATE TABLE IF NOT EXISTS cart (
    cart_id INT AUTO_INCREMENT PRIMARY KEY,
    customer_id SMALLINT UNSIGNED NOT NULL,
    delivery_person_id SMALLINT UNSIGNED,
    date DATETIME,
    status ENUM('Delivered', 'Paid') DEFAULT 'Paid',
    FOREIGN KEY (customer_id) REFERENCES users(id),
    FOREIGN KEY (delivery_person_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Cart details table
CREATE TABLE IF NOT EXISTS cart_details (
    detail_id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    dish_id INT NOT NULL,
    quantity INT NOT NULL,
    FOREIGN KEY (cart_id) REFERENCES cart(cart_id),
    FOREIGN KEY (dish_id) REFERENCES dishes(dish_id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;





-- Procedimientos
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
