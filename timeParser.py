import re
from datetime import datetime, timedelta

DAY = 60*60*24
HOUR = 60*60
MINUTE = 60
SECOND = 1

class TimeParser(object):

    def __init__(self):
        pass

    def isLeapYear(self, year: int) -> bool:
        if year % 4:
            return False
        if not year % 100 and year % 400:
            return False
        return True

    def getMonthDays(self, month: int, year: int) -> int:
        monthes = {
            1: 31,
            2: 29 if self.isLeapYear(year) else 28,
            3: 31,
            4: 30,
            5: 31,
            6: 30,
            7: 31,
            8: 31,
            9: 30,
            10: 31,
            11: 30,
            12: 31
        }
        return monthes.get(month, 0)

    def getMonthName(self, month: int) -> str:
        monthes = {
            1: "Janvier",
            2: "Février",
            3: "Mars",
            4: "Avril",
            5: "Mai",
            6: "Juin",
            7: "Juillet",
            8: "Août",
            9: "Septembre",
            10: "Octobre",
            11: "Novembre",
            12: "Décembre"
        }
        return monthes.get(month, "MoisNonDéfini")

    def getMultiplicatorMonthes(self, value) -> int:
        if value < 0:
            return 0
        currentDateTime = datetime.now()
        currentMonth = currentDateTime.month
        currentYear = currentDateTime.year
        totalDays = 0
        for i in range(0, value):
            totalDays += self.getMonthDays(currentMonth, currentYear)
            currentMonth = currentMonth + 1 if currentMonth < 12 else 1
            currentYear = currentYear + 1 if currentMonth == 1 else currentYear
        return totalDays * DAY

    def getMultiplicatorYears(self, value) -> int:
        if value < 0:
            return 0
        currentDateTime = datetime.now()
        currentYear = currentDateTime.year
        totalDays = 0
        for i in range(0, value):
            totalDays += 366 if self.isLeapYear(currentYear) and currentDateTime.month <= 2 else 365
            currentYear += 1
        return totalDays * DAY

    def getMultiplicator(self, string: str, value: int):
        switcher = {
            's': SECOND,
            'm': MINUTE,
            'h': HOUR,
            'j': DAY,
            'semaine': DAY * 7,
            'S': DAY * 7,
            'mois': self.getMultiplicatorMonthes,
            'M': self.getMultiplicatorMonthes,
            'a': self.getMultiplicatorYears
        }
        return switcher.get(string, 0)

    def parse(self, string: str):
        parsedTime = 0
        reg = re.compile(r'(\d+|def|Def)(mois|semaine|a|m|M|S|h|j|s)?')
        matches = reg.findall(string)
        if len(matches) < 1:
            return -1, False
        for match in matches:
            if match[0].lower() == 'def':
                return -1, True
            if not match[1]:
                return -1, False
            value = int(match[0])
            multiplicator = self.getMultiplicator(match[1], value)
            if not isinstance(multiplicator, int):
                multiplicator = multiplicator(value)
                value = 1
            if value > 0 and multiplicator > 0:
                parsedTime += value * multiplicator
        return parsedTime, True

    def handle(self, args):
        idx = 0
        totalTime = 0
        while idx < len(args):
            value, isTime = self.parse(args[idx])
            if not isTime:
                if idx == 0:
                    return -1, idx
                break
            if value == -1:
                return -1, idx + 1
            totalTime += value
            idx += 1
        return totalTime, idx

    def delta(self, args):
        seconds, index = self.handle(args)
        if seconds > 0:
            return timedelta(seconds=seconds), index
        return None, index

    def endDate(self, args):
        delta, index = self.delta(args)
        if not delta:
            return None, index
        return datetime.now() + delta, index


if __name__ == "__main__":
    tests = [
        ('2h30m', 'Pour', 'la', 'raison', 'suivante'),
        ('1heure',),
        ('2h', '5min', 'Pour', 'la', 'raison', 'suivante'),
        ('3hrs', '2m'),
        ('1hr', '3mi', 'Pour', 'la', 'raison', 'suivante'),
        ('20mins',),
        ('30minutes', 'Pour', 'la', 'raison', 'suivante'),
        ('1minute',),
        ('def', 'Parce', 'que', 'je', 'le', 'veux'),
        ('Definitif',),
        ('2j', 'Yolo'),
        ('Je', 'refuse'),
        ('2mois', 'Mashallah'),
        ('8mois',),
        ('2semaines',),
        ('2ans', 'Yolo'),
        ('1a1M1S1j1h1m1s', 'Pour', 'tester'),
        ('2j', '1200tokens'),
        ('2j', '1800', 'tokens')
    ]

    timeParser = TimeParser()
    for test in tests:
        print('--------------------')
        print(test)
        date, index = timeParser.endDate(test)
        if date:
            print(date)
        else:
            print('infinite')
        print(index)
        print(test[index:])
