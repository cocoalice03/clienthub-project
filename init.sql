-- Création de la table clients
CREATE TABLE IF NOT EXISTS clients (
    id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(255) NOT NULL
);

-- Insertion de données de test initiales
INSERT INTO clients (name) VALUES 
('Colombe MADOUNGOU'),
('Justin BIEBER'),
('Tiakola LAMELO');