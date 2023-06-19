import sys
import sqlite3
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QCalendarWidget, QVBoxLayout, QWidget, QLineEdit, QMessageBox, QComboBox, QDialog


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Giriş Yap veya Kayıt Ol")
        self.setGeometry(100, 100, 300, 250)

        self.username_label = QLabel("Kullanıcı Adı:", self)
        self.username_label.move(50, 50)

        self.username_input = QLineEdit(self)
        self.username_input.move(150, 50)

        self.password_label = QLabel("Şifre:", self)
        self.password_label.move(50, 100)

        self.password_input = QLineEdit(self)
        self.password_input.move(150, 100)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.usertype_label = QLabel("Kullanici Tipi:", self)
        self.usertype_label.move(50, 150)

        self.usertype_combobox = QComboBox(self)
        self.usertype_combobox.addItem("Normal Kullanici")
        self.usertype_combobox.addItem("Admin")
        self.usertype_combobox.move(150, 150)

        self.login_button = QPushButton("Giriş Yap", self)
        self.login_button.move(50, 200)
        self.login_button.clicked.connect(self.login)

        self.register_button = QPushButton("Kayıt Ol", self)
        self.register_button.move(160, 200)
        self.register_button.clicked.connect(self.open_register_window)

        self.db_connection = self.create_db_connection()
        self.create_user_table()

    def create_db_connection(self):
        conn = None
        try:
            conn = sqlite3.connect("users.db")
            print("SQLite veritabanına bağlantı başarılı.")
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")
        return conn

    def create_user_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS users ( 
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL,
                usertype TEXT NOT NULL
            )
        """

        try: 
            cursor = self.db_connection.cursor()
            cursor.execute(create_table_query)
            self.db_connection.commit()
            print("users tablosu oluşturuldu")
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        usertype = self.usertype_combobox.currentText()

        select_user_query = """
            SELECT * FROM users WHERE username=? AND password=? AND usertype=?
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(select_user_query, (username, password, usertype))
            user = cursor.fetchone()

            if user is not None:
                self.close()
                self.open_calendar_window(user[0])
            else:
                QMessageBox.warning(self, "Giriş Başarısız", "Geçersiz kullanıcı adı veya şifre veya kullanıcı tipi!")
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")

    def open_register_window(self):
        self.register_window = RegisterWindow(self.db_connection)
        self.register_window.show()

    def open_calendar_window(self, user_id):
        self.calendar_window = CalendarWindow(user_id, self.db_connection)
        self.calendar_window.show()


class RegisterWindow(QDialog):
    def __init__(self, db_connection):
        super().__init__()

        self.setWindowTitle("Kayıt Ol")
        self.setGeometry(100, 100, 300, 500)

        self.db_connection = db_connection

        self.username_label = QLabel("Kullanıcı Adı:", self)
        self.username_label.move(50, 50)

        self.username_input = QLineEdit(self)
        self.username_input.move(150, 50)

        self.password_label = QLabel("Şifre:", self)
        self.password_label.move(50, 100)

        self.password_input = QLineEdit(self)
        self.password_input.move(150, 100)
        self.password_input.setEchoMode(QLineEdit.Password)

        self.namesurname_label = QLabel("Ad Soyad:", self)
        self.namesurname_label.move(50, 150)

        self.namesurname_input = QLineEdit(self)
        self.namesurname_input.move(150, 150)

        self.tckimlik_label = QLabel("TC Kimlik No.", self)
        self.tckimlik_label.move(50, 200)

        self.tckimlik_input = QLineEdit(self)
        self.tckimlik_input.move(150, 200)

        self.telefonno_label = QLabel("Telefon No.", self)
        self.telefonno_label.move(50, 250)

        self.telefonno_input = QLineEdit(self)
        self.telefonno_input.move(150, 250)

        self.email_label = QLabel("E posta: ", self)
        self.email_label.move(50, 300)

        self.email_input = QLineEdit(self)
        self.email_input.move(150, 300)

        self.adres_label = QLabel("Adres:", self)
        self.adres_label.move(50, 350)

        self.adres_input = QLineEdit(self)
        self.adres_input.move(150, 350)

        self.usertype_label = QLabel("Kullanici tipi:", self)
        self.usertype_label.move(50, 400)

        self.usertype_combobox = QComboBox(self)
        self.usertype_combobox.addItem("Normal Kullanici")
        self.usertype_combobox.addItem("Admin")
        self.usertype_combobox.move(150, 400)

        self.register_button = QPushButton("Kayıt Ol", self)
        self.register_button.move(100, 450)
        self.register_button.clicked.connect(self.register)

    def register(self):
        username = self.username_input.text()
        password = self.password_input.text()
        usertype = self.usertype_combobox.currentText()


        insert_user_query = """
            INSERT INTO users (username, password, usertype) VALUES (?, ?, ?)
        """

        try:
            cursor = self.db_connection.cursor()
            cursor.execute(insert_user_query, (username, password, usertype))
            self.db_connection.commit()
            QMessageBox.information(self, "Kayıt Başarılı", "Kaydınız başarıyla oluşturuldu")
            self.close()
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")


class CalendarWindow(QMainWindow):
    def __init__(self, user_id, db_connection):
        super().__init__()

        self.setWindowTitle("Takvim Uygulaması")
        self.setGeometry(100, 100, 400, 300)

        self.calendar_widget = QCalendarWidget(self)
        self.calendar_widget.setGeometry(20, 20, 360, 200)
        self.calendar_widget.clicked.connect(self.open_event_dialog)

        self.event_input = QLineEdit(self)
        self.event_input.setGeometry(20, 230, 240, 30)

        self.event_type_combobox = QComboBox(self)
        self.event_type_combobox.setGeometry(280, 230, 100, 30)
        self.event_type_combobox.addItem("Toplantı")
        self.event_type_combobox.addItem("İş Planı")

        self.add_event_button = QPushButton("Etkinlik Ekle", self)
        self.add_event_button.setGeometry(280, 230, 100, 30)
        self.add_event_button.clicked.connect(self.open_event_dialog)

        self.user_id = user_id
        self.db_connection = db_connection
        self.create_events_table()

    def create_events_table(self):
        create_table_query = """
            CREATE TABLE IF NOT EXISTS events (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                date TEXT NOT NULL,
                event TEXT NOT NULL,
                event_type TEXT NOT NULL,
                user_id INTEGER NOT NULL,
                FOREIGN KEY (user_id) REFERENCES users (id)
            )
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(create_table_query)
            self.db_connection.commit()
            print("events tablosu oluşturuldu.")
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")

    def open_event_dialog(self, date):
        selected_date = date.toString("yyyy-MM-dd")

        select_event_query = """
            SELECT * FROM events WHERE date=? AND user_id=?
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(select_event_query, (selected_date, self.user_id))
            event = cursor.fetchone()

            if event is not None:
                self.edit_event_dialog = EditEventDialog(self, event[2], event[3])
                self.edit_event_dialog.exec_()
            else:
                self.add_event_dialog = AddEventDialog(self, selected_date)
                self.add_event_dialog.exec_()
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")

    def add_event(self, date, event, event_type):
        insert_event_query = """
            INSERT INTO events (date, event, event_type, user_id) VALUES (?, ?, ?, ?)
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(insert_event_query, (date, event, event_type, self.user_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Etkinlik Eklendi", "Etkinlik başarıyla eklendi!")
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")

    def update_event(self, date, event, event_type):
        update_event_query = """
            UPDATE events SET event=?, event_type=? WHERE date=? AND user_id=?
        """
        try:
            cursor = self.db_connection.cursor()
            cursor.execute(update_event_query, (event, event_type, date, self.user_id))
            self.db_connection.commit()
            QMessageBox.information(self, "Etkinlik Güncellendi", "Etkinlik başarıyla güncellendi!")
        except sqlite3.Error as e:
            print(f"SQLite veritabanı hatası: {e}")


class AddEventDialog(QDialog):
    def __init__(self, parent, selected_date):
        super().__init__(parent)

        self.setWindowTitle("Etkinlik Ekle")
        self.setGeometry(100, 100, 300, 200)

        self.selected_date = selected_date

        self.event_label = QLabel("Etkinlik:", self)
        self.event_label.move(50, 50)

        self.event_input = QLineEdit(self)
        self.event_input.move(100, 50)

        self.event_type_label = QLabel("Etkinlik Türü:", self)
        self.event_type_label.move(50, 100)

        self.event_type_combobox = QComboBox(self)
        self.event_type_combobox.addItem("Toplantı")
        self.event_type_combobox.addItem("İş Planı")
        self.event_type_combobox.move(150, 100)

        self.add_event_button = QPushButton("Ekle", self)
        self.add_event_button.move(100, 150)
        self.add_event_button.clicked.connect(self.add_event)

    def add_event(self):
        event = self.event_input.text()
        event_type = self.event_type_combobox.currentText()

        self.parent().add_event(self.selected_date, event, event_type)
        self.accept()


class EditEventDialog(QDialog):
    def __init__(self, parent, event, event_type):
        super().__init__(parent)

        self.setWindowTitle("Etkinlik Düzenle")
        self.setGeometry(100, 100, 300, 200)

        self.event = event
        self.event_type = event_type

        self.event_label = QLabel("Etkinlik:", self)
        self.event_label.move(50, 50)

        self.event_input = QLineEdit(self)
        self.event_input.setText(event)
        self.event_input.move(100, 50)

        self.event_type_label = QLabel("Etkinlik Türü:", self)
        self.event_type_label.move(50, 100)

        self.event_type_combobox = QComboBox(self)
        self.event_type_combobox.addItem("Toplantı")
        self.event_type_combobox.addItem("İş Planı")
        self.event_type_combobox.setCurrentText(event_type)
        self.event_type_combobox.move(150, 100)

        self.update_event_button = QPushButton("Güncelle", self)
        self.update_event_button.move(100, 150)
        self.update_event_button.clicked.connect(self.update_event)

    def update_event(self):
        event = self.event_input.text()
        event_type = self.event_type_combobox.currentText()

        self.parent().update_event(self.parent().calendar_widget.selectedDate().toString("yyyy-MM-dd"), event, event_type)
        self.accept()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    login_window = LoginWindow()
    login_window.show()
    sys.exit(app.exec())

