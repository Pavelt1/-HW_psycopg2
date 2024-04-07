import psycopg2

conn = psycopg2.connect(database="test_py",user="postgres",password="1996")

def create_table(name_table:str):
    with conn.cursor() as cur:
        cur.execute("""CREATE TABLE IF NOT EXISTS %s(
                    id SERIAL PRIMARY KEY,
                    first_name VARCHAR(15) NOT NULL,
                    last_name VARCHAR(20) NOT NULL,
                    email VARCHAR(20) NOT NULL UNIQUE);
                    """,(name_table,))
        
        cur.execute("""CREATE TABLE IF NOT EXISTS phone_%s (
                    user_id INT REFERENCES %s(id),
                    tel_numer INT VARCHAR(20) NOT NULL UNIQUE);
                    """,(name_table,name_table,)) 
               
        conn.commit()

def add_user(table,first_name,last_name,email):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO %s
                    VALUES(%s,%s,%s);""",(table,first_name,last_name,email,))
        conn.commit()

def additional_num(table,user_id,number):
    with conn.cursor() as cur:
        cur.execute("""INSERT INTO phone_%s
                    VALUES(%s,%s);""",(table,user_id,number,))
        conn.commit()

def change_value(table,f_name,l_name,email,id):
    with conn.cursor() as cur:
        cur.execute("""UPDATE %s
                    SET first_name = %s
                    last_name = %s
                    email = %s
                    WHERE id = %s;""",(table,f_name,l_name,email,id,))
        conn.commit()

def delete_phone(table,id,number):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM %s
                    WHERE user_id = %s AND 
                    tel_numer = %s;""",(table,id,number,))
        conn.commit()

def delete_client(table,id):
    with conn.cursor() as cur:
        cur.execute("""DELETE FROM %s
                    WHERE id = %s ;""",(table,id,))
        conn.commit()


def find_client(table,data_user):
    with conn.cursor() as cur:
        if isinstance(data_user,str):
            cur.execute("""SELECT * FROM %s
                        WHERE first_name = %s 
                        OR last_name = %s 
                        OR email = %s;""",(table,data_user,data_user,data_user,))
        elif isinstance(data_user,int):
            cur.execute("""SELECT * FROM phone_%s
                        JOIN %s a ON phone_%s.user_id=a.id
                        WHERE tel_numer = %s;
                        """,(table,table,table,data_user,))  
        selectt = cur.fetchone()
    print(selectt)


