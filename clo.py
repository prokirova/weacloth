import sqlite3, os

bd = sqlite3.connect('clothes.db')

def convert_to_binary_data(filename):
    with open(filename, 'rb') as file:
        blob_data = sqlite3.Binary(file.read())
    return blob_data

id = 1
name = 'зимняя куртка'
cursor = bd.cursor()
#cursor.execute('create table clothes(id, name, photo)')

def insert(id, name, photo):
    try:

        print("Подключен к SQLite")

        sqlite_insert_blob_query = """INSERT INTO clothes
                                  (id, name, photo) VALUES (?, ?, ?)"""

        photo = convert_to_binary_data(photo)
        data_tuple = (id, name, photo)
        cursor.execute(sqlite_insert_blob_query, data_tuple)
        bd.commit()
        print("Изображение и файл успешно вставлены как BLOB в таблиу")
        cursor.close()
    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if bd:
            bd.close()
            print("Соединение с SQLite закрыто")


def write_to_file(data, filename):
    with open(filename, 'wb') as file:
        file.write(data)
    print("Данный из blob сохранены в: ", filename, "\n")

def get(id):
    try:
        sqlite_connection = sqlite3.connect('clothes.db')
        cursor = sqlite_connection.cursor()
        print("Подключен к SQLite")

        sql_fetch_blob_query = """SELECT * from clothes where id = ?"""
        cursor.execute(sql_fetch_blob_query, (id,))
        record = cursor.fetchall()
        for row in record:
            print("Id = ", row[0], "Name = ", row[1])
            name = row[1]
            photo = row[2]


            print("Сохранение изображения  на диске \n")
            photo_path = os.path.join(name + ".jpg")
            write_to_file(photo, photo_path)

        cursor.close()
        return photo_path

    except sqlite3.Error as error:
        print("Ошибка при работе с SQLite", error)
    finally:
        if sqlite_connection:
            sqlite_connection.close()
            print("Соединение с SQLite закрыто")

insert(1, "зимняя куртка", "—Pngtree—cartoon hand drawn winter down_5471236.png")
get(1)

