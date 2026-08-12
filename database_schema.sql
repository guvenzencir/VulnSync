CREATE DATABASE IF NOT EXISTS vulnsync_db;
USE vulnsync_db;

CREATE TABLE IF NOT EXISTS exploits (
    id INT PRIMARY KEY,
    title VARCHAR(500) NOT NULL,
    type VARCHAR(100),
    platform VARCHAR(100),
    author VARCHAR(255),
    link VARCHAR(500),
    discovered_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
