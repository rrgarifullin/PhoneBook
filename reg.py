import csv
import re


class Worker:

    workers_info = []

    def __init__(self, info):
        self.info = info
        self.worker_info = []

    def get_lfs_name(self):
        lfs = str()
        for i in range(3):
            lfs = lfs + ' ' + self.info[i]
        lfs = lfs.split(' ')
        lastname, name, surname = lfs[1], lfs[2], lfs[3]
        self.worker_info.append(lastname)
        self.worker_info.append(name)
        self.worker_info.append(surname)

    def get_place_of_work(self):
        organization = self.info[3]
        position = self.info[4]
        self.worker_info.append(organization)
        self.worker_info.append(position)

    def get_contacts(self):
        number = self.info[5]
        if number != '':
            if 'доб' in number:
                pattern = re.compile(r'(\+7|8)\s*\(?(\d{3})\)?[\s*|-]*(\d{3})[\s*|-]*(\d{2})[\s*|-]*(\d{2})\s*\(?(\w+)?\.?\s*(\d+)?\)?')
                formatted_number = pattern.sub(r'+7(\2)\3-\4-\5 доб.\7', number)
            else:
                pattern = re.compile(r'(\+7|8)\s*\(?(\d{3})\)?[\s*|-]*(\d{3})[\s*|-]*(\d{2})[\s*|-]*(\d{2})')
                formatted_number = pattern.sub(r'+7(\2)\3-\4-\5', number)
        else:
            formatted_number = ''
        self.worker_info.append(formatted_number)

        email = self.info[6]
        self.worker_info.append(email)

    def check_doubles(self):
        checked = True
        for worker in self.workers_info[1:]:
            if worker[0] == self.worker_info[0] and worker[1] == self.worker_info[1]:
                for i in range(3, 7):
                    if worker[i] != self.worker_info[i]:
                        worker[i] += self.worker_info[i]
                        checked = False
        if checked:
            self.workers_info.append(self.worker_info)


def open_csv():
    with open('phonebook_raw.csv', 'r', encoding='utf-8') as f:
        rows = csv.reader(f, delimiter=',')
        contacts_list = list(rows)
        return contacts_list


def write_csv():
    with open('phonebook.csv', 'w', encoding='utf-8') as f:
        datawriter = csv.writer(f, delimiter=',')
        datawriter.writerows(Worker.workers_info)


def main():
    contacts_list = open_csv()
    Worker.workers_info.append(contacts_list[0])
    for work in contacts_list[1:]:
        worker = Worker(work)
        worker.get_lfs_name()
        worker.get_place_of_work()
        worker.get_contacts()
        worker.check_doubles()
    write_csv()


if __name__ == '__main__':
    main()
