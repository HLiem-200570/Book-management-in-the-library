import json
from multiprocessing import Value
import os
from datetime import datetime

# Lớp BookManager dùng để quản lý các hàm liên quan đến quản lí sách
class BookManager:
    def __init__(self, json_file = "Book_data.json"):
        self.json_file = json_file          #Hàm dùng lưu tên Book_data.json vào self.json_file để lần sau ko cần nhập tên sách
        self.books = self.load_books()    #Hàm dùng để load sách từ file json


    #========== XỬ LÝ FILE ===========# 

    # Đọc dữ liệu file #
    def load_books(self):
        if os.path.exists(self.json_file): # dòng này kiểm tra xem file có tên có tồn tại ko
            try:
                with open (self.json_file, 'r', encoding = 'utf-8') as f:   #dòng này dùng để mở file với self.json: tên sách
                                                                               # "r": reading -> chế độ đọc
                                                                               # và utf - 8 là mã hóa để đọc được tiếng việt
                    data = json.load(f)
                    if isinstance(data, list):
                        return data
                    if isinstance(data, dict) and 'books' in data:
                        return data ['books']
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
            with open (self.json_file, 'w', encoding = 'utf-8') as f:
                json.dump(self.books, f, ensure_ascii = False, indent = 2) # Dòng này dùng để ghi data vào file json dump(data muốn ghi, nơi ghi, không phải kí tự ascci, thụt lề 2 unit)
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
    #------------ hàm để clear màn hình cho đẹp------
    os.system('cls')
    #------------------------
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



