import sender_stand_request
import data

def get_user_body(name):
    current_body = data.user_body.copy()
    current_body["firstName"] = name
    return current_body

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов

# def test_create_user_2_letter_in_first_name_get_success_response():

# Функция для позитивной проверки
def positive_assert(first_name):
    # В переменную user_body сохраняется обновленное тело запроса с именем first_name
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 201
    assert user_response.status_code == 201
    # Проверяется, что в ответе есть поле authToken, и оно не пустое
    assert user_response.json()["authToken"] != ""

    # В переменную users_table_response сохраняется результат запрос на получение данных из таблицы user_model
    users_table_response = sender_stand_request.get_users_table()

    # Строка, которая должна быть в ответе запроса на получение данных из таблицы users
    str_user = user_body["firstName"] + "," + user_body["phone"] + "," \
               + user_body["address"] + ",,," + user_response.json()["authToken"]

    # Проверка, что такой пользователь есть, и он единственный
    assert users_table_response.text.count(str_user) == 1

# Тест 1. Успешное создание пользователя
# Параметр fisrtName состоит из 2 символов
def test_create_user_2_letter_in_first_name_get_success_response():
    positive_assert("Aa")

# Тест 2. Успешное создание пользователя
# Параметр fisrtName состоит из 15 символов
def test_create_user_15_letter_in_first_name_get_success_response():
    positive_assert("Ааааааааааааааа")

# Функция для негативной проверки - недопустимое значение параметра fisrtName
def negative_assert_symbol(first_name):
    # В переменную user_body сохраняется обновленное тело запроса с именем first_name
    user_body = get_user_body(first_name)
    # В переменную user_response сохраняется результат запроса на создание пользователя
    user_response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert user_response.status_code == 400
    # Проверяется, что в ответе есть атрибут "code" и он равен 400
    assert user_response.json()["code"] == 400
    # Проверяется, что в ответе есть атрибут "message" и он равен "Имя пользователя введено некорректно. \
    # Имя может содержать только русские или латинские буквы, длина должна быть не менее 2 и не более 15 символов"
    assert user_response.json()["message"] == "Имя пользователя введено некорректно. " \
                                              "Имя может содержать только русские или латинские буквы, " \
                                              "длина должна быть не менее 2 и не более 15 символов"

# Тест 3. Ошибка при создании пользователя
# Параметр fisrtName состоит из 1 символа
def test_create_user_1_letter_in_first_name_get_error_response():
    negative_assert_symbol("A")

# Тест 4. Ошибка при создании пользователя
# Параметр fisrtName состоит из 16 символов
def test_create_user_16_letter_in_first_name_get_error_response():
    negative_assert_symbol("Аааааааааааааааа")

# Тест 5. Успешное создание пользователя
# Параметр fisrtName состоит из английских букв
def test_create_user_english_letter_in_first_name_get_success_response():
    positive_assert("QWErty")

# Тест 6. Успешное создание пользователя
# Параметр fisrtName состоит из русских букв
def test_create_user_russian_letter_in_first_name_get_success_response():
    positive_assert("Мария")

# Тест 7. Ошибка при создании пользователя
# Параметр fisrtName содержит пробелы
def test_create_user_has_space_in_first_name_get_error_response():
    negative_assert_symbol( "Человек и Ко")

# Тест 8. Ошибка при создании пользователя
# Параметр fisrtName содержити спецсимоволы
def test_create_user_has_special_symbol_in_first_name_get_error_response():
    negative_assert_symbol("№%@")

# Тест 9. Ошибка при создании пользователя
# Параметр fisrtName содержит цифры
def test_create_user_has_number_in_first_name_get_error_response():
    negative_assert_symbol("123")

# Функция для негативной проверки - параметр fisrtName не задан
def negative_assert_no_firstname(user_body):
    # В переменную response сохраняется результат запроса на создание пользователя
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400
    # Проверяется, что в ответе есть атрибут "code" и он равен 400
    assert response.json()["code"] == 400
    # Проверяется, что в ответе есть атрибут "message" и текст сообщения
    assert response.json()["message"] == "Не все необходимые параметры были переданы"

# Тест 10. Ошибка при создании пользователя
# Параметр fisrtName не передан в запросе
def test_create_user_no_first_name_get_error_response():
    # Копируется словарь с телом запроса из файла data в переменную user_body
    # Иначе можно потерять данные из исходного словаря
    user_body = data.user_body.copy()
    # Удаление параметра firstName из запроса
    user_body.pop("firstName")
    # Проверка полученного ответа
    negative_assert_no_firstname(user_body)

# Тест 11. Ошибка при создании пользователя
# Параметр fisrtName состоит из пустой строки
def test_create_user_empty_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body("")
    # Проверка полученного ответа
    negative_assert_no_firstname(user_body)

# Тест 12. Ошибка при создании пользователя
# Параметр fisrtName имеет другой тип - число
def test_create_user_number_type_first_name_get_error_response():
    # В переменную user_body сохраняется обновлённое тело запроса
    user_body = get_user_body(12)
    # В переменную response сохраняется результат запроса на создание пользователя
    response = sender_stand_request.post_new_user(user_body)

    # Проверяется, что код ответа равен 400
    assert response.status_code == 400
