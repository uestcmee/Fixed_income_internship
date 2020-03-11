import sqlite3

class InitSQL:
    def __init__(self,db='test.db'):
        self.db=db
        # self.InitSQL()
    def InitSQL(self):
        conn=sqlite3.connect(self.db)
        cursor=conn.cursor()
        try:
            cursor.execute('DROP TABLE returns')
        except:
            pass
        cursor.execute('''CREATE TABLE returns
        (
        ID int  identity (1,1) ,
        StockID varchar(20),
        LongFac float,
        ShortFac float,
        LongMA int,
        ShortMA int,
        StartYear int,
        EndYear int,
        Return float,
        PRIMARY KEY(ID)
        );
        ''')
        cursor.close()
        conn.commit()
        conn.close()

    def UpdateSQL(self):
        conn=sqlite3.connect(self.db)
        cursor=conn.cursor()
        a=cursor.execute('SELECT count(*) FROM returns;')
        print('row count = ',a.fetchall()[0])
        cursor.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    sql=InitSQL('CSI.db')
    # sql.UpdateSQL() # 获取行数
