from jira import JIRA
from time import sleep
from JazzCsvProcessor import JazzCsvProcessor
from ChangelogProcessor import ChangelogProcessor
from params import jira_server_host
import getpass


class JiraApiProcessor:

    def __init__(self):
        self.options = {'server': jira_server_host}
        self.jira_user_login, self.jira_user_password = self.set_credentials()

    def set_credentials(self):
        while 1:
            jira_user_login = input("Введите имя пользователя Jira\n")
            if not jira_user_login:
                print("Не указано имя пользователя!")
                continue
            jira_user_password = getpass.getpass("Введите пароль пользователя Jira\n")
            if not jira_user_password:
                print("Не указан пароль!")
                continue
            if None not in [jira_user_login, jira_user_password]:
                break
        return jira_user_login, jira_user_password

    def process_comments_from_jazz(self):
        print('Обработка комментариев, выгруженных из Jazz')
        jira = JIRA(self.options, basic_auth=(self.jira_user_login, self.jira_user_password))
        dict_of_issues_with_comments = JazzCsvProcessor().get_jazz_issue_id_and_comments_from_csv_file()
        for jazz_issue_id in dict_of_issues_with_comments.keys():
            print('Обработка комментариев в дефекте Jazz RTC {}'.format(jazz_issue_id))
            if len(dict_of_issues_with_comments.get(jazz_issue_id)) == 0:
                print('Для дефекта RTC JAZZ {} отсутствуют комментарии, пропускаем')
                continue
            jira_issue = jira.search_issues('PROJECT = ARSPSBR AND STATUS != "Отменен (Canceled)" AND SUMMARY ~ {}'
                                            .format('"RTC ' + jazz_issue_id + '%"'),
                                            maxResults=1, expand='changelog', fields='comment', json_result=True)
            if len(jira_issue.get('issues')) == 0:
                print('Дефекта RTC JAZZ {} нет в JIRA. Пропускаем обновление комментариев'.format(jazz_issue_id))
                continue
            jira_comments_list = jira_issue.get('issues')[0].get('fields').get('comment').get('comments')
            if len(jira_comments_list) == 0:
                for jazz_comment in dict_of_issues_with_comments.get(jazz_issue_id):
                    jira.add_comment(jira_issue.get('issues')[0].get('key'), jazz_comment)
                    print('#', end='')
                    sleep(2)
                print()
            else:
                jira_comment_bodys = []
                for jira_comment in jira_comments_list:
                    jira_comment_bodys.append(jira_comment.get('body'))
                delta_comments_list = [comment for comment in dict_of_issues_with_comments.get(jazz_issue_id) if
                                       comment not in jira_comment_bodys]
                if len(delta_comments_list) == 0:
                    print('Для дефекта RTC JAZZ {} нет новых комментариев'.format(jazz_issue_id))
                    continue
                else:
                    for delta_comment in delta_comments_list:
                        jira.add_comment(jira_issue.get('issues')[0].get('key'), delta_comment)
                        print('#', end='')
                        sleep(2)
                    print()
                    print('Для дефекта RTC JAZZ {} добавлены новые комментарии'.format(jazz_issue_id))
            sleep(2)
        print('Обработка комментариев, выгруженных из Jazz прошла успешно')

    def process_issues_from_jazz(self):
        print('Обработка дефектов, выгруженных из Jazz')
        jira = JIRA(self.options, basic_auth=(self.jira_user_login, self.jira_user_password))
        list_of_input_issues = JazzCsvProcessor().process_csv_issues()
        for issue in list_of_input_issues:
            new_issue = jira.create_issue(fields=issue)
            print('Для дефекта {} из RTC в JIRA создан дефект {}'.format(issue.get('summary'), new_issue.key))
        print('Обработка дефектов, выгруженных из Jazz прошла успешно')

    def process_tags_from_changelog(self):
        print('Обработка changelog-ов для выставления меток в задачах Jira')
        jira = JIRA(self.options, basic_auth=(self.jira_user_login, self.jira_user_password))
        changelog_processor = ChangelogProcessor()
        new_issues = changelog_processor.get_list_of_issues_from_changelog('New_Issues')
        all_issues = changelog_processor.get_list_of_issues_from_changelog('All_Issues')
        for release in new_issues:
            for issue in new_issues.get(release):
                issue_query = ''
                if 'jazz' in issue:
                    issue_query = 'PROJECT = ARSPSBR AND STATUS != "Отменен (Canceled)" AND SUMMARY ~ {}'.format('"RTC JAZZ ' + issue[4:] + '%"')
                elif 'ARSPSBR' in issue:
                    issue_query = 'PROJECT = ARSPSBR AND STATUS != "Отменен (Canceled)" AND "Partner Issue Key" ~ {}'.format('"' + issue + '"')
                jira_issue_json = jira.search_issues(issue_query, maxResults=1, json_result=True)
                jira_issue = jira.issue(jira_issue_json.get('issues')[0].get('key'))
                current_labels = jira_issue_json.get('issues')[0].get('fields').get('labels')
                new_label = 'new@' + release
                current_labels.append(new_label)
                jira_issue.update(fields={"labels": current_labels})
                print('Метка ' + new_label + ' успешно добавлена в задачу ' + jira_issue)
        for release in all_issues:
            for issue in all_issues.get(release):
                issue_query = ''
                if 'jazz' in issue:
                    issue_query = 'PROJECT = ARSPSBR AND STATUS != "Отменен (Canceled)" AND SUMMARY ~ {}'.format('"RTC JAZZ ' + issue[9:] + '%"')
                elif 'ARSPSBR' in issue:
                    issue_query = 'PROJECT = ARSPSBR AND STATUS != "Отменен (Canceled)" AND "Partner Issue Key" ~ {}'.format('"' + issue + '"')
                jira_issue_json = jira.search_issues(issue_query, maxResults=1, json_result=True)
                jira_issue = jira.issue(jira_issue_json.get('issues')[0].get('key'))
                current_labels = jira_issue_json.get('issues')[0].get('fields').get('labels')
                new_label = 'all@' + release
                current_labels.append(new_label)
                jira_issue.update(fields={"labels": current_labels})
                print('Метка ' + new_label + ' успешно добавлена в задачу ' + jira_issue)