from sqlalchemy import create_engine, inspect
import sqlite3
# Path to your database
db_path = "instance/data.db"
engine = create_engine(f"sqlite:///{db_path}")

inspector = inspect(engine)

# List tables
print("Tables:", inspector.get_table_names())

# List columns in each table
for table_name in inspector.get_table_names():
    print(f"\nTable: {table_name}")
    for column in inspector.get_columns(table_name):
        print(f"  {column['name']} ({column['type']})")
tables = ['course_items', 'specializations']

for table in tables:
    print(f"\nTable: {table}")
    cursor.execute(f"PRAGMA table_info({table});")
    columns = [col[1] for col in cursor.fetchall()]
    print("Columns:", columns)
    
    cursor.execute(f"SELECT * FROM {table}")
    rows = cursor.fetchall()
    
    for row in rows:
        row_dict = dict(zip(columns, row))
        print(row_dict)
