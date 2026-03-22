CREATE DATABASE IF NOT EXISTS smart_agriculture;
USE smart_agriculture;

CREATE TABLE IF NOT EXISTS login (
    admin_id VARCHAR(50) PRIMARY KEY,
    password VARCHAR(100) NOT NULL
);

INSERT IGNORE INTO login VALUES ('admin', 'admin123');

CREATE TABLE IF NOT EXISTS farmer_register (
    farmer_id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    phone VARCHAR(15) NOT NULL,
    password VARCHAR(100) NOT NULL,
    city VARCHAR(100) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    status ENUM('request','approved','rejected','pending') DEFAULT 'request'
);

CREATE TABLE IF NOT EXISTS user_register (
    user_id VARCHAR(50) PRIMARY KEY,
    first_name VARCHAR(100) NOT NULL,
    last_name VARCHAR(100) NOT NULL,
    phone VARCHAR(15) NOT NULL,
    email VARCHAR(150) NOT NULL,
    pincode VARCHAR(10) NOT NULL,
    city VARCHAR(100) NOT NULL,
    address TEXT NOT NULL,
    state VARCHAR(100) NOT NULL,
    country VARCHAR(100) NOT NULL,
    password VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    price DECIMAL(10,2) NOT NULL,
    farmer_price DECIMAL(10,2) NOT NULL
);

CREATE TABLE IF NOT EXISTS item_details (
    iditem_details INT AUTO_INCREMENT PRIMARY KEY,
    category_id INT NOT NULL,
    farmer_id VARCHAR(50) NOT NULL,
    date_added DATE NOT NULL,
    quantity INT NOT NULL,
    total_amount DECIMAL(10,2) NOT NULL,
    status ENUM('pending','approved','rejected') DEFAULT 'pending',
    item_description TEXT,
    FOREIGN KEY (category_id) REFERENCES category(category_id) ON DELETE CASCADE,
    FOREIGN KEY (farmer_id) REFERENCES farmer_register(farmer_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS user_booking (
    iduser_booking INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    iditem_details INT NOT NULL,
    booking_date DATE NOT NULL,
    shipping_address TEXT NOT NULL,
    total_amount_user DECIMAL(10,2) NOT NULL,
    status ENUM('ADDED','Paid','Delivered','Cancelled') DEFAULT 'ADDED',
    FOREIGN KEY (user_id) REFERENCES user_register(user_id) ON DELETE CASCADE,
    FOREIGN KEY (iditem_details) REFERENCES item_details(iditem_details) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS compliant (
    idcompliant INT AUTO_INCREMENT PRIMARY KEY,
    user_id VARCHAR(50) NOT NULL,
    details TEXT NOT NULL,
    date_sent DATE NOT NULL,
    reply TEXT DEFAULT NULL,
    status ENUM('pending','replied') DEFAULT 'pending',
    FOREIGN KEY (user_id) REFERENCES user_register(user_id) ON DELETE CASCADE
);

CREATE TABLE IF NOT EXISTS bank (
    card_no VARCHAR(20) PRIMARY KEY,
    card_holder_name VARCHAR(100) NOT NULL,
    cvv_no VARCHAR(5) NOT NULL,
    expiry_date DATE NOT NULL
);

INSERT IGNORE INTO bank VALUES ('4111111111111111','Test User','123','2027-12-31');
