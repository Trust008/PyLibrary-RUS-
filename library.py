import json
import hashlib

GENRES = ["Фантастика", "Детектив", "Роман", "Поэзия", "Драма", "Комедия", "Научная"]


def get_user_genre_choice():
    print("Доступные жанры:", GENRES)
    user_genre = input("Введите жанр книги или введите свой жанр: ")
    return user_genre

def library():
    try:
        with open("books.json", "r") as f:
            data = f.read()
            if not data:
                return {}
            books_dict = json.loads(data)
        return books_dict
    except json.decoder.JSONDecodeError:
        print(f"Ошибка декодирования, создаю новую библиотеку...")
        return {}


def add_new_book():
    name = input("Введите название книги: ")
    author = input("Введите автора книги: ")
    genre = get_user_genre_choice()

    books_dict = library()

    md5 = hashlib.md5()
    md5.update(name.encode("utf-8"))
    book_id_enc = md5.hexdigest()

    if book_id_enc in books_dict:
        print("Книга уже существует")
    else:
        book = {
            "book_id": book_id_enc,
            "name": name,
            "author": author,
            "genre": genre
        }

        books_dict[book_id_enc] = book

        with open("books.json", "w") as file:
            json.dump(books_dict, file, indent=2)
        print(f"Новая книга под уникальным номером - {book_id_enc} успешно добавлена в библиотеку")


def view_all_books():
    books_dict = library()
    if not books_dict:
        return "Библиотека пуста."

    books_data = [{"Название": book["name"], "Автор": book["author"]} for book_id, book in books_dict.items()]
    json_str = json.dumps(books_data, ensure_ascii=False, indent=2)
    return json_str


def view_books_by_genre():
    genre = get_user_genre_choice()
    books_dict = library()
    filtered_books = [book for book_id, book in books_dict.items() if book["genre"] == genre]

    if not filtered_books:
        return f"Нет книг в жанре '{genre}'."

    books_data = [{"Название": book["name"], "Автор": book["author"]} for book in filtered_books]
    json_str = json.dumps(books_data, ensure_ascii=False, indent=2)
    return json_str


def search_book():
    search_query = input("Введите ключевое слово для поиска: ")
    books_dict = library()
    matching_books = []

    for book_id, book_info in books_dict.items():
        if 'name' in book_info and search_query.lower() in book_info['name'].lower():
            matching_books.append(book_info)
        elif 'author' in book_info and search_query.lower() in book_info['author'].lower():
            matching_books.append(book_info)

    if matching_books:
        books_data = [{"Название": book["name"], "Автор": book["author"], "Жанр": book["genre"]} for book in matching_books]
        json_str = json.dumps(books_data, ensure_ascii=False, indent=2)
        return json_str
    else:
        return "Книга не найдена."


def remove_book_by_title():
    books = library()
    name = input("Введите название книги: ")
    keys_to_remove = []

    for book_id, book_info in books.items():
        if 'name' in book_info and book_info['name'] == name:
            keys_to_remove.append(book_id)
            print(f"Найдена книга - {name}, вы действительно хотите ее удалить? (y|n)")
            check = input()

            if check.lower() == "y":
                if keys_to_remove:
                    for key in keys_to_remove:
                        del books[key]

                    with open("books.json", "w") as file:
                        json.dump(books, file, indent=2)
                    return f"Книга с названием '{name}' успешно удалена."
                else:
                    return f"Книга с названием '{name}' не найдена."
            else:
                print("Отмена действия, книга осталась в библиотеке")
                return f"Действие отменено, книга с названием '{name}' осталась в библиотеке."

    return f"Книга с названием '{name}' не найдена."

def main():
    while True:
        print("\nДобро пожаловать в библиотеку сэр! Чего желаете?")
        print("\nМеню:")
        print("1 - Просмотреть библиотеку")
        print("2 - Добавить книгу")
        print("3 - Удалить книгу по названию")
        print("4 - Поиск книги по ключевому слову")
        print("5 - Просмотреть книги по жанру")
        print("0 - Выйти из программы")

        choice = input("\nВыберите действие (введите соответствующую цифру): ")

        if choice == "1":
            print(view_all_books())
        elif choice == "2":
            add_new_book()
        elif choice == "3":
            print(remove_book_by_title())
        elif choice == "4":
            print(search_book())
        elif choice == "5":
            print(view_books_by_genre())
        elif choice == "0":
            print("Программа завершена.")
            break
        else:
            print("Некорректный ввод. Пожалуйста, введите цифру от 0 до 5.")

if __name__ == "__main__":
    main()
