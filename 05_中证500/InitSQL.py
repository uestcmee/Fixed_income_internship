import sqlite3

class InitSQL:
    def __init__(self,db='test.db'):
        self.db=db
        self.InitSQL()
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
        #ID int  identity (1,1) ,
        # PRIMARY KEY(StockID,LongFac,ShortFac,LongMA,ShortMA)
        # for i in range(5):
        #     cursor.execute('INSERT INTO returns VALUES (null,\'000000\','+str(float(1))+',1.0,20,5,2000,2001,1.01);')
        # a=cursor.execute('SELECT * FROM returns WHERE startyear=2000 ')
        # b=a.fetchall()
        # print(b)
        cursor.close()
        conn.commit()
        conn.close()

if __name__ == '__main__':
    InitSQL('test.db')