import datetime

from pymongo import MongoClient
import pymongo
# 암호화 알고리즘. 256을 제일 많이 사용한다.
from passlib.hash import pbkdf2_sha256
from bson.objectid import ObjectId
from config import MONGODB_URL

# 원문 비밀번호를, 암호화 하는 함수
def hash_password(original_password):
    salt = 'eungok'
    password = original_password + salt
    password = pbkdf2_sha256.hash(password)
    return password

def check_password(input_password, hashed_password):
    salt = 'eungok'
    password = input_password + salt
    result = pbkdf2_sha256.verify(password , hashed_password)
    return result

class MyMongo:
     
    def __init__(self, db_url, database):
        self.database = database
        self.client = MongoClient(db_url)
    
    def user_insert(self, username, email, phone, password):
        db = self.client.os
        users = db.users
        pw = hash_password(password)
        user = {"username": username,
                "email": email,
                "phone": phone,
                "password": pw,
                "create_at": datetime.datetime.utcnow()
        }
        result = users.insert_one(user)
        # print(result)
        return result

    def verify_password(self, input_password, email):
        db = self.client.os
        users = db.users
        user = users.find_one({"email":email})
        # print(user)
        if user:
            result = check_password(input_password, user['password'])
            if result:
                print("Verify Success")
                return "1"
            else:
                print("Verify Fail")
                return "2"
        else:
            print("ID is Not Founded")
            return "3"

    def find_user(self, email):
        db = self.client.os
        users = db.users
        user = users.find_one({"email":email})
        return user
    
    def find_data(self):
        db = self.client.os
        lists = db.lists
        list = lists.find()
        # for i in list:
        #     print(i)
        return list
    
    def find_one_data(self, ids):
        db = self.client.os
        list = db.lists
        data = list.find_one({'_id': ObjectId(ids)})
        print(f'fwefwe{data}')
        return data
    
    def insert_list(self, title, desc, author):
        db = self.client.os
        lists = db.lists
        list = {"title": title,
                "desc": desc,
                "author": author,
                "create_at": datetime.datetime.utcnow()
                # "create_at":datetime.date.today().strftime('%Y년 %m월 %d일')
        }
        result = lists.insert_one(list)
        return result
        
    def delete_data(self, id):
        db = self.client.os
        lists = db.lists
        lists.delete_one({'_id': ObjectId(id)})
        return "1"
    
    # [컬렉션 객체].update_one( { [조건값] }, {"$set":{수정값}} )
    def update_data(self, id, title, desc):
        db = self.client.os
        list = db.lists
        list.update_one({'_id': ObjectId(id)}, {"$set":{"title":title, "desc":desc}})
        return "1"

# mymongo = MyMongo(MONGODB_URL, 'os')
# mymongo.user_insert("KIM", "2@naver.com", "010-1111-1111", "1234")
# mymongo.verify_password("1234", ObjectId('64ba29b2379f06c38a1ae246'))


# mymongo.verify_password("1234", "3@naver.com")
# mymongo.find_data()

# mymongo.insert_list("제목","내용","작가")

# mymongo.update_data("64bf337932e6fca9a642f312","제목123","내용")

