import sqlite3
import os

DB_DIR = os.environ.get("DB_DIR", os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else ".")
DB_PATH = os.path.join(DB_DIR, "vocacional.db")


def create_tables(cur):
    cur.execute("DROP TABLE IF EXISTS estudios")
    cur.execute("DROP TABLE IF EXISTS tipos_estudio")
    cur.execute("DROP TABLE IF EXISTS islas")
    cur.execute("DROP TABLE IF EXISTS respuestas")
    cur.execute("DROP TABLE IF EXISTS numeric_responses;")
    cur.execute("CREATE TABLE numeric_responses (id SERIAL PRIMARY KEY, question_id INT, response INT CHECK (response >= 1 AND response <= 5));")
    cur.excecute("""CREATE TABLE islas (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)
    
    cur.execute("""
        CREATE TABLE tipos_estudio (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        )
    """)

    cur.execute("""
        CREATE TABLE estudios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            isla_id INTEGER NOT NULL,
            tipo_id INTEGER NOT NULL,
            categoria TEXT NOT NULL,
            FOREIGN KEY (isla_id) REFERENCES islas(id),
            FOREIGN KEY (tipo_id) REFERENCES tipos_estudio(id)
        )
    """)


def seed_data(cur):
    # --- Islas ---
    islas = [
        "Tenerife", "Gran Canaria", "Lanzarote", "Fuerteventura",
        "La Palma", "La Gomera", "El Hierro"
    ]
    for isla in islas:
        cur.execute("INSERT INTO islas (nombre) VALUES (?)", (isla,))

    # --- Tipos de estudio ---
    tipos = ["Grado Universitario", "Ciclo Formativo Grado Superior", "Ciclo Formativo Grado Medio"]
    for t in tipos:
        cur.execute("INSERT INTO tipos_estudio (nombre) VALUES (?)", (t,))

    # Mapeo de IDs
    cur.execute("SELECT id, nombre FROM islas")
    isla_map = {row[1]: row[0] for row in cur.fetchall()}

    cur.execute("SELECT id, nombre FROM tipos_estudio")
    tipo_map = {row[1]: row[0] for row in cur.fetchall()}

    GRADO = tipo_map["Grado Universitario"]
    CFGS = tipo_map["Ciclo Formativo Grado Superior"]
    CFGM = tipo_map["Ciclo Formativo Grado Medio"]

    # Categorias vocacionales (coinciden con questionnaire-data)
    # sanitario, tecnologico, economico, artistico, deportivo, social_juridico, humanistico, agropecuario_maritimo

    # =============================================
    # TENERIFE - Oferta completa (ULL + ciclos)
    # =============================================
    tf = isla_map["Tenerife"]

    estudios_tf = [
        # --- Sanitario ---
        ("Grado en Medicina", tf, GRADO, "sanitario"),
        ("Grado en Enfermeria", tf, GRADO, "sanitario"),
        ("Grado en Farmacia", tf, GRADO, "sanitario"),
        ("Grado en Psicologia", tf, GRADO, "sanitario"),
        ("Grado en Fisioterapia", tf, GRADO, "sanitario"),
        ("Grado en Logopedia", tf, GRADO, "sanitario"),
        ("T.S. en Laboratorio Clinico y Biomedico", tf, CFGS, "sanitario"),
        ("T.S. en Imagen para el Diagnostico y Medicina Nuclear", tf, CFGS, "sanitario"),
        ("T.S. en Higiene Bucodental", tf, CFGS, "sanitario"),
        ("T.S. en Dietética", tf, CFGS, "sanitario"),
        ("T.M. en Cuidados Auxiliares de Enfermeria", tf, CFGM, "sanitario"),
        ("T.M. en Farmacia y Parafarmacia", tf, CFGM, "sanitario"),
        ("T.M. en Emergencias Sanitarias", tf, CFGM, "sanitario"),

        # --- Tecnologico ---
        ("Grado en Ingenieria Informatica", tf, GRADO, "tecnologico"),
        ("Grado en Ingenieria Industrial", tf, GRADO, "tecnologico"),
        ("Grado en Ingenieria Electronica y Automatica", tf, GRADO, "tecnologico"),
        ("Grado en Ingenieria Civil", tf, GRADO, "tecnologico"),
        ("Grado en Ingenieria Quimica", tf, GRADO, "tecnologico"),
        ("Grado en Arquitectura Tecnica", tf, GRADO, "tecnologico"),
        ("T.S. en Desarrollo de Aplicaciones Web", tf, CFGS, "tecnologico"),
        ("T.S. en Desarrollo de Aplicaciones Multiplataforma", tf, CFGS, "tecnologico"),
        ("T.S. en Administracion de Sistemas Informaticos en Red", tf, CFGS, "tecnologico"),
        ("T.S. en Automatizacion y Robotica Industrial", tf, CFGS, "tecnologico"),
        ("T.S. en Energias Renovables", tf, CFGS, "tecnologico"),
        ("T.M. en Sistemas Microinformaticos y Redes", tf, CFGM, "tecnologico"),
        ("T.M. en Instalaciones Electricas y Automaticas", tf, CFGM, "tecnologico"),

        # --- Economico ---
        ("Grado en Administracion y Direccion de Empresas", tf, GRADO, "economico"),
        ("Grado en Economia", tf, GRADO, "economico"),
        ("Grado en Contabilidad y Finanzas", tf, GRADO, "economico"),
        ("Grado en Turismo", tf, GRADO, "economico"),
        ("T.S. en Administracion y Finanzas", tf, CFGS, "economico"),
        ("T.S. en Comercio Internacional", tf, CFGS, "economico"),
        ("T.S. en Gestion de Alojamientos Turisticos", tf, CFGS, "economico"),
        ("T.S. en Agencias de Viajes y Gestion de Eventos", tf, CFGS, "economico"),
        ("T.M. en Gestion Administrativa", tf, CFGM, "economico"),
        ("T.M. en Actividades Comerciales", tf, CFGM, "economico"),

        # --- Artistico ---
        ("Grado en Bellas Artes", tf, GRADO, "artistico"),
        ("Grado en Diseno", tf, GRADO, "artistico"),
        ("Grado en Historia del Arte", tf, GRADO, "artistico"),
        ("T.S. en Animaciones 3D, Juegos y Entornos Interactivos", tf, CFGS, "artistico"),
        ("T.S. en Iluminacion, Captacion y Tratamiento de Imagen", tf, CFGS, "artistico"),
        ("T.S. en Sonido para Audiovisuales y Espectaculos", tf, CFGS, "artistico"),
        ("T.M. en Video Disc-Jockey y Sonido", tf, CFGM, "artistico"),

        # --- Deportivo ---
        ("Grado en Ciencias de la Actividad Fisica y del Deporte", tf, GRADO, "deportivo"),
        ("T.S. en Acondicionamiento Fisico", tf, CFGS, "deportivo"),
        ("T.S. en Ensenanza y Animacion Sociodeportiva", tf, CFGS, "deportivo"),
        ("T.M. en Conduccion de Actividades Fisico-Deportivas en el Medio Natural", tf, CFGM, "deportivo"),

        # --- Social/Juridico ---
        ("Grado en Derecho", tf, GRADO, "social_juridico"),
        ("Grado en Trabajo Social", tf, GRADO, "social_juridico"),
        ("Grado en Relaciones Laborales", tf, GRADO, "social_juridico"),
        ("Grado en Sociologia", tf, GRADO, "social_juridico"),
        ("T.S. en Integracion Social", tf, CFGS, "social_juridico"),
        ("T.S. en Educacion Infantil", tf, CFGS, "social_juridico"),
        ("T.S. en Mediacion Comunicativa", tf, CFGS, "social_juridico"),
        ("T.M. en Atencion a Personas en Situacion de Dependencia", tf, CFGM, "social_juridico"),

        # --- Humanistico ---
        ("Grado en Historia", tf, GRADO, "humanistico"),
        ("Grado en Estudios Clasicos", tf, GRADO, "humanistico"),
        ("Grado en Filologia Hispanica", tf, GRADO, "humanistico"),
        ("Grado en Filosofia", tf, GRADO, "humanistico"),
        ("Grado en Periodismo", tf, GRADO, "humanistico"),
        ("Grado en Maestro en Educacion Primaria", tf, GRADO, "humanistico"),
        ("Grado en Maestro en Educacion Infantil", tf, GRADO, "humanistico"),

        # --- Agropecuario/Maritimo ---
        ("Grado en Biologia", tf, GRADO, "agropecuario_maritimo"),
        ("Grado en Ciencias del Mar", tf, GRADO, "agropecuario_maritimo"),
        ("Grado en Ciencias Ambientales", tf, GRADO, "agropecuario_maritimo"),
        ("T.S. en Gestion Forestal y del Medio Natural", tf, CFGS, "agropecuario_maritimo"),
        ("T.S. en Ganaderia y Asistencia en Sanidad Animal", tf, CFGS, "agropecuario_maritimo"),
        ("T.M. en Produccion Agroecologica", tf, CFGM, "agropecuario_maritimo"),
        ("T.M. en Actividades Maritimo-Pesqueras", tf, CFGM, "agropecuario_maritimo"),
        ("T.M. en Aprovechamiento y Conservacion del Medio Natural", tf, CFGM, "agropecuario_maritimo"),
    ]

    for e in estudios_tf:
        cur.execute("INSERT INTO estudios (nombre, isla_id, tipo_id, categoria) VALUES (?,?,?,?)", e)

    # =============================================
    # GRAN CANARIA - Oferta completa (ULPGC + ciclos)
    # =============================================
    gc = isla_map["Gran Canaria"]

    estudios_gc = [
        # Sanitario
        ("Grado en Medicina", gc, GRADO, "sanitario"),
        ("Grado en Enfermeria", gc, GRADO, "sanitario"),
        ("Grado en Fisioterapia", gc, GRADO, "sanitario"),
        ("Grado en Veterinaria", gc, GRADO, "sanitario"),
        ("T.S. en Laboratorio Clinico y Biomedico", gc, CFGS, "sanitario"),
        ("T.S. en Higiene Bucodental", gc, CFGS, "sanitario"),
        ("T.S. en Protesica Dental", gc, CFGS, "sanitario"),
        ("T.M. en Cuidados Auxiliares de Enfermeria", gc, CFGM, "sanitario"),
        ("T.M. en Farmacia y Parafarmacia", gc, CFGM, "sanitario"),

        # Tecnologico
        ("Grado en Ingenieria Informatica", gc, GRADO, "tecnologico"),
        ("Grado en Ingenieria de Telecomunicaciones", gc, GRADO, "tecnologico"),
        ("Grado en Ingenieria Mecanica", gc, GRADO, "tecnologico"),
        ("Grado en Arquitectura", gc, GRADO, "tecnologico"),
        ("T.S. en Desarrollo de Aplicaciones Web", gc, CFGS, "tecnologico"),
        ("T.S. en Desarrollo de Aplicaciones Multiplataforma", gc, CFGS, "tecnologico"),
        ("T.S. en Administracion de Sistemas Informaticos en Red", gc, CFGS, "tecnologico"),
        ("T.S. en Energias Renovables", gc, CFGS, "tecnologico"),
        ("T.M. en Sistemas Microinformaticos y Redes", gc, CFGM, "tecnologico"),
        ("T.M. en Instalaciones de Telecomunicaciones", gc, CFGM, "tecnologico"),

        # Economico
        ("Grado en Administracion y Direccion de Empresas", gc, GRADO, "economico"),
        ("Grado en Economia", gc, GRADO, "economico"),
        ("Grado en Turismo", gc, GRADO, "economico"),
        ("T.S. en Administracion y Finanzas", gc, CFGS, "economico"),
        ("T.S. en Comercio Internacional", gc, CFGS, "economico"),
        ("T.S. en Gestion de Alojamientos Turisticos", gc, CFGS, "economico"),
        ("T.M. en Gestion Administrativa", gc, CFGM, "economico"),
        ("T.M. en Actividades Comerciales", gc, CFGM, "economico"),

        # Artistico
        ("Grado en Diseno", gc, GRADO, "artistico"),
        ("T.S. en Animaciones 3D, Juegos y Entornos Interactivos", gc, CFGS, "artistico"),
        ("T.S. en Sonido para Audiovisuales y Espectaculos", gc, CFGS, "artistico"),
        ("T.M. en Video Disc-Jockey y Sonido", gc, CFGM, "artistico"),

        # Deportivo
        ("Grado en Ciencias de la Actividad Fisica y del Deporte", gc, GRADO, "deportivo"),
        ("T.S. en Acondicionamiento Fisico", gc, CFGS, "deportivo"),
        ("T.S. en Ensenanza y Animacion Sociodeportiva", gc, CFGS, "deportivo"),
        ("T.M. en Conduccion de Actividades Fisico-Deportivas en el Medio Natural", gc, CFGM, "deportivo"),

        # Social/Juridico
        ("Grado en Derecho", gc, GRADO, "social_juridico"),
        ("Grado en Trabajo Social", gc, GRADO, "social_juridico"),
        ("Grado en Relaciones Laborales", gc, GRADO, "social_juridico"),
        ("T.S. en Integracion Social", gc, CFGS, "social_juridico"),
        ("T.S. en Educacion Infantil", gc, CFGS, "social_juridico"),
        ("T.M. en Atencion a Personas en Situacion de Dependencia", gc, CFGM, "social_juridico"),

        # Humanistico
        ("Grado en Historia", gc, GRADO, "humanistico"),
        ("Grado en Lengua Espanola y Literaturas Hispanicas", gc, GRADO, "humanistico"),
        ("Grado en Lenguas Modernas", gc, GRADO, "humanistico"),
        ("Grado en Geografia y Ordenacion del Territorio", gc, GRADO, "humanistico"),
        ("Grado en Maestro en Educacion Primaria", gc, GRADO, "humanistico"),
        ("Grado en Maestro en Educacion Infantil", gc, GRADO, "humanistico"),

        # Agropecuario/Maritimo
        ("Grado en Biologia", gc, GRADO, "agropecuario_maritimo"),
        ("Grado en Ciencias del Mar", gc, GRADO, "agropecuario_maritimo"),
        ("Grado en Ingenieria Nautica y Transporte Maritimo", gc, GRADO, "agropecuario_maritimo"),
        ("T.S. en Gestion Forestal y del Medio Natural", gc, CFGS, "agropecuario_maritimo"),
        ("T.M. en Produccion Agroecologica", gc, CFGM, "agropecuario_maritimo"),
        ("T.M. en Actividades Maritimo-Pesqueras", gc, CFGM, "agropecuario_maritimo"),
    ]

    for e in estudios_gc:
        cur.execute("INSERT INTO estudios (nombre, isla_id, tipo_id, categoria) VALUES (?,?,?,?)", e)

    # =============================================
    # LANZAROTE - Oferta reducida (ciclos + sede UNED)
    # =============================================
    lz = isla_map["Lanzarote"]

    estudios_lz = [
        ("T.S. en Laboratorio Clinico y Biomedico", lz, CFGS, "sanitario"),
        ("T.M. en Cuidados Auxiliares de Enfermeria", lz, CFGM, "sanitario"),
        ("T.M. en Farmacia y Parafarmacia", lz, CFGM, "sanitario"),
        ("T.S. en Desarrollo de Aplicaciones Web", lz, CFGS, "tecnologico"),
        ("T.S. en Administracion de Sistemas Informaticos en Red", lz, CFGS, "tecnologico"),
        ("T.M. en Sistemas Microinformaticos y Redes", lz, CFGM, "tecnologico"),
        ("T.M. en Instalaciones Electricas y Automaticas", lz, CFGM, "tecnologico"),
        ("T.S. en Administracion y Finanzas", lz, CFGS, "economico"),
        ("T.S. en Gestion de Alojamientos Turisticos", lz, CFGS, "economico"),
        ("T.M. en Gestion Administrativa", lz, CFGM, "economico"),
        ("T.M. en Actividades Comerciales", lz, CFGM, "economico"),
        ("T.S. en Integracion Social", lz, CFGS, "social_juridico"),
        ("T.S. en Educacion Infantil", lz, CFGS, "social_juridico"),
        ("T.M. en Atencion a Personas en Situacion de Dependencia", lz, CFGM, "social_juridico"),
        ("T.S. en Acondicionamiento Fisico", lz, CFGS, "deportivo"),
        ("T.M. en Conduccion de Actividades Fisico-Deportivas en el Medio Natural", lz, CFGM, "deportivo"),
        ("T.M. en Produccion Agroecologica", lz, CFGM, "agropecuario_maritimo"),
        ("T.M. en Actividades Maritimo-Pesqueras", lz, CFGM, "agropecuario_maritimo"),
    ]

    for e in estudios_lz:
        cur.execute("INSERT INTO estudios (nombre, isla_id, tipo_id, categoria) VALUES (?,?,?,?)", e)

    # =============================================
    # FUERTEVENTURA - Oferta reducida
    # =============================================
    fv = isla_map["Fuerteventura"]

    estudios_fv = [
        ("T.M. en Cuidados Auxiliares de Enfermeria", fv, CFGM, "sanitario"),
        ("T.M. en Farmacia y Parafarmacia", fv, CFGM, "sanitario"),
        ("T.M. en Emergencias Sanitarias", fv, CFGM, "sanitario"),
        ("T.S. en Desarrollo de Aplicaciones Web", fv, CFGS, "tecnologico"),
        ("T.M. en Sistemas Microinformaticos y Redes", fv, CFGM, "tecnologico"),
        ("T.M. en Instalaciones Electricas y Automaticas", fv, CFGM, "tecnologico"),
        ("T.S. en Administracion y Finanzas", fv, CFGS, "economico"),
        ("T.S. en Gestion de Alojamientos Turisticos", fv, CFGS, "economico"),
        ("T.M. en Gestion Administrativa", fv, CFGM, "economico"),
        ("T.S. en Educacion Infantil", fv, CFGS, "social_juridico"),
        ("T.M. en Atencion a Personas en Situacion de Dependencia", fv, CFGM, "social_juridico"),
        ("T.S. en Acondicionamiento Fisico", fv, CFGS, "deportivo"),
        ("T.M. en Produccion Agroecologica", fv, CFGM, "agropecuario_maritimo"),
    ]

    for e in estudios_fv:
        cur.execute("INSERT INTO estudios (nombre, isla_id, tipo_id, categoria) VALUES (?,?,?,?)", e)

    # =============================================
    # LA PALMA - Oferta reducida
    # =============================================
    lp = isla_map["La Palma"]

    estudios_lp = [
        ("T.M. en Cuidados Auxiliares de Enfermeria", lp, CFGM, "sanitario"),
        ("T.M. en Farmacia y Parafarmacia", lp, CFGM, "sanitario"),
        ("T.S. en Desarrollo de Aplicaciones Web", lp, CFGS, "tecnologico"),
        ("T.M. en Sistemas Microinformaticos y Redes", lp, CFGM, "tecnologico"),
        ("T.M. en Instalaciones Electricas y Automaticas", lp, CFGM, "tecnologico"),
        ("T.S. en Energias Renovables", lp, CFGS, "tecnologico"),
        ("T.S. en Administracion y Finanzas", lp, CFGS, "economico"),
        ("T.M. en Gestion Administrativa", lp, CFGM, "economico"),
        ("T.S. en Educacion Infantil", lp, CFGS, "social_juridico"),
        ("T.M. en Atencion a Personas en Situacion de Dependencia", lp, CFGM, "social_juridico"),
        ("T.S. en Gestion Forestal y del Medio Natural", lp, CFGS, "agropecuario_maritimo"),
        ("T.M. en Produccion Agroecologica", lp, CFGM, "agropecuario_maritimo"),
        ("T.M. en Aprovechamiento y Conservacion del Medio Natural", lp, CFGM, "agropecuario_maritimo"),
    ]

    for e in estudios_lp:
        cur.execute("INSERT INTO estudios (nombre, isla_id, tipo_id, categoria) VALUES (?,?,?,?)", e)

    # =============================================
    # LA GOMERA - Oferta minima
    # =============================================
    lg = isla_map["La Gomera"]

    estudios_lg = [
        ("T.M. en Cuidados Auxiliares de Enfermeria", lg, CFGM, "sanitario"),
        ("T.M. en Sistemas Microinformaticos y Redes", lg, CFGM, "tecnologico"),
        ("T.M. en Gestion Administrativa", lg, CFGM, "economico"),
        ("T.M. en Atencion a Personas en Situacion de Dependencia", lg, CFGM, "social_juridico"),
        ("T.M. en Produccion Agroecologica", lg, CFGM, "agropecuario_maritimo"),
        ("T.M. en Aprovechamiento y Conservacion del Medio Natural", lg, CFGM, "agropecuario_maritimo"),
    ]

    for e in estudios_lg:
        cur.execute("INSERT INTO estudios (nombre, isla_id, tipo_id, categoria) VALUES (?,?,?,?)", e)

    # =============================================
    # EL HIERRO - Oferta minima
    # =============================================
    eh = isla_map["El Hierro"]

    estudios_eh = [
        ("T.M. en Cuidados Auxiliares de Enfermeria", eh, CFGM, "sanitario"),
        ("T.M. en Sistemas Microinformaticos y Redes", eh, CFGM, "tecnologico"),
        ("T.M. en Gestion Administrativa", eh, CFGM, "economico"),
        ("T.M. en Atencion a Personas en Situacion de Dependencia", eh, CFGM, "social_juridico"),
        ("T.M. en Produccion Agroecologica", eh, CFGM, "agropecuario_maritimo"),
    ]

    for e in estudios_eh:
        cur.execute("INSERT INTO estudios (nombre, isla_id, tipo_id, categoria) VALUES (?,?,?,?)", e)


def main():
    if os.path.exists(DB_PATH):
        os.remove(DB_PATH)
        print(f"Base de datos anterior eliminada: {DB_PATH}")

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    create_tables(cur)
    seed_data(cur)

    conn.commit()

    # Verificar
    cur.execute("SELECT COUNT(*) FROM islas")
    print(f"Islas: {cur.fetchone()[0]}")

    cur.execute("SELECT COUNT(*) FROM tipos_estudio")
    print(f"Tipos de estudio: {cur.fetchone()[0]}")

    cur.execute("SELECT COUNT(*) FROM estudios")
    print(f"Estudios totales: {cur.fetchone()[0]}")

    cur.execute("""
        SELECT i.nombre, COUNT(e.id)
        FROM islas i
        LEFT JOIN estudios e ON e.isla_id = i.id
        GROUP BY i.id
        ORDER BY COUNT(e.id) DESC
    """)
    print("\nEstudios por isla:")
    for row in cur.fetchall():
        print(f"  {row[0]}: {row[1]}")

    conn.close()
    print(f"\nBase de datos creada exitosamente en: {DB_PATH}")


if __name__ == "__main__":
    main()
