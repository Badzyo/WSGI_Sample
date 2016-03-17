from psycopg2 import connect


class PGManager:

    tbl_create_query = '''CREATE TABLE IF NOT EXISTS USER_DATA (
                          DATA_ID BIGSERIAL PRIMARY KEY,
                          VC_TEXT TEXT      NOT NULL,
                          D_DATE  DATE      NOT NULL,
                          D_TIME  TIME      NOT NULL
                          );'''

    insert_query = '''INSERT
                      INTO USER_DATA
                      (VC_TEXT, D_DATE, D_TIME)
                      VALUES (%s, TO_DATE(%s, 'DD.MM.YYYY'), %s)'''

    select_query = '''SELECT   *
                      FROM     USER_DATA
                      ORDER BY DATA_ID DESC LIMIT 1;'''

    def __init__(self, db, user, password):
        params = "dbname={} user={} password={}".format(db, user, password)
        self._conn = connect(params)
        cursor = self._conn.cursor()
        cursor.execute(self.tbl_create_query)
        self._conn.commit()
        cursor.close()

    def __del__(self):
        self._conn.close()

    def write_data(self, data):
        cursor = self._conn.cursor()
        cursor.execute(self.insert_query, (data['text'],
                                           data['date'],
                                           data['time']))
        self._conn.commit()
        cursor.close()
        return 'OK'

    def read_last_data(self):
        cursor = self._conn.cursor()
        cursor.execute(self.select_query)
        raw_data = cursor.fetchone()
        prev_data = dict()
        prev_data['text'] = raw_data[1]
        prev_data['date'] = raw_data[2].strftime('%d.%m.%Y')
        prev_data['time'] = raw_data[3].strftime('%H:%M:%S')
        self._conn.commit()
        cursor.close()
        return prev_data

db = PGManager('test', 'pyuser', '123456')
