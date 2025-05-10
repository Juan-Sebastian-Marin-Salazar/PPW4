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


-- Tabla de categorías
CREATE TABLE categories (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(50) NOT NULL
);

INSERT INTO categories (name)
VALUES ('Sushi y Sashimi');

INSERT INTO categories (name)
VALUES ('Platos Fuertes');

INSERT INTO categories (name)
VALUES ('Donburis y Especialidades');

INSERT INTO categories (name)
VALUES ('Postres');

INSERT INTO categories (name)
VALUES ('Bebidas');

INSERT INTO categories (name)
VALUES ('Entradas y Extras');

-- Tabla de platillos
CREATE TABLE dishes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    descr VARCHAR(255) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    image VARCHAR(255),
    category_id INT,
    FOREIGN KEY (category_id) REFERENCES categories(id)
);

-- Sushi y Sashimi (category_id = 1)
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Ride on Time', 'Un roll vibrante con atún fresco, mango dulce y una salsa especial de la casa que realza los sabores tropicales. Perfecto.', 220.00, 'img/Img_Menu/Category 1 img 1.jpg', 1);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Silent Screamer', 'Nigiri de anguila glaseada con salsa teriyaki casera y un toque de wasabi, una combinación intensa y llena de carácter.', 190.00, 'img/Img_Menu/Category 1 img 2.png', 1);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Your Eyes', 'Delicado sashimi surtido con cortes seleccionados de atún, salmón y hamachi, servidos sobre hielo para una experiencia fresca y auténtica.', 250.00, 'img/Img_Menu/Category 1 img 3.png', 1);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Plastic Love', 'Un sofisticado roll de salmón ahumado, queso crema y aguacate, envuelto en alga nori y acompañado de una reducción de soya y miel.', 200.00, 'img/Img_Menu/Category 1 img 4.jpg', 1);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Dream in the Screen', 'Roll crujiente relleno de tempura de camarón, pepino y un toque de mayonesa picante, ideal para quienes buscan una mezcla perfecta de textura y sabor.', 180.00, 'img/Img_Menu/Category 1 img 5.jpg', 1);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Tokai', 'Roll de atún picante con pepino y cebollín, cubierto con un ligero toque de salsa sriracha. Un platillo inspirado en la intensidad y energía de la ciudad.', 210.00, 'img/Img_Menu/Category 1 img 6.jpg', 1);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Machi no Dorufin', 'Un roll refrescante con pulpo, pepino y cebolla morada, acompañado de salsa ponzu y ajonjolí tostado.', 230.00, 'img/Img_Menu/Category 1 img 7.jpeg', 1);

-- Platos Fuertes (category_id = 2)
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Daydream', 'Ramen tonkotsu con un caldo cremoso cocinado por horas, acompañado de chashu de cerdo, huevo marinado y cebollín fresco. Un sueño hecho realidad en cada sorbo.', 240.00, 'img/Img_Menu/Category 2 img 1.jpg', 2);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Rainy Day', 'Ramen shoyu con caldo de soya, hongos shiitake, bambú y fideos artesanales, perfecto para reconfortar el alma en un día lluvioso.', 220.00, 'img/Img_Menu/Category 2 img 2.png', 2);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Magic Ways', 'Udon en un caldo miso con tofu sedoso, alga wakame y un toque de jengibre. Suave, envolvente y lleno de umami.', 210.00, 'img/Img_Menu/Category 2 img 3.png', 2);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('I Love You', 'Yakisoba salteado al wok con vegetales frescos, carne de res y una mezcla especial de salsas dulces y saladas. Un platillo que se siente como un abrazo.', 230.00, 'img/Img_Menu/Category 2 img 4.jpg', 2);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Morning Glory', 'Omurice: arroz salteado con salsa de tomate envuelto en una tortilla esponjosa, servido con un toque de salsa demi-glace. Un clásico desayuno japonés.', 190.00, 'img/Img_Menu/Category 2 img 5.jpg', 2);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Hatsu Koi', 'Gyudon: un tazón de arroz cubierto con finas láminas de res cocidas a fuego lento en una salsa de soya y mirin. Suave y nostálgico, como un primer amor.', 220.00, 'img/Img_Menu/Category 2 img 6.png', 2);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Step Into The Light', 'Yakitori: brochetas de pollo a la parrilla, marinadas en una salsa dulce y salada, servidas con un toque de cebollín fresco.', 170.00, 'img/Img_Menu/Category 2 img 7.jpg', 2);

-- Donburis y Especialidades (category_id = 3)
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Beleza Pula', 'Katsudon: chuleta de cerdo empanizada y bañada en una mezcla de huevo y salsa dashi, servida sobre arroz caliente. Un platillo energético y lleno de sabor.', 230.00, 'img/Img_Menu/Category 3 img 1.jpg', 3);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Sparkle', 'Chirashi don: una selección de sashimi fresco servido sobre un lecho de arroz de sushi, decorado con huevas de salmón y alga nori. Una experiencia brillante en cada bocado.', 260.00, 'img/Img_Menu/Category 3 img 2.jpg', 3);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Someday', 'Filete de salmón glaseado con teriyaki, acompañado de arroz y ensalada de pepino japonés. Un platillo reconfortante que deja huella.', 280.00, 'img/Img_Menu/Category 3 img 3.jpg', 3);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Bay City', 'Tonkatsu: crujiente chuleta de cerdo empanizada, servida con salsa especial de la casa, repollo rallado y arroz japonés.', 210.00, 'img/Img_Menu/Category 3 img 4.jpg', 3);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Breezin', 'Takoyaki: esferas de masa crujiente rellenas de pulpo, cubiertas con salsa tonkatsu, mayonesa japonesa y copos de bonito seco. Una explosión de sabor.', 180.00, 'img/Img_Menu/Category 3 img 5.jpg', 3);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Summer Connection', 'Poke bowl con salmón marinado, aguacate, edamames y arroz sushi, aliñado con un toque de salsa de sésamo. Ligero y refrescante, perfecto para los días cálidos.', 250.00, 'img/Img_Menu/Category 3 img 6.png', 3);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Carnaval', 'Tempura de camarón y verduras, rebozado en una masa ligera y crujiente, servido con salsa tentsuyu casera.', 200.00, 'img/Img_Menu/Category 3 img 7.png', 3);

-- Postres (category_id = 4)
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Candy Hearts', 'Dorayaki: esponjosos panqueques japoneses rellenos de crema de fresa y frijol dulce. Un postre nostálgico y reconfortante.', 120.00, 'img/Img_Menu/Category 4 img 1.jpg', 4);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Lovers Paradise', 'Mochi de helado con sabores variados: matcha, fresa y vainilla, cubiertos con una ligera capa de arroz glutinoso. Suaves y dulces, ideales para compartir.', 140.00, 'img/Img_Menu/Category 4 img 2.jpg', 4);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Shyness Boy', 'Cheesecake japonés, ligero y esponjoso, con un toque de miel y frutos rojos.', 130.00, 'img/Img_Menu/Category 4 img 3.jpg', 4);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Summer Blue', 'Taiyaki crujiente relleno de crema de matcha y chocolate blanco.', 110.00, 'img/Img_Menu/Category 4 img 4.jpg', 4);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Midnight Pretenders', 'Helado de sésamo negro, con una textura cremosa y un sabor profundo y elegante.', 140.00, 'img/Img_Menu/Category 4 img 5.jpg', 4);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Please Let Me Wonder (PleWo)', 'Helado de vainilla con miel y almendras caramelizadas, servido con un toque de canela.', 130.00, 'img/Img_Menu/Category 4 img 6.jpg', 4);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Long Kiss Good Bye', 'Parfait de frutas con capas de crema batida, granola crujiente y un toque de jarabe de yuzu.', 150.00, 'img/Img_Menu/Category 4 img 7.jpeg', 4);

-- Bebidas (category_id = 5)
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Windy Summer', 'Té matcha frío con leche y un toque de miel, refrescante y cremoso.', 90.00, 'img/Img_Menu/Category 5 img 1.jpg', 5);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('September', 'Coctel de umeshu con soda y limón, un licor de ciruela japonés con un toque efervescente.', 120.00, 'img/Img_Menu/Category 5 img 2.jpg', 5);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Midnight Cruisin', 'Café japonés con un toque de licor de amaretto, perfecto para noches largas.', 130.00, 'img/Img_Menu/Category 5 img 3.jpg', 5);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Hot Stuff', 'Ginger ale con limón y un toque de jarabe de chile, burbujeante y con un ligero picante.', 100.00, 'img/Img_Menu/Category 5 img 4.png', 5);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Miss You, Miss Me', 'Batido de plátano y miel, cremoso y reconfortante.', 90.00, 'img/Img_Menu/Category 5 img 5.jpg', 5);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Springin Night', 'Frappe de matcha con leche condensada, ideal para una noche tranquila.', 110.00, 'img/Img_Menu/Category 5 img 6.jpg', 5);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('I Can\'t Stop the Loneliness', 'Coctel de sake con jugo de durazno, delicado y afrutado.', 140.00, 'img/Img_Menu/Category 5 img 7.jpg', 5);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Remember Summer Days', 'Té de jazmín helado con un toque de miel, evocando el verano.', 80.00, 'img/Img_Menu/Category 5 img 8.png', 5);

-- Entradas y Extras (category_id = 6)
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Dress Down', 'Ensalada de algas con tofu y ajonjolí, ligera y sofisticada.', 120.00, 'img/Img_Menu/Category 6 img 1.jpg', 6);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Wash', 'Sopa de miso tradicional con alga wakame, tofu y cebollín, un clásico reconfortante.', 80.00, 'img/Img_Menu/Category 6 img 2.png', 6);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Loveland Island', 'Edamames al vapor con sal de mar, el snack perfecto para acompañar cualquier platillo.', 90.00, 'img/Img_Menu/Category 6 img 3.jpg', 6);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Love Space', 'Gyoza de cerdo doradas a la plancha, rellenas de carne jugosa con un toque de ajo y jengibre.', 140.00, 'img/Img_Menu/Category 6 img 4.jpg', 6);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('Summer Goddess', 'Ramune de melón, una gaseosa japonesa chispeante y refrescante.', 70.00, 'img/Img_Menu/Category 6 img 5.png', 6);
INSERT INTO dishes(name, descr, price, image, category_id) VALUES('I\'m in Love (inlove)', 'Onigiri relleno de salmón o umeboshi (ciruela encurtida), envuelto en alga nori.', 100.00, 'img/Img_Menu/Category 6 img 6.jpg', 6);


-- Tabla de carritos 
CREATE TABLE IF NOT EXISTS carts (
    id INT AUTO_INCREMENT PRIMARY KEY,
    user_id SMALLINT UNSIGNED NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    active TINYINT(1) NOT NULL DEFAULT 1, -- 1 para activo, 0 para inactivo
    FOREIGN KEY (user_id) REFERENCES users(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de detalles del carrito 
CREATE TABLE IF NOT EXISTS cart_items (
    id INT AUTO_INCREMENT PRIMARY KEY,
    cart_id INT NOT NULL,
    dish_id INT NOT NULL,
    quantity INT NOT NULL DEFAULT 1,
    FOREIGN KEY (cart_id) REFERENCES carts(id) ON DELETE CASCADE,
    FOREIGN KEY (dish_id) REFERENCES dishes(id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

-- Tabla de pedidos
CREATE TABLE IF NOT EXISTS orders (
    order_id SMALLINT UNSIGNED NOT NULL AUTO_INCREMENT,
    owner_id SMALLINT UNSIGNED NOT NULL,
    order_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    cost DECIMAL(10, 2) NOT NULL,
    delivered BOOLEAN NOT NULL DEFAULT FALSE,
    PRIMARY KEY (order_id),
    FOREIGN KEY (owner_id) REFERENCES users(id)
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


CALL sp_AddUser('Edgar@gmail.com','123','Edgar','0');

CALL sp_AddUser('Sebastian@gmail.com','123','Sebastian','0');

CALL sp_AddUser('Ricardo@gmail.com','123','Ricardo','1');

CALL sp_AddUser('Miguel@gmail.com','123','Miguel','2');