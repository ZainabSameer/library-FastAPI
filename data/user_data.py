from models.user import UserModel

def create_users():
    user1 = UserModel(username="zainab", email="zainab@gmail.com")
    user1.set_password("Zanoob@66")
    user2 = UserModel(username="sameer", email="sameer@gmail.com")
    user2.set_password("Sameer@123")
    user3 = UserModel(username="fatima", email="fatima@gmail.com")
    user3.set_password("123456")
    user4 = UserModel(username="ali", email="ali@kpmg.com")
    user4.set_password("123456")


    return [user1, user2, user3, user4]

user_list = create_users()