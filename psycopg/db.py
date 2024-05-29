def create_tables(conn, cursor):
    print("Creating tables...")
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS Companies (
        company_id SERIAL PRIMARY KEY,
        company_name VARCHAR UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Products (
        product_id SERIAL PRIMARY KEY,
        company_id SERIAL REFERENCES Companies (company_id) ON DELETE CASCADE,
        product_name VARCHAR UNIQUE NOT NULL,
        price INTEGER,
        description VARCHAR,
        active BOOLEAN DEFAULT true
        );

        CREATE TABLE IF NOT EXISTS Warranties (
        warranty_id SERIAL PRIMARY KEY,
        product_id SERIAL REFERENCES Products (product_id) ON DELETE CASCADE,
        warranty_months VARCHAR NOT NULL
        );

        CREATE TABLE IF NOT EXISTS Categories (
        category_id SERIAL PRIMARY KEY,
        category_name VARCHAR UNIQUE NOT NULL
        );

        CREATE TABLE IF NOT EXISTS ProductsCategoriesXref (
        product_id SERIAL REFERENCES Products (product_id) ON DELETE CASCADE,
        category_id SERIAL REFERENCES Categories (category_id) ON DELETE CASCADE,
        PRIMARY KEY(product_id, category_id)
        );
    """)
    conn.commit()
