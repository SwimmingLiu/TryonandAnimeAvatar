import pymysql
from datetime import datetime

from flaskProject1.upload import get_random_filename, upload_img


class DatabaseManager:
    def __init__(self, host, user, password, db):
        self.connection = pymysql.connect(host=host, user=user, password=password, db=db)
        self.cursor = self.connection.cursor()

    def add_record(self, table, userid, result_url, generate_time, task_status):
        """
        添加记录到指定表。
        """
        sql = f"INSERT INTO {table} (userid, result_url, generate_time, task_status) VALUES (%s, %s, %s, %s)"
        self.cursor.execute(sql, (userid, result_url, generate_time, task_status))
        self.connection.commit()

    def delete_record(self, table, userid):
        """
        根据userid删除记录。
        """
        sql = f"DELETE FROM {table} WHERE userid = %s"
        self.cursor.execute(sql, (userid,))
        self.connection.commit()

    def update_record(self, table, userid, generate_time, new_status,new_url):
        """
        更新指定用户的task_status。
        """
        sql = f"UPDATE {table} SET result_url = %s , task_status = %s WHERE userid = %s and generate_time = %s"
        self.cursor.execute(sql, (new_url,new_status, userid,generate_time))
        self.connection.commit()

    def query_records(self, table, userid=None):
        """
        查询记录，可根据userid过滤。
        """
        sql = f"SELECT * FROM {table}"
        if userid:
            sql += " WHERE userid = %s"
            self.cursor.execute(sql, (userid,))
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def query_return(self, table, userid=None):
        """
        查询记录，可根据userid过滤。
        """
        sql = f"SELECT * FROM {table}"
        if userid:
            sql += " WHERE userid = %s ORDER BY generate_time DESC;"
            self.cursor.execute(sql, (userid,))
        else:
            self.cursor.execute(sql)
        return self.cursor.fetchall()

    def close(self):
        """
        关闭数据库连接。
        """
        self.connection.close()

def getImgUrl(file_loc):
    file_name = get_random_filename()
    upload_img(file_name, file_loc)
    file_url = 'https://oss.flik1337.com/' + file_name  # 结果
    return file_url
