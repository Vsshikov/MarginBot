import parser
import telebot
import os
import json
import random

bot = telebot.TeleBot('985195843:AAF0W6UHkNXPGpYv0oVQH0BuwzlcX2o5AkY')

keyboard_number = telebot.types.ReplyKeyboardMarkup(row_width= 5)
keyboard_number.add('1')
keyboard_number.add('2')
keyboard_number.add('3')
keyboard_number.add('4')
keyboard_number.add('5')
keyboard_number.add('6')
keyboard_number.add('7')
keyboard_number.add('8')
keyboard_number.add('9')
keyboard_number.add('10')

def giveslashmarkup(roundstate):
    keyboard = telebot.types.ReplyKeyboardMarkup()
    for i, market in enumerate(roundstate['markets']):
        keyboard.add('/' + str(i + 1))
    return keyboard


def defiftrue(reverse_chance):
    chance = 1/reverse_chance
    random_outcome = random.random()
    if random_outcome <= chance:
        return True
    else:
        return False


def startup(reverse_chance, win, loss):
    if defiftrue(reverse_chance):
        return win
    else:
        return loss


def strlist(intlist):
    str_list = []
    for i, item in enumerate(intlist):
        str_list.append(str(item))
    return str_list


# Функция для смены типа работы
# возможные аргументы = setup, main_menu, game
def setmode(mode):
    with open('EventLog.json', 'r') as event_file:
        event_data = json.load(event_file)
    if mode == 'main_menu':
        event_data['is_main_menu'] = True
        event_data['is_setup'] = False
        event_data['is_game'] = False
    elif mode == 'setup':
        event_data['is_main_menu'] = False
        event_data['is_setup'] = True
        event_data['is_game'] = False
    elif mode == 'game':
        event_data['is_main_menu'] = False
        event_data['is_setup'] = False
        event_data['is_game'] = True
    with open('EventLog.json', 'w') as event_file:
        json.dump(event_data, event_file)


# Проверяет, соответствует ли аттрибут в json-файле указанному значению
def checkjson(filename, attribute_name, attribute_value):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data[attribute_name] == attribute_value


# Возвращает значение указанного атрибута json-файла
def getjson(filename, attribute_name):
    with open(filename, 'r') as file:
        data = json.load(file)
        return data[attribute_name]


# Меняет указанный аттрибут json-файла на указанное значение
def setjson(filename, attribute_name, attribute_value):
    with open(filename, 'r') as file:
        data = json.load(file)
    data[attribute_name] = attribute_value
    with open(filename, 'w') as file:
        json.dump(data, file, indent=4)


# Проверяет, является ли содержание сообщения telegram типом integer
def message_isint(message):
    try:
        int(message.text)
        return True
    except ValueError:
        return False


# Проверяет, является ли содержание сообщения telegram типом float или с типом int
def message_isfloat(message):
    try:
        float(message.text)
        return True
    except ValueError:
        return False


# Проверяет, подходит ли текст сообщения для названия команды
def message_isroundtype(message):
    if type(message) == str:
        if (message.text.lower == 'вложения') or (message.text.lower == 'квиз'):
            return True
        else:
            return False


# Увеличивает значение аттрибута JSON-файла на 1
def iterjson(filename, attribute_name, step=1):
    setjson(filename, attribute_name, getjson(filename, attribute_name) + step)


# Меняет аттрибут в Settings.json
def modsettings(attribute_name, attribute_value):
    setjson('Settings.json', attribute_name, attribute_value)


# Меняет указанный bool атрибут из EventLog у EventLog.json на противоположный
def modlog(attribute_name, *args):
    if len(args) == 0:
        if getjson('EventLog.json', attribute_name):
            setjson('EventLog.json', attribute_name, False)
        else:
            setjson('EventLog.json', attribute_name, True)
    else:
        setjson('EventLog.json', attribute_name, args[0])


# Возвращает указанный аттрибут из EventLog.json
def getlog(attribute_name):
    return getjson('EventLog.json', attribute_name)


# Возвращает указанный аттрибут из Settings.json
def getsettings(attribute_name):
    return getjson('Settings.json', attribute_name)


# ФУНКЦИИ ДЛЯ СБРОСА
#   EVENTLOG
def resetlog():
    exec(open('EventLogReset.py').read())


@bot.message_handler(commands=['resetlog'])
def handle_resetlog(message):
    resetlog()
    bot.send_message(message.chat.id, 'Лог успешно сброшен')


#   SETTINGS
def resetsettings():
    exec(open('SettingsReset.py').read())


def givemarketdata():
    with open('Markets.json', 'r') as roundfile:
        markets = json.load(roundfile)
        string = ''
        for i, market in enumerate(markets):
            string += ('/' + str(i + 1) + ' ')
            string += market['name']
            string += '\n'
            string += '    Уравнение:\n    '
            string += market['coef_tip']
            string += '\n    Настроенные константы:'
            for const in market['nums']:
                if const['show']:
                    string += '\n    - '
                    string += const['vname']
                    string += const['comment']
            string += '\n'
        return string


def givecurrentmarkets():
    marketlist = getlog('current_markets_list')
    string = ''
    for i, market in enumerate(marketlist):
        string += ('/' + str(i + 1) + ' ')
        string += market['name']
        string += '\n'
        string += '    Уравнение:\n    '
        string += market['coef_tip']
        string += '\n    Настроенные константы:'
        for const in market['nums']:
            if const['show']:
                string += '\n    - '
                string += const['vname']
                string += ' = '
                string += str(const['value'])
                string += const['comment']
        string += '\n'
    return string


def givecurrentroundstate():
    state = getlog('current_round_state')
    list = state['markets']
    string = ''
    for i, market in enumerate(list):
        string += (str(i + 1) + ') ')
        string += market['name']
        string += '\n'
        string += '    Уравнение:\n    '
        string += market['coef_tip']
        string += '\n    Настроенные константы:'
        for const in market['nums']:
            if const['show']:
                string += '\n    - '
                string += const['vname']
                string += ' = '
                string += str(const['value'])
                string += const['comment']
        string += '\n'
    return string


def message_islashint(message):
    try:
        value = int(message.text[1:])
        return True
    except ValueError:
        return False


def processmarket(market, pos_in_roundstate):
    # ВЫЧИСЛЕНИЕ ЗНАЧЕНИЙ ПЕРЕМЕННЫХ
    current_game_team_list = getlog('current_game_team_list')
    for num in market['nums']:
        # ДОБАВЛЕНИЕ В ПРОГРАММУ УЖЕ ЗАРАНЕЕ УКАЗАННЫХ КОНСТАНТ
        if num['type'] == 'const':
            exec(num['vname'] + '=' + str(num['value']))
        # ВЫЧИСЛЕНИЕ КОНСТАНТЫ, ЕСЛИ ЭТО КОЛИЧЕСТВО КОМАНД В ЭТОМ РЫНКЕ
        if num['type'] == 'teams_in_market':
            exec(num['vname'] + '= 0')
            for team in current_game_team_list:
                for active in team['actives']:
                    if active['current_actmarket'] == pos_in_roundstate:
                        exec(num['vname'] + '+= 1')
    # ВЫЧИСЛЕНИЕ КОЭФФИЦИЕНТОВ
    coef = eval(market['coef_evaluation'])
    print(coef)
    # УМНОЖЕНИЕ АКТИВОВ НА КОЭФФИЦИЕНТЫ
    for i, team in enumerate(current_game_team_list):
        for j, active in enumerate(team['actives']):
            if active['current_actmarket'] == pos_in_roundstate:
                current_game_team_list[i]['actives'][j]['actvalue'] *= coef
    # МОДИФИКАЦИЯ РАБОЧЕГО СПИСКА КОМАНД (СПИСОК КОМАНД В НАСТРОЙКАХ ПРИ ЭТОМ НЕ МЕНЯЕТСЯ
    modlog('current_game_team_list', current_game_team_list)


def processroundstart(round, message):
    markup = giveslashmarkup(round)
    if round['type'] == 'quiz':
        modlog('pending_nextround', True)
        modlog('is_quiz_gameplay', True)
        bot.send_message(message.chat.id, 'Начинаю раунд ' + str(getlog('current_game_round_num') + 1) + ', в этом '
                                                                                                         'раунде вы '
                                                                                                         'можете '
                                                                                                         'самостоятельно '
                                                                                                         'ввести '
                                                                                                         'коэффициенты '
                                                                                                         'для умножения '
                                                                                                         'активов команд.\n'
                                                                                                         'Для вывода списка команд введите /showteamlist\n'
                                                                                                         'Чтобы умножить активы команды на какое-либо число, введите команду с её номером (например /1)\n'
                                                                                                         'Чтобы закончить раунд, введите /finishround')
    if round['type'] == 'invest':
        modlog('invest_gameplay', True)
        current_game_markets_list = getsettings('rounds')[getlog('current_game_round_num')]['markets']
        modlog('current_game_markets_list', current_game_markets_list)
        bot.send_message(message.chat.id, 'Начинаю раунд '
                         + str(getlog('current_game_round_num') + 1)
                         + ', сейчас вам нужно будет ввести, куда каждая команда вкладывает свои активы\n'
                           'Я по очереди буду указывать все активы команд. '
                           'Для указания рынка, в который пойдёт актив, потребуется ввести число с номером рынка в раунде\n'
                           'Для вывода списка доступных в этом раунде рынков введите /showroundmarkets')
        bot.send_message(message.chat.id, 'Команда '
                         + getsettings('teams')[getlog('current_game_team_num')]['teamname']
                         + ', актив #'
                         + str(getlog('current_game_act_num') + 1)
                         + ', '
                         + str(
            getsettings('teams')[getlog('current_game_team_num')]['actives'][getlog('current_game_act_num')][
                'actvalue'])
                         + ' рублей', reply_markup=markup)




# РАБОТАЕМ НАД КОМАНДАМИ ДЛЯ БОТА
# СТРУКТУРА ОБРАБОТКИ КОМАНДЫ:
#   В ДЕКОРАТОРЕ - САМА КОМАНДА
#   ВНУТРИ ФУНКЦИИ - ПРОВЕРКА ОБСТОЯТЕЛЬСТВ (АТТРИБУТОВ В ФАЙЛАХ EventLog.json, MarketReset.py.json, Teams.json)
#   ДЕЙСТВИЯ ФУНКЦИЙ - В ЗАВИСИМОСТИ ОТ ОБСТОЯТЕЛЬСТВ
@bot.message_handler(commands=['start'])
def start(message):
    print(type(message))
    # Если бот ещё не включён
    if checkjson('EventLog.json', 'is_online', False):
        # системная часть
        # переводим EventLog в активированное состояние
        with open('EventLog.json', 'r') as event_file:
            event_log = json.load(event_file)
            event_log['is_online'] = True
        with open('EventLog.json', 'w') as event_file:
            json.dump(event_log, event_file)
        setmode('main_menu')
        bot.send_message(message.chat.id, 'Добро пожаловать! '
                                          'Я - бот-ассистент, который будет помогать вам вести игру.')
        bot.send_message(message.chat.id, 'Для настройки бота введите /setup \n'
                                          'Для сброса настроек бота введите /reset (если что-то идёт не так, '
                                          'лучше жать сюда)\n '
                                          'Для начала игры с выбранными настройками введите /startgame (в разработке)\n'
                                          'Для вывода в чат списка команд и их активов введите /showteamlist', )
    # Если бот уже включён
    else:
        bot.send_message(message.chat.id, 'Бот уже работает, для возвращения в главное меню введите /mainmenu')


@bot.message_handler(commands=['reset'])
def reset(message):
    resetlog()
    resetsettings()
    bot.send_message(message.chat.id, 'Настройки успешно сброшены, для повторного запуска бота введите /start')


@bot.message_handler(commands=['showteamlist'])
def showteamlist(message):
    string = 'Список команд с их активами:\n'
    for i, team in enumerate(getsettings('teams')):
        string += '/'
        string += str(i + 1)
        string += ' '
        string += team['teamname']
        string += '\nАктивы команды:\n'
        for active in team['actives']:
            string += '    '
            string += str(active['actvalue'])
            string += '\n'
    bot.send_message(message.chat.id, string)


@bot.message_handler(commands=['setup'])
def setup(message):
    setjson('EventLog.json', 'is_setup', True)
    bot.send_message(message.chat.id, 'Перехожу в режим настройки')
    bot.send_message(message.chat.id, 'Что нужно настроить? \n'
                                      '/fullsetup для полной пошаговой настройки игры \n'
                                      '/roundsetup для перехода в режим настройки отдельного раунда (coming soon)\n'
                                      '/marketsetup для настройки библиотеки рынков (coming soon)\n'
                                      '/teamsetup для выбора и настройки команд (coming soon)\n'
                                      '/mainmenu для выхода из режима настройки и перехода в главное меню')


@bot.message_handler(commands=['fullsetup'])
def fullsetupstart(message):
    if checkjson('EventLog.json', 'is_setup', True):
        if checkjson('EventLog.json', 'is_fullsetup', False):
            setjson('EventLog.json', 'is_fullsetup', True)
            setjson('EventLog.json', 'is_fullsetup_roundnum', True)
            bot.send_message(message.chat.id, 'Перехожу в режим полной настройки')
            bot.send_message(message.chat.id, 'Сколько раундов будет в игре?', reply_markup=keyboard_number)


# КОМАНДА ДЛЯ ДОБАВЛЕНИЯ НОВОГО РЫНК
@bot.message_handler(commands=['addmarket'])
def add_market(message):
    if getlog('is_fullsetup_marketslist'):
        modlog('is_fullsetup_marketslist', False)
        modlog('is_fullsetup_addmarket', True)
        bot.send_message(message.chat.id, 'Чтобы вывести список известных боту рынков в чат введите /showallmarkets\n'
                                          'Чтобы выбрать рынок для дальнейшей настройки введите команду с его номером '
                                          'в списке или просто щелкните на его номер.')


@bot.message_handler(commands=['showallmarkets'])
def showallmarkets(message):
    bot.send_message(message.chat.id, 'Полный список знакомых боту рынков: \n' + givemarketdata())


@bot.message_handler(commands=['finishmarkets'])
def finishmarkets(message):
    modlog('is_fullsetup_roundtype', True)
    bot.send_message(message.chat.id, 'Сохраняю настройки раунда.')
    rounds = getsettings('rounds')
    rounds[getlog('current_round_setup_num')] = getlog('current_round_state')
    modsettings('rounds', rounds)
    iterjson('EventLog.json', 'current_round_setup_num')
    if getlog('current_round_setup_num') < getsettings('total_round_num'):
        modlog('is_fullsetup_addmarket', False)
        modlog('is_fullsetup_marketslist', False)
        modlog('is_fullsetup_roundtype', True)
        available_round_types = telebot.types.ReplyKeyboardMarkup(True, True)
        available_round_types.add('Вложения')
        available_round_types.add('Квиз')
        bot.send_message(message.chat.id, 'Перехожу к настройке ' + str(getlog('current_round_setup_num') + 1) + '-го раунда, выберите его тип.', reply_markup=available_round_types)
        print(getlog('is_fullsetup_roundtype'))
        setjson('EventLog.json', 'is_fullsetup_roundtype', True)
        print(getlog('is_fullsetup_roundtype'))
        return
    else:
        modlog('is_fullsetup_roundtype', False)
        modlog('is_fullsetup_marketlist', False)
        modlog('is_fullsetup_actnum', True)
        bot.send_message(message.chat.id, 'Перехожу к настройкам команд и активов.\nСколько активов будет в распоряжении у команд?')
        return


@bot.message_handler(commands=['showroundslist'])
def showroundslist(message):
    string = 'Список раундов на игру:\n'
    for i, round in enumerate(getsettings('rounds')):
        string += str(i + 1)
        string += ') Тип раунда - '
        string += round['type']
        string += '\n'
        if round['type'] == 'invest':
            string += '    Используемые рынки:\n'
            for j, market in enumerate(round['markets']):
                string += '    '
                string += str(j + 1)
                string += ') Название рынка - '
                string += market['name']
                string += '\n         Способ вычисления константы:\n'
                string += market['coef_tip']
                string += '\n         Где:\n'
                for num in market['nums']:
                    if num['show']:
                        string += '          - '
                        string += str(num['vname'])
                        string += ' = '
                        string += str(num['value'])
                        string += num['comment']
                        string += '\n'
    bot.send_message(message.chat.id, string)


@bot.message_handler(commands=['showroundmarkets'])
def showroundmarkets(message):
    if getlog('invest_gameplay'):
        markets = getsettings('rounds')[getlog('current_game_round_num')]['markets']
        string = ''
        for i, market in enumerate(markets):
            string += ('/' + str(i + 1) + ' ')
            string += market['name']
            string += '\n'
            string += '    Уравнение:\n    '
            string += market['coef_tip']
            string += '\n    Настроенные константы:'
            for const in market['nums']:
                if const['show']:
                    string += '\n    - '
                    string += const['vname']
                    string += const['comment']
            string += '\n'
        bot.send_message(message.chat.id, 'Список настроенных для раунда рынков:\n' + string)


@bot.message_handler(commands=['startgame'])
def startgame(message):
    bot.send_message(message.chat.id, 'LET THE GAME BEGIN!')
    resetlog()
    modlog('is_online', True)
    modlog('is_game', True)
    modlog('current_game_round_num', 0)
    modlog('current_game_team_num', 0)
    modlog('current_game_act_num', 0)
    modlog('current_game_team_list', getsettings('teams'))
    round = getsettings('rounds')[getlog('current_game_round_num')]
    processroundstart(round, message)


@bot.message_handler(commands=['countcoefs'])
def countcoefs(message):
    if getlog('pending_countcoefs'):
        modlog('pending_countcoefs')
        rounds = getsettings('rounds')
        markets = rounds[getlog('current_game_round_num')]['markets']
        for i, market in enumerate(markets):
            processmarket(market, i)
        string = 'Список команд с их активами после подсчёта:\n'
        for i, team in enumerate(getlog('current_game_team_list')):
            string += str(i + 1)
            string += ') '
            string += team['teamname']
            string += '\nАктивы команды:\n'
            for active in team['actives']:
                string += '    '
                string += str(active['actvalue'])
                string += '\n'
        bot.send_message(message.chat.id, string)
        if getlog('current_game_round_num') < getsettings('total_round_num'):
            modlog('pending_nextround', True)
            bot.send_message(message.chat.id, 'Для того, чтобы сохранить изменения активов команд и перейти к следующему раунду, введите /nextround')
        else:
            bot.send_message(message.chat.id, 'Для того, чтобы перейти к окончательным результатам игры, введите /finish')


@bot.message_handler(commands=['nextround'])
def nextround(message):
    if getlog('pending_nextround'):
        modlog('pending_nextround')
        modsettings('teams', getlog('current_game_team_list'))
        modlog('current_game_team_num', 0)
        modlog('current_game_act_num', 0)
        modlog('is_quiz_gameplay', False)
        modlog('invest_gameplay', False)
        modlog('current_game_team_list', getsettings('teams'))
        iterjson('EventLog.json', 'current_game_round_num')
        round = getsettings('rounds')[getlog('current_game_round_num')]
        processroundstart(round, message)


@bot.message_handler(commands=['finish'])
def finish(message):
    modsettings('teams', getlog('current_game_team_list'))
    bot.send_message(message.chat.id, 'ИГРА ОКОНЧЕНА, А ЭТО PLACEHOLDER-СООБЩЕНИЕ. КОМАНДА /showteamlist ВСЁ ЕЩЁ РАБОТАЕТ.\nДл начала новой игры с указанными настройками введите'
                                      '/resetlog, a затем /startgame (work in progress)')


# ОБРАБОТКА СООБЩЕНИЯ С ЧИСЛОМ
# ПРИМЕНЕНИЕ:
#   УСТАНОВКА КОЛИЧЕСТВА РАУНДОВ
#   УСТАНОВКА ТИПА РАУНДА
#   УСТАНОВКА КОНСТАНТ
#   УСТАНОВКА КОЛИЧЕСТВА КОМАНД
#   УСТАНОВКА КОЛИЧЕСТВА АКТИВОВ
@bot.message_handler(func=message_isfloat)
def nummessageresponce(message):
    if getjson('EventLog.json', 'is_fullsetup_teamname'):
        return ()

    # ОБРАБОТКА ЧИСЛА ПРИ НАСТРОЙКЕ КОЛИЧЕСТВА РАУНДОВ
    elif checkjson('EventLog.json', 'is_fullsetup_roundnum', True):
        setjson('Settings.json', 'total_round_num', int(message.text))
        if checkjson('EventLog.json', 'is_fullsetup_roundnum', True):
            setjson('EventLog.json', 'is_fullsetup_roundnum', False)
            setjson('EventLog.json', 'is_fullsetup_roundtype', True)
            setjson('EventLog.json', 'current_round_setup_num', 0)
            setjson('EventLog.json', 'current_const_setup-num', 0)
            rounds = []
            for i in range(int(message.text)):
                round = dict(type='', markets=[])
                rounds.append(round)
            modsettings('rounds', rounds)
            bot.send_message(message.chat.id, 'Количество раундов установлено (' + message.text + ')')
            available_round_types = telebot.types.ReplyKeyboardMarkup(True, True)
            available_round_types.add('Вложения')
            available_round_types.add('Квиз')
            bot.send_message(message.chat.id, 'Выберите тип 1-го раунда', reply_markup=available_round_types)
            return ()

    # ОБРАБОТКА ЧИСЛА ПРИ НАСТРОЙКЕ КОНСТАНТЫ
    elif getlog('is_fullsetup_consts'):
        market = getlog('current_market_state')
        market['nums'][getlog('current_const_setup_num')]['value'] = float(message.text)
        modlog('current_market_state', market)
        bot.send_message(message.chat.id,
                         'Константа ' + market['nums'][getlog('current_const_setup_num')]['vname'] + ' настроена.')
        while True:
            iterjson('EventLog.json', 'current_const_setup_num')
            if getlog('current_const_setup_num') >= len(market['nums']):
                break
            if market['nums'][getlog('current_const_setup_num')]['is_settable']:
                break

        # ЕСЛИ НАСТРОЙКА КОНСТАНТ ОКОНЧЕНА, ПЕРЕХОДИМ В МЕНЮ ДОБАВЛЕНИЯ РЫНКОВ
        if getlog('current_const_setup_num') >= len(market['nums']):
            modlog('current_const_setup_num', 0)
            modlog('is_fullsetup_consts')
            modlog('is_fullsetup_marketslist', True)
            marketlist = getlog('current_markets_list')
            marketlist.append(market)
            modlog('current_markets_list', marketlist)
            roundstate = getlog('current_round_state')
            roundmarkets = roundstate['markets']
            roundmarkets.append(market)
            roundstate['markets'] = roundmarkets
            modlog('current_round_state', roundstate)
            bot.send_message(message.chat.id, 'Состояние раунда на данный момент:\n' + givecurrentroundstate())
            bot.send_message(message.chat.id, 'Список настроенных пресетов рынков:\n' + givecurrentmarkets())
            bot.send_message(message.chat.id,
                             'Для для добавления в раунд уже настроенного рынка из списка введите команду с номером '
                             'требуемого рынка, \n '
                             'Для настройки нового рынка введите /addmarket, \n'
                             'Если вы хотите использовать все рынки из этого списка в данном раунде, введите '
                             '/useallmarkets '
                             'Для завершения добавления рынков и сохранения настроек для этого раунда введите '
                             '/finishmarkets')

        else:
            bot.send_message(message.chat.id,
                             'Введите значение для константы ' + market['nums'][getlog('current_const_setup_num')][
                                 'vname'])

    # ОБРАБОТКА ЧИСЛА ПРИ НАСТРОЙКЕ ЧИСЛА АКТИВОВ
    elif getlog('is_fullsetup_actnum'):
        modsettings('total_actives_num', int(message.text))
        modlog('is_fullsetup_actnum')
        modlog('is_fullsetup_teamnum', True)
        bot.send_message(message.chat.id, 'Количество активов настроено')
        bot.send_message(message.chat.id, 'Введите количество команд')
        return

    # ОБРАБОТКА ЧИСЛА ПРИ НАСТРОЙКЕ ЧИСЛА КОМАНД
    elif getlog('is_fullsetup_teamnum'):
        modsettings('total_team_num', int(message.text))
        modlog('is_fullsetup_teamnum')
        modlog('is_fullsetup_teamname', True)
        for i in range(int(message.text)):
            teamlist = getsettings('teams')
            teamlist.append(dict(teamname='', actives=[]))
            for j in range(getsettings('total_actives_num')):
                teamlist[i]['actives'].append(dict(actvalue=10000, current_actmarket=None))
            modsettings('teams', teamlist)
        bot.send_message(message.chat.id, 'Число команд установлено')
        bot.send_message(message.chat.id, 'Введите название 1 команды:')


    elif getlog('is_quiz_coef'):
        modlog('is_quiz_coef')
        teams = getlog('current_game_team_list')
        for i, act in enumerate(teams[getlog('chosen_team_num')]['actives']):
            teams[getlog('chosen_team_num')]['actives'][i]['actvalue'] *= float(message.text)
        modlog('current_game_team_list', teams)
        string = 'Список команд с их активами после подсчёта:\n'
        for i, team in enumerate(getlog('current_game_team_list')):
            string += str(i + 1)
            string += ') '
            string += team['teamname']
            string += '\nАктивы команды:\n'
            for active in team['actives']:
                string += '    '
                string += str(active['actvalue'])
                string += '\n'
        bot.send_message(message.chat.id, string)
        bot.send_message(message.chat.id, 'Чтобы продолжить раунд с квизом введите номер команды из списка для умножения её активов.\n'
                                          'Чтобы перейти к следующему раунду и сохранить изменения, введите /nextround')


# ДОБАВЛЕНИЕ ПУНКТА ИЗ РАНЕЕ ВЫВЕДЕННОГО СПИСКА
@bot.message_handler(func=message_islashint)
def slashint(message):
    value = int(message.text[1:])

    # ВЫБОР РЫНКА ИЗ ПРЕСЕТА
    if getlog('is_fullsetup_marketslist'):
        current_round_state = getlog('current_round_state')
        current_market_list = getlog('current_markets_list')
        current_round_state['markets'].append(current_market_list[value - 1])
        modlog('current_round_state', current_round_state)
        bot.send_message(message.chat.id, 'Рынок добавлен')
        return

    # ВЫБОР РЫНКА ПРИ НАСТРОЙКЕ С НУЛЯ
    elif getlog('is_fullsetup_addmarket'):
        with open('Markets.json', 'r') as marketsfile:
            chosenmarket = json.load(marketsfile)[(value - 1)]
        modlog('current_market_state', chosenmarket)
        modlog('is_fullsetup_addmarket')
        bot.send_message(message.chat.id, 'Выбран рынок ' + getlog('current_market_state')['name'])
        settable_const_list = []
        for const in getlog('current_market_state')['nums']:
            if const['is_settable']:
                settable_const_list.append(const)
        modlog('settable_const_list', settable_const_list)
        if len(settable_const_list) == 0:
            modlog('is_fullsetup_marketslist', True)
            bot.send_message(message.chat.id, 'В рынке нет настраиваемых констант, перехожу обратно к настройке раунда')
            bot.send_message(message.chat.id, 'Состояние раунда на данный момент:\n' + givecurrentroundstate())
            bot.send_message(message.chat.id, 'Список настроенных пресетов рынков:\n' + givecurrentmarkets())
            bot.send_message(message.chat.id,
                             'Для для добавления в раунд уже настроенного рынка из списка введите команду с номером '
                             'требуемого рынка, \n '
                             'Для настройки нового рынка введите /addmarket, \n'
                             'Если вы хотите использовать все рынки из этого списка в данном раунде, введите '
                             '/useallmarkets '
                             'Для завершения добавления рынков и сохранения настроек для этого раунда введите '
                             '/finishmarkets')
            return
        else:
            modlog('is_fullsetup_consts')
            bot.send_message(message.chat.id, 'Выбран рынок ' + chosenmarket[
                'name'] + '\nДля продолжения введите константы этого рынка. Если требуется ввести десятичную дробь, '
                          'нужно вводить через точку.')
            for i, const in enumerate(chosenmarket['nums']):
                if const['is_settable']:
                    bot.send_message(message.chat.id, const['vname'] + const['comment'] + ':')
                    modlog('current_const_setup_num', i)
                    break


    elif getlog('invest_gameplay'):
        teamlist = getlog('current_game_team_list')
        teamlist[getlog('current_game_team_num')]['actives'][getlog('current_game_act_num')]['current_actmarket'] = value - 1
        modlog('current_game_team_list', teamlist)
        iterjson('EventLog.json', 'current_game_act_num')
        round = getsettings('rounds')[getlog('current_game_round_num')]
        markup = giveslashmarkup(round)
        if getlog('current_game_act_num') < getsettings('total_actives_num'):
            bot.send_message(message.chat.id, 'Команда '
                             + getsettings('teams')[getlog('current_game_team_num')]['teamname']
                             + ', актив #'
                             + str(getlog('current_game_act_num') + 1)
                             + ', '
                             + str(getsettings('teams')[getlog('current_game_team_num')]['actives'][getlog('current_game_act_num')]['actvalue'])
                             + ' рублей', reply_markup=markup)
        else:
            iterjson('EventLog.json', 'current_game_team_num')
            if getlog('current_game_team_num') < getsettings('total_team_num'):
                modlog('current_game_act_num', 0)
                bot.send_message(message.chat.id, 'Команда '
                                 + getsettings('teams')[getlog('current_game_team_num')]['teamname']
                                 + ', актив #'
                                 + str(getlog('current_game_act_num') + 1)
                                 + ', '
                                 + str(getsettings('teams')[getlog('current_game_team_num')]['actives'][getlog('current_game_act_num')]['actvalue'])
                                 + ' рублей', reply_markup=markup)
            else:
                modlog('current_game_act_num', 0)
                modlog('current_game_team_num', 0)
                modlog('invest_gameplay', False)
                modlog('pending_countcoefs', True)
                bot.send_message(message.chat.id, 'Всем активам присвоены рынки. Введите /countcoefs для вычисления коэффициентов и вывода нового списка команд и активов')

    elif getlog('is_quiz_gameplay'):
        modlog('chosen_team_num', value - 1)
        modlog('is_quiz_coef')
        bot.send_message(message.chat.id, 'Теперь введите коэффициент для умножения на него активов команды. Дробные числа вводите через точку.')






# ОБРАБОТКА СООБЩЕНЦИЙ С ТЕКСТОМ
@bot.message_handler(content_types=['text'])
def handleteamnames(message):
    # ОБРАБОТКА ТЕКСТА ПРИ ВВОДЕ НАЗВАНИЯ КОМАНДЫ
    if getlog('is_fullsetup_teamname'):
        teams = getsettings('teams')
        teams[getlog('current_team_setup_num')]['teamname'] = message.text
        modsettings('teams', teams)
        iterjson('EventLog.json', 'current_team_setup_num')
        if getlog('current_team_setup_num') >= getsettings('total_team_num'):
            modlog('is_fullsetup_teamname')
            modlog('is_fullsetup')
            modlog('is_setup')
            modlog('is_main_menu')
            bot.send_message(message.chat.id,
                             'Название получено. \n Полная настройка завершена, возвращаюсь в главное меню')
            bot.send_message(message.chat.id, 'Для настройки бота введите /setup \n'
                                              'Для сброса настроек бота введите /reset (если что-то идёт не так, '
                                              'лучше жать сюда)\n '
                                              'Для начала игры с выбранными настройками введите /startgame (в '
                                              'разработке)\n '
                                              'Для вывода в чат списка команд и их активов введите /showteamlist', )
            return
        bot.send_message(message.chat.id, 'Название получено')
        bot.send_message(message.chat.id,
                         'Введите название ' + str(getlog('current_team_setup_num') + 1) + '-й команды: ')
        return

    # НАСТРОЙКА ТИПА РАУНДА
    elif getlog('is_fullsetup_roundtype') and (message.text.lower() == 'квиз' or message.text.lower() == 'вложения'):
        bot.send_message(message.chat.id, 'Тип раунда настроен')
        rounds = getsettings('rounds')
        if message.text.lower() == 'квиз':
            rounds[getlog('current_round_setup_num')]['type'] = 'quiz'
            modsettings('rounds', rounds)
            iterjson('EventLog.json', 'current_round_setup_num')
            modlog('is_fullsetup_roundtype')
            if getlog('current_round_setup_num') >= getsettings('total_round_num'):
                modlog('is_fullsetup_teams', True)
                modlog('is_fullsetup_actnum', True)
                modlog('current_round_setup_num', 0)
                bot.send_message(message.chat.id, 'Раунды настроены, перехожу к настройке команд')
                bot.send_message(message.chat.id, 'Сколько активов будет в распоряжении у команд?')
                return
            modlog('is_fullsetup_roundtype', True)
            available_round_types = telebot.types.ReplyKeyboardMarkup(True, True)
            available_round_types.add('Вложения')
            available_round_types.add('Квиз')
            bot.send_message(message.chat.id,
                             'Коэффициенты для умножения активов команд можно будет вручную ввести в ходе игры'
                             'Перехожу к настройке следующего раунда')
            bot.send_message(message.chat.id,
                             'Введите тип ' + str(getlog('current_round_setup_num') + 1) + '-го раунда.',
                             reply_markup=available_round_types)
        elif message.text.lower() == 'вложения':
            rounds[getlog('current_round_setup_num')]['type'] = 'invest'
            modlog('current_round_state', rounds[getlog('current_round_setup_num')])
            modlog('is_fullsetup_roundtype', False)
            if len(getlog('current_markets_list')) == 0:
                modlog('is_fullsetup_marketslist', True)
                bot.send_message(message.chat.id,
                                 'Список настроенных рынков пуст. Для добавления пресета рынка используйте команду '
                                 '/addmarket')
            else:
                modlog('is_fullsetup_marketslist', True)
                bot.send_message(message.chat.id, 'Список настроенных пресетов рынков:\n' + givecurrentmarkets())
                bot.send_message(message.chat.id,
                                 'Для для добавления в раунд уже настроенного рынка из списка введите команду с '
                                 'номером требуемого рынка, \n '
                                 'Для настройки нового рынка введите /addmarket, \n'
                                 'Если вы хотите использовать все рынки из этого списка в данном раунде, введите '
                                 '/useallmarkets '
                                 'Для завершения добавления рынков и сохранения настроек для этого раунда введите '
                                 '/finishmarkets')






bot.polling()
