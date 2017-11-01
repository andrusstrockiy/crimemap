import pymysql
import dbconfig


connection = pymysql.connect(host='localhost',
                             user=dbconfig.db_user,
                             passwd=dbconfig.db_password)

try:
    with connection.cursor() as cursor:
        sql = 'CREATE DATABASE IF NOT EXISTS crimemap default charset utf8'
        cursor.execute(sql)
        sql = 'create table if not exists crimemap.crimes(' \
              'id int not null auto_increment,' \
              'latitude float(10,6),' \
              'longitude float(10,6),' \
              'date datetime,' \
              'category varchar(50),' \
              'description varchar(100),' \
              'updated_at timestamp,' \
              'PRIMARY KEY (id)' \
              ')'
        cursor.execute(sql)
        connection.commit()
finally:
    connection.close()