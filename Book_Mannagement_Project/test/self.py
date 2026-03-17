import sys
import os
import csv

#======================ACCOUNT====================
def gotoxy(x, y):
    # hàm này để đưa con trỏ tời vị trí x, y trong terminal (làm đẹp thôi)
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

class User:
    def __init__(self, userID, username, password):
        self.userID = userID
        self.username = username
        self.password = password 
    def login(self):
        pass
    def display_info(self):
        pass
class Admin(User):
    def __init__(self, userID, username, password): 
        #==== hàm này tạo constructor cho nhanh thay vì phải code lại self.username = username....
        super().__init__(userID, username, password)
    # methods
    def login_admin():
        os.system("cls")
        while True:
            print("╔══════════════════════════════════════╗")
            print("║             Login Admin              ║")
            print("╠══════════════════════════════════════╣")
            print("║          't' to Enter your           ║")
            print("║      Admin ID:                       ║")
            print("║      Username:                       ║")
            print("║      Password:                       ║")
            print("║                                      ║")
            print("║          'r' to return               ║")
            print("╚══════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == "t":
                gotoxy(20, 4)
                ID_temp = input().strip()            
                gotoxy(20, 5)
                username_temp = input().strip() 
                gotoxy(20, 6)
                password_temp = input().strip()
                if Account_system.is_account(ID_temp, username_temp, password_temp):
                    return True
                else: 
                    print(ID_temp)
                    print(username_temp)
                    print(password_temp)
                    n = input()
                    Account_system.incorrect_screen(Admin.login_admin)
            elif choice == "r":
                return False
            else: Account_system.error_screen(Admin.login_admin)
class Member(User):
    def __init__(self, userID, username, password):
        super().__init__(userID, username, password)
    @staticmethod
    def login_member():
        os.system('cls')
        while True:
            print("╔══════════════════════════════════════╗")
            print("║             Login Member             ║")
            print("╠══════════════════════════════════════╣")
            print("║          't' to Enter your           ║")
            print("║      Student ID:                     ║")
            print("║      Username:                       ║")
            print("║      Password:                       ║")
            print("║                                      ║")
            print("║          'r' to return               ║")
            print("╚══════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == "t":
                gotoxy(20, 4)
                ID_temp = input().strip()            
                gotoxy(20, 5)
                username_temp = input().strip() 
                gotoxy(20, 6)
                password_temp = input().strip()
                if Account_system.is_account(ID_temp, username_temp, password_temp):
                    return True
                else: Account_system.incorrect_screen(Member.login_member)
            elif choice == "t":
                return False
            else: Account_system.error_screen(Member.login_member)
    
    @staticmethod     
    def Signin_member():
        os.system('cls')
        while True:
            print("╔══════════════════════════════════════╗")
            print("║            Sign in Member            ║")
            print("╠══════════════════════════════════════╣")
            print("║          't' to Enter your           ║")
            print("║      Student ID:                     ║")
            print("║      Username:                       ║")
            print("║      Password:                       ║")
            print("║                                      ║")
            print("║          'r' to return               ║")
            print("╚══════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == "t":
                gotoxy(20, 4)
                ID_temp = input().strip()            
                gotoxy(20, 5)
                username_temp = input().strip() 
                gotoxy(20, 6)
                password_temp = input().strip()
                if Account_system.is_account(ID_temp, username_temp, password_temp):
                    Account_system.registered_screen()
                else: 
                    if Account_system.ID_isRegistered(ID_temp):  
                        isRegistered_screen(Member.Signin_member)
                    else:
                       Account_system.create_account(ID_temp, username_temp, password_temp)
                       Account_system.account_success_screen(Account_system.login_screen)
            else: Account_system.error_screen(Member.login_member)
class Account_system:
    #boolean        
    def ID_isRegistered(ID):
        lib = Library()
        account = lib.load_data(Library.DATA_ACCOUNT)
        for row in account:
            if len(row) >= 1 and row[0] == ID:
                return True
        return False
    def is_account(ID, username, password):
        #kiểm tra tài khoản đúng hay ko
        lib = Library()
        account = lib.load_data(Library.DATA_ACCOUNT)
        for row in account: # xét từng hàng trong list
            if len(row) >= 3:
                if row[0] == ID and row[1] == username and row[2] == password:
                    return True
        return False
    #handle
    def create_account(ID, username, password):
        lib = Library()
        account = lib.load_data(Library.DATA_ACCOUNT)
        account.append([ID, username, password])
        lib.save_data(Library.DATA_ACCOUNT, account)
    #screen    
    def error_screen(back_func):
        os.system("cls")
        print("╔══════════════════════════════════════╗")
        print("║                ERROR                 ║")
        print("╠══════════════════════════════════════╣")       
        print("║             1. Return                ║")
        print("║             0. Exit                  ║")
        print("╚══════════════════════════════════════╝")

        choice = input("👉 Choose: ").strip()

        if choice == "1":
            back_func()
        elif choice == "0":
            exit("Thank you!")
        else:
            error_screen(back_func)
    def incorrect_screen(back_func):
        os.system("cls")
        print("╔══════════════════════════════════════╗")
        print("║         ACCOUNT NOT CORRECT          ║")
        print("╠══════════════════════════════════════╣")       
        print("║             1. Return                ║")
        print("║             0. Exit                  ║")
        print("╚══════════════════════════════════════╝")

        choice = input("👉 Choose: ")

        if choice == "1":
            back_func()
        elif choice == "0":
            exit("Thank you!")
        else:
            Account_system.error_screen(back_func)
    def registered_screen(back_func):
        os.system('cls')
        print("╔══════════════════════════════════════╗")
        print("║     You already have an account!!    ║")
        print("╠══════════════════════════════════════╣")
        print("║           'r' to return              ║")
        print("╚══════════════════════════════════════╝")
        
        choice = input("👉 Choose an option: ").strip()
        if choice == "r": 
            back_func()
        else: 
            Account_system.error_screen(back_func)
    def account_success_screen(back_func):
        os.system('cls')
        print("╔══════════════════════════════════════╗")
        print("║             Successful!              ║")
        print("╠══════════════════════════════════════╣")
        print("║           'r' to return              ║")
        print("╚══════════════════════════════════════╝")
        
        choice = input("👉 Choose an option: ").strip()
        if choice == "r": 
            back_func()
        else: 
            Account_system.error_screen(back_func)
    def isRegistered_screen(back_func):
        os.system('cls')
        print("╔══════════════════════════════════════╗")
        print("║           ID is registered!          ║")
        print("╠══════════════════════════════════════╣")
        print("║           'r' to return              ║")
        print("╚══════════════════════════════════════╝")
        
        choice = input("👉 Choose an option: ").strip()
        if choice == "r": 
            back_func()
        else: 
            Account_system.error_screen(back_func)
    @staticmethod
    def login_screen():
        while True:
            # nếu mình nhập sai thì phải lựa chọn lại => dùng while cho tới khi nhập đúng thì thôi
            # và nếu mình dùng xong hết tính năng thì có thể quay lại menu -> while để tái sử dụng
            # while kết hơp chung với hàm error_screen
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║                Login                 ║")
            print("╠══════════════════════════════════════╣")
            print("║1. Login Admin                        ║")
            print("║2. Login Member                       ║")
            print("║3. Sign in Member                     ║")
            print("║0. Exit                               ║")
            print("╚══════════════════════════════════════╝")
            #================= choosing ==============
            choice = input("👉 Choose an option: ").strip()
            if choice == "1":
                if Admin.login_admin():
                    return True
            elif choice == "2": 
                if Member.login_member():
                    return True
            elif choice == '3': 
                if Member.Signin_member():
                    return True
            elif choice == "0":
                exit("Thank you!")
            else: 
                Account_system.error_screen(Account_system.login_screen)
#=================================================                
                
class Book:
    pass

class Book_Record:
    pass

class Library:
    DATA_ACCOUNT = "Account_data.csv"
    DATA_BOOK = "Book_data.csv"
    def __init__(self):
        pass
    @staticmethod #  này ko lưu dữ liệu nên chỉ thực hiện hành động thôi -> xài
    def load_data( path): #tải data xuống list để thao tác
        try: 
            data = [] 
            with open(path, "r", encoding="utf-8", newline="") as f:
                # tạo list                              
                reader = csv.reader(f)        #['id', 'name', 'author', 'year'] <-- header               
                next(reader)  # bỏ header     #['B01', 'Doraemon', 'Fujiko', '1995']         
                                              #['B02', 'Harry Potter', 'J.K.Rowling', '1997']
                return list(reader) 
        except Exception as e: 
            print("Có Lỗi xảy ra!", e)
            return [] #dự kiến hàm này trả về list -> trả về list rỗng để tránh lỗi khi tạo và sử dụng list
        
    def save_data(self, path, data):
        with open(path, "w", encoding="utf-8", newline="") as f:
            writer = csv.writer(f)
            writer.writerow(["ID","Username","Password"]) # ghi headreader
            writer.writerows(data) #ghi dữ liệu
    def update_data(self, path):
        pass
    def find_data():
        pass
    def edit_data():
        pass
    
                
if __name__ == "__main__":
    Account_system.login_screen()            
