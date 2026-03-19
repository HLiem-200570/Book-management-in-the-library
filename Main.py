import json
import os
import sys
from datetime import datetime

class UI:# tạo class này để mấy hàm mà độc lập riêng biệt cho vào đây đỡ rối
    #đa số hàm riêng biệt là vì "làm cho đẹp" nên mình đặt là UI =))
    @staticmethod
    def gotoxy(x, y):
    # hàm này để đưa con trỏ tời vị trí x, y trong terminal (làm đẹp thôi)
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()
    @staticmethod
    def error():
        while True:
            os.system("cls")
            print("╔══════════════════════════════════════╗")
            print("║                ERROR                 ║")
            print("╠══════════════════════════════════════╣")       
            print("║             1. Return                ║")
            print("║             0. Exit                  ║")
            print("╚══════════════════════════════════════╝")

            choice = input("👉 Choose: ").strip()

            if choice == "1":
                return
            elif choice == "0":
                exit("Thank you!")
            else: error()
    def end():
        os.system("cls")
        print("╔══════════════════════════════════════╗")
        print("║              Thank you!              ║")
        print("╚══════════════════════════════════════╝")
        exit()

#@staticmethod : khi ko dùng biến, dữ liệu của object đó thì xài -> xài xong như 1 hàm độc lập
class Library:#class này để quản lí tất cả các object tụi mình đã tạo 
    def __init__(self):
        self.bookData = "Book_data.json"
        self.bookManager = BookManager()
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
    def load_book(self, filename, data): 
        books = []
        data = self.load_data(bookData)
        for item in data:
            book = Book(
                book_ID = item["_id"],
                title = item["title"], 
                author = item["authors"], 
                category = item["categories"], 
                quantity = item["quantity"], 
                date = item["publishedDate"]
            )
            books.append(book)
        return books
    def admin_menu(self):
        while True:
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║            Book MANAGEMENT           ║")
            print("╠══════════════════════════════════════╣")
            print("║ 1. Add new book                      ║")
            print("║ 2. Display book list                 ║")
            print("║ 3. Search book                       ║")
            print("║ 4. Edit book information             ║")
            print("║ 5. Delete book                       ║")
            print("║--------------------------------------║")
            print("║ 6. View all borrow records           ║")
            print("║--------------------------------------║")
            print("║ 0. Exit                              ║")
            print("╚══════════════════════════════════════╝")
            choice = int(input("👉 Choose an option: "))
            #================ choice ==========
            if choice == 1:
                ...
            elif choice == 2:
                ...
            elif choice == 3:   
                self.bookManager.search_book()
            elif choice == 4:
                ...
            elif choice == 5:
                ...
            elif choice == 6:
                ...
            elif choice == 0:
                UI.end()
            else: UI.error()
    def member_menu(self):
        while True:
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║            Book MANAGEMENT           ║")
            print("╠══════════════════════════════════════╣")
            print("║ 1. Display book list                 ║")
            print("║ 2. Search book                       ║")
            print("║--------------------------------------║")
            print("║ 3. Borrow book                       ║")
            print("║ 4. Return book                       ║")
            print("║ 5. My borrow history                 ║")
            print("║--------------------------------------║")
            print("║ 0. Exit                              ║")
            print("╚══════════════════════════════════════╝")
            choice = int(input("👉 Choose an option: "))
            #================ choice ==========
            if choice == 1:
                ...
            elif choice == 2:
                ...
            elif choice == 3:   
                ...
            elif choice == 4:
                ...
            elif choice == 5:
                ...
            elif choice == 0:
                UI.end()
            else: UI.error()
        
class BookManager:# class BookManager dùng để quản lý các hàm liên quan đến quản lí sách
    def __init__(self, json_file = "Book_data.json"):
        self.json_file = json_file          #Hàm dùng lưu tên Book_data.json vào self.json_file để lần sau ko cần nhập tên sách
        self.books = self.load_books()    #Hàm dùng để load sách từ file json


    #========== XỬ LÝ FILE ===========# 

    # Đọc dữ liệu file #
    def load_books(self):
        if os.path.exists(self.json_file): # dòng này kiểm tra xem file có tên có tồn tại ko
            try:
                with open (self.json_file, 'r', encoding = 'utf - 8') as f:   #dòng này dùng để mở file với self.json: tên sách
                                                                               # "r": reading -> chế độ đọc
                                                                               # và utf - 8 là mã hóa để đọc được tiếng việt
                    return json.load(f)
            except json.JSONDecodeError:  # Nếu file gặp lỗi thì code này sẽ chạy
                print("⚠️ File was wrong, create a new file!")
                return []
        else:# trường hợp không tìm thấy file
            print("⚠️ File doesn't exists, create a new file")
            return []

    # Lưu data vào file
    def save_data(self):
        try:
            with open (self.json_file, 'w', encoding = 'utf - 8') as f:
                json.dump({'books': self.books}, f, ensure_ascii = False, indent = 2) # Dòng này dùng để ghi data vào file json dump(data muốn ghi, nơi ghi, không phải kí tự ascci, thụt lề 2 unit)
            return True
        except Exception as e:
            print(f"An error occurred when save file!")
            return False
        #self.books = Library.load_book()    #Hàm dùng để load sách từ file json
    #===========tools
    def add_Book(self, book_data):
        if self.check_book_exists(book_data['_id']):
            print(f"Book id {book_data["_id"]} has exists!")
            return False

        if not self.check_book_exists(book_data):
            return False
    # Tìm sách theo ID
    def find_book_id(self, book_id):
        id_list = self.load_books()
        for book in id_list:
            if book['_id'] == book_id:
                return book
        return None

    # Tìm sách theo tên
    def find_book_title(self, key_word):
        book_list = self.load_books()
        result = []
        key_word = key_word.lower()
        for book in book_list:
            if key_word in book['title'].lower():
                result.append(book)
        return result

    # Hàm dùng để hiển thị sách
    def display_book(self, book):
        print(f"\n{'='*60}")
        print(f"ID: {book['_id']}")
        print(f"Title: {book['title']}")
        print(f"Page count: {book['pageCount']}")
        print(f"Status: {book['status']}")
        print(f"Authors: {', '.join(book['authors'])}")
        print(f"Categories: {', '.join(book['categories'])}")
        print(f"Quantity: {book['quantity']}")
        print(f"{'='*60}")  # FIX: f-string lồng nhau sai cú pháp

    # Hiển thị menu tìm kiếm sách
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
                    book_id = int(input("Enter book ID: "))  # FIX: đổi id -> book_id
                    book = self.find_book_id(book_id)
                    if book:
                        self.display_book(book)
                except ValueError:
                    print("ID was wrong!")

            elif search == "2":
                key_word = input("Enter book title: ")
                result = self.find_book_title(key_word)

                if result:
                    print(f"\nFound {len(result)} result(s)")
                    for book in result:
                        self.display_book(book)
                else:
                    print("Books not found")

            elif search == "0":
                break
            else:
                print("Invalid choice, please try again.")

    def display_book_list(self):
        if not self.books:
            print("📫 Books not in library")
            return

        books_per_page = 10
        total_books = len(self.books)
        total_pages = (total_books + books_per_page - 1) // books_per_page
        current_page = 1

        while True:
            os.system('cls')
            # Tính vị trí
            start = (current_page - 1) * books_per_page
            end = min(start + books_per_page, total_books)

            # ===== HIỂN THỊ TIÊU ĐỀ =====
            print(f"\n")
            print("╔" + "═"*78 + "╗")
            print("║" + " "*26 + "📚 TABLE OF CONTENTS" + f"{'':^32}" + "║")
            print("║" + " "*30 + f"(Page {current_page:03d}/{total_pages:03d})" + " "*34 + "║")
            print("╠" + "═"*78 + "╣")

            # ===== HIỂN THỊ TỪNG SÁCH =====  # FIX: thêm vòng lặp và khai báo biến
            for i, book in enumerate(self.books[start:end], start=start):
                authors_display = ', '.join(book.get('authors', []))
                amount = book.get('amount', 0)
                title = book.get('title', 'N/A')
                book_id = book.get('_id', 'N/A')

                print(f"║  🆔[{book_id:03d}] 📖 {title:<64} ║")
                print(f"║        ✍️{authors_display:<68} ║")
                print(f"║       Remaining: {amount:<58}  ║")

                if i < end - 1:  # FIX: i giờ đã được định nghĩa trong vòng lặp
                    print("║" + " "*78 + "║")

            # ===== FOOTER =====
            print("╠" + "═"*78 + "╣")
            footer = f" Display {start+1}-{end} in total {total_books} books"
            print(f"║{footer}{' '*(78 - len(footer))}║")
            print("╚" + "═"*78 + "╝")

            # ===== MENU ĐIỀU HƯỚNG =====  # FIX: gộp song ngữ, thêm xử lý [V] và [P]
            nav_options = []
            if current_page < total_pages:
                nav_options.append("[N] Next page")
            if current_page > 1:
                nav_options.append("[P] Previous page")
            nav_options.append("[V] View details")
            nav_options.append("[0] Exit")

            print("\n" + " | ".join(nav_options))
            choice = input("👉 Enter your choice: ").upper()

            if choice == 'N' and current_page < total_pages:
                current_page += 1
            elif choice == 'P' and current_page > 1:  # FIX: thêm xử lý P
                current_page -= 1
            elif choice == 'V':                        # FIX: thêm xử lý V
                self.view_book_detail()
            elif choice == '0':
                break
            else:
                print("Invalid choice, please try again.")

    def view_book_detail(self):
        """View book details from table of contents"""
        try:
            book_id = int(input("\n👉 Enter book ID to view details: "))  # FIX: gộp 2 input thành 1
            book = self.find_book_id(book_id)

            if book:
                self.display_book(book)
                input("\n⏸️  Press Enter to continue...")       # FIX: gộp 2 input thành 1
            else:
                print("❌ Book not found!")
                input("\n⏸️  Press Enter to continue...")       # FIX: gộp 2 input thành 1
        except ValueError:
            print("❌ ID must be a number!")
            input("\n⏸️  Press Enter to continue...")           # FIX: gộp 2 input thành 1
    def create_borrow_record(self, member_id, book_id): pass
    def return_book(self, record_id): pass
    def get_available(self): pass
    #============ functions
    def search_book(self):
        os.system('cls')
        print("╔═══════════════════════════════════════════════╗")
        print("║  Search:                                      ║")
        print("╠═══════════════════════════════════════════════╣")       
        print("║                't' to Search                  ║")
        print("║                'r' to Return                  ║")
        print("╚═══════════════════════════════════════════════╝")
        choice = input("👉 Choose an option: ").strip()
        if choice == 'r':
            return
        elif choice != 't': 
            UI.error()
        #choice == t   
        UI.gotoxy(10, 2)
        keyword = input().strip()
        books = self.find_book(keyword)
        num_result = len(books) # tổng số cuốn sách tìm đươc
        if num_result == 0:
            os.system('cls')
            print("╔═══════════════════════════════════════════════╗")
            print("║                 Nothing Found                 ║")
            print("╠═══════════════════════════════════════════════╣")       
            print("║                 'r' to return                 ║")
            print("╚═══════════════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == 'r': return
            else: UI.error()
        i = 0
        while True:
            books[i].display_book()
            print("╔═══════════════════════════════════════════════╗")
            print(f"║  <{i + 1}/{num_result}>{'':^39}║")
            print("║     'j': Back | '0': Exit  | 'l': Next        ║")      
            print("╚═══════════════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == "j": i = (i + 1) % num_result # vd num = 3: i = (0 + 1)%3 = 1... khi tới i = (0+4)%3 = 1 => quay lại trang đầu tiên
            elif choice == "l": i = (i - 1) % num_result
            elif choice == "0": return 
            else: UI.error()
         
    # ---------- CATEGORY ----------
    def show_books_by_category(self):
        categories = {}

        for book in self.books:
            categories.setdefault(book.category, []).append(book)

        print("\n Books by Category:")
        for cat, books in categories.items():
            print(f"\n {cat}:")
            for b in books:
                print(f"- {b.title}")

    # ---------- MOST BORROWED ----------
    def show_most_borrowed_books(self, top_n=5):
        sorted_books = sorted(self.books, key=lambda b: b.borrow_count, reverse=True)

        print("\n Most Borrowed Books:")
        for b in sorted_books[:top_n]:
            print(f"{b.title} - {b.borrow_count} times")

    def edit_book(self, item): 
        while True:
            os.system('cls')
            Book.display_book(item)
            print("╔═══════════════════════════════════════════════╗")
            print("║  1. Title          2. Author                  ║")
            print("║  3. Category       4. Quantity                ║")
            print("║  5. Availble       0. Return                  ║")
            print("╚═══════════════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == "1": item["title"] = input("New title: ").strip()
            elif choice == "2": item["author"] = input("New author: ").strip()
            elif choice == "3": item["category"] = input("New category: ").strip()
            elif choice == "4": item["quantity"] = input("New quantity: ").strip()
            elif choice == "5": ...
            elif choice == "0": return
            else: 
                UI.error()
                continue
            Library.save_data(book_data, ...)
            ... # in màn hình thành công lưu
        
        
class Book: 
    def __init__(self, book_ID, title, author, category, quantity, date):
        self.book_ID = book_ID
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity
        self.date = date
    def get_available(): ...
        #avail = self.quantity - 
    def is_available(): pass
    def update(): pass
    def decrease(): pass # ch rõ decrease cái j, có thể là available
    def increase(): pass


#======================ACCOUNT====================
class User:
    def __init__(self, user_ID, username, password):
        self.user_ID = user_ID
        self.username = username
        self.password = password 
    def display_info(self, role):
        os.system("cls")
        print("╔══════════════════════════════════════╗")
        print(f"║          Your role {role: <6}            ║") #:< căn lề : kí tự tối đa 6 -> dùng để căn khuôn cho đẹp
        print("╠══════════════════════════════════════╣")
        print(f"║      ID {role: <6}:                      ║")
        print("║      Username:                       ║")
        print("║      Password:                       ║")
        print("║          'r' to return               ║")
        print("╚══════════════════════════════════════╝")
        choice = input("👉 Choose an option: ").strip()
        if choice == "r": return
        else: UI.error()
                  
class Admin(User):
    def __init__(self, admin_ID, username, password): 
        #==== hàm này tạo constructor cho nhanh thay vì phải code lại self.username = username....
        super().__init__(admin_ID, username, password)

class Member(User):
    def __init__(self, member_ID, username, password):
        super().__init__(member_ID, username, password)
    
class AccSystem:
    def __init__(self):
        self.lib = Library()
        self.accData = "Account_data.json"
    #boolean      
    def ID_isRegistered(self, ID):
        account = self.lib.load_data(self.accData)
        for check in account:
            if check["ID"] == ID:
                return True
        return False
    def is_account(self, ID, username, password):
        #kiểm tra tài khoản đúng hay ko
        account = self.lib.load_data(self.accData)
        for check in account: # xét từng hàng trong list
            if check["ID"] == ID and check["Username"] == username and check["Password"] == password:
                return True
        return False
    #handle
    def create_account(self, ID, username, password):
        data = self.lib.load_data(self.accData)
        new_account = {
        "ID": ID,
        "Username": username,
        "Password": password
        }

        data.append(new_account)
        self.lib.save_data(self.accData, data)
    #screen ==== chỉ in ra màn hình và thao tác => ko lưu trữ giá trị => dùng staticmethod
    #==========màn hình đăng nhập                
    def login_screen(self): #trả về chuỗi: role: admin/member
        while True:
            # nếu mình nhập sai thì phải lựa chọn lại => dùng while cho tới khi nhập đúng thì thôi
            # và nếu mình dùng xong hết tính năng thì có thể quay lại menu -> while để tái sử dụng
            # while kết hơp chung với hàm error
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║               Welcome!               ║")
            print("╠══════════════════════════════════════╣")
            print("║1. Login Admin                        ║")
            print("║2. Login Member                       ║")
            print("║3. Create a member account            ║")
            print("║0. Exit                               ║")
            print("╚══════════════════════════════════════╝")
            #================= choosing ==============
            choice = input("👉 Choose an option: ").strip()
            if choice == "1":
                if self.login("admin"): return "admin" 
            elif choice == "2":
                if self.login("member"): return "member" 
            elif choice == '3': 
                self.Sign_up() 
            elif choice == "0":
                UI.end()
            else: 
                UI.error()
    def login(self, role): # boolean
        while True:
            os.system("cls")
            print("╔══════════════════════════════════════╗")
            print(f"║              Login {role: <6}            ║") #:< căn lề : kí tự tối đa 6 -> dùng để căn khuôn cho đẹp
            print("╠══════════════════════════════════════╣")
            print("║          't' to Enter your           ║")
            print(f"║      ID {role: <6}:                      ║")
            print("║      Username:                       ║")
            print("║      Password:                       ║")
            print("║                                      ║")
            print("║          'r' to return               ║")
            print("╚══════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == "t":
                UI.gotoxy(20, 5)
                ID = input().strip()            
                UI.gotoxy(20, 6)
                username = input().strip() 
                UI.gotoxy(20, 7)
                password = input().strip()
                if self.is_account(ID, username, password):
                    return True
                else: 
                    while True:
                        os.system("cls")
                        print("╔══════════════════════════════════════╗")
                        print("║         ACCOUNT NOT CORRECT          ║")
                        print("╠══════════════════════════════════════╣")       
                        print("║             1. Return                ║")
                        print("║             0. Exit                  ║")
                        print("╚══════════════════════════════════════╝")

                        choice = input("👉 Choose: ")

                        if choice == "1":
                            return
                        elif choice == "0":
                            exit("Thank you!")
                        else:
                            UI.error()
            elif choice == "r":
                return False
            else: 
                UI.error()
    def Sign_up(self): # ko trả về gì
        while True:
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║           Create an account          ║")
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
                UI.gotoxy(20, 5)
                ID = input().strip()            
                UI.gotoxy(20, 6)
                username = input().strip() 
                UI.gotoxy(20, 7)
                password = input().strip()
                if self.is_account(ID, username, password):
                    self.registered_scr()
                else: 
                    if self.ID_isRegistered(ID):  #=========nếu đã đăng kí ID
                        while True:
                            os.system('cls')
                            print("╔══════════════════════════════════════╗")
                            print("║           ID is registered!          ║")
                            print("╠══════════════════════════════════════╣")
                            print("║           'r' to return              ║")
                            print("╚══════════════════════════════════════╝")
                            
                            choice = input("👉 Choose an option: ").strip()
                            if choice == "r": 
                                return 
                            else: 
                                UI.error()
                    else: # ==========nếu chưa đăng kí          
                        self.create_account(ID, username, password)
                        while True:
                            os.system('cls')
                            print("╔══════════════════════════════════════╗")
                            print("║             Successful!              ║")
                            print("╠══════════════════════════════════════╣")
                            print("║           'r' to return              ║")
                            print("╚══════════════════════════════════════╝")
                            choice = input("👉 Choose an option: ").strip()
                            if choice == "r": 
                                return 
                            else: 
                                UI.error()
            elif choice == "r": 
                return False
            else: UI.error()
#=================================================  

def main(): pass

if __name__ == "__main__":
    # đăng nhập rồi mới được vào 
    '''
    acc = AccSystem()
    role = acc.login_screen()  # => admin/member
    '''
    manager = BookManager()
    while True:
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
            ...
        elif choice == 2:
            manager.display_book_list()
    lib = Library()
    #if role =="admin":
    lib.admin_menu()
    #else:  
        #lib.member_menu()
        



