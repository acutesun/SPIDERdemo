import sqlite3


class DataOut(object):
    def __init__(self):
        self.conn = sqlite3.connect('MTime.db')
        self.create_table()
        self.datas = []

    def create_table(self):
        tables = '''
        id integer primary key,
        MovieId integer,
        MovieTitle varchar(40) NOT NULL,
        RatingFinal REAL NOT NULL DEFAULT 0.0,
        ROtherFinal REAL NOT NULL DEFAULT 0.0,
        RPictureFinal REAL NOT NULL DEFAULT 0.0,
        RDirectorFinal REAL NOT NULL DEFAULT 0.0,
        RStoryFinal REAL NOT NULL DEFAULT 0.0,
        Usercount integer NOT NULL DEFAULT 0,
        AttitudeCount integer NOT NULL DEFAULT 0,
        TotalBoxOffice varchar(20) NOT NULL,
        TodayBoxOffice varchar(20) NOT NULL,
        Rank integer NOT NULL DEFAULT 0,
        isRelease integer NOT NULL
        '''
        self.conn.execute('create table IF NOT EXISTS MTime({0})'.format(tables))

    def store_data(self, data):
        '''将数据保存到内存，大于10存储到数据库'''
        if data:
            self.datas.append(data)
        if len(self.datas)>10:
            self.output_db('MTime')

    def output_db(self, table_name):
        ''' 将数据存储到数据库 '''
        for data in self.datas[:]:
            self.conn.execute('''
            insert into %s(MovieId,MovieTitle,RatingFinal,
            ROtherFinal,RPictureFinal,RDirectorFinal,RStoryFinal,Usercount,
            AttitudeCount,TotalBoxOffice,TodayBoxOffice,Rank, isRelease
            ) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?)
            ''' % table_name, data)
            self.datas.remove(data)
        self.conn.commit()

    def output_end(self):
        ''' 关闭数据库 '''
        if self.datas:
            self.output_db('MTime')
        self.conn.close()
