import mysql.connector
from mysql.connector import Error
from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

DB_CONFIG = {
    'host': 'localhost',
    'user': 'deepak711',
    'password': 'deepak711',
    'database': 'blueoptimadashboard'
}

def get_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f'Error: {e}')
        return None
    
@app.route('/bce-detail', methods=['GET'])
def get_bce_detail():
    year = int(request.args.get('year', 2025))
    month = int(request.args.get('month', 11))
    bce_min = float(request.args.get('bceMin', 0))
    bce_max = request.args.get('bceMax')
    bce_max = float(bce_max) if bce_max and bce_max != 'null' else None

    filter_cols = [
        'Country', 'Employer', 'Segment', 'JobRole', 'Prod_Bucket', 'Engineer_Level', 'HCL_Manager_email'
    ]
    filters = [ "m.Year = %s", "m.Month = %s" ]
    params = [year, month]
    for col in filter_cols:
        val = request.args.get(col)
        if val:
            filters.append(f"d.{col} = %s")
            params.append(val)
    filters.append("m.BCE_Per_Day >= %s")
    params.append(bce_min)
    if bce_max is not None:
        filters.append("m.BCE_Per_Day < %s")
        params.append(bce_max)

    query = f"""
        SELECT d.UID, d.Developer_First_name, d.Developer_Last_name, m.BCE_Per_Day, m.Justification_Category
        FROM developers d
        JOIN developers_monthly_stats m ON d.UID = m.UID
        WHERE {' AND '.join(filters)}
        ORDER BY m.BCE_Per_Day ASC
    """

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/bce-justification', methods=['POST'])
def update_bce_justification():
    data = request.get_json()
    uid = data.get('uid')
    year = int(data.get('year', 2025))
    month = int(data.get('month', 11))
    category = data.get('category')
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute(
        "UPDATE developers_monthly_stats SET Justification_Category = %s WHERE UID = %s AND Year = %s AND Month = %s",
        (category, uid, year, month)
    )
    conn.commit()
    cursor.close()
    conn.close()
    return jsonify({'status': 'success'})
    
@app.route('/developers', methods=['GET'])
def get_developers():

    filter_cols = [
        'Country', 'Employer', 'Segment', 'JobRole', 'Prod_Bucket', 'Engineer_Level', 'HCL_Manager_email', 'Employee'
    ]
    filters = []
    params = []
    for col in filter_cols:
        val = request.args.get(col)
        if val:
            if col == 'Employee':
                filters.append("CONCAT(d.Developer_First_name, ' ', d.Developer_Last_name) = %s")
            else:
                filters.append(f"d.{col} = %s")
            params.append(val)

    # Get latest Year/Month for each developer
    stats_subquery = """
        SELECT UID, Year, Month, Total_BCE, BCE_Per_Day, Tenure, Percentage_BCE
        FROM developers_monthly_stats m1
        WHERE (Year, Month) = (
            SELECT MAX(Year), MAX(Month) FROM developers_monthly_stats m2 WHERE m2.UID = m1.UID
        )
    """

    query = f"""
        SELECT d.*, s.Total_BCE, s.BCE_Per_Day, s.Tenure, s.Percentage_BCE
        FROM developers d
        JOIN ({stats_subquery}) s ON d.UID = s.UID
    """
    if filters:
        query += " WHERE " + " AND ".join(filters)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/developers/least', methods=['GET'])
def get_least_developers():
    year = request.args.get('year')
    month = request.args.get('month')
    filter_cols = [
        'Country', 'Employer', 'Segment', 'JobRole', 'Prod_Bucket', 'Engineer_Level', 'HCL_Manager_email'
    ]
    filters = []
    params = [year, month]
    for col in filter_cols:
        val = request.args.get(col)
        if val:
            filters.append(f"d.{col} = %s")
            params.append(val)

    query = """
        SELECT d.UID, d.Developer_First_name, d.Developer_Last_name, m.Percentage_BCE
        FROM developers d
        JOIN developers_monthly_stats m ON d.UID = m.UID
        WHERE m.Year = %s AND m.Month = %s
    """
    if filters:
        query += " AND " + " AND ".join(filters)
    query += " ORDER BY m.Percentage_BCE ASC LIMIT 5"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)
## Remove duplicate imports and app initialization
    filters = []
    params = []
    filter_cols = [
        'Country', 'Employer', 'Segment', 'JobRole', 'Prod_Bucket', 'Engineer_Level', 'HCL_Manager_email'
    ]
    for col in filter_cols:
        val = request.args.get(col)
        if val:
            filters.append(f"d.{col} = %s")
            params.append(val)

    # Get latest Year/Month for each developer
    stats_subquery = """
        SELECT UID, Year, Month, Total_BCE, BCE_Per_Day, Tenure, Percentage_BCE
        FROM developers_monthly_stats m1
        WHERE (Year, Month) = (
            SELECT MAX(Year), MAX(Month) FROM developers_monthly_stats m2 WHERE m2.UID = m1.UID
        )
    """

    query = f"""
        SELECT d.*, s.Total_BCE, s.BCE_Per_Day, s.Tenure, s.Percentage_BCE
        FROM developers d
        JOIN ({stats_subquery}) s ON d.UID = s.UID
    """
    if filters:
        query += " WHERE " + " AND ".join(filters)

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/developers/trends', methods=['GET'])
def get_trends():
    uid = request.args.get('uid')
    query = "SELECT Year, Month, Total_BCE, BCE_Per_Day FROM developers_monthly_stats"
    params = []
    if uid:
        query += " WHERE UID = %s"
        params.append(uid)
    query += " ORDER BY Year, Month"
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/developers/top', methods=['GET'])
def get_top_developers():
    year = request.args.get('year')
    month = request.args.get('month')
    filter_cols = [
        'Country', 'Employer', 'Segment', 'JobRole', 'Prod_Bucket', 'Engineer_Level', 'HCL_Manager_email'
    ]
    filters = []
    params = [year, month]
    for col in filter_cols:
        val = request.args.get(col)
        if val:
            filters.append(f"d.{col} = %s")
            params.append(val)

    query = """
        SELECT d.UID, d.Developer_First_name, d.Developer_Last_name, m.Percentage_BCE
        FROM developers d
        JOIN developers_monthly_stats m ON d.UID = m.UID
        WHERE m.Year = %s AND m.Month = %s
    """
    if filters:
        query += " AND " + " AND ".join(filters)
    query += " ORDER BY m.Percentage_BCE DESC LIMIT 5"

    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute(query, params)
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return jsonify(results)

@app.route('/developers/filters', methods=['GET'])
def get_filter_options():
    columns = [
        'Country', 'Employer', 'Segment', 'JobRole', 'Prod_Bucket', 'Engineer_Level', 'HCL_Manager_email', 'Employee'
    ]
    conn = get_connection()
    cursor = conn.cursor()
    options = {}
    for col in columns:
        filter_clauses = []
        filter_params = []
        for fcol in columns:
            if fcol != col and fcol != 'Employee':
                val = request.args.get(fcol)
                if val:
                    filter_clauses.append(f"{fcol} = %s")
                    filter_params.append(val)
        if col == 'Employee':
            query = "SELECT DISTINCT CONCAT(Developer_First_name, ' ', Developer_Last_name) AS Employee FROM developers"
        else:
            query = f"SELECT DISTINCT {col} FROM developers"
        if filter_clauses:
            query += " WHERE " + " AND ".join(filter_clauses)
        cursor.execute(query, filter_params)
        options[col] = [row[0] for row in cursor.fetchall() if row[0] is not None]
    # Add year and month options from developers_monthly_stats
    cursor.execute("SELECT DISTINCT Year FROM developers_monthly_stats ORDER BY Year DESC")
    options['Year'] = [row[0] for row in cursor.fetchall() if row[0] is not None]
    cursor.execute("SELECT DISTINCT Month FROM developers_monthly_stats ORDER BY Month DESC")
    options['Month'] = [row[0] for row in cursor.fetchall() if row[0] is not None]
    cursor.close()
    conn.close()
    return jsonify(options)

if __name__ == "__main__":
    app.run(debug=True)
