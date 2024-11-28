import pymysql
from config.settings import DB_CONFIG
from utils.logutil import logger
from pymysql import cursors


class MysqlUtil:
    def __init__(self):
        self.db = pymysql.connect(**DB_CONFIG)
        self.cursor = self.db.cursor(cursor=pymysql.cursors.DictCursor)

    # 获取单条数据
    def get_fetchone(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchone()

    # 获取多条数据
    def get_fetchall(self, sql):
        self.cursor.execute(sql)
        return self.cursor.fetchall()

    def sql_execute(self, sql):
        try:
            if self.db and self.cursor:
                self.cursor.execute(sql)
                self.db.commit()
        except Exception as e:
            self.db.rollback()
            logger.error(e)
            logger.error("sql语句执行错误，已执行回滚操作")
            return False

    @staticmethod
    def close(self):
        if self.cursor is not None:
            self.cursor.close()
        if self.db is not None:
            self.db.close()


if __name__ == '__main__':
    mysql = MysqlUtil()
    res = mysql.get_fetchall("select * from test_case_list_pos")
    print(res)

