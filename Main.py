import json
from multiprocessing import Value
import os
import sys
from datetime import datetime

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
                gotoxy(20, 5)
                ID_temp = input().strip()            
                gotoxy(20, 6)
                username_temp = input().strip() 
                gotoxy(20, 7)
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
                gotoxy(20, 5)
                ID_temp = input().strip()            
                gotoxy(20, 6)
                username_temp = input().strip() 
                gotoxy(20, 7)
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
                gotoxy(20, 5)
                ID_temp = input().strip()            
                gotoxy(20, 6)
                username_temp = input().strip() 
                gotoxy(20, 7)
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
        account = lib.load_data(Library.ACCDATA)
        for check in account:
            if check["ID"] == ID:
                return True
        return False
    def is_account(ID, username, password):
        #kiểm tra tài khoản đúng hay ko
        lib = Library()
        account = lib.load_data(Library.ACCDATA)
        for check in account: # xét từng hàng trong list
            if len(check) >= 3:
                if check["ID"] == ID and check["Username"] == username and check["Password"] == password:
                    return True
        return False
    #handle
    def create_account(ID, username, password):
        lib = Library()
        new_account = {
        "ID": ID,
        "Username": username,
        "Password": password
        }

        data.append(new_account)
        lib.save_data(Library.ACCDATA, new_account)
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

# Lớp BookManager dùng để quản lý các hàm liên quan đến quản lí sách
class BookManager:
    def __init__(self, json_file = "Book_data.json"):
        self.json_file = json_file          #Hàm dùng lưu tên Book_data.json vào self.json_file để lần sau ko cần nhập tên sách
        self.books = self.load_books()    #Hàm dùng để load sách từ file json


    #========== XỬ LÝ FILE ===========# 
class Library:
    ACCDATA = "Account_data.json"
    # Đọc dữ liệu file #
    def load_data(self, filename): 
        if os.path.exists(filename): # dòng này kiểm tra xem file có tên có tồn tại ko
            try:
<<<<<<< HEAD
                with open (self.json_file, 'r', encoding = 'utf-8') as f:   #dòng này dùng để mở file với self.json: tên sách
                                                                               # "r": reading -> chế độ đọc
                                                                               # và utf - 8 là mã hóa để đọc được tiếng việt
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    if isinstance(data, dict) and 'books' in data:
                        return data ['books']
                    return json.load(f)
=======
                with open (filename, 'r', encoding = 'utf - 8') as f:    #dòng này dùng để mở file với self.json: tên sách
                                                                               #                             "r": reading -> chế độ đọc
                                                                               # và utf - 8 là mã hóa để đọc được tiếng việt
                    data = json.load(f)
                    return data
>>>>>>> 30a8a58cb12295289d0255543ead3d991561b1e3
            except json.JSONDecodeError:  # Nếu file gặp lỗi thì code này sẽ chạy
                print("⚠️ File was wrong, create a new file!")
                return []
        else:# trường hợp không tìm thấy file
            print("⚠️ File doesn't exists, create a new file")
            return []
    # Lưu data vào file
    def save_data(self, filename, data):
        try:
<<<<<<< HEAD
            with open (self.json_file, 'w', encoding = 'utf-8') as f:
                json.dump(self.books, f, ensure_ascii = False, indent = 2) # Dòng này dùng để ghi data vào file json dump(data muốn ghi, nơi ghi, không phải kí tự ascci, thụt lề 2 unit)
=======
            with open (filename, 'w', encoding = 'utf - 8') as f:
                json.dump(data, f, ensure_ascii = False, indent = 2) # Dòng này dùng để ghi data vào file json dump(data muốn ghi, nơi ghi, không phải kí tự ascci, thụt lề 2 unit)
>>>>>>> 30a8a58cb12295289d0255543ead3d991561b1e3
            return True
        except Exception as e:
            print(f"An error occurred when save file!")
            return False



# Book data management
    def check_book_exits(self, book_id):
        for book in self.books:
            if book['_id'] == book_id:
                return True
            return False

    def generate_new_id(self):
        if not self.books:
            return 1
        return max(book['_id'] for book in self.books)+1

    def add_book(self):
        print(f"\n{"="*50}")
        print("➡️ADD NEW BOOK⬅️")
        print("="*50)
        print("Press 0 at any fields to cancel \n")

        try:
    #-----title-----#
            tittle = input("Enter your title: ")
            if tittle == "0":
                print("Cancelled‼️")
                return False
            if not tittle:
                print("")
                return False
        except:
            ...

#Tìm sách theo ID
    def find_book_id(self, id):
        id_list = self.load_books()
        for book in id_list:
            if book['_id'] == id:
                return book
        return None

#Tìm sách theo tên
    def find_book_title(self, key_word):
        book_list = self.load_books()
        result = []
        key_word = key_word.lower()
        for book in book_list:
            if key_word in book['title'].lower():
                result.append(book)
        return result


#Hàm dùng để hiển thị sách
    def display_book(self, book):
        print(f"\n{'='*60}")
        print(f"ID: {book['_id']}")
        print(f"Title: {book['title']}")
        print(f"Page count: {book['pageCount']}")
        print(f"Status: {book['status']}")
        print(f"Authors: {', '.join(book['authors'])}")
        print(f"Categories: {','.join(book['categories'])}")
        print(f"Amount: {book['amount']}")
        print(f"{'='*60}")
    


#Hiển thị menu tìm kiếm sách
    def search_book_menu(self):
        while True:
            print(f"\n{'='*50}")
            print("🔍 Find book!")
            print("="*50)
            print("1. Find books by ID")
            print("2. Find books by title")
            print("0. Exit")
            print("-"*50)

            search = input("👉 Enter your choice: ")

            if search == "1":
                try:
                    id = int(input("Enter book ID: "))
                    book = self.find_book_id(id)
                    if book:
                        self.display_book(book)
                except ValueError:
                    print("ID was wrong!")

            elif search == "2":
                key_word = input("Enter book title: ")
                result = self.find_book_title(key_word)

                if result:
                    print(f"\nFinded {len(result)} result")
                    for book in result:
                        self.display_book(book)
                else:
                    print("Books not found")
                
            elif search == "0":
                break
            else:
                print("Something went wrong")

    def display_book_list(self):
        if not self.books:
            print("📫 Books not in library")
            return

        books_per_page = 10
        total_books = len(self.books)
        total_pages = (total_books + books_per_page - 1) // books_per_page
        current_page = 1

        while True:
            # Tính vị trí
            start = (current_page - 1) * books_per_page
            end = min(start + books_per_page, total_books)
                
                # ===== HIỂN THỊ TIÊU ĐỀ DẠNG MỤC LỤC =====
            print(f"\n")
            print("╔" + "═"*78 + "╗")
            print("║" + " "*30 + "📚 TABLE OF CONTENTS" + " "*33 + "║")
            print("║" + " "*26 + f"(page {current_page}/{total_pages})" + " "*43 + "║")
            print("╠" + "═"*78 + "╣")
                
                # ===== HIỂN THỊ TỪNG SÁCH DẠNG MỤC LỤC =====
            for i in range(start, end):
                book = self.books[i]

                book_id = book['_id']
                title = book['title']
                authors = ', '.join(book['authors'])
                amount = book.get('amount', 0)
                    
                    # ===== ĐỊNH DẠNG DẠNG MỤC LỤC =====
                    # STT. Tên sách ........................... Trang
                    
                    # Tính độ dài để thêm dấu chấm
                    # Công thức: 70 ký tự - độ dài tên - độ dài tác giả
                    
                    # Dòng 1: Số thứ tự và tên sách
                stt = i + 1  # Số thứ tự bắt đầu từ 1
                    
                    # Nếu tên sách quá dài, cắt và thêm "..."
                if len(title) > 55:
                        title_display = title[:52] + "..."
                else:
                    title_display = title
                    # Tính số dấu chấm cần thêm
                    dots_count = 70 - len(f"{stt}. {title_display}") - len(str(book_id))
                    dots = "." * max(dots_count, 3)  # Ít nhất 3 dấu chấm
                    
                    # In dòng sách
                    print(f"║ {stt:>3}. {title_display}{dots}{book_id:>5} ║")
                    
                    # Dòng 2: Tác giả (thụt vào)
                    if len(authors) > 70:
                        authors_display = authors[:67] + "..."
                    else:
                        authors_display = authors
                    
                    print(f"║      ✍️  {authors_display:<67} ║")
                    
                    # Dòng 3: Số lượng (nếu muốn)
                    print(f"║      📦 Remaining: {amount} books{' '*54} ║")
                    # Đường kẻ ngăn cách giữa các sách
                    if i < end - 1:  # Không kẻ ở sách cuối
                        print("║" + " "*78 + "║")

                 # ===== FOOTER MỤC LỤC =====
            print("╠" + "═"*78 + "╣")
            print(f"║ Display {start+1}-{end} in total {total_books} books{' '*(78 - len(f' Display {start+1}-{end} in total {total_books} books'))} ║")
            print("╚" + "═"*78 + "╝")
                
                # ===== MENU ĐIỀU HƯỚNG =====
            if current_page < total_pages:
                print("\n[N] Next page | [P] Previous page | [V] View details | [0] Exit")
                choice = input("👉 Enter your choice: ").upper()
                
                if choice == 'N':
                    current_page += 1
                elif choice == 'P' and current_page > 1:
                    current_page -= 1
                elif choice == 'V':
                    self.view_book_detail()
                elif choice == '0':
                    break
            else:
                print("\n[P] Previous page | [V] View details | [0] Exit")
                choice = input("👉 Enter your choice: ").upper()
                    
                if choice == 'P' and current_page > 1:
                    current_page -= 1
                elif choice == 'V':
                    self.view_book_detail()
                elif choice == '0':
                    break

    def view_book_detail(self):
        """
        View books detail from table of contents
        """
        try:
            book_id = int(input("\n👉 Enter ID to view details: "))
            book = self.find_book_id(book_id)
            
            if book:
                self.display_book(book)
                input("\n⏸️  Press Enter to continue...")
            else:
                print("❌ Books not found!")
                input("\n⏸️  Press Enter to continue...")
        except ValueError:
            print("❌ ID must be number!")
            input("\n⏸️  Press Enter to countinue...")






if __name__ == "__main__":
    Account_system.login_screen() # trả về Boolean
    #------------ hàm để clear màn hình cho đẹp------
    os.system('cls')
    #------------------------
<<<<<<< HEAD
    manager = BookManager()

    while True:
        print("\n")
        print("╔══════════════════════════════════════╗")
        print("║      📚 LIBRARY MANAGEMENT 📚       ║")
        print("╠══════════════════════════════════════╣")
        print("║ 1. Add new book                      ║")
        print("║ 2. Display book list                 ║")
        print("║ 3. Search book                       ║")
        print("║ 4. Edit book information             ║")
        print("║ 5. Delete book                       ║")
        print("║--------------------------------------║")
        print("║ 6. Borrow book                       ║")
        print("║ 7. Return book                       ║")
        print("║ 8. Borrowed book list                ║")
        print("║--------------------------------------║")
        print("║ 0. Exit                              ║")
        print("╚══════════════════════════════════════╝")
        choice = int(input("👉 Choose an option: "))
        #================ choice ==========
        if choice == 1:
            manager.add_book()
        elif choice == 2:
             manager.display_book_list()
        elif choice == 3:
            manager.search_book_menu()
        elif choice == 4:
            ...
        elif choice == 5:
            ...
        elif choice == 6:
            ...
        elif choice == 7:
            ...
        elif choice == 8:
            ...
        elif choice == 0:
            break
            os.system('cls')
            print("Thank you!")
        else: print("ERROR")
=======
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
>>>>>>> 30a8a58cb12295289d0255543ead3d991561b1e3



