def create_db(cursor,db_name):
    db=f"create  database if not exists {db_name}"
    cursor.execute(db)

def create_table(cursor,table_name):
    tb=f"create table if not exists {table_name} (name varchar(250),price varchar(100),header varchar(500),comment varchar(500),rev_name varchar(500));"
    cursor.execute(tb)
def insert_table(cursor,table_name,lst):
    insert_quary=f"insert into  {table_name} values (%(name)s,%(price)s,%(header)s,%(comment)s,%(rev_name)s); "
    cursor.executemany(insert_quary,lst)