from params import issue_csv_file_name
from params import comments_csv_file_name
from params import issue_pattern_dict
from params import test_env
from params import sst_env
from params import prod_env


class JazzCsvProcessor:

    def __init__(self):
        self.issues_csv_file_name = issue_csv_file_name
        self.comments_csv_file_name = comments_csv_file_name

    def get_jazz_issue_id_and_comments_from_csv_file(self):
        print('Обработка файла {} с выгрузкой комментариев по дефектам из Jazz'.format(self.comments_csv_file_name))
        issue_with_comments_dict = {}
        with open(self.comments_csv_file_name, encoding='utf-16') as csv_comments_data:
            lines = csv_comments_data.readlines()
            i = 1
            while i < len(lines):
                if lines[i].split("\t")[0].strip("\"").isdigit():
                    comments = []
                    issue_id = lines[i].split("\t")[0].strip("\"")
                    if lines[i].split("\t")[1].strip("\"") != '\n':
                        comments.append(lines[i].split("\t")[1].strip("\""))
                    while not lines[i + 1].split("\t")[0].strip("\"").isdigit():
                        i += 1
                        if lines[i].strip("\"") == '\n':
                            continue
                        if lines[i].strip("\"")[0].isdigit():
                            comments.append(lines[i].strip("\""))
                        else:
                            comments[len(comments) - 1] += lines[i].strip("\"").strip("\"")
                        if i == len(lines) - 1:
                            break
                    i += 1
                    issue_with_comments_dict[issue_id] = comments
        print('Обработка файла {} с выгрузкой комментариев по дефектам из Jazz закончена успешно'.format(
            self.comments_csv_file_name))
        print('Сформирован список комментариев для обновления в Jira в количестве {} дефектов'.format(
            len(issue_with_comments_dict.keys())))
        return issue_with_comments_dict

    def process_csv_issues(self):
        print('Обработка файла {} с выгрузкой дефектов из Jazz'.format(self.issues_csv_file_name))
        list_of_input_issues = []
        with open(self.issues_csv_file_name, encoding='utf-16') as csv_issues_data:
            lines = csv_issues_data.readlines()
            i = 1
            while i < len(lines):
                if lines[i].split("\t")[0].strip("\"").isdigit():
                    issue_id = lines[i].split("\t")[0].strip("\"")
                    summary = lines[i].split("\t")[1].strip("\"")
                    fix_place = lines[i].split("\t")[2].strip("\"")
                    planned_for = lines[i].split("\t")[3].strip("\"")
                    priority = lines[i].split("\t")[4].strip("\"")
                    description = lines[i].split("\t")[5].strip("\"")
                    while not lines[i + 1].split("\t")[0].strip("\"").isdigit():
                        i += 1
                        description += lines[i].strip("\"")
                        if i == len(lines) - 1:
                            break
                    i += 1
                    current_issue_dict = issue_pattern_dict.copy()
                    current_issue_dict['summary'] = 'RTC JAZZ' + ' ' + issue_id + ' ' + summary
                    current_issue_dict['description'] = description
                    if fix_place in test_env:
                        current_issue_dict['customfield_12300']['value'] = 'Тестовая'
                    elif fix_place in sst_env:
                        current_issue_dict['customfield_12300']['value'] = 'Копия промышленной эксплуатации'
                    elif fix_place in prod_env:
                        current_issue_dict['customfield_12300']['value'] = 'Промышленная эксплуатация'
                    current_issue_dict['fixVersions'][0]['name'] = planned_for
                    if priority == 'Не присвоено':
                        current_issue_dict['priority']['name'] = 'Самый низкий'
                    else:
                        current_issue_dict['priority']['name'] = priority
                    list_of_input_issues.append(current_issue_dict)
        print('Обработка файла {} с выгрузкой дефектов из Jazz закончена успешно'.format(self.issues_csv_file_name))
        print('Сформирован список для загрузки в Jira в количестве {} дефектов'.format(str(len(list_of_input_issues))))
        return list_of_input_issues
