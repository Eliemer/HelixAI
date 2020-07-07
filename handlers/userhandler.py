from flask import jsonify
from dao.user import UserDAO

class UserHandler:
    def build_user_dict(self,row):
        result ={}
        result['user_id'] = row[0]
        result['first_name'] = row[1]
        result['last_name'] = row[2]
        result['email'] = row[3]
        result['institution'] = row[4]
        result['address'] = row[5]
        result['city'] = row[6]
        result['country'] = row[7]
        result['login_id']=row[8]
  

        return result

    def getAllUsers(self):
        dao = UserDAO()
        user_list = dao.getAllUsers()
        result_list = []
        for row in user_list:
            result = self.build_user_dict(row)
            result_list.append(result)
        return jsonify(UserList=result_list)
    def getUserById(self, user_id):
        return null