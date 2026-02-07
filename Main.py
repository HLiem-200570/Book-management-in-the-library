import json
from multiprocessing import Value
import os
from datetime import datetime

# Lớp BookManager dùng để quản lý các hàm liên quan đến quản lí sách
class BookManager:
    def __init__(self, json_file = "Book_data.json"):
        self.json_file = json_file          #Hàm dùng lưu tên Book_data.json vào self.json_file để lần sau ko cần nhập tên sách
        self.books = self.load_books    #Hàm dùng để load sách từ file json


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



# Book data management
    def add_Book(self, book_data):

        if self.check_book_exists(book_data['_id']):
            print(f"Book id {book_data["_id"]} has exists!")
            return False

        if not self.check_book_exists(book_data):
            return False

    def display_book_list(self):
        if not self.books:
            print("📫 Books not in library")
            return


    def find_book_id(self, id):
        id_list = self.load_books()
        for book in id_list:
            if book['_id'] == id:
                return book
        return None

    def find_book_title(self, key_word):
        book_list = self.load_books()
        result = []
        key_word = key_word.lower()
        for book in book_list:
            if key_word in book['title'].lower():
                result.append(book)
        return result


    def display_book(self, book):
        print(f"\n{'='*60}")
        print(f"ID: {book['_id']}")
        print(f"Title: {book['title']}")
        print(f"Page count: {book['pageCount']}")
        print(f"Status: {book['status']}")
        print(f"Authors: {', '.join(book['authors'])}")
        print(f"Categories: {','.join(book['categories'])}")
        print(f"Amount: {book['amount']}")
        print(f"{"="*60}")
    

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








if __name__ == "__main__":
    #------------ hàm để clear màn hình cho đẹp------
    os.system('cls')
    #------------------------
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
            ...
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
        elif choice == 0:
            break
            os.system('cls')
            print("Thank you!")
        else: print("ERROR")



