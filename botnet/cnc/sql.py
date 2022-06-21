import pymysql




def check_password(username,password):
    db = pymysql.connect(host='localhost',
                     user='root',
                     password='a4b3c2d1A4B3C2D1',
                     database='bot')
    cursor = db.cursor()
    sql = f'select * from users where username="{username}" and password = "{password}"'
    cursor.execute(sql)
    result = cursor.fetchall()
    if len(result) != 0:
        return True
    else:
        return False

    
    