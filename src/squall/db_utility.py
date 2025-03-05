# db_utility.py

import sqlite3


def get_table_names(db_path: str) -> list[str]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    table_names = [table[0] for table in tables]
    return table_names


def get_data_from_table(db_path: str, table_name: str) -> list[tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = f"SELECT * FROM {table_name} LIMIT 1000;"
    cursor.execute(sql)

    # Get column names
    column_names = tuple([description[0] for description in cursor.description])

    data = cursor.fetchall()
    data.insert(0, column_names)
    return data

def get_schema(db_path: str) -> dict[str, dict]:
    sql = "SELECT * FROM sqlite_master;"
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    result = cursor.fetchall()

    tables = {}
    for table in result:
        if table[0] == "index":
            # skip it
            continue

        table_name = table[1]
        schema = table[4]
        columns = {}
        for item in schema.split("\n")[1:]:
            item_no_commas = item.replace(",", "")
            if "PRIMARY KEY" in item_no_commas or len(item_no_commas) <= 1 or "FOREIGN KEY" in item_no_commas:
                # skip it
                continue
            if "ON" in item_no_commas and "DELETE" in item_no_commas:
                continue

            items = [i.strip() for i in item.split(",") if i]
            for item in items:
                column_name, column_type, *_ = item.split()
                column_name = column_name.replace('"', "").replace("[", "").replace("]", "")
                column_name = column_name.replace("(", "").replace(")", "")
                column_schema = item
                column_schema = column_schema.replace("\t", "")
                columns[column_name] = {}
                columns[column_name]["Type"] = column_type
                columns[column_name]["Schema"] = column_schema
        tables[table_name] = {}
        tables[table_name]["Schema"] = schema
        tables[table_name]["Columns"] = columns

    return tables

def get_primary_keys(db_path: str, table_name: str) -> list[tuple[str]]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f'SELECT l.name FROM pragma_table_info("{table_name}") as l WHERE l.pk <> 0;'
    cursor.execute(sql)
    result = cursor.fetchall()
    return result

def get_column_types(db_path: str, table_name: str) -> dict[str, str]:
    """
    Get all the column data types and return it as a dictionary
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f"PRAGMA table_info({table_name});"
    cursor.execute(sql)
    result = cursor.fetchall()
    return {key: value for _, key, value, *_ in result}

def run_sql(db_path: str, sql: str) -> list[tuple]:
    """
    Runs the user provided SQL. This may be a select, update, drop
    or any other SQL command

    If there are results, they will be returned
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql)
    headers = [name[0] for name in cursor.description]
    result = cursor.fetchall()
    result.insert(0, tuple(headers))
    conn.commit()
    return result

def run_row_update(db_path: str, sql: str, column_values: list, primary_key_value) -> None:
    """
    Update a row the database using the supplied SQL command(s)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, (*column_values, primary_key_value))
    conn.commit()
