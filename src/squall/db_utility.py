# db_utility.py

import sqlite3

from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy import inspect
from sqlalchemy.engine.reflection import Inspector


def get_db_inspector(db_path: Path) -> Inspector:
    engine = create_engine(rf"sqlite:///{db_path}")
    return inspect(engine)


def get_data_from_table(db_path: Path, table_name: str) -> list[tuple]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()

    sql = f"SELECT * FROM {table_name} LIMIT 1000;"
    cursor.execute(sql)

    # Get column names
    column_names = tuple([description[0] for description in cursor.description])

    data = cursor.fetchall()
    data.insert(0, column_names)
    return data


def get_schema(tables: list[str], db_inspector: Inspector) -> dict[str, dict]:
    table_data: dict = {}
    for table in tables:
        columns = db_inspector.get_columns(table)
        column_data: dict = {}
        for column in columns:
            column_name = column["name"]
            column_type = str(column["type"])
            column_data[column_name] = {}
            column_data[column_name]["Type"] = column_type
            column_data[column_name]["Schema"] = column
        table_data[table] = {}
        table_data[table]["Columns"] = column_data

    return table_data


def get_primary_keys(db_path: Path, table_name: str) -> list[tuple[str]]:
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f'SELECT l.name FROM pragma_table_info("{table_name}") as l WHERE l.pk <> 0;'
    cursor.execute(sql)
    result = cursor.fetchall()
    return result


# Currently not used
def get_column_types(db_path: Path, table_name: str) -> dict[str, str]:
    """
    Get all the column data types and return it as a dictionary
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    sql = f"PRAGMA table_info({table_name});"
    cursor.execute(sql)
    result = cursor.fetchall()
    return {key: value for _, key, value, *_ in result}


def run_sql(db_path: Path, sql: str) -> list[tuple]:
    """
    Runs the user-provided SQL. This may be a select, update, drop
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


def run_row_update(
    db_path: Path, sql: str, column_values: list, primary_key_value
) -> None:
    """
    Update a row in the database using the supplied SQL command(s)
    """
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute(sql, (*column_values, primary_key_value))
    conn.commit()
