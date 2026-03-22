import json
import os
import sys
from datetime import datetime

BOOK_FILE    = "Book_data.json"
ACCOUNT_FILE = "Account_data.json"

# ============================================================
# DATA 
# ============================================================

class FileManager:
    # Đọc/ghi file JSON — dùng chung cho Book và Account
    def __init__(self, filename):
        self.filename = filename
        
    def load(self):# -> list[dict] | []
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
        # -> bool
        try:
            with open(self.filename, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return True
        except Exception:
            print("An error occurred when save file!")
            return False


# ============================================================
# MODEL 
# ============================================================

class Book:
    # Đại diện 1 cuốn sách — thêm display_book(), to_dict(), from_dict()
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

    def get_available(self, borrow_records):# -> int  (quantity - số đang mượn chưa trả)
        borrowed = sum(
            1 for r in borrow_records
            if r.book_id == self.book_ID and r.return_date is None
        )
        return self.quantity - borrowed

    def is_available(self, borrow_records):# -> bool
        return self.get_available(borrow_records) > 0

    def display_book(self):# -> None  (in thông tin sách ra terminal)
        print("╔" + "═"*60 + "╗")
        print(f"║  ID        : {str(self.book_ID):<44} ║")
        print(f"║  Title     : {self.title:<44} ║")
        print(f"║  Page count: {str(self.pageCount):<44} ║")
        print(f"║  Status    : {self.status:<44} ║")
        print(f"║  Authors   : {', '.join(self.author):<44} ║")
        print(f"║  Categories: {', '.join(self.category):<44} ║")
        print(f"║  Quantity  : {str(self.quantity):<44} ║")
        print("╚" + "═"*60 + "╝")

    def to_dict(self):# -> dict  (dùng để lưu xuống JSON)
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
    def from_dict(data):# -> Book  (chuyển dict từ JSON thành object Book)
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


class BorrowRecord:
    # Đại diện 1 lần mượn sách — liên kết Member ↔ Book
    # Thêm mới: thay thế dict thô trong borrow_history
    def __init__(self, book_id, book_title, member_id, borrow_date, return_date=None):
        self.book_id     = book_id
        self.book_title  = book_title
        self.member_id   = member_id
        self.borrow_date = borrow_date
        self.return_date = return_date   # None = chưa trả

    def is_returned(self):# -> bool
        return self.return_date is not None

    def to_dict(self): # -> dict  (lưu vào borrow_history của account)
        return {
            "book_id":     self.book_id,
            "title":       self.book_title,
            "borrow_date": self.borrow_date,
            "return_date": self.return_date
        }
    @staticmethod
    def from_dict(data, member_id=""):# -> BorrowRecord  (đọc từ borrow_history trong JSON)
        return BorrowRecord(
            book_id     = data["book_id"],
            book_title  = data.get("title", ""),
            member_id   = member_id,
            borrow_date = data.get("borrow_date", ""),
            return_date = data.get("return_date")
        )

class User:
    # Class cha — chứa thông tin đăng nhập cơ bản
    def __init__(self, user_ID, username, password):
        self.user_ID  = user_ID
        self.username = username
        self.password = password

    def display_info(self, role):# -> None  (in thông tin tài khoản ra terminal)
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

    def to_dict(self, role="member"):# -> dict  (khung account cơ bản, dùng khi tạo admin)
        return {
            "ID":                  self.user_ID,
            "Username":            self.username,
            "Password":            self.password,
            "role":                role,
            "total_borrows":       0,
            "currently_borrowing": 0,
            "borrow_history":      []
        }


class Member(User):
    # Thêm mới: kế thừa User, thêm logic mượn/trả sách
    # borrow_history lưu list[BorrowRecord] thay vì list[dict]
    def __init__(self, member_ID, username, password):
        super().__init__(member_ID, username, password)
        self.borrow_history      = []   # list[BorrowRecord]
        self.total_borrows       = 0
        self.currently_borrowing = 0

    def add_borrow_record(self, record: BorrowRecord):# -> None  (thêm record + tăng số liệu khi mượn thành công)
        self.borrow_history.append(record)
        self.total_borrows       += 1
        self.currently_borrowing += 1

    def mark_returned(self, book_id):# -> bool  (tìm record chưa trả -> ghi return_date -> giảm currently_borrowing)
        for record in reversed(self.borrow_history):
            if str(record.book_id) == str(book_id) and not record.is_returned():
                record.return_date       = datetime.now().strftime("%Y-%m-%d")
                self.currently_borrowing = max(0, self.currently_borrowing - 1)
                return True
        return False

    def get_active_borrows(self):# -> list[BorrowRecord]  (chỉ các sách chưa trả)
        return [r for r in self.borrow_history if not r.is_returned()]

    def to_dict(self, role="member"):# -> dict  (ghi đầy đủ Member + borrow_history xuống JSON)
        return {
            "ID":                  self.user_ID,
            "Username":            self.username,
            "Password":            self.password,
            "role":                role,
            "total_borrows":       self.total_borrows,
            "currently_borrowing": self.currently_borrowing,
            "borrow_history":      [r.to_dict() for r in self.borrow_history]
        }
    @staticmethod
    def from_account(data):# -> Member  (load dict từ JSON thành object Member đầy đủ)
        m = Member(data["ID"], data["Username"], data["Password"])
        m.total_borrows       = data.get("total_borrows", 0)
        m.currently_borrowing = data.get("currently_borrowing", 0)
        m.borrow_history      = [
            BorrowRecord.from_dict(r, data["ID"])
            for r in data.get("borrow_history", [])
        ]
        return m


# ============================================================
# LOGIC  
# ============================================================

class BookManager:
    # Quản lý toàn bộ nghiệp vụ liên quan đến sách
    # Thay đổi: borrow/return giờ dùng Member object thay vì thao tác dict thô
    def __init__(self):
        self.repo  = FileManager(BOOK_FILE)
        self.books = self.repo.load()
        
    def add_Book(self):# -> None  (nhận input -> kiểm tra ID -> thêm sách -> lưu file)
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

    def find_book_id(self, book_id):# -> dict | None
        for book in self.books:
            if book['_id'] == book_id:
                return book
        return None

    def find_book_title(self, key_word):# -> list[dict]
        result   = []
        key_word = key_word.lower()
        for book in self.books:
            if key_word in book['title'].lower():
                result.append(book)
        return result

    def find_book(self, key_word): # -> list[Book]  (dùng cho search_book())
        return [Book.from_dict(b) for b in self.find_book_title(key_word)]

    def search_book(self): # -> None  (màn hình tìm kiếm, duyệt kết quả bằng j/l)
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

    def display_book_list(self):# -> None  (hiển thị danh sách sách có phân trang)
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

            print("╔" + "═"*88 + "╗")
            print("║" + " "*31 + "📚 TABLE OF CONTENTS" + f"{'':^37}" + "║")
            print("║" + " "*30 + f"(Page {current_page:03d}/{total_pages:03d})" + " "*44 + "║")
            print("╠" + "═"*88 + "╣")

            for i, book in enumerate(self.books[start:end], start=start):
                authors_display = ', '.join(book.get('authors', []))
                amount          = book.get('quantity', 0)
                title           = book.get('title', 'N/A')
                book_id         = book.get('_id', 'N/A')

                print(f"║  🆔[{book_id:03d}] 📖 {title:<74} ║")
                print(f"║        ✍️  {authors_display:<76} ║")
                print(f"║       Remaining: {amount:<68}  ║")

                if i < end - 1:
                    print("║" + " "*88 + "║")

            print("╠" + "═"*88 + "╣")
            footer = f" Display {start+1}-{end} in total {total_books} books"
            print(f"║{footer}{' '*(88 - len(footer))}║")
            print("╚" + "═"*88 + "╝")

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

    def view_book_detail(self): # -> None  (nhập ID -> gọi Book.display_book())
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

    def borrow_book(self, book_id, member_id): # -> bool
        # Thay đổi: dùng Member.from_account() + add_borrow_record() thay vì thao tác dict thô
        accounts = FileManager(ACCOUNT_FILE).load()
        acc_data = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not acc_data:
            print("❌ Member not found.")
            return False

        for book in self.books:
            if str(book["_id"]) == str(book_id):
                if book.get("quantity", 0) > 0:
                    book["quantity"]    -= 1
                    book["is_borrowed"]  = True
                    book["borrow_count"] = book.get("borrow_count", 0) + 1
                    self.repo.save(self.books)

                    record = BorrowRecord(
                        book_id     = book["_id"],
                        book_title  = book["title"],
                        member_id   = member_id,
                        borrow_date = datetime.now().strftime("%Y-%m-%d")
                    )
                    member = Member.from_account(acc_data)
                    member.add_borrow_record(record)

                    for i, a in enumerate(accounts):
                        if str(a["ID"]) == str(member_id):
                            accounts[i] = member.to_dict(role=acc_data.get("role", "member"))
                            break
                    FileManager(ACCOUNT_FILE).save(accounts)

                    print(f"✅ Borrowed book: {book['title']}")
                    return True
                else:
                    print("❌ Book not available to borrow.")
                    return False

        print("❌ Book ID not found.")
        return False

    def borrow_book_interactive(self, member_id): # -> None  (nhận input -> gọi borrow_book())
        try:
            book_id = int(input("Enter book ID to borrow: ").strip())
            self.borrow_book(book_id, member_id)
        except ValueError:
            print("❌ ID must be a number!")

    def return_book(self, book_id, member_id):# -> bool
        # Thay đổi: dùng Member.from_account() + mark_returned() thay vì thao tác dict thô
        accounts = FileManager(ACCOUNT_FILE).load()
        acc_data = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not acc_data:
            print("❌ Member not found.")
            return False

        for book in self.books:
            if str(book["_id"]) == str(book_id):
                if not book.get("is_borrowed", False):
                    print("❌ This book was not borrowed.")
                    return False

                book["quantity"]   += 1
                book["is_borrowed"] = False
                self.repo.save(self.books)

                member = Member.from_account(acc_data)
                member.mark_returned(book_id)

                for i, a in enumerate(accounts):
                    if str(a["ID"]) == str(member_id):
                        accounts[i] = member.to_dict(role=acc_data.get("role", "member"))
                        break
                FileManager(ACCOUNT_FILE).save(accounts)

                print(f"✅ Returned book: {book['title']}")
                return True

        print("❌ Book ID not found.")
        return False

    def return_book_interactive(self, member_id): # -> None  (nhận input -> gọi return_book())
        try:
            book_id = int(input("Enter book ID to return: ").strip())
            self.return_book(book_id, member_id)
        except ValueError:
            print("❌ ID must be a number!")

    def list_borrowed_books(self): # -> None  (in danh sách sách đang được mượn, dành cho admin)
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

    def my_borrow_history(self, member_id): # -> None
        # Thay đổi: dùng Member.from_account() + rec.is_returned() thay vì check dict thô
        accounts = FileManager(ACCOUNT_FILE).load()
        acc_data = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not acc_data:
            print("❌ Member not found.")
            return

        member = Member.from_account(acc_data)

        if not member.borrow_history:
            print("📭 No borrow history!")
            return

        print("\n" + "="*70)
        print(f"📋 BORROW HISTORY — {member.username}")
        print(f"   Total borrows: {member.total_borrows} | "
              f"Currently borrowing: {member.currently_borrowing}")
        print("="*70)
        for i, rec in enumerate(member.borrow_history, start=1):
            status = rec.return_date if rec.is_returned() else "Not returned yet"
            print(f"{i:>2}. [{rec.book_id}] {rec.book_title:<40} "
                  f"Borrowed: {rec.borrow_date} | Returned: {status}")
        print("="*70)

    def show_my_profile(self, member_id):# -> None
        # Thay đổi: dùng Member.get_active_borrows() thay vì lọc list dict thủ công
        accounts = FileManager(ACCOUNT_FILE).load()
        acc_data = next((a for a in accounts if str(a["ID"]) == str(member_id)), None)
        if not acc_data:
            print("❌ Member not found.")
            return

        member = Member.from_account(acc_data)
        active = member.get_active_borrows()

        os.system('cls')
        print("╔══════════════════════════════════════════════════╗")
        print("║                  MY PROFILE                      ║")
        print("╠══════════════════════════════════════════════════╣")
        print(f"║  ID               : {str(member.user_ID):<29}║")
        print(f"║  Username         : {member.username:<29}║")
        print(f"║  Role             : {acc_data.get('role','member'):<29}║")
        print("╠══════════════════════════════════════════════════╣")
        print(f"║  Total borrows    : {str(member.total_borrows):<29}║")
        print(f"║  Currently borrow : {str(member.currently_borrowing):<29}║")
        print("╠══════════════════════════════════════════════════╣")

        if active:
            print("║  Books currently borrowed:                       ║")
            for rec in active:
                line = f"  [{rec.book_id}] {rec.book_title[:35]} (since {rec.borrow_date})"
                print(f"║{line:<50}║")
        else:
            print("║  No books currently borrowed.                    ║")

        print("╚══════════════════════════════════════════════════╝")

    def edit_book(self, item): # -> None  (vòng lặp sửa từng field -> lưu khi chọn 0)
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

    def delete_book(self, book_id):# -> (bool, str)  (không cho xóa nếu đang được mượn)
        book = self.find_book_id(book_id)
        if not book:
            return False, "Book not found!"
        if book.get("is_borrowed", False):
            return False, "Cannot delete — book is currently borrowed!"
        self.books = [b for b in self.books if b["_id"] != book_id]
        if self.repo.save(self.books):
            return True, f"Book '{book['title']}' deleted successfully!"
        return False, "Failed to save!"

    def show_statistics(self):# -> None  (in top 5 sách mượn nhiều nhất + tổng kho)
        os.system('cls')
        print("╔══════════════════════════════════════════════════════════╗")
        print("║                    LIBRARY STATISTICS                    ║")
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

    def show_books_by_category(self): # -> None  (nhóm sách theo thể loại rồi in ra)
        categories = {}
        for book in self.books:
            for cat in book.get('categories', []):
                categories.setdefault(cat, []).append(book)
        print("\n Books by Category:")
        for cat, books in categories.items():
            print(f"\n  {cat}:")
            for b in books:
                print(f"  - {b['title']}")


class AccSystem:
    # Quản lý đăng nhập / đăng ký tài khoản
    def __init__(self):
        self.repo = FileManager(ACCOUNT_FILE)

    def ID_isRegistered(self, ID):# -> bool  (kiểm tra ID đã tồn tại chưa, tránh trùng khi tạo mới)
        account = self.repo.load()
        for check in account:
            if check["ID"] == ID:
                return True
        return False

    def is_account(self, ID, username, password): # -> bool  (kiểm tra tài khoản hợp lệ khi đăng nhập)
        account = self.repo.load()
        for check in account:
            if check["ID"] == ID and check["Username"] == username and check["Password"] == password:
                return True
        return False

    def create_account(self, ID, username, password): # -> None
        # Thay đổi: dùng Member().to_dict() để tạo account với đầy đủ fields borrow
        data        = self.repo.load()
        new_account = Member(ID, username, password).to_dict(role="member")
        data.append(new_account)
        self.repo.save(data)

    def login_screen(self): # -> (str, str)  tức là (role, member_id)
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

    def login(self, role): # -> str | False  (trả về member_id nếu đúng, False nếu sai hoặc thoát)
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
                    return ID
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

    def Sign_up(self): # -> None  (nhận input -> kiểm tra trùng -> tạo account member mới)
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
# PRESENTATION 
# ============================================================

class UI:
    # Helper tĩnh — không cần self, gọi thẳng UI.xxx()
    @staticmethod
    def gotoxy(x, y):
        # -> None  (di chuyển con trỏ terminal tới (x, y))
        sys.stdout.write(f"\033[{y};{x}H")
        sys.stdout.flush()

    @staticmethod
    def end(): # -> None  (in lời tạm biệt -> thoát chương trình)
        os.system("cls")
        print("╔══════════════════════════════════════╗")
        print("║              Thank you!              ║")
        print("╚══════════════════════════════════════╝")
        exit()


class Library:
    # Điều phối menu admin/member -> gọi xuống BookManager
    def __init__(self):
        self.bookManager = BookManager()

    def admin_menu(self):# -> None  (menu admin)
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

    def member_menu(self, member_id): # -> None  (menu member)
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

def main(): pass

if __name__ == "__main__":
    acc             = AccSystem()
    role, member_id = acc.login_screen()   # -> (role, member_id)

    lib = Library()
    if role == "admin":
        lib.admin_menu()
    else:
        lib.member_menu(member_id)

