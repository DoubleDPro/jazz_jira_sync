from JiraApiProcessor import JiraApiProcessor
from params import available_commands_with_descr
import sys

greetings = '''Введи команду для запуска.
Список доступных комманд:
'''
for key in available_commands_with_descr.keys():
    greetings += '{} - {}\n'.format(key, available_commands_with_descr.get(key))
while True:
    print(greetings)
    input_command = ''
    while True:
        input_command = input('Введи букву - ')
        if input_command in available_commands_with_descr.keys():
            print('Понял. Выполняем команду - "{}"'.format(available_commands_with_descr.get(input_command)))
            break
        else:
            print('Команды {} нет в списке доступных. Попробуй ещё раз...'.format(input_command))

    if input_command == 'e':
        print('Программа завершена')
        sys.exit()
    elif input_command == 'i':
        JiraApiProcessor().process_issues_from_jazz()
    elif input_command == 'c':
        JiraApiProcessor().process_comments_from_jazz()
    elif input_command == 't':
        JiraApiProcessor().process_tags_from_changelog()
    print('Команда "{}" выполнена успешно'.format(available_commands_with_descr.get(input_command)))

    is_continue = input("Продолжить?(y/n)")
    if is_continue == 'y':
        continue
    elif is_continue == 'n':
        break
    else:
        print('Команда не распознана. Завершаю программу...')
        break
print('Программа завершена')
