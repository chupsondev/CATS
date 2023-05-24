import requests
from requests_toolbelt.multipart.encoder import MultipartEncoder
import random
import string
import time
from cats_tools import cprint, COLORS, tabulate

URL = "https://themis.ii.uni.wroc.pl/"
HOST = "themis.ii.uni.wroc.pl"

LANGUAGES = {
    "cpp": "g++",
    "c": "gcc",
    "RAM": "ram",
    "py": "py3",
}


def result_ready(text):
    not_ready = ["waiting", "compiling", "running"]
    for i in not_ready:
        if text.find(i) != -1:
            return False
    return True


verdicts = {
    "accepted": ("✅", COLORS.GREEN),
    "wrong answer": ("❌", COLORS.FAIL),
    "time limit exceeded": ("⏱", COLORS.WARNING),
}


class ThemisSingleTest:
    def __init__(self, test_number, verdict, time, max_time, memory, points):
        self.test_number = test_number
        self.verdict = verdict
        self.time = time
        self.max_time = max_time
        self.memory = memory
        self.points = points

    def print_test_result(self):
        cprint(f"{verdicts[self.verdict][0]} {self.test_number}. {self.verdict}", verdicts[self.verdict][1])
        print(tabulate(f"{self.time} sec./{self.max_time} sec. {self.memory} mem. {self.points} pts."))



class ThemisResult:
    def __init__(self, raw_result):
        self.raw_result = raw_result
        self.tests: list[ThemisSingleTest] = []
        self.summary_emotes = ""
        self.parse_result()

    def parse_single_test(self, text):
        text = text.split('<td>')
        test_number = text[1].split('>')[1].split('<')[0]
        test_number = test_number.split('.')[0]
        test_number = int(test_number)

        verdict = text[8].split('>')[1].split('<')[0]

        time = text[3].split('<')[0]
        time = float(time.split(' ')[0])
        max_time = text[4].split('<')[0]
        max_time = float(max_time.split(' ')[0])

        memory = text[6].split('<')[0]

        points = text[7].split('<')[0]
        points = int(float(points.split(' ')[0]))

        self.summary_emotes += verdicts[verdict][0]
        self.tests.append(ThemisSingleTest(test_number,
                                           verdict,
                                           time,
                                           max_time,
                                           memory,
                                           points))

    def parse_result(self):
        text = self.raw_result
        text = text.split('<tr>')[2:]

        for test in text:
            self.parse_single_test(test)

    def print_result(self):
        for test in self.tests:
            test.print_test_result()
        print(self.summary_emotes)

class Themis:

    def auth(self):
        response = requests.post(URL + 'login', data={'userid': self.login, 'passwd': self.password},
                                 headers={'Host': HOST, 'Referer': 'https://themis.ii.uni.wroc.pl/'})
        return response.request.headers['Cookie']

    def __init__(self, login, password):
        self.login = login
        self.password = password
        self.cookies = self.auth()

    def submit(self, group_code, problem_code, file_path):
        problem_url = URL + group_code + '/' + problem_code

        code = open(file_path, 'r').read()

        extension = file_path.split('.')[-1]

        encoder = MultipartEncoder(
            fields={
                'source': code,
                'file': "",
                "lang": LANGUAGES[extension], },
            boundary="------WebKitFormBoundary" + ''.join(random.sample(string.ascii_letters + string.digits, 16))
        )

        headers = {
            "host": HOST,
            "cookie": self.cookies,
            "connection": "keep-alive",
            "content-type": encoder.content_type,
            "referer": problem_url
        }

        response = requests.post(problem_url + "/submit", headers=headers, data=encoder)
        results_code = response.text
        results_url = URL + group_code + "/result/" + results_code

        result = None

        while True:
            response = requests.get(results_url, headers=headers)
            if result_ready(response.text):
                result = response.text
                break
            time.sleep(0.3)

        return ThemisResult(result)
