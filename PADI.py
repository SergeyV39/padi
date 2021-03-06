from tabulate import tabulate
from colorama import Fore, Back, Style, init


#comment
def depth():
    while True:
        # for keys in depth_and_time:
        #     print(keys)
        #     print(tabulate(depth_and_time[keys], headers='keys', tablefmt='grid', stralign='center'))
        try:
            h = int(input('Введите глубину не менее 1м и не более 42м: '))
        except ValueError:
            continue
        if 0 < h <= 10:
            h = 10
        elif 10 <= h <= 22 and h % 2 != 0:
            h = h + h % 2
        elif 22 < h <= 25:
            h = 25
        elif 25 < h <= 30:
            h = 30
        elif 30 < h <= 35:
            h = 35
        elif 35 < h <= 40:
            h = 40
        elif h == 41 or h == 42:
            h = 42
        elif h > 42 or h <= 0:
            continue
        print('\nТаблица определения группы по азоту для глубины', h, 'метров.')
        print(tabulate(depth_and_time[h], headers='keys', tablefmt='grid', stralign='center'), '\n')
        return h


def time(d):
    while True:
        try:
            time_input = int(input('Введите время проведенное под водой в минутах: '))
        except ValueError:
            continue
        if time_input > max(depth_and_time[d]):
            print('Введенное вами время', time_input, 'минут превышает бездекомпрессионный предел',
                  max(depth_and_time[d]), 'минут.\nПринимаем его к расчетам.')
            return max(depth_and_time[d])
        elif time_input > 0:
            return time_input


def first_dive(d, t):
    global count_dives, count
    for depth_time in depth_and_time[d]:
        if depth_time >= t and count_dives > 1:
            print('Группа по азоту после', count, 'погружения:', depth_and_time[d][depth_time])
            count_dives -= 1
            count += 1
            return next_dive(depth_and_time[d][depth_time])
        elif depth_time >= t:
            print('Группа по азоту после', count, 'погружения:', depth_and_time[d][depth_time])
            return print(Fore.RED, '\nПрофиль погружения:', Fore.BLUE, '\nГлубина погружения:', Fore.GREEN, d,
                         Fore.MAGENTA, '\nВремя погружения:', Fore.RED, t, Fore.BLUE,
                         '\nГруппа по азоту:', Fore.GREEN, depth_and_time[d][depth_time])


def next_dive(nitro_group, depth_next=0, inp_text=0):
    corrected_group = relax_group(nitro_group, inp_text)
    depth_next = depth()
    while corrected_group not in corrected_time[depth_next]:
        print('Слишко мало отдохнули. Введите большее время отдыха')
        corrected_group = relax_group(nitro_group, inp_text)
    time_next = time(depth_next) + corrected_time[depth_next][corrected_group]
    max_time = max(depth_and_time[depth_next]) - corrected_time[depth_next][corrected_group]
    if time_next > max(depth_and_time[depth_next]) and max_time > 0:
        print('Максимально возможное время нахождения под водой с учетом отдыха составляет', max_time,
              'минут.\nПринимаем его к расчетам.')
        return first_dive(depth_next, max_time)
    elif time_next < max(depth_and_time[depth_next]):
        return first_dive(depth_next, time_next)
    elif max_time <= 0:
        print('Вы недостаточно отдохнули, чтобы погружаться на данную глубину')
        while True:
            try:
                inp_text = input('Для выхода нажмите ENTER, для продолжения введите новое время отдыха: ')
                break
            except ValueError:
                inp_text = 0
                continue
        if inp_text.isdigit():
            return next_dive(nitro_group, depth_next, int(inp_text))
        else:
            return print('THE END')


def relax_group(nitro_group, inp_text=0):
    while True:
        try:
            if inp_text:
                t = inp_text
            else:
                t = int(input('Введите время отдыха на поверхности в минутах: '))
        except ValueError:
            continue
        for i in relax_time[nitro_group]:
            if t >= i:
                print('Группа по азоту после отдыха на поверхности:', relax_time[nitro_group][i])
                return relax_time[nitro_group][i]


depth_and_time = {
    10: {10: 'A', 20: 'B', 26: 'C', 30: 'D', 34: 'E', 37: 'F', 41: 'G', 45: 'H', 50: 'I', 54: 'J', 59: 'K', 64: 'L',
         70: 'M', 75: 'N', 82: 'O', 88: 'P', 95: 'Q', 104: 'R', 112: 'S', 122: 'T', 133: 'U', 145: 'V', 160: 'W',
         178: 'X', 199: 'Y', 219: 'Z'},
    12: {9: 'A', 17: 'B', 23: 'C', 26: 'D', 29: 'E', 32: 'F', 35: 'G', 38: 'H', 42: 'I', 45: 'J', 49: 'K', 53: 'L',
         57: 'M', 62: 'N', 66: 'O', 71: 'P', 76: 'Q', 82: 'R', 88: 'S', 94: 'T', 101: 'U', 108: 'V', 116: 'W', 125: 'X',
         134: 'Y', 147: 'Z'},
    14: {8: 'A', 15: 'B', 19: 'C', 22: 'D', 24: 'E', 27: 'F', 29: 'G', 32: 'H', 35: 'I', 37: 'J', 40: 'K', 43: 'L',
         47: 'M', 50: 'N', 53: 'O', 57: 'P', 61: 'Q', 64: 'R', 68: 'S', 73: 'T', 77: 'U', 82: 'V', 87: 'W', 92: 'X',
         98: 'Y'},
    16: {7: 'A', 13: 'B', 17: 'C', 19: 'D', 21: 'E', 23: 'F', 25: 'G', 27: 'H', 29: 'I', 32: 'J', 34: 'K', 37: 'L',
         39: 'M', 42: 'N', 45: 'O', 48: 'P', 50: 'Q', 53: 'R', 56: 'S', 60: 'T', 63: 'U', 67: 'V', 70: 'W', 72: 'X'},
    18: {6: 'A', 11: 'B', 15: 'C', 16: 'D', 18: 'E', 20: 'F', 22: 'G', 24: 'H', 26: 'I', 28: 'J', 30: 'K', 32: 'L',
         34: 'M', 36: 'N', 39: 'O', 41: 'P', 43: 'Q', 46: 'R', 48: 'S', 51: 'T', 53: 'U', 55: 'V', 56: 'W'},
    20: {6: 'A', 10: 'B', 13: 'C', 15: 'D', 16: 'E', 18: 'F', 20: 'G', 21: 'H', 23: 'I', 25: 'J', 26: 'K', 28: 'L',
         30: 'M', 32: 'N', 34: 'O', 36: 'P', 38: 'Q', 40: 'R', 42: 'S', 44: 'T', 45: 'U'},
    22: {5: 'A', 9: 'B', 12: 'C', 13: 'D', 15: 'E', 16: 'F', 18: 'G', 19: 'H', 21: 'I', 22: 'J', 24: 'K', 25: 'L',
         27: 'M', 29: 'N', 30: 'O', 32: 'P', 34: 'Q', 36: 'R', 37: 'S'},
    25: {4: 'A', 8: 'B', 10: 'C', 11: 'D', 13: 'E', 14: 'F', 15: 'G', 17: 'H', 18: 'I', 19: 'J', 21: 'K', 22: 'L',
         23: 'M', 25: 'N', 26: 'O', 28: 'P', 29: 'Q'},
    30: {3: 'A', 6: 'B', 8: 'C', 9: 'D', 10: 'E', 11: 'F', 12: 'G', 13: 'H', 14: 'I', 15: 'J', 16: 'K', 17: 'L',
         19: 'M', 20: 'N'},
    35: {3: 'A', 5: 'B', 7: 'C', 8: 'D', 9: 'F', 10: 'G', 11: 'H', 12: 'I', 13: 'J', 14: 'K'},
    40: {5: 'B', 6: 'C', 7: 'E', 8: 'F', 9: 'G'},
    42: {4: 'B', 6: 'D', 7: 'E', 8: 'F'}
}
relax_time = {
    'A': {0: 'A', },
    'B': {48: 'A', 0: 'B', },
    'C': {70: 'A', 22: 'B', 0: 'C', },
    'D': {79: 'A', 31: 'B', 9: 'C', 0: 'D'},
    'E': {88: 'A', 39: 'B', 17: 'C', 8: 'D', 0: 'E'},
    'F': {95: 'A', 47: 'B', 25: 'C', 16: 'D', 8: 'E', 0: 'F'},
    'G': {102: 'A', 54: 'B', 32: 'C', 23: 'D', 14: 'E', 7: 'F', 0: 'G'},
    'H': {108: 'A', 60: 'B', 38: 'C', 29: 'D', 21: 'E', 13: 'F', 6: 'G', 0: 'H'},
    'I': {114: 'A', 66: 'B', 44: 'C', 35: 'D', 27: 'E', 19: 'F', 12: 'G', 6: 'H', 0: 'I'},
    'J': {120: 'A', 72: 'B', 50: 'C', 41: 'D', 32: 'E', 25: 'F', 18: 'G', 12: 'H', 6: 'I', 0: 'J'},
    'K': {125: 'A', 77: 'B', 55: 'C', 46: 'D', 38: 'E', 30: 'F', 23: 'G', 17: 'H', 11: 'I', 5: 'J', 0: 'K'},
    'L': {130: 'A', 82: 'B', 60: 'C', 51: 'D', 43: 'E', 35: 'F', 28: 'G', 22: 'H', 16: 'I', 10: 'J', 5: 'K', 0: 'L'},
    'M': {135: 'A', 86: 'B', 65: 'C', 56: 'D', 47: 'E', 40: 'F', 33: 'G', 26: 'H', 20: 'I', 15: 'J', 10: 'K', 5: 'L',
          0: 'M'},
    'N': {139: 'A', 91: 'B', 69: 'C', 60: 'D', 52: 'E', 44: 'F', 37: 'G', 31: 'H', 25: 'I', 19: 'J', 14: 'K', 9: 'L',
          4: 'M', 0: 'N'},
    'O': {144: 'A', 95: 'B', 73: 'C', 64: 'D', 56: 'E', 48: 'F', 42: 'G', 35: 'H', 29: 'I', 24: 'J', 18: 'K', 13: 'L',
          9: 'M', 4: 'N', 0: 'O'},
    'P': {148: 'A', 99: 'B', 77: 'C', 68: 'D', 60: 'E', 52: 'F', 46: 'G', 39: 'H', 33: 'I', 28: 'J', 22: 'K', 17: 'L',
          13: 'M', 8: 'N', 4: 'O', 0: 'P'},
    'Q': {151: 'A', 103: 'B', 81: 'C', 72: 'D', 64: 'E', 56: 'F', 49: 'G', 43: 'H', 37: 'I', 31: 'J', 26: 'K', 21: 'L',
          17: 'M', 12: 'N', 8: 'O', 4: 'P', 0: 'Q'},
    'R': {155: 'A', 107: 'B', 85: 'C', 76: 'D', 68: 'E', 60: 'F', 53: 'G', 47: 'H', 41: 'I', 35: 'J', 30: 'K', 25: 'L',
          20: 'M', 16: 'N', 12: 'O', 8: 'P', 4: 'Q', 0: 'R'},
    'S': {159: 'A', 110: 'B', 88: 'C', 79: 'D', 71: 'E', 64: 'F', 57: 'G', 50: 'H', 44: 'I', 39: 'J', 33: 'K', 28: 'L',
          24: 'M', 19: 'N', 15: 'O', 11: 'P', 7: 'Q', 4: 'R', 0: 'S'},
    'T': {162: 'A', 114: 'B', 92: 'C', 83: 'D', 74: 'E', 67: 'F', 60: 'G', 54: 'H', 48: 'I', 42: 'J', 37: 'K', 32: 'L',
          27: 'M', 23: 'N', 18: 'O', 14: 'P', 11: 'Q', 7: 'R', 3: 'S', 0: 'T'},
    'U': {165: 'A', 117: 'B', 95: 'C', 86: 'D', 78: 'E', 70: 'F', 63: 'G', 57: 'H', 51: 'I', 45: 'J', 40: 'K', 35: 'L',
          30: 'M', 26: 'N', 22: 'O', 18: 'P', 14: 'Q', 10: 'R', 7: 'S', 3: 'T', 0: 'U'},
    'V': {168: 'A', 120: 'B', 98: 'C', 89: 'D', 81: 'E', 73: 'F', 66: 'G', 60: 'H', 54: 'I', 48: 'J', 43: 'K', 38: 'L',
          34: 'M', 29: 'N', 25: 'O', 21: 'P', 17: 'Q', 13: 'R', 10: 'S', 6: 'T', 3: 'U', 0: 'V'},
    'W': {171: 'A', 123: 'B', 101: 'C', 92: 'D', 84: 'E', 76: 'F', 69: 'G', 63: 'H', 57: 'I', 51: 'J', 46: 'K', 41: 'L',
          37: 'M', 32: 'N', 28: 'O', 24: 'P', 20: 'Q', 16: 'R', 13: 'S', 9: 'T', 6: 'U', 3: 'V', 0: 'W'},
    'X': {174: 'A', 126: 'B', 104: 'C', 95: 'D', 87: 'E', 79: 'F', 72: 'G', 66: 'H', 60: 'I', 54: 'J', 49: 'K', 44: 'L',
          40: 'M', 35: 'N', 31: 'O', 27: 'P', 23: 'Q', 19: 'R', 16: 'S', 12: 'T', 9: 'U', 6: 'V', 3: 'W', 0: 'X'},
    'Y': {177: 'A', 129: 'B', 107: 'C', 98: 'D', 90: 'E', 82: 'F', 75: 'G', 69: 'H', 63: 'I', 57: 'J', 52: 'K', 47: 'L',
          42: 'M', 38: 'N', 34: 'O', 30: 'P', 26: 'Q', 22: 'R', 19: 'S', 15: 'T', 12: 'U', 9: 'V', 6: 'W', 3: 'X',
          0: 'Y'},
    'Z': {180: 'A', 132: 'B', 110: 'C', 101: 'D', 92: 'E', 85: 'F', 78: 'G', 72: 'H', 66: 'I', 60: 'J', 55: 'K',
          50: 'L', 45: 'M', 41: 'N', 36: 'O', 32: 'P', 29: 'Q', 25: 'R', 21: 'S', 18: 'T', 15: 'U', 12: 'V', 9: 'W',
          6: 'X', 3: 'Y', 0: 'Z'}
}
corrected_time = {
    10: {'A': 10, 'B': 20, 'C': 26, 'D': 30, 'E': 34, 'F': 37, 'G': 41, 'H': 45, 'I': 50, 'J': 54, 'K': 59, 'L': 64,
         'M': 70, 'N': 75, 'O': 82, 'P': 88, 'Q': 95, 'R': 104, 'S': 112, 'T': 122, 'U': 133, 'V': 145, 'W': 160,
         'X': 178, 'Y': 199, 'Z': 219},
    12: {'A': 9, 'B': 17, 'C': 23, 'D': 26, 'E': 29, 'F': 32, 'G': 35, 'H': 38, 'I': 42, 'J': 45, 'K': 49, 'L': 53,
         'M': 57, 'N': 62, 'O': 66, 'P': 71, 'Q': 76, 'R': 82, 'S': 88, 'T': 94, 'U': 101, 'V': 108, 'W': 116, 'X': 125,
         'Y': 134, 'Z': 147},
    14: {'A': 8, 'B': 15, 'C': 19, 'D': 22, 'E': 24, 'F': 27, 'G': 29, 'H': 32, 'I': 35, 'J': 37, 'K': 40, 'L': 43,
         'M': 47, 'N': 50, 'O': 53, 'P': 57, 'Q': 61, 'R': 64, 'S': 68, 'T': 73, 'U': 77, 'V': 82, 'W': 87, 'X': 92,
         'Y': 98},
    16: {'A': 7, 'B': 13, 'C': 17, 'D': 19, 'E': 21, 'F': 23, 'G': 25, 'H': 27, 'I': 29, 'J': 32, 'K': 34, 'L': 37,
         'M': 39, 'N': 42, 'O': 45, 'P': 48, 'Q': 50, 'R': 53, 'S': 56, 'T': 60, 'U': 63, 'V': 67, 'W': 70, 'X': 72},
    18: {'A': 6, 'B': 11, 'C': 15, 'D': 16, 'E': 18, 'F': 20, 'G': 22, 'H': 24, 'I': 26, 'J': 28, 'K': 30, 'L': 32,
         'M': 34, 'N': 36, 'O': 39, 'P': 41, 'Q': 43, 'R': 46, 'S': 48, 'T': 51, 'U': 53, 'V': 55, 'W': 56},
    20: {'A': 6, 'B': 10, 'C': 13, 'D': 15, 'E': 16, 'F': 18, 'G': 20, 'H': 21, 'I': 23, 'J': 25, 'K': 26, 'L': 28,
         'M': 30, 'N': 32, 'O': 34, 'P': 36, 'Q': 38, 'R': 40, 'S': 42, 'T': 44, 'U': 45},
    22: {'A': 5, 'B': 9, 'C': 12, 'D': 13, 'E': 15, 'F': 16, 'G': 18, 'H': 19, 'I': 21, 'J': 22, 'K': 24, 'L': 25,
         'M': 27, 'N': 29, 'O': 30, 'P': 32, 'Q': 34, 'R': 36, 'S': 37},
    25: {'A': 4, 'B': 8, 'C': 10, 'D': 11, 'E': 13, 'F': 14, 'G': 15, 'H': 17, 'I': 18, 'J': 19, 'K': 21, 'L': 22,
         'M': 23, 'N': 25, 'O': 26, 'P': 28, 'Q': 29},
    30: {'A': 3, 'B': 6, 'C': 8, 'D': 9, 'E': 10, 'F': 11, 'G': 12, 'H': 13, 'I': 14, 'J': 15, 'K': 16, 'L': 17,
         'M': 19, 'N': 20},
    35: {'A': 3, 'B': 5, 'C': 7, 'D': 8, 'E': 9, 'F': 9, 'G': 10, 'H': 11, 'I': 12, 'J': 13, 'K': 14},
    40: {'A': 2, 'B': 5, 'C': 6, 'D': 7, 'E': 7, 'F': 8, 'G': 9},
    42: {'A': 1, 'B': 4, 'C': 6, 'D': 6, 'E': 7, 'F': 8}}
count = 1

while True:
    try:
        count_dives = int(input('Сколько планируется погружений? '))
        break
    except ValueError:
        continue

init()
depth_first = depth()
time_first = time(depth_first)
first_dive(depth_first, time_first)
