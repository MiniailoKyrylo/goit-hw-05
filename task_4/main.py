import contact_book

def input_error(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except ValueError as ve:
            contact_book.output(f'ПОМИЛКА -> {ve}', 'r')
        except Exception as e:
            contact_book.output(f'ПОМИЛКА -> {e}', 'r')
    return wrapper

@input_error
def menu_selection(command: str = '') -> None:

    """
    Функція викликає необхідну функцію залежно від команди.

    Параметри:
    - command: Рядок з командою

    Повертає:
    Нічого
    """

    if not command:
        command = input('ЗАПИТ -> Введіть команду для виконання або її ідентифікатор: ')

    if command in ['1', 'add contact']:
        contact_book.add_contact()
    elif command in ['2', 'find contact']:
        contact_book.print_result_find_number(contact_book.find_contact())
    elif command in ['3', 'edit contact']:
        contact_book.edit_contact()
    elif command in ['4', 'display contacts']:
        contact_book.display_contacts()
    elif command in ['5', 'help']:
        display_help()
    elif command in ['6', 'exit']:
        exit()
    else:
        raise ValueError(f'Команда "{command}" - не може бути виконана, так як не розпізнана.')


def display_help() -> None:

    """
    Виводить на екран усі можливі команди.

    Параметри:
    - command: Рядок з командою

    Повертає:
    Нічого
    """
    
    commands = {1: ['add contact', 'Додати новий контакт'],
                2: ['find contact', 'Знайти контакт за іменем або номером телефона'],
                3: ['edit contact', 'Змінити існуючий контакт'],
                4: ['display contacts', 'Показати усі контакти'],
                5: ['help', 'Показати усі доступні команди'],
                6: ['exit', 'Вийти з програми'],
                }
    
    contact_book.output(f'ПЕРЕЛІК ДОСТУПНИХ КОМАНД', 'w')
    contact_book.output(f"ID\t{'Koманда':<20}\tОпис", 'g')
    for i, (id, name_about) in enumerate(commands.items(), start=1):
        contact_book.output(f"{i}\t{name_about[0]:<20}\t{name_about[1]}", 'g')

contact_book.output('ВІТАННЯ -> Ласкаво прошу до бота для роботи з телефонною книгою!', 'w')
contact_book.output('УВАГА -> Для ознайомлення з усіма командами - введіть "help"', 'y')
while True:
    menu_selection()