import os

from flask import jsonify
import psycopg2

database_name = os.environ.get('DATABASE_NAME')
conn = psycopg2.connect(f"dbname={database_name}")
cursor = conn.cursor()


def company_create(request):
    post_data = request.form if request.form else request.json
    company_name = post_data['company_name']

    if not company_name:
        return jsonify({"message": "company_name is a Required Field"}), 400

    result = cursor.execute("""
        SELECT * FROM Companies
        WHERE company_name=%s""",
                            [company_name])
    result = cursor.fetchone()
    if result:
        return jsonify({"message": 'company already exists'}), 400

    try:
        cursor.execute(
            """
            INSERT INTO Companies
            (company_name)
            VALUES(%s);
            """,
            [company_name]
        )
        conn.commit()

        return jsonify({"message": f"{company_name} has been added to the Companies table."}), 200

    except Exception as e:
        print(e)
        return jsonify({"message": "Company could not be added"}), 404


def companies_get():
    try:
        cursor.execute(
            """
            SELECT *
            FROM Companies;
            """
        )
        results = cursor.fetchall()
        if results:
            company_list = []

            for company in results:
                company_record = {
                    'company_id': company[0],
                    'company_name': company[1]
                }

                company_list.append(company_record)

            return jsonify(({"message": "companies found", "result": company_list})), 200
        else:
            return jsonify(({"message": f"No companies found"})), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Could not fetch companies data"}), 404


def company_get_by_id(company_id):
    try:
        cursor.execute(
            """
            SELECT *
            FROM Companies
            WHERE company_id=%s;
            """, [company_id]
        )
        result = cursor.fetchone()

        if result:
            company_list = []

            company_record = {
                'company_id': result[0],
                'company_name': result[1]
            }

            company_list.append(company_record)

            return jsonify(({"message": f"company with id {company_id} found", "result": company_list})), 200
        else:
            return jsonify(({"message": "No company found"})), 404
    except Exception as e:
        print(e)
        return jsonify({"message": "Could not fetch company data"}), 404


def company_update_by_id(request, company_id):
    post_data = request.form if request.form else request.json
    company_name = post_data['company_name']

    if not company_name:
        return jsonify({"message": "company_name is a Required Field"}), 400

    try:
        cursor.execute("""
            UPDATE Companies
            SET company_name=%s
            WHERE company_id=%s""",
                       [company_name, company_id])
        conn.commit()

        cursor.execute(
            """
            SELECT *
            FROM Companies
            WHERE company_id=%s;
            """, [company_id]
        )
        result = cursor.fetchone()

        if result:
            company_list = []

            company_record = {
                'company_id': result[0],
                'company_name': result[1]
            }

            company_list.append(company_record)

            return jsonify(({"message": f"{company_name} has been updated", "result": company_list})), 200
        else:
            return jsonify(({"message": "No company found"})), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "Company could not be updated"}), 404


def company_delete(company_id):
    company = {}
    company['company_id'] = int(company_id)

    print('company: ', company)
    if not company['company_id']:
        return jsonify({"message": 'company_id is required'}), 400

    try:
        cursor.execute(
            """
            SELECT *
            FROM Companies
            WHERE company_id=%s;
            """, [company_id]
        )
        result = cursor.fetchone()

        if result:
            cursor.execute("""
                DELETE FROM Companies
                WHERE company_id=%s
                """, [company_id])
            conn.commit()

            return jsonify({"message": f"company with id {company_id} has been deleted."}), 200
        else:
            return jsonify({"message": f"no company exists with id {company_id}"}), 404

    except Exception as e:
        print(e)
        return jsonify({"message": "company could not be deleted"}), 404
