import json
import os
import sys
from datetime import datetime

#======================ACCOUNT====================
AccData = "Account_data.json"
BookData = "Book_data.json"
def gotoxy(x, y):
    # hàm này để đưa con trỏ tời vị trí x, y trong terminal (làm đẹp thôi)
    sys.stdout.write(f"\033[{y};{x}H")
    sys.stdout.flush()

class User:
    def __init__(self, ID, username, password):
        self.ID = ID
        self.username = username
        self.password = password 
    def login(self):
        pass
    def display_info(self):
        pass
class Admin(User):
    def __init__(self, ID, username, password): 
        #==== hàm này tạo constructor cho nhanh thay vì phải code lại self.username = username....
        super().__init__(ID, username, password)
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
                gotoxy(20, 5)
                ID_temp = input().strip()            
                gotoxy(20, 6)
                username_temp = input().strip() 
                gotoxy(20, 7)
                password_temp = input().strip()
                if AccSystem.is_account(ID_temp, username_temp, password_temp):
                    return True
                else: 
                    print(ID_temp)
                    print(username_temp)
                    print(password_temp)
                    n = input()
                    AccSystem.incorrect_screen(Admin.login_admin)
            elif choice == "r":
                return False
            else: AccSystem.error_screen(Admin.login_admin)
class Member(User):
    def __init__(self, ID, username, password):
        super().__init__(ID, username, password)
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
                gotoxy(20, 5)
                ID_temp = input().strip()            
                gotoxy(20, 6)
                username_temp = input().strip() 
                gotoxy(20, 7)
                password_temp = input().strip()
                if AccSystem.is_account(ID_temp, username_temp, password_temp):
                    return True
                else: AccSystem.incorrect_screen(Member.login_member)
            elif choice == "r":
                return False
            else: AccSystem.error_screen(Member.login_member)
    
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
                gotoxy(20, 5)
                ID_temp = input().strip()            
                gotoxy(20, 6)
                username_temp = input().strip() 
                gotoxy(20, 7)
                password_temp = input().strip()
                if AccSystem.is_account(ID_temp, username_temp, password_temp):
                    AccSystem.registered_screen(Member.Signin_member)
                else: 
                    if AccSystem.ID_isRegistered(ID_temp):  
                        AccSystem.isRegistered_screen(Member.Signin_member)                    
                        AccSystem.create_account(ID_temp, username_temp, password_temp)
                        AccSystem.Success_screen(AccSystem.login_screen)
            else: AccSystem.error_screen(Member.login_member)
class AccSystem:
    #boolean        
    def ID_isRegistered(ID):
        lib = Library()
        account = lib.load_data(AccData)
        for check in account:
            if check["ID"] == ID:
                return True
        return False
    def is_account(ID, username, password):
        #kiểm tra tài khoản đúng hay ko
        lib = Library()
        account = lib.load_data(AccData)
        for check in account: # xét từng hàng trong list
            if check["ID"] == ID and check["Username"] == username and check["Password"] == password:
                return True
        return False
    #handle
    def create_account(ID, username, password):
        lib = Library()
        data = lib.load_data(AccData)
        new_account = {
        "ID": ID,
        "Username": username,
        "Password": password
        }

        data.append(new_account)
        lib.save_data(AccData, data)
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
            AccSystem.error_screen(back_func)
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
            AccSystem.error_screen(back_func)
    def Success_screen(back_func):
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
            AccSystem.error_screen(back_func)
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
            AccSystem.error_screen(back_func)
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
                AccSystem.error_screen(AccSystem.login_screen)
#=================================================  

# Lớp BookManager dùng để quản lý các hàm liên quan đến quản lí sách
class BookManager:
    def __init__(self, json_file = "Book_data.json"):
        self.json_file = json_file          #Hàm dùng lưu tên Book_data.json vào self.json_file để lần sau ko cần nhập tên sách
        self.books = self.load_books()    #Hàm dùng để load sách từ file json


    #========== XỬ LÝ FILE ===========# 
class Library:
    # Đọc dữ liệu file #
    def load_data(self, filename): 
        if os.path.exists(filename): # dòng này kiểm tra xem file có tên có tồn tại ko
            try:
                with open (filename, 'r', encoding = 'utf - 8') as f:    #dòng này dùng để mở file với self.json: tên sách
                                                                               #                             "r": reading -> chế độ đọc
                                                                               # và utf - 8 là mã hóa để đọc được tiếng việt
                    data = json.load(f)
                    return data
            except json.JSONDecodeError:  # Nếu file gặp lỗi thì code này sẽ chạy
                print("⚠️ File was wrong, create a new file!")
                return []
        else:# trường hợp không tìm thấy file
            print("⚠️ File doesn't exists, create a new file")
            return []
    # Lưu data vào file
    def save_data(self, filename, data):
        try:
            with open (filename, 'w', encoding = 'utf - 8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 2) # Dòng này dùng để ghi data vào file json dump(data muốn ghi, nơi ghi, không phải kí tự ascci, thụt lề 2 unit)
            return True
        except Exception as e:
            print(f"An error occurred when save file!")
            return False
        
    # Book data management
    def add_Book(self, book_data):

        if self.check_book_exists(book_data['_id']):
            print(f"Book id {book_data["_id"]} has exists!")
            return False

        if not self.check_book_exists(book_data):
            return False
    def find_book(self, book_id): pass
    def create_borrow_record(self, member_id, book_id): pass
    def return_book(self, record_id): pass

if __name__ == "__main__":
    AccSystem.login_screen() # trả về Boolean
    #------------ hàm để clear màn hình cho đẹp------
    os.system('cls')
    #------------------------
    print("╔══════════════════════════════════════╗")
    print("║      📚 LIBRARY MANAGEMENT 📚        ║")
    print("╠══════════════════════════════════════╣")
    print("║ 1. Add new book                      ║")
    print("║ 2. Display book list                 ║")
    print("║ 3. Search book                       ║")
    print("║ 4. Edit book information             ║")
    print("║ 5. Delete book                       ║")
    print("║--------------------------------------║")
    print("║ 6. Borrow book                       ║")
    print("║ 7. Return book                       ║")
    print("║--------------------------------------║")
    print("║ 0. Exit                              ║")
    print("╚══════════════════════════════════════╝")
    choice = int(input("👉 Choose an option: "))
    #================ choice ==========
    if choice == 1:
        load_books
    elif choice == 2:
        ...
    elif choice == 3:   
        ...
    elif choice == 4:
        ...
    elif choice == 5:
        ...
    elif choice == 6:
        ...
    elif choice == 7:
        ...
    elif choice == 0:
        os.system('cls')
        print("Thank you!")
    else: print("ERROR")



