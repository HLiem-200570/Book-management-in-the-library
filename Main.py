import json
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
                with open (self.json_file, 'r', encoding = 'utf - 8') as f:    #dòng này dùng để mở file với self.json: tên sách
                                                                               #                             "r": reading -> chế độ đọc
                                                                               # và utf - 8 là mã hóa để đọc được tiếng việt
                    data = json.load(f)
                    return data.get("Book_data", [])
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



