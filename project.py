# -*- coding: utf-8 -*-

import joblib  # to load models
import numpy as np  # operations with arrays
import json  # work with json requests and responses

import csv

# words of agreement
accept = ['да', 'конечно', 'точно', 'верно', 'согласен', 'естественно', 'правильно', 'ага', 'именно', 'правда']
accept

# words of disagreemnt
decline = ['не', 'нет', 'неверно', 'не верно', 'неправильно', 'не правильно', 'не точно', 'неточно', 'несогласен',
           'не согласен', 'неа', 'не правда', 'неправда', 'несогласен', 'не согласен']
decline

# all categories
сategories = [1, 2, 3, 66, 78, 89, 2201]

# all themes
themes = [1, 2, 3, 4, 5, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18,
          19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35,
          36, 37, 38, 39, 41, 42, 43, 44, 47, 49, 50, 52, 53, 59, 60, 61, 63,
          64]

# id: name of theme
translateT = {1: 'Нечитаемые/поврежденные дорожные знаки',
              11: 'Наличие опасно выступающих элементов над покрытиями (дорожными, тротуарными и т.д.), таких как арматура, бетонные блоки и т.п.',
              12: 'Ямы, выбоины, выступы на дороге, тротуаре',
              14: 'Подтопление проезжей части',
              15: 'Открытый (просевший) люк или ливневка на дороге',
              19: 'Реклама на тротуаре вдоль дорог',
              2: 'Противоречия при установке дорожных знаков / разметки / светофора, неправильно установленные дорожные знаки / разметка / светофор',
              21: 'Неисправность/недоступность инфраструктуры для маломобильных граждан / колясок на дорогах',
              22: 'Неисправное освещение на дорогах',
              23: 'Грязь, мусор, разрушение стен и покрытия в подземных и надземных пешеходных переходах',
              24: 'Мусор, свалки у обочин дорог, на тротуаре, газоне',
              3: 'Стертая дорожная разметка',
              32: 'Нескошенная трава вдоль тротуаров и обочин дорог',
              35: 'Некачественный уход за деревьями, кустарниками вдоль дорог, тротуаров (кронирование, вырубка сухостоев, ликвидация аварийных деревьев)',
              39: 'Неубранный снег, гололёд на проезжей части, тротуаре',
              41: 'Снеговые кучи на обочинах дорог, тротуаре',
              64: 'Брошенный разукомплектованный автомобиль на проезжей части',
              8: 'Неисправный светофор', 9: 'Повреждение дорожного ограждения',
              13: 'Ямы, выбоины, выступы на придомовой территории',
              16: 'Открытый (просевший) люк или ливневка во дворе',
              18: 'Реклама на тротуаре во дворах',
              20: 'Неисправность/недоступность инфраструктуры для маломобильных граждан / колясок во дворе',
              25: 'Мусор на придомовой территории',
              26: 'Нарушение графика вывоза мусора с контейнерной площадки',
              27: 'Несвоевременная уборка территории контейнерной площадки',
              30: 'Вытоптанный, заезженный газон',
              31: 'Нескошенная трава на придомовой территории',
              37: 'Некачественный уход за деревьями, кустарниками на придомовой территории (кронирование, вырубка сухостоев, ликвидация аварийных деревьев) во дворах',
              38: 'Брошенный разукомплектованный автомобиль на проезжей части, во дворе',
              42: 'Неубранный снег, гололед во дворе',
              43: 'Снег, сосульки на крыше дома',
              44: 'Снег, наледь на входных группах, перилах',
              5: 'Неисправное освещение во дворах',
              28: 'Скопление мусора в парках, скверах',
              33: 'Нескошенная трава вдоль пешеходных дорожек с твердым покрытием в парках',
              34: 'Ямы, выбоины, выступы на пешеходной дорожке, тротуаре',
              36: 'Некачественный уход за деревьями, кустарниками вдоль пешеходных дорожек, тротуаров (кронирование, вырубка сухостоев, ликвидация аварийных деревьев) в парках',
              47: 'Неубранный снег, наледь на пешеходных дорожках, тротуаре',
              6: 'Неисправное освещение в парках',
              17: 'Реклама на тротуаре',
              10: 'Повреждения остановочного павильона',
              29: 'Грязь, мусор на остановке',
              49: 'Неубранный снег, наледь на остановке',
              59: 'Неудовлетворительное санитарное состояние транспортного средства',
              60: 'Отказ водителей принимать банковские карты в качестве оплаты за проезд',
              61: 'Несоблюдение маршрута',
              63: 'Некорректное поведение водителя/кондуктора',
              4: 'Неисправное уличное освещение',
              50: 'Проблемы при получении социальной помощи на условиях заключения социального контракта',
              52: 'Проблемы при получении социальной помощи на оплату лечения, проживания и проезда к месту лечения',
              53: 'Проблемы при получении социальной помощи на устранение аварийных ситуаций и ремонт инженерных сетей жилого помещения'}
# id: name of categorie
translateC = {1: 'Дороги',
              2: 'Дворы',
              3: 'Парки и общественные территории',
              66: 'Рекламные конструкции',
              78: 'Общественный транспорт',
              89: 'Уличное освещение',
              2201: 'Социальная помощь'}

# id of theme: id of categorie
themeToCat = {1: 1,
              2: 1,
              3: 1,
              4: 89,
              5: 2,
              6: 3,
              8: 1,
              9: 1,
              10: 78,
              11: 1,
              12: 1,
              13: 2,
              14: 1,
              15: 1,
              16: 2,
              17: 66,
              18: 2,
              19: 1,
              20: 2,
              21: 1,
              22: 1,
              23: 1,
              24: 1,
              25: 2,
              26: 2,
              27: 2,
              28: 3,
              29: 78,
              30: 2,
              31: 2,
              32: 1,
              33: 3,
              34: 3,
              35: 1,
              36: 3,
              37: 2,
              38: 2,
              39: 1,
              41: 1,
              42: 2,
              43: 2,
              44: 2,
              47: 3,
              49: 78,
              50: 2201,
              52: 2201,
              53: 2201,
              59: 78,
              60: 78,
              61: 78,
              63: 78,
              64: 1}

# id of categorie: ids of themes
catToThemes = {
    1: [1, 11, 12, 14, 15, 19, 2, 21, 22, 23, 24, 3, 32, 35, 39, 41, 64, 8, 9],
    2: [13, 16, 18, 20, 25, 26, 27, 30, 31, 37, 38, 42, 43, 44, 5],
    3: [28, 33, 34, 36, 47, 6],
    66: [17],
    78: [10, 29, 49, 59, 60, 61, 63],
    89: [4],
    2201: [50, 52, 53]
}


def getCatOfTheme(theme):
    ''' returns id of categorie of theme '''
    return themeToCat[themes[theme]]


def getThemesOfCat(categorie):
    ''' returns ids of themes of categorie '''
    return catToThemes[сategories[categorie]]


def translateTheme(n):
    ''' returns translation of theme from id '''
    return translateT[themes[n]]


def translateCategorie(n):
    ''' returns translation of categorie from id '''
    return translateC[сategories[n]]


def askTheme(theme):
    ''' returns agreement or disagreement with statement about theme '''
    print(f"Вы подразумевали {translateTheme(theme)}?")
    ans = input()
    return not any(x in ans.lower() for x in decline)


def askCat(categorie):
    ''' returns agreement or disagreement with statement about theme '''
    print(f"Вы подразумевали категорию {translateCategorie(categorie)}?")
    ans = input()
    return not any(x in ans.lower() for x in decline)


def ask(txt):
    if any(x in txt[0].lower() for x in decline):
        return -1
    elif any(x in txt[0].lower() for x in accept):
        return 1
    else:
        return 0


def to_zeros(arr, cat):
    x = getThemesOfCat(cat)
    for i in range(len(arr[0])):
        if themes[i] not in x:
            arr[0][i] = 0


cat_model = joblib.load('./clfs/cat_clf')  # load classificator of categories
themes_model = joblib.load('./clfs/themes_clf')  # load classificator of themes

sessionStorage = {}


def call_process(request):
    # Начинаем формировать ответ, согласно документации
    # мы собираем словарь, который потом при помощи
    # библиотеки json преобразуем в JSON и отдадим Алисе
    response = {
        'session': request.json['session'],
        'version': request.json['version'],
        'response': {
            'end_session': False
        }
    }

    dialog(request.json, response)

    # Преобразовываем в JSON и возвращаем
    return json.dumps(response, ensure_ascii=False, indent=2)


def ask1(req, res, user_id):
    print("First asks")
    sessionStorage[user_id]['cats'] += 1
    if sessionStorage[user_id]['cats']-1 == 0:
        sessionStorage[user_id]['themes'] = themes_model.predict_proba(sessionStorage[user_id]['message'])
        sessionStorage[user_id]['categories'] = cat_model.predict_proba(sessionStorage[user_id]['message'])
        sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
        res['response']['text'] = f'Вы подразумевали {translateTheme(sessionStorage[user_id]["theme_max"])}?'

    elif sessionStorage[user_id]['cats']-1 == 1:
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = f'Принято:\nТема: {translateTheme(sessionStorage[user_id]["theme"])}\n Категория: {translateC[sessionStorage[user_id]["categorie"]]}'
            res['response']['end_session'] = True
        elif ask(sessionStorage[user_id]['message']) == -1:
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
            res['response'][
                'text'] = f'Вы подразумевали {translateTheme(sessionStorage[user_id]["theme_max"])}?'
            sessionStorage[user_id]['askcat'] = True

    else:
        sessionStorage[user_id]["noask"] = True
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = f'Принято:\nТема: {translateTheme(sessionStorage[user_id]["theme"])}\n Категория: {translateC[sessionStorage[user_id]["categorie"]]}'
            res['response']['end_session'] = True
        else:
            print("Reask message")
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            res['response']['text'] = f'Пожалуйста, повторите сообщение, указав больше важной информации'
            sessionStorage[user_id]['cats'] += 1



def reask(req, res, user_id):
    print('Reasking...')
    sessionStorage[user_id]["reask_msg"] = False
    if sessionStorage[user_id]['cats'] == 0:
        sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
        res['response']['text'] = f'Вы подразумевали {translateTheme(sessionStorage[user_id]["theme_max"])}?'
        sessionStorage[user_id]['cats'] += 1

    elif sessionStorage[user_id]['cats'] == 1:
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = f'Принято:\nТема: {translateTheme(sessionStorage[user_id]["theme"])}\n Категория: {translateC[sessionStorage[user_id]["categorie"]]}'
            res['response']['end_session'] = True
        elif ask(sessionStorage[user_id]['message']) == -1:
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
            res['response'][
                'text'] = f'Вы подразумевали категорию {translateTheme(sessionStorage[user_id]["theme_max"])}?'
            sessionStorage[user_id]['cats'] += 1
            sessionStorage[user_id]['askcat'] = True
            sessionStorage[user_id]['reask'] = False

    else:
        if ask(sessionStorage[user_id]['message']) == 1:
            sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
            sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
            res['response'][
                'text'] = f'Принято:\nТема: {translateTheme(sessionStorage[user_id]["theme"])}\n Категория: {translateC[sessionStorage[user_id]["categorie"]]}'
            res['response']['end_session'] = True
        elif ask(sessionStorage[user_id]['message']) == -1:
            sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
            sessionStorage[user_id]['cat_max'] = np.argmax(sessionStorage[user_id]['categories'], axis=1)[0]
            res['response'][
                'text'] = f'В таком случае, Вы подразумевали категорию {translateCategorie(sessionStorage[user_id]["cat_max"])}?'
            sessionStorage[user_id]['cats'] += 1000
            sessionStorage[user_id]['askcat'] = True
            sessionStorage[user_id]['reask'] = False


def askcat(req, res, user_id):
    print("Asking cat...")
    print(sessionStorage[user_id]["categories"][0])
    if ask(sessionStorage[user_id]['message']) == 1:
        res['response']['text'] = f'Принято\nВы подразумевали {translateTheme(sessionStorage[user_id]["theme_max"])}'
        sessionStorage[user_id]["categorie"] = sessionStorage[user_id]["cat_max"]
        sessionStorage[user_id]['askcat'] = False
        sessionStorage[user_id]['asktheme'] = True
        to_zeros(sessionStorage[user_id]["themes"], sessionStorage[user_id]["categorie"])
        print(sessionStorage[user_id]["themes"])
    else:
        if not sessionStorage[user_id]['categories'].any():
            res['response']['text'] = 'К сожалению не удалось распознать категорию сообщения'
            res['response']['end_session'] = True
            return
        sessionStorage[user_id]['categories'][0][sessionStorage[user_id]['cat_max']] = 0
        sessionStorage[user_id]['cat_max'] = np.argmax(sessionStorage[user_id]['categories'], axis=1)[0]
        print(sessionStorage[user_id])
        res['response'][
            'text'] = f'В таком случае, Вы подразумевали категорию {translateCategorie(sessionStorage[user_id]["cat_max"])}?'


def askTheme(req, res, user_id):
    print("Asking themes...")
    print(sessionStorage[user_id]["themes"])
    if sessionStorage[user_id]['new']:
        sessionStorage[user_id]["theme_max"] = np.argmax(sessionStorage[user_id]["themes"])
        sessionStorage[user_id]['new'] = False
    if ask(sessionStorage[user_id]['message']) == 1:
        sessionStorage[user_id]['theme'] = sessionStorage[user_id]['theme_max']
        sessionStorage[user_id]['categorie'] = getCatOfTheme(sessionStorage[user_id]['theme'])
        res['response'][
            'text'] = f'Принято:\nТема: {translateTheme(sessionStorage[user_id]["theme"])}\n Категория: {translateC[sessionStorage[user_id]["categorie"]]}'
        res['response']['end_session'] = True
    else:
        if not sessionStorage[user_id]['themes'].any():
            res['response']['text'] = 'К сожалению не удалось распознать ntve сообщения'
            res['response']['end_session'] = True
            return
        sessionStorage[user_id]['themes'][0][sessionStorage[user_id]['theme_max']] = 0
        sessionStorage[user_id]['theme_max'] = np.argmax(sessionStorage[user_id]['themes'], axis=1)[0]
        res['response'][
            'text'] = f'В таком случае, Вы подразумевали {translateTheme(sessionStorage[user_id]["theme_max"])}?'


def dialog(req, res):
    user_id = req['session']['user_id']
    if req['session']['new']:
        # Это новый пользователь.
        # Инициализируем сессию и поприветствуем его.
        sessionStorage[user_id] = {
            'theme_max': -1,
            'cat_max': -1,
            'noask': False,
            'message': '',
            'address': '',
            'theme': '',
            'categorie': '',
            'cats': 0,
            'reask': False,
            'themes': np.array([]),
            'categories': np.array([]),
            'askcat': False,
            'asktheme': False,
            'new': True,
        }
        # Заполняем текст ответа
        print("New user")
        res['response']['text'] = 'Здравствуйте! Пожалуйста, расскажите, что произошло'
        return

    sessionStorage[user_id]['message'] = [req['request']['original_utterance']]

    if not sessionStorage[user_id]["noask"]:
        ask1(req, res, user_id)

    elif sessionStorage[user_id]['reask']:
        reask(req, res, user_id)
        return

    elif sessionStorage[user_id]['askcat']:
        askcat(req, res, user_id)
        return

    elif sessionStorage[user_id]['asktheme']:
        askTheme(req, res, user_id)
        return


    '''else:
        f_name = '/content/drive/MyDrive/Data/dataset.csv'
        with open(f_name, mode='a') as csvfile:
            writer = csv.writer(csvfile, delimiter=';',
                                quotechar='"', quoting=csv.QUOTE_MINIMAL)
        # print([сategories[cat], translateCategorie(cat), themes[theme], translateTheme(theme), message])
        writer.writerow(
            [sessionStorage[user_id]['categorie'], translateCategorie(cat), themes[theme], translateTheme(theme),
             message])'''


'''else:
        if check_address(req):
            sessionStorage[user_id]['address'] = req['request']['original_utterance']
            # создать вызов
            call = Call()
            call.message = sessionStorage[user_id]['message']
            call.address = sessionStorage[user_id]['address']
            try:
                call.recognize_call()
            except:
                res['response']['text'] = f'Пожалуйста, уточните адрес. Возможно вы ошиблись или не указали полное название населенного пункта'
            else:
                db_sess = db_session.create_session()
                db_sess.add(call)
                db_sess.commit()
                res['response']['text'] = f'Вызов принят. К Вам отправилась {SERVICES[call.service]} по адресу: {call.address}'
                res['response']['end_session'] = True
        else:
            res['response']['text'] = f'Пожалуйста, уточните адрес. Возможно вы ошиблись или не указали полное название населенного пункта'''