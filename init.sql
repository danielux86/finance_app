CREATE USER IF NOT EXISTS 'server'@'localhost' IDENTIFIED BY '1234';

GRANT ALL PRIVILEGES ON *.* TO 'server'@'localhost';

CREATE TABLE utenti (
    email VARCHAR(100) NOT NULL UNIQUE PRIMARY KEY,
    ticker VARCHAR(5) NOT NULL
);

CREATE TABLE data (
    id INT AUTO_INCREMENT PRIMARY KEY,
    email VARCHAR(100) NOT NULL,
    ticker VARCHAR(5) NOT NULL,
    valore FLOAT(10),
    timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (email) REFERENCES utenti(email)
);