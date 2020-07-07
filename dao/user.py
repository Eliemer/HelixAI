
import sqlite3

class UserDAO:
    def __init__(self):
        connection_path ="/home/stated/databse/capstone"
        self.conn = sqlite3.connect(connection_path)
        
    def getAllUsers(self):
        cur = self.conn.cursor()
        query = "select * from User;"
        cur.execute(query)
        result = []
        for row in cur:
            result.append(row)
        return result
    def getUserById(self, user_id):
        cur = self.conn.cursor();
        query = "select * from User where user_id = %s"
        cursor.execute(query,(user_id,))
        result = []
        for row in cur:
            result.append(row)
        return result
    # def getUserByInstitution(self,institution):

    # def getTrainedConfigFileByUserID(self, user_id):
    # def insert(self):
    # def delete(self):
    # def update(self);
    
