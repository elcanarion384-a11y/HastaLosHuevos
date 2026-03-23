DROP TABLE IF EXISTS ramas_recomendadas;
DROP TABLE IF EXISTS respuestas_usuario;

CREATE TABLE ramas_recomendadas (
    id SERIAL PRIMARY KEY,
    branch_name VARCHAR(255) NOT NULL,
    recommended_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE respuestas_usuario (
    id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    response_data JSONB NOT NULL,
    submitted_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
