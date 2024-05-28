def create_tables(conn, cursor):
    print("Creating tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Products (
        product_id SERIAL PRIMARY KEY,
        product_name VARCHAR NOT NULL UNIQUE,
        description VARCHAR,
        price FLOAT,
        active BOOLEAN DEFAULT true
        );
    """)
    conn.commit()
