import datetime

class User:
    def __init__(self, user_id, name, username, password):
        self.user_id = user_id
        self.name = name
        self.username = username
        self.password = password

    def login(self, username, password): pass
    def display_info(self): pass


class Admin(User):
    def __init__(self, user_id, name, username, password):
        super().__init__(user_id, name, username, password)

    def add_book(self, library, book): pass
    def remove_book(self, library, book_id): pass
    def update_book(self, library, book_id, new_data): pass
    def view_reports(self, library): pass


class Member(User):
    def __init__(self, user_id, name, username, password):
        super().__init__(user_id, name, username, password)
        self.borrowed_records = []

    def borrow_book(self, record): pass
    def return_book(self, record): pass
    def view_borrowed_books(self): pass
    def display_info(self): pass


class Book:
    def __init__(self, book_id, title, author, category, quantity):
        self.book_id = book_id
        self.title = title
        self.author = author
        self.category = category
        self.quantity = quantity
        self.available = quantity

    def is_available(self): pass
    def decrease(self, amount=1): pass
    def increase(self, amount=1): pass
    def update(self, title, author, category): pass
    def display_info(self): pass


class Book_borrow:
    def __init__(self, borrow_id, member, book, borrow_date, due_date):
        self.borrow_id = borrow_id
        self.member = member
        self.book = book
        self.borrow_date = borrow_date
        self.due_date = due_date
        self.return_date = None
        self.status = "Borrowed"
        self.fine_amount = 0.0

    def mark_returned(self, return_date): pass
    def is_overdue(self, current_date): pass
    def calculate_fine(self, current_date): pass
    def display_record(self): pass


class Library:
    def __init__(self):
        self.books = []
        self.members = []
        self.records = []

    def register_member(self, member): pass
    def find_book(self, book_id): pass
    def create_borrow_record(self, member_id, book_id): pass
    def return_book(self, record_id): pass
    def save_data(self, file_path): pass
    def load_data(self, file_path): pass
    
#========================= Menu==================
def main():
	os.system('cls')
	library = Library()
	admin = Admin("AD001", "Quan tri vien", "admin", "123456")
	library.books = [
        Book("B001", "Lap trinh Python", "Nguyen Van A", "CNTT", 3),
        Book("B002", "Cau truc du lieu", "Tran Thi B", "CNTT", 2),
    ]
	library.members = [
        Member("M001", "Nguyen Minh", "minh", "123"),
    ]
	while True:
        print("╔══════════════════════════════════════╗")
        print("║   HE THONG QUAN LY THU VIEN SACH     ║")
        print("╠══════════════════════════════════════╣")
        print("║1. Login Admin                        ║")
        print("║2. Login Member                       ║")
        print("║0. Exit                               ║")
        print("╚══════════════════════════════════════╝")
        choice = input("Chon: ").strip()

        if choice == "1":
            uname = input("Username: ")
            pwd   = input("Password: ")
            if admin.username == uname and admin.password == pwd:
                print(f"Xin chao {admin.name}!")
                while True:
					print("╔══════════════════════════════════════╗")
					print("║          LIBRARY MANAGEMENT          ║")
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
                    c = input("Chon: ").strip()
                    if c == "0":
                        break

        elif choice == "2":
            uname = input("Username: ")
            pwd   = input("Password: ")
            member = None
            for m in library.members:
                if m.username == uname and m.password == pwd:
                    member = m
                    break
            if not member:
                print("Sai tai khoan.")
                continue
            print(f"Xin chao {member.name}!")
            while True:
                print("╔══════════════════════════════════════╗")
                print(f"║    MENU THANH VIEN - {member.name}   ║")
                print("╠══════════════════════════════════════╣")
                print("║1. View available                     ║")
                print("║2. Borrow book                        ║")
                print("║3. Return book                        ║")
                print("║4. View borrowed books                ║")
                print("║0. Log out                            ║")
                print("╚══════════════════════════════════════╝")
                c = input("Chon: ").strip()
                if c == "0":
                    break

        elif choice == "0":
            print("Goodbye!!")
            break


if __name__ == "__main__":
    main()
