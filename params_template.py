# Params for JIRA
jira_server_host = ''
test_env = ('')
sst_env = ('')
prod_env = ('')
issue_pattern_dict = {
    'project': {'id': 0},
    'summary': '',
    'description': '',
    'issuetype': {'name': 'Дефект'},
    'customfield_14700': [{'value': 'Функциональное'}],
    'customfield_12300': {'value': ''},
    'customfield_12607': [{'value': 'функциональный'}],
    'fixVersions': [{'name': ''}],
    'priority': {'name': ''},
    'assignee': {'name': ''}
}

# Params for Jazz
issue_csv_file_name = ''
comments_csv_file_name = ''

# Common params
available_commands_with_descr = {
    'e': 'Завершение программы',
    'i': 'Обработка списка дефектов',
    'c': 'Обработка списка комментов'
}
