# Завдання - 3
# Розробіть Python-скрипт для аналізу файлів логів. Скрипт повинен вміти читати лог-файл, переданий як аргумент командного рядка, 
# і виводити статистику за рівнями логування наприклад, INFO, ERROR, DEBUG. Також користувач може вказати рівень логування як другий 
# аргумент командного рядка, щоб отримати всі записи цього рівня.

# Імпортуємо модуль для парсингу значень у тексті
import sys

def load_logs(file_path: str) -> list:
    
    ''' Відкриває файл для читання, зчитує рядки та викликає для кожного функцію parse_log_line '''
    
    logs = [] 

    try:
        with open(file_path, 'r') as file:
            logs = [parse_log_line(line) for line in file]
            if not logs:
                print(f"Файл '{file_path}' - не містить логів.")
                exit()
    except FileNotFoundError:
        print(f"Файл '{file_path}' - не знайдено.")
    except Exception as e:
        print(f"Файл '{file_path}' - не оброблено ({e}).")
    finally:
        return logs # Повертаємо список з результатом який отримаємо після функції parse_log_line

def parse_log_line(line: str) -> dict:
    
    ''' Ділення за значеннями рядка з файлу та повернення словника з рівнем логування та повідомленням '''
    
    parts = line.strip().split(' ', 3)
    log_line = {'date': parts[0], 'time': parts[1], 'level': parts[2], 'message': parts[3]}
    
    return log_line # Повертаємо словник з результатом ділення строки


# Фільтрація логів за рівнем
def filter_logs_by_level(logs: list, level: str) -> list:

    ''' Фільтрує усі логи зі списку, який повертає функція load_logs за заданим рвінем логувіання  '''
    
    return [log for log in logs if log['level'] == level.upper()] # Повертає список з усіма логами з заданим рівнем логування

def count_logs_by_level(logs: list) -> dict:

    ''' Підраховує кількість логів за рівнем логування '''

    counts = {'INFO': 0, 'ERROR': 0, 'DEBUG': 0, 'WARNING': 0}
    
    for log in logs:
        counts[log['level']] += 1

    return counts # Повертає словник з рівнем логування та його кількістю


def display_log_counts(log_counts: dict) -> None:

    ''' Виводе на екран список з рівня логування та кількості логів такого рівня '''

    if all(value != 0 for value in log_counts.values()): # Перевіряє чи є хоч один коректний рівень логування

        print(f'РіВЕНЬ ЛОГУВАННЯ | КІЛЬКІСТЬ\n---------------- | ---------')

        for level, count in log_counts.items():
            print(f"{level:<16} | {count:<9}") 

def display_log_by_level(logs: dict) -> None:

    ''' Виводе на екран список усіх логів за заданим рівнем логування '''
  
    if logs:
        print(f'Деталі логів для рівня {sys.argv[2].upper()}:')
        for item in logs:
            print(f'{item['date']} {item['time']} {item['level']} {item['message']}')
    else:
        print(f'Логів за заданим рівнем {sys.argv[2].upper()} - не знайдено')

if __name__ == "__main__":

    if len(sys.argv) < 2:
        print("Використовуйте конструкції: [python task_3.py logs.txt] або [python task_3.py logs.txt 'log_level']")
    else:
        log_file_path = sys.argv[1] # Шлях до файлу з логами як аргумент
        log_level = sys.argv[2] if len(sys.argv) >= 3 else None # Рівень помилки як аргумент
        logs = load_logs(log_file_path) # Завантаження логів

        display_log_counts(count_logs_by_level(logs)) # Вивести кількість логів

        if log_level: # Якщо вказаний рівенб логування для деталізації
            display_log_by_level(filter_logs_by_level(logs, log_level))