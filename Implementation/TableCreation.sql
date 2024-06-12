CREATE DATABASE CAFETERIA;
USE CAFETERIA;

CREATE TABLE Roles (
    role_id INT AUTO_INCREMENT PRIMARY KEY,
    role_name VARCHAR(50) NOT NULL
);

CREATE TABLE Users (
    user_id varchar(32) PRIMARY KEY,
    user_name VARCHAR(100) NOT NULL,
    user_role varchar,
    FOREIGN KEY (user_role) REFERENCES Roles(role_id)
);

CREATE TABLE MenuItems (
    menu_item_id INT AUTO_INCREMENT PRIMARY KEY,
    menu_item_name VARCHAR(100) NOT NULL,
    price DECIMAL(10, 2) NOT NULL,
    availability TINYINT(1) NOT NULL
);

CREATE TABLE Feedback (
    feedback_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    menu_item_id INT,
    comment TEXT,
    rating INT,
    feedback_date DATE,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id)
);

CREATE TABLE Recommendations (
    recommendation_id INT AUTO_INCREMENT PRIMARY KEY,
    menu_item_id INT,
    date DATE,
    meal_type ENUM('Breakfast', 'Lunch', 'Dinner'),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id)
);

CREATE TABLE UserPreference (
    preference_id INT AUTO_INCREMENT PRIMARY KEY,
    user_id INT,
    menu_item_id INT,
    FOREIGN KEY (user_id) REFERENCES Users(user_id),
    FOREIGN KEY (menu_item_id) REFERENCES MenuItems(menu_item_id)
);
