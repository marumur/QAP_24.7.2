from api import PetFriends
from settings import *
import os
import imghdr
pf = PetFriends()


def test_get_api_key_valid_user(email=valid_email, password=valid_password):
    """ Проверяем, что запрос api ключа возвращает статус 200, и в результате содержится слово key"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert 'key' in result


def test_get_list_of_pets_with_valid_key(filter=''):
    """ Проверяем, что запрос всех питомцев возвращает не пустой список.
    Для этого сначала получаем api ключ и сохраняем в переменную auth_key. Далее, используя этот ключ
    запрашиваем список всех питомцев и проверяем, что список не пустой.
    Доступное значение параметра filter - 'my_pets' либо '' """

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets']) > 0


def test_get_empty_list_of_my_pets_after_delete_all_with_valid_key(filter="my_pets"):
    """Проверяем, что при отсутствии своих питомцев и попытке получить их список, в ответ
    приходит пустой список 'pets'/ Так же проверяем полное удаление всех своих питомцев"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter)

    # Если список пустой, сохраняем status и result
    # Если список не пустой, запускаем цикл, где удаляем первого питомца в нашем списке
    # пока список не опустеет
    if len(my_pets['pets']) == 0:
        status, result = pf.get_list_of_pets(auth_key, filter)
    else:
        while len(my_pets['pets']) > 0:
            pet_id = my_pets['pets'][0]['id']
            status, _ = pf.delete_pet(auth_key, pet_id)
            _, my_pets = pf.get_list_of_pets(auth_key, filter)

        # Получаем список своих питомцев
        status, result = pf.get_list_of_pets(auth_key, filter)

    # Сверяем полученные данные с нашими ожиданиями
    assert status == 200
    assert len(result['pets']) == 0 and 'pets' in my_pets


def test_add_new_pet(name=name1, animal_type=animal_type1, age=age1, pet_photo=pet_photo1):
    """Проверяем возможноcть создания питомца с фотографией"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Запрашиваем ключ api и сохраняем в переменую auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.add_new_pet(auth_key, name, animal_type, age, pet_photo)

    # Сверяем полученный ответ с ожидаемым результатом
    assert status == 200
    assert result['name'] == name


def test_successful_delete_self_pet():
    """Проверяем возможность удаления питомца"""

    # Получаем ключ auth_key и запрашиваем список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, если список своих питомцев пустой, то добавляем нового питомца, и опять запрашиваем список своих питомцев
    if len(my_pets['pets']) == 0:
        pf.add_new_pet(auth_key, "Масюк", "кот", "6", "images/masyuk.jpg")
        _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Берём id первого питомца из списка и отправляем запрос на удаление
    pet_id = my_pets['pets'][0]['id']
    status, _ = pf.delete_pet(auth_key, pet_id)

    # Ещё раз запрашиваем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, "my_pets")

    # Проверяем, что статус ответа равен 200, и в списке питомцев нет id удалённого питомца
    assert status == 200
    assert pet_id not in my_pets.values()


def test_successful_update_self_pet_info(name='Бобик', animal_type='собака', age=9):
    """Проверяем возможность обновления информации о питомце"""

    # Получаем ключ auth_key и список своих питомцев
    _, auth_key = pf.get_api_key(valid_email, valid_password)
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Если список не пустой, то пробуем обновить его имя, тип и возраст
    if len(my_pets['pets']) > 0:
        status, result = pf.update_pet_info(auth_key, my_pets['pets'][0]['id'], name, animal_type, age)

        # Проверяем, что статус ответа = 200 и имя питомца соответствует заданному
        assert status == 200
        assert result['name'] == name

    else:
        # если список питомцев пустой, то вызываем исключение  с текстом об отстутствии своих питомцев
        raise Exception('There is no my pets')


def test_successful_create_pet_simple(name=name2, animal_type=animal_type2, age=age2):
    """Проверяем возможность создания питомца без фотографии"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)
    print(result)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name


def test_successful_add_photo_of_pet(pet_photo=pet_photo2):
    """Проверяем возможность добавления фотографии уже существующиму питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Получаем список своих питомцев
    _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

    # Если в словаре my_pets есть ключ 'pets', он не равен None и больше 0
    if my_pets is not None and 'pets' in my_pets and len(my_pets['pets']) > 0:
        # Додавляем фотографию питомцу с id 0
        status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

        # Проверяем, что статус ответа = 200, и в ответе значение ключа 'pet_photo' не равно нулю или None
        assert status == 200
        assert result['pet_photo'] != 0 and not None

    else:
        # В случае отсутствия своих питомцев вызывается ошибка
        raise Exception('There is no my pets')


'''Негативные тесты'''


def test_get_api_key_invalid_user(email=invalid_email, password=valid_password):
    """ Проверяем, что запрос api ключа с некорректным email возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа - в result
    status, result = pf.get_api_key(email, password)

    # Проверяем, что статус ответа = 403
    assert status == 403

    # Вызывается исключение
    raise Exception('Invalid email or password')


def test_get_api_key_invalid_password(email=valid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа с некорректным password возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Проверяем что статус ответа = 403
    assert status == 403

    # Вызывается исключение
    raise Exception('Invalid email or password')


def test_get_api_key_invalid_user_and_password(email=invalid_email, password=invalid_password):
    """ Проверяем, что запрос api ключа с некорректным email и password возвращает статус 403"""

    # Отправляем запрос и сохраняем полученный ответ с кодом статуса в status, а текст ответа в result
    status, result = pf.get_api_key(email, password)

    # Проверяем, что статус ответа = 403
    assert status == 403

    # Вызывается исключение
    raise Exception('Invalid email or password')


def test_get_list_of_pets_with_invalid_key(filter=''):
    """ Проверяем, что при попытке получить список всех питомцев на сайте с неверным auth_key в доступе будет отказано"""

    # передача некорректного auth_key
    auth_key = {
        "key": "242b32dc0fd5f1b1277dd53193dbbc63b284d0b47233591432519991"
    }
    # Попытка получить список питомцев
    status, result = pf.get_list_of_pets(auth_key, filter)

    # Проверяем что статус ответа = 403
    assert status == 403

    # Вызывается исключение
    raise Exception('Invalid auth_key')


def test_add_incorrect_type_photo_of_pet(pet_photo=pet_photo3):
    """Проверяем возможность добавления некорректного файла вместо фотографии уже существующему питомцу"""

    # Получаем полный путь изображения питомца и сохраняем в переменную pet_photo
    pet_photo = os.path.join(os.path.dirname(__file__), pet_photo)

    # Проверяем формат файла изображения с помощью imghdr
    image_format = imghdr.what(pet_photo)  # Проверка формата файла

    # Если формат определен
    if image_format in ['jpeg', 'jpg', 'png']:

        # Получаем ключ auth_key и список своих питомцев
        _, auth_key = pf.get_api_key(valid_email, valid_password)
        _, my_pets = pf.get_list_of_pets(auth_key, filter='my_pets')

        # Если в словаре my_pets есть ключ 'pets', он не равен None и больше 0
        if my_pets is not None and 'pets' in my_pets and len(my_pets['pets']) > 0:

            # Добавляем фотографию питомцу с id 0
            status, result = pf.add_photo_of_pet(auth_key, my_pets['pets'][0]['id'], pet_photo)

            # Сверяем полученные данные с нашими ожиданиями
            assert status == 200
            assert result['pet_photo'] != 0

        else:
            # При отсутствии созданных нами питомцев вызываем исключение
            raise Exception('There is no my pets')

    else:
        # Если формат файла не является JPG, JPEG or PNG вызывается исключение
        raise Exception('Invalid image format. The file should be in JPG, JPEG or PNG format')


def test_create_pet_simple_with_49_simbols_name(name=name49, animal_type=animal_type2, age=age2):
    """Проверяем возможность создания питомца без фотографии c именем в 49 символов"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_50_simbols_name(name=name50, animal_type=animal_type2, age=age2):
    """Проверяем возможность создания питомца без фотографии c именем в 50 символов"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_51_simbols_name(name=name51, animal_type=animal_type2, age=age2):
    """Проверяем возможность создания питомца без фотографии c именем в 51 символ"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_99_simbols_name(name=name99, animal_type=animal_type2, age=age2):
    """Проверяем возможность создания питомца без фотографии c именем в 99 символов"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_100_simbols_name(name=name100, animal_type=animal_type2, age=age2):
    """Проверяем возвожность создания питомца без фотографии c именем в 100 символов"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_101_simbols_name(name=name101, animal_type=animal_type2, age=age2):
    """Проверяем возвожность создания питомца без фотографии c именем в 101 символ"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name


def test_create_pet_simple_with_empty_name(name=name_empty, animal_type=animal_type2, age=age2):
    """Проверяем возможность создания питомца без фотографии c пустым именем. Тут есть момент, что бэк пропускает
    пустое значение, но фронт выдает инфо о необходимости ввести имя питомца"""

    # Получаем ключ auth_key
    _, auth_key = pf.get_api_key(valid_email, valid_password)

    # Добавляем питомца
    status, result = pf.create_pet_simple(auth_key, name, animal_type, age)

    # Проверяем, что статус ответа = 200, и в ответе значение ключа 'name' соответствует переданным данным
    assert status == 200
    assert result['name'] == name
