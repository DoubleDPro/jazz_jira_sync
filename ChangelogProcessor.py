import json
from params import changelog_filenames


class ChangelogProcessor:

    def __init__(self):
        self.changelog_filenames = changelog_filenames

    def get_list_of_issues_from_changelog(self, section):
        print('Получение списка задач из секции new_issues из файлов {}'.format(', '.join(self.changelog_filenames)))
        new_issues = {}
        for changelog_filename in self.changelog_filenames:
            with open(changelog_filename, encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                current_release = json_data['Release']
                if (new_issues.get(current_release)) is None:
                    new_issues[current_release] = list()
                for new_issue in json_data[section]:
                    new_issues[current_release].append(new_issue)
        return new_issues