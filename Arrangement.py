import json
import os
import sys
from datetime import datetime


# ============================================================
# CẤU HÌNH FILE
# ============================================================

BOOK_FILE    = "Book_data.json"
ACCOUNT_FILE = "Account_data.json"


# ============================================================
# DATA LAYER
# ============================================================

class FileManager:
    # class này dùng để đọc/ghi file JSON
    def __init__(self, filename):
        self.filename = filename

    def load(self):
        # đọc file JSON, trả về list[dict]. Nếu lỗi hoặc không tồn tại trả về []
        if os.path.exists(self.filename):
            try:
                with open(self.filename, 'r', encoding='utf-8') as f:
                    return json.load(f)
            except json.JSONDecodeError:
                print("⚠️ File was wrong, create a new file!")
                return []
        else:
            print("⚠️ File doesn't exists, create a new file")
            return []

    def save(self, data):
        # ghi data (list[dict]) xuống file JSON. Trả về bool
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            print("An error occurred when save file!")
            return False


# ============================================================
# MODEL LAYER
# ============================================================

class Book:
    def __init__(self, book_ID, title, author, category, quantity, date, pageCount=0, status="PUBLISH", isbn=""):
        self.book_ID   = book_ID
        self.title     = title
        self.author    = author    # list[str]
        self.category  = category  # list[str]
        self.quantity  = quantity
        self.date      = date
        self.pageCount = pageCount
        self.status    = status
        self.isbn      = isbn

    def get_available(self, borrow_records):
        # đếm số phiếu mượn chưa trả, lấy quantity trừ đi
        borrowed = sum(
            1 for r in borrow_records
            if r.book_id == self.book_ID and r.return_date is None
        )
        return self.quantity - borrowed

    def is_available(self, borrow_records):
        return self.get_available(borrow_records) > 0

    def display_book(self):
        # in thông tin chi tiết 1 cuốn sách ra terminal
        print("╔" + "═"*60 + "╗")
        print(f"║  ID        : {str(self.book_ID):<44} ║")
        print(f"║  Title     : {self.title:<44} ║")
        print(f"║  Page count: {str(self.pageCount):<44} ║")
        print(f"║  Status    : {self.status:<44} ║")
        print(f"║  Authors   : {', '.join(self.author):<44} ║")
        print(f"║  Categories: {', '.join(self.category):<44} ║")
        print(f"║  Quantity  : {str(self.quantity):<44} ║")
        print("╚" + "═"*60 + "╝")

    def update(self): pass
    def decrease(self): pass
    def increase(self): pass

    def to_dict(self):
        # chuyển object Book → dict để lưu xuống file JSON
        return {
            "_id":           self.book_ID,
            "title":         self.title,
            "isbn":          self.isbn,
            "pageCount":     self.pageCount,
            "publishedDate": self.date,
            "status":        self.status,
            "authors":       self.author,
            "categories":    self.category,
            "quantity":      self.quantity
        }

    @staticmethod
    def from_dict(data):
        # chuyển dict từ JSON → object Book để dùng display_book() và các hàm khác
        return Book(
            book_ID   = data["_id"],
            title     = data.get("title", ""),
            author    = data.get("authors", []),
            category  = data.get("categories", []),
            quantity  = data.get("quantity", 0),
            date      = data.get("publishedDate", ""),
            pageCount = data.get("pageCount", 0),
            status    = data.get("status", "PUBLISH"),
            isbn      = data.get("isbn", "")
        )


class User:
    def __init__(self, user_ID, username, password):
        self.user_ID  = user_ID
        self.username = username
        self.password = password

    def display_info(self, role):
        os.system("cls")
        print("╔══════════════════════════════════════╗")
        print(f"║          Your role {role: <6}            ║")
        print("╠══════════════════════════════════════╣")
        print(f"║      ID {role: <6}:                      ║")
        print("║      Username:                       ║")
        print("║      Password:                       ║")
        print("║          'r' to return               ║")
        print("╚══════════════════════════════════════╝")
        choice = input("👉 Choose an option: ").strip()
        if choice == "r":
            return

    def to_dict(self, role="member"):
        # chuyển object User → dict để lưu xuống Account_data.json
        # cấu trúc account gồm: thông tin đăng nhập + dữ liệu mượn sách của member
        return {
            "ID":                  self.user_ID,
            "Username":            self.username,
            "Password":            self.password,
            "role":                role,
            "total_borrows":       0,   # tổng số lần mượn từ trước đến nay
            "currently_borrowing": 0,   # số sách đang mượn chưa trả
            "borrow_history":      []   # lịch sử: [{book_id, title, borrow_date, return_date}]
        }


class Admin(User):
    def __init__(self, admin_ID, username, password):
        super().__init__(admin_ID, username, password)


class Member(User):
    def __init__(self, member_ID, username, password):
        super().__init__(member_ID, username, password)


# ============================================================
# BUSINESS LOGIC LAYER
# ============================================================

class BookManager:
    # class này quản lý các hàm liên quan đến sách
    def __init__(self):
        self.repo  = FileManager(BOOK_FILE)
        self.books = self.repo.load()   # load sách từ file json lên

    # ========== THÊM SÁCH ==========

    def add_Book(self):
        while True:
            try:
                book_id = int(input("👉 Book ID      : ").strip())
            except ValueError:
                print("   ⚠️  ID must be a number!")
                continue
            if book_id == 0:
                return
            if any(b['_id'] == book_id for b in self.books):
                print(f"   ❌ ID {book_id} already exists! Please enter a different ID.")
                continue
            break

        title = input("👉 Title        : ").strip()
        while not title:
            print("   ⚠️  Title cannot be empty!")
            title = input("👉 Title        : ").strip()

        isbn = input("👉 ISBN         : ").strip()

        while True:
            try:
                page_count = int(input("👉 Page count   : ").strip())
                break
            except ValueError:
                print("   ⚠️  Page count must be a number!")

        authors_input = input("👉 Authors (comma-separated): ").strip()
        authors = [a.strip() for a in authors_input.split(',') if a.strip()]

        categories_input = input("👉 Categories (comma-separated): ").strip()
        categories = [c.strip() for c in categories_input.split(',') if c.strip()]

        while True:
            try:
                quantity = int(input("👉 Quantity     : ").strip())
                if quantity < 0:
                    print("   ⚠️  Quantity must be >= 0!")
                    continue
                break
            except ValueError:
                print("   ⚠️  Quantity must be a number!")

        new_book = {
            "_id":           book_id,
            "title":         title,
            "isbn":          isbn,
            "pageCount":     page_count,
            "publishedDate": {"$date": datetime.now().strftime("%Y-%m-%dT%H:%M:%S.000+0000")},
            "status":        "PUBLISH",
            "authors":       authors,
            "categories":    categories,
            "quantity":      quantity,
            "borrow_count":  0
        }

        self.books.append(new_book)
        if self.repo.save(self.books):
            print(f"\n✅ Book '{title}' added successfully!")
        else:
            print("\n❌ Failed to save to file!")
            self.books.pop()

        input("\n⏸️  Press Enter to continue...")

    # ========== TÌM SÁCH ==========

    def find_book_id(self, book_id):
        for book in self.books:
            if book['_id'] == book_id:
                return book
        return None

    def find_book_title(self, key_word):
        result   = []
        key_word = key_word.lower()
        for book in self.books:
            if key_word in book['title'].lower():
                result.append(book)
        return result

    def find_book(self, key_word):
        # tìm sách rồi chuyển sang list[Book] — dùng cho search_book()
        return [Book.from_dict(b) for b in self.find_book_title(key_word)]

    # ========== HIỂN THỊ ==========

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
            return

        UI.gotoxy(12, 2)
        keyword    = input().strip()
        books      = self.find_book(keyword)
        num_result = len(books)

        if num_result == 0:
            os.system('cls')
            print("╔═══════════════════════════════════════════════╗")
            print("║                 Nothing Found                 ║")
            print("╠═══════════════════════════════════════════════╣")
            print("║                 'r' to return                 ║")
            print("╚═══════════════════════════════════════════════╝")
            input("👉 Choose an option: ").strip()
            return

        i = 0
        while True:
            os.system('cls')
            books[i].display_book()
            print("╔═══════════════════════════════════════════════╗")
            print(f"║  <{i + 1}/{num_result}>{'':^39}║")
            print("║     'j': Back | '0': Exit  | 'l': Next        ║")
            print("╚═══════════════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if   choice == "j": i = (i + 1) % num_result
            elif choice == "l": i = (i - 1) % num_result
            elif choice == "0": return

    def display_book_list(self):
        if not self.books:
            print("📫 Books not in library")
            return

        books_per_page = 10
        total_books    = len(self.books)
        total_pages    = (total_books + books_per_page - 1) // books_per_page
        current_page   = 1

        while True:
            os.system('cls')
            start = (current_page - 1) * books_per_page
            end   = min(start + books_per_page, total_books)

            print("╔" + "═"*78 + "╗")
            print("║" + " "*26 + "📚 TABLE OF CONTENTS" + f"{'':^32}" + "║")
            print("║" + " "*30 + f"(Page {current_page:03d}/{total_pages:03d})" + " "*34 + "║")
            print("╠" + "═"*78 + "╣")

            for i, book in enumerate(self.books[start:end], start=start):
                authors_display = ', '.join(book.get('authors', []))
                amount          = book.get('quantity', 0)
                title           = book.get('title', 'N/A')
                book_id         = book.get('_id', 'N/A')

                print(f"║  🆔[{book_id:03d}] 📖 {title:<64} ║")
                print(f"║        ✍️  {authors_display:<66} ║")
                print(f"║       Remaining: {amount:<58}  ║")

                if i < end - 1:
                    print("║" + " "*78 + "║")

            print("╠" + "═"*78 + "╣")
            footer = f" Display {start+1}-{end} in total {total_books} books"
            print(f"║{footer}{' '*(78 - len(footer))}║")
            print("╚" + "═"*78 + "╝")

            nav_options = []
            if current_page < total_pages: nav_options.append("[N] Next page")
            if current_page > 1:           nav_options.append("[P] Previous page")
            nav_options.append("[V] View details")
            nav_options.append("[0] Exit")
            print("\n" + " | ".join(nav_options))

            choice = input("👉 Enter your choice: ").upper()
            if   choice == 'N' and current_page < total_pages: current_page += 1
            elif choice == 'P' and current_page > 1:           current_page -= 1
            elif choice == 'V': self.view_book_detail()
            elif choice == '0': break

    def view_book_detail(self):
        try:
            book_id  = int(input("\n👉 Enter book ID to view details: "))
            book_raw = self.find_book_id(book_id)
            if book_raw:
                Book.from_dict(book_raw).display_book()
                input("\n⏸️  Press Enter to continue...")
            else:
                print("❌ Book not found!")
                input("\n⏸️  Press Enter to continue...")
        except ValueError:
            print("❌ ID must be a number!")
            input("\n⏸️  Press Enter to continue...")

    # ========== MƯỢN / TRẢ SÁCH ==========

    def borrow_book(self, book_id, member_id):
        # mượn sách: cập nhật cả books lẫn account của member
        accounts = FileManager(ACCOUNT_FILE).load()
        member   = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not member:
            print("❌ Member not found.")
            return False

        for book in self.books:
            if str(book["_id"]) == str(book_id):
                if book.get("quantity", 0) > 0:
                    # cập nhật sách
                    book["quantity"]    -= 1
                    book["is_borrowed"]  = True
                    book["borrow_count"] = book.get("borrow_count", 0) + 1
                    self.repo.save(self.books)

                    # cập nhật member
                    member["total_borrows"]       = member.get("total_borrows", 0) + 1
                    member["currently_borrowing"] = member.get("currently_borrowing", 0) + 1
                    member.setdefault("borrow_history", []).append({
                        "book_id":     book["_id"],
                        "title":       book["title"],
                        "borrow_date": datetime.now().strftime("%Y-%m-%d"),
                        "return_date": None
                    })
                    FileManager(ACCOUNT_FILE).save(accounts)

                    print(f"✅ Borrowed book: {book['title']}")
                    return True
                else:
                    print("❌ Book not available to borrow.")
                    return False

        print("❌ Book ID not found.")
        return False

    def borrow_book_interactive(self, member_id):
        try:
            book_id = int(input("Enter book ID to borrow: ").strip())
            self.borrow_book(book_id, member_id)
        except ValueError:
            print("❌ ID must be a number!")

    def return_book(self, book_id, member_id):
        # trả sách: cập nhật cả books lẫn borrow_history của member
        accounts = FileManager(ACCOUNT_FILE).load()
        member   = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not member:
            print("❌ Member not found.")
            return False

        for book in self.books:
            if str(book["_id"]) == str(book_id):
                if not book.get("is_borrowed", False):
                    print("❌ This book was not borrowed.")
                    return False

                # cập nhật sách
                book["quantity"]   += 1
                book["is_borrowed"] = False
                self.repo.save(self.books)

                # cập nhật return_date trong borrow_history
                for record in reversed(member.get("borrow_history", [])):
                    if str(record["book_id"]) == str(book_id) and record["return_date"] is None:
                        record["return_date"] = datetime.now().strftime("%Y-%m-%d")
                        break
                member["currently_borrowing"] = max(0, member.get("currently_borrowing", 1) - 1)
                FileManager(ACCOUNT_FILE).save(accounts)

                print(f"✅ Returned book: {book['title']}")
                return True

        print("❌ Book ID not found.")
        return False

    def return_book_interactive(self, member_id):
        try:
            book_id = int(input("Enter book ID to return: ").strip())
            self.return_book(book_id, member_id)
        except ValueError:
            print("❌ ID must be a number!")

    def list_borrowed_books(self):
        # hiển thị danh sách sách đang được mượn (dành cho admin)
        borrowed = [book for book in self.books if book.get("is_borrowed", False)]
        if not borrowed:
            print("📭 No borrowed books!")
            return
        print("\n" + "="*60)
        print("📚 LIST OF BORROWED BOOKS")
        print("="*60)
        for i, book in enumerate(borrowed, start=1):
            print(f"{i:>2}. ID: {book['_id']} | Title: {book['title']} | "
                  f"Authors: {', '.join(book['authors'])} | Remaining: {book.get('quantity', 0)}")
        print("="*60)

    def my_borrow_history(self, member_id):
        # hiển thị lịch sử mượn của 1 member cụ thể
        accounts = FileManager(ACCOUNT_FILE).load()
        member   = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not member:
            print("❌ Member not found.")
            return

        history = member.get("borrow_history", [])
        if not history:
            print("📭 No borrow history!")
            return

        print("\n" + "="*70)
        print(f"📋 BORROW HISTORY — {member['Username']}")
        print(f"   Total borrows: {member.get('total_borrows', 0)} | "
              f"Currently borrowing: {member.get('currently_borrowing', 0)}")
        print("="*70)
        for i, record in enumerate(history, start=1):
            return_date = record['return_date'] if record['return_date'] else "Not returned yet"
            print(f"{i:>2}. [{record['book_id']}] {record['title']:<40} "
                  f"Borrowed: {record['borrow_date']} | Returned: {return_date}")
        print("="*70)

    def show_my_profile(self, member_id):
        # hiển thị thông tin cá nhân + thống kê mượn sách của member
        accounts = FileManager(ACCOUNT_FILE).load()
        member   = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not member:
            print("❌ Member not found.")
            return

        currently = member.get("currently_borrowing", 0)
        total     = member.get("total_borrows", 0)
        history   = member.get("borrow_history", [])

        # sách đang mượn chưa trả
        active = [r for r in history if r["return_date"] is None]

        os.system('cls')
        print("╔══════════════════════════════════════════════════╗")
        print("║                  MY PROFILE                      ║")
        print("╠══════════════════════════════════════════════════╣")
        print(f"║  ID               : {str(member['ID']):<29}║")
        print(f"║  Username         : {member['Username']:<29}║")
        print(f"║  Role             : {member['role']:<29}║")
        print("╠══════════════════════════════════════════════════╣")
        print(f"║  Total borrows    : {str(total):<29}║")
        print(f"║  Currently borrow : {str(currently):<29}║")
        print("╠══════════════════════════════════════════════════╣")

        if active:
            print("║  Books currently borrowed:                       ║")
            for r in active:
                line = f"  [{r['book_id']}] {r['title'][:35]} (since {r['borrow_date']})"
                print(f"║{line:<50}║")
        else:
            print("║  No books currently borrowed.                    ║")

        print("╚══════════════════════════════════════════════════╝")

    # ========== SỬA / XOÁ SÁCH ==========

    def edit_book(self, item):
        while True:
            os.system('cls')
            Book.from_dict(item).display_book()
            print("╔═══════════════════════════════════════════════╗")
            print("║  1. Title          2. Author                  ║")
            print("║  3. Category       4. Quantity                ║")
            print("║  5. Available      0. Save & Return           ║")
            print("╚═══════════════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()

            if   choice == "1": item["title"]      = input("New title: ").strip()
            elif choice == "2": item["authors"]    = [input("New author: ").strip()]
            elif choice == "3": item["categories"] = [input("New category: ").strip()]
            elif choice == "4":
                try:
                    item["quantity"] = int(input("New quantity: ").strip())
                except ValueError:
                    print("⚠️  Quantity must be a number!")
                    input("\n⏸️  Press Enter to continue...")
            elif choice == "5": pass
            elif choice == "0":
                for i, b in enumerate(self.books):
                    if b["_id"] == item["_id"]:
                        self.books[i] = item
                        break
                if self.repo.save(self.books):
                    print("✅ Saved successfully!")
                else:
                    print("❌ Failed to save!")
                input("\n⏸️  Press Enter to continue...")
                return

    def delete_book(self, book_id):
        # xóa sách theo ID, không cho xóa nếu đang được mượn
        book = self.find_book_id(book_id)
        if not book:
            return False, "Book not found!"
        if book.get("is_borrowed", False):
            return False, "Cannot delete — book is currently borrowed!"
        self.books = [b for b in self.books if b["_id"] != book_id]
        if self.repo.save(self.books):
            return True, f"Book '{book['title']}' deleted successfully!"
        return False, "Failed to save!"

    # ========== THỐNG KÊ ==========

    def show_statistics(self):
        # thống kê: sách mượn nhiều nhất + số sách hiện có trong kho
        os.system('cls')
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                    LIBRARY STATISTICS                   ║")
        print("╠══════════════════════════════════════════════════════════╣")

        sorted_books = sorted(self.books, key=lambda b: b.get('borrow_count', 0), reverse=True)
        print("║  📈 Most borrowed books (top 5):                         ║")
        for i, b in enumerate(sorted_books[:5], start=1):
            line = f"  {i}. {b['title'][:35]:<35} — {b.get('borrow_count', 0)} times"
            print(f"║{line:<58}║")

        print("╠══════════════════════════════════════════════════════════╣")

        total_titles = len(self.books)
        total_copies = sum(b.get('quantity', 0) for b in self.books)
        borrowed_now = sum(1 for b in self.books if b.get('is_borrowed', False))

        print(f"║  📚 Total titles in library : {total_titles:<28}║")
        print(f"║  📦 Total copies available  : {total_copies:<28}║")
        print(f"║  🔖 Books currently borrowed: {borrowed_now:<28}║")
        print("╚══════════════════════════════════════════════════════════╝")
        input("\n⏸️  Press Enter to continue...")

    def show_books_by_category(self):
        categories = {}
        for book in self.books:
            for cat in book.get('categories', []):
                categories.setdefault(cat, []).append(book)
        print("\n Books by Category:")
        for cat, books in categories.items():
            print(f"\n  {cat}:")
            for b in books:
                print(f"  - {b['title']}")

    def create_borrow_record(self, member_id, book_id): pass
    def get_available(self): pass


class AccSystem:
    # class này quản lý đăng nhập / đăng ký tài khoản
    def __init__(self):
        self.repo = FileManager(ACCOUNT_FILE)

    def ID_isRegistered(self, ID):
        account = self.repo.load()
        for check in account:
            if check["ID"] == ID:
                return True
        return False

    def is_account(self, ID, username, password):
        account = self.repo.load()
        for check in account:
            if check["ID"] == ID and check["Username"] == username and check["Password"] == password:
                return True
        return False

    def create_account(self, ID, username, password):
        data        = self.repo.load()
        new_account = Member(ID, username, password).to_dict(role="member")
        data.append(new_account)
        self.repo.save(data)

    def login_screen(self):
        # trả về (role, member_id)
        while True:
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║               Welcome!               ║")
            print("╠══════════════════════════════════════╣")
            print("║1. Login Admin                        ║")
            print("║2. Login Member                       ║")
            print("║3. Create a member account            ║")
            print("║0. Exit                               ║")
            print("╚══════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()
            if choice == "1":
                result = self.login("admin")
                if result: return "admin", result
            elif choice == "2":
                result = self.login("member")
                if result: return "member", result
            elif choice == '3':
                self.Sign_up()
            elif choice == "0":
                UI.end()

    def login(self, role):
        # trả về member_id nếu đúng, False nếu sai hoặc thoát
        while True:
            os.system("cls")
            print("╔══════════════════════════════════════╗")
            print(f"║              Login {role: <6}            ║")
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
                ID       = input().strip()
                UI.gotoxy(20, 6)
                username = input().strip()
                UI.gotoxy(20, 7)
                password = input().strip()
                if self.is_account(ID, username, password):
                    return ID   # trả về ID để dùng cho borrow/return/profile
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
                            return False
                        elif choice == "0":
                            exit("Thank you!")
            elif choice == "r":
                return False

    def Sign_up(self):
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
                ID       = input().strip()
                UI.gotoxy(20, 6)
                username = input().strip()
                UI.gotoxy(20, 7)
                password = input().strip()
                if self.is_account(ID, username, password):
                    while True:
                        os.system('cls')
                        print("╔══════════════════════════════════════╗")
                        print("║        Account already exists!       ║")
                        print("╠══════════════════════════════════════╣")
                        print("║           'r' to return              ║")
                        print("╚══════════════════════════════════════╝")
                        choice = input("👉 Choose an option: ").strip()
                        if choice == "r":
                            return
                else:
                    if self.ID_isRegistered(ID):
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
            elif choice == "r":
                return False


# ============================================================
# PRESENTATION LAYER
# ============================================================

class UI:
    @staticmethod
    def gotoxy(x, y):
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    @staticmethod
    def end():
        os.system("cls")
        print("╔══════════════════════════════════════╗")
        print("║              Thank you!              ║")
        print("╚══════════════════════════════════════╝")
        exit()


class Library:
    def __init__(self):
        self.bookManager = BookManager()

    def admin_menu(self):
        while True:
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║           ADMIN DASHBOARD            ║")
            print("╠══════════════════════════════════════╣")
            print("║ 1. Add new book                      ║")
            print("║ 2. Display book list                 ║")
            print("║ 3. Search book                       ║")
            print("║ 4. Edit book information             ║")
            print("║ 5. Delete book                       ║")
            print("║--------------------------------------║")
            print("║ 6. View all borrow records           ║")
            print("║ 7. Statistics                        ║")
            print("║--------------------------------------║")
            print("║ 0. Exit                              ║")
            print("╚══════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()

            if choice == "1":
                self.bookManager.add_Book()
            elif choice == "2":
                self.bookManager.display_book_list()
            elif choice == "3":
                self.bookManager.search_book()
            elif choice == "4":
                try:
                    book_id  = int(input("Enter book ID to edit: "))
                    book_raw = self.bookManager.find_book_id(book_id)
                    if book_raw:
                        self.bookManager.edit_book(book_raw)
                    else:
                        print("❌ Book not found!")
                        input("\n⏸️  Press Enter to continue...")
                except ValueError:
                    print("❌ ID must be a number!")
                    input("\n⏸️  Press Enter to continue...")
            elif choice == "5":
                try:
                    book_id  = int(input("Enter book ID to delete: "))
                    ok, msg  = self.bookManager.delete_book(book_id)
                    print(f"✅ {msg}" if ok else f"❌ {msg}")
                    input("\n⏸️  Press Enter to continue...")
                except ValueError:
                    print("❌ ID must be a number!")
                    input("\n⏸️  Press Enter to continue...")
            elif choice == "6":
                self.bookManager.list_borrowed_books()
                input("\n⏸️  Press Enter to continue...")
            elif choice == "7":
                self.bookManager.show_statistics()
            elif choice == "0":
                UI.end()

    def member_menu(self, member_id):
        while True:
            os.system('cls')
            print("╔══════════════════════════════════════╗")
            print("║           MEMBER PORTAL              ║")
            print("╠══════════════════════════════════════╣")
            print("║ 1. Display book list                 ║")
            print("║ 2. Search book                       ║")
            print("║--------------------------------------║")
            print("║ 3. Borrow book                       ║")
            print("║ 4. Return book                       ║")
            print("║ 5. My borrow history                 ║")
            print("║ 6. My profile                        ║")
            print("║--------------------------------------║")
            print("║ 0. Exit                              ║")
            print("╚══════════════════════════════════════╝")
            choice = input("👉 Choose an option: ").strip()

            if choice == "1":
                self.bookManager.display_book_list()
            elif choice == "2":
                self.bookManager.search_book()
            elif choice == "3":
                self.bookManager.borrow_book_interactive(member_id)
                input("\n⏸️  Press Enter to continue...")
            elif choice == "4":
                self.bookManager.return_book_interactive(member_id)
                input("\n⏸️  Press Enter to continue...")
            elif choice == "5":
                self.bookManager.my_borrow_history(member_id)
                input("\n⏸️  Press Enter to continue...")
            elif choice == "6":
                self.bookManager.show_my_profile(member_id)
                input("\n⏸️  Press Enter to continue...")
            elif choice == "0":
                UI.end()


# ============================================================
# ENTRY POINT
# ============================================================

def main(): pass

if __name__ == "__main__":
    acc             = AccSystem()
    role, member_id = acc.login_screen()   # trả về (role, ID)

    lib = Library()
    if role == "admin":
        lib.admin_menu()
    else:
        lib.member_menu(member_id)

