### Імпортування до проєкту
import re
import os
from colorama import Fore

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            output(f'ПОМИЛКА -> {ve}', 'r')
        except Exception as e:
            output(f'ПОМИЛКА -> {e}', 'r')
    return wrapper

@input_error
def add_contact(path: str = 'task_4/contacts.txt', name: str = '', phone_number:str = '') -> None:
    
    """
    Функція додає новий контакт, якщо введено коректний номер та такий номер раніше не використовувася.

    Параметри:
    - path: Шлях до файлу контактів.
    - name: Ім'я контакту.
    - phone_number: Номер телефону контакту.

    Повертає:
    Нічого    
    """    

    # Запит користувача на введення імені та номеру телефону контакта.
    if not name:  
        name = input('ЗАПИТ -> Введіть ім`я контакта: ')
    if not phone_number:
        phone_number = input(f'ЗАПИТ -> Введіть номер телефона для {name}: ')
    
    # Перевіряємо введений номера телефона на коректність та друкуємо повідомлення що контакт не збережено, бо номер введено не коректно. 
    phone_number_standart = standart_phone_number(phone_number)
    if not phone_number_standart[0]:
        raise ValueError(f'Контакт не створено: "{phone_number}" - не може бути номером телефону')
    
    # Перевіряємо чи не існує такого номера у наших контактах та друкуємо повідомлення що контакт не збережено, бо такий номер телефону вже зайнятий
    else:        
        phone_number_find = find_contact(find_value = phone_number_standart[1])
        if phone_number_find[0]:
            raise ValueError(f'Номер "{phone_number_standart[1]}" вже використовується контактом {phone_number_find[1][phone_number_standart[1]]}')
        
        # Виконуємо дадовання номеру телефону до списку контактів
        else:

            phone_number_and_name = format_number_name(phone_number_standart[1], name)  # Поєднуєму номер телефону та ім'я у один рядок через двокрапку
            open_read_file(path, flag = 'a', text = phone_number_and_name) # Відкриваємо файл для запису та записуємо новий контакт
            output(f'ВИКОНАНО -> Контакт збережено {phone_number_standart[1]} - {name}', 'g') # Друкуємо повідомлення що контакт збережено

def standart_phone_number(phone_number: str) -> list:

    """
    Функція стандартизує номер телефону у формат +380001112233 якщо вдається розпізнати переданий рядок.

    Параметри:
    - phone_number: Номер телефону у довільному форматі

    Повертає:
    - result: list [True, 'стандартизований номер'] або [False, 'переданий рядок без змін'] 
    """ 
    
    # Змінна для повернення результату, чи буде номер стандартизованим
    result = [False, phone_number]

    # Парсинг номера телефона
    phone_number_pars_one = re.sub(r'\D', '', phone_number) # Видаляємо усі символи окрім цифр з номера телефона
    phone_number_pars_two = re.search(r"\d{10}(?:$)", phone_number_pars_one)  # Знаходимо 10 цифр з кінця номера телефона
    
    # Генерація позитивної відповіді якщо є можливість стандартизувати номер
    if phone_number_pars_two != None:
        phone_number_standart = '+38' + phone_number_pars_two.group()
        result = [True, phone_number_standart]

    # Повернення результату
    return result

def open_read_file(path: str = 'task_4/contacts.txt', flag: str = 'r', text: str = '') -> str:

    """
    Функція працює з файлом телефонної книги.

    Параметри:
    - path: Шлях до файлу контактів.
    - flag: Флаг для роботи 'r' - прочитати вміст файла, 'a' - додати у кінець файла, 'w' - перезаписати файл.
    - text: Текст для запису у файл.

    Повертає:
    - content_file: Вміст файлу, якщо він існує інакше пустий рядок    
    """

    # Змінна для повернення результата функції.
    content_file = str()  

    # Відловлювання помилок при роботі з файлом
    try:            
        full_path = os.path.join(os.getcwd(), path) # Створюємо повний шлях до файлу контактів      
        if (flag == 'r'): # Прочитати вміст файлу та зберегти у змінній.
            with open(full_path, "r", encoding='utf-8') as file:
                content_file = file.read()
        elif (flag == 'a'): # Записати у кінець файлу з нового рядка, якщо файл пустий записати без переносу на новий рядок.
            with open(full_path, 'a', encoding='utf-8') as file:
                if file.tell() == 0:
                    file.write(text)
                else:
                    file.write('\n' + text)        
        elif (flag == 'w'): # Перезаписати файл з новим текстом.
            with open(full_path, 'w', encoding='utf-8') as file:
                file.write(text)
    except FileNotFoundError:
        output("ПОМИЛКА -> Файл не знайдено.", 'r')
    except IOError:
        output("ПОМИЛКА - > Неможливо прочитати або записати данні.", 'r')
    except Exception as e:
        output(f'ПОМИЛКА -> {e}', 'r')
    finally:
        return content_file # Повертаємо результат

def find_contact(path: str = 'task_4/contacts.txt', find_value = '') -> list:
    
    """
    Функція шукає співпадіння серед існуючих контактів

    Параметри:
    - path: Шлях до файлу контактів.
    - find_value: Рядок для пошуку

    Повертає:
    - result_find: list [True, {знайдені співпадіння}] або [False, {пустий словник}}] 
    """

    # Відкриваємо файл з контактами для читання та считуємо усю книгу як рядок та конвертуємо текст у словник
    content_file = open_read_file(path, "r")
    
    # Змінна для повернення результату
    match_find = {}
    result_find = [False, match_find]

    # Якщо файл з контактами існує і не пустий
    if content_file:
        all_contacts = convert_str_dict(content_file)

        # Запит користувача на рядок пошуку якщо не передано
        if not find_value:
            find_value = input('ЗАПИТ -> Введіть данні ім`я або номер телефону для пошуку: ').casefold()
        
        # Пробуємо стандартизувати рядок пошуку до номера телефона.
        st_phone_number = standart_phone_number(find_value)

        # Якщо є номери у списку контактів
        if all_contacts:
            for phone_number, name in all_contacts.items():
                if phone_number == st_phone_number[1]: # Знайдено збіг по номеру телефона
                    match_find[phone_number] = name 
                elif name.casefold() == find_value: # Знайдено збіг за іменем
                    match_find[phone_number] = name
            if match_find:
                result_find = [True, match_find]

    # Повернення результату 
    return result_find

def convert_str_dict(text) -> dict:
    
    """
    Функція перетворює текст з телефонної книги у словник формату "НОМЕР ТЕЛЕФОНА: ІМ'Я"

    Параметри:
    - text: Текст для конвертації.

    Повертає:
    - all_contacts_dict: dict {ключ: значення} або {пустий словник}
    """
  
    # Змінна для зберігання контактів як словника
    all_contacts_dict = {}

    # Створюємо список за розподільником переносу рядка, розподіляємо кожен рядок на ключ: значення та додаємо до словника
    for item in text.split('\n'):
        # Ловимо помилку якщо вхідний текст неможливо конвертувати
        try:
            phone_number, name = item.split(': ')
            all_contacts_dict[phone_number] = name
        except ValueError:
            all_contacts_dict = {}
            break
        except Exception as e:
            output(f'ПОМИЛКА (convert_str_dict) -> {e}', 'r')
            all_contacts_dict = {}
            break
    
    return all_contacts_dict # Повертаємо результат

@input_error
def edit_contact(path: str = 'task_4/contacts.txt', find_value: str = '') -> None:

    """
    Функція редагує вже існуючий контакт.

    Параметри:
    - path: Шлях до файлу контактів.
    - input_value: Ім'я контакту або номер телефона.

    Повертає:
    Нічого
    """

    # Відкриваємо файл з контактами для читання та считуємо усю книгу як рядок 
    content_file = open_read_file(path, "r")
    # print(content_file)

    # if all_contacts_str:
    #     return

    # Запит на пошуковий рядок, якщо не передано.
    if find_value:
        find_value = input('ЗАПИТ -> Введіть ім`я або номер телефону для пошуку: ').casefold()

    
    # # Конвертуємо текст у словник
    # all_contacts_dict = convert_str_dict(content_file)
    
    # Змінна для збереження результатів пошуку
    result_dict = {}

    # Find
    result_find = find_contact(find_value = find_value)
    
    if not result_find[0]:
        raise ValueError(f'Контакта за Вашим запитом не знайдено.')
    
    if result_find[0]:
        output(f"ЗНАЙДЕНО КОНТАКТИ", 'w')
        output(f"ID\tІм'я контакта\tНомер телефона", 'g')
        for i, (phone_number, name) in enumerate(result_find[1].items(), start=1):
            output(f"{i}\t{name:<15}\t{phone_number}", 'g')

        while True:
            contact_replace = input('ЗАПИТ: Введіть ідентифікатор контака, який потрібно змінити: ')
            if contact_replace.isdigit():
                contact_replace = int(contact_replace)
                if 0 < contact_replace <= len(result_find[1]):
                    phone_number = list(result_find[1].keys())[contact_replace - 1]
                    contact_replace = [phone_number, result_find[1][phone_number]]
                    old_phone_number_and_name = f'{contact_replace[0]}: {contact_replace[1]}'
                    break
        
        
        # Запитуємо що саме змінити ім'я чи номер телефону
        while True:
            replace = input('ЗАПИТ -> Яку інформацію Ви хочете змінити? Якщо ім`я напишіть "name" або "number" якщо номер телефона: ').casefold()
            if replace in ['name', 'number']:
                break

        check_all_if = False

        if replace == 'name':
            new_name = input('ЗАПИТ -> Введіть нове ім`я: ')
            new_phone_number_and_name = f'{contact_replace[0]}: {new_name}'
            check_all_if = True
            print(new_phone_number_and_name)

        elif replace == 'number':
            new_contact_number = input('ЗАПИТ -> Введіть новий номер телефона: ')

            # Перевіряємо введений номера телефона на коректність
            phone_number_standart = standart_phone_number(new_contact_number)

            # Друкуємо повідомлення що контакт не збережено, бо номер не коректний
            if not phone_number_standart[0]:
                raise KeyError(f'Задане "{phone_number}" - не може бути номером телефону')
            
            else:

                # Перевіряємо чи не існує такого номера у наших контактах
                phone_number_find = find_contact(find_value = phone_number_standart[1])

                # Друкуємо повідомлення що контакт не збережено, бо такий номер телефону вже зайнятий
                if phone_number_find[0]:
                    raise KeyError(f'Номер "{phone_number_standart[1]}" вже використовується контактом {phone_number_find[1][phone_number_standart[1]]}')
                else:
                    new_phone_number_and_name = f'{phone_number_standart[1]}: {contact_replace[1]}'
                    check_all_if = True
                    

        if check_all_if:
            
            new_content_file = content_file.replace(old_phone_number_and_name, new_phone_number_and_name)   
  
            # Записуємо результат у файл
            open_read_file(path, "w", new_content_file)
            output(f'ВИКОНАНО -> Контакт змінено {new_phone_number_and_name}', 'g')

@input_error
def display_contacts(path: str = 'task_4/contacts.txt') -> None:

    """
    Функція друкує на екран усі контакти з телефонної книги.

    Параметри:
    - path: Шлях до файлу контактів.

    Повертає:
    Нічого
    """

    # Відкриваємо файл з контактами для читання та считуємо усю книгу як рядок 
    content_file = open_read_file(r'task_4\contacts.txt', "r")
    # Конвертуємо текст у словник
    all_contacts = convert_str_dict(content_file)

    # Якщо словник не пустий то друкуємо його, а якщо пустий то сповіщаємо про це
    if all_contacts:
        output(f'СПИСОК КОНТАКТІВ', 'w')
        output(f'Ім`я контакта\tНомер телефона', 'g')
        for phone_number, name in all_contacts.items():
            output(f'{name:<15}\t{phone_number}', 'g')
    else:
        raise ValueError(f'Телефона книга не містить контактів або пошкоджена.')

def print_result_find_number(result_find: list) -> None:
    
    """
    Функція друкує на екран результати пошуку.

    Параметри:
    - result_find: Список знайдених контактів

    Повертає:
    Нічого
    """

    # Якщо словник не пустий то друкуємо його, а якщо пустий то сповіщаємо про це
    if result_find[0]:
        output(f'РЕЗУЛЬТАТ ПОШУКУ', 'w')
        output(f'Ім`я контакта\tНомер телефона', 'g')
        for phone_number, name in result_find[1].items():
            output(f'{name:<15}\t{phone_number}', 'g')
    else:
        output('УВАГА: Контакт за Вашим запитом не знайдено', 'y')

def format_number_name(phone_number: str, name: str) -> str:

    """
    Функція поєднує номер телефона та ім'я контакта за формою "НОМЕР: ІМ'Я"

    Параметри:
    - phone_number: Номер телефона
    - name: Ім'я контакта

    Повертає:
    Нічого
    """

    return f'{phone_number}: {name}'

def output(text: str, flag: str = 'w') -> None:

    """
    Функція додає кольорове забарвлення фукції print()

    Параметри:
    - text: Текст для фарбування
    - flag: Флаг кольору

    Повертає:
    Нічого
    """

    colors = {'y': Fore.YELLOW, 'g': Fore.GREEN, 'b': Fore.BLUE, 'r': Fore.RED, 'w': Fore.WHITE}
    print(f'{colors[flag]}{text}{Fore.RESET}')