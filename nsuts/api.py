import aiohttp
import json, io
from .utils import translit

ENDPONT='https://olympic.nsu.ru/nsuts-new/api/'

headers={'Accept': ' application/json, text/plain, */*',
         'Cookie': None}

class LoginFailedException(Exception):
    pass

class Langs:
    mingw8_1c='mingw8.1c'
    mingw8_1cpp='mingw8.1cpp'
    vc2015='vc2015'
    vcc2015='vcc2015'
    vcc2019='vcc2019'
    sharp2019='sharp2019'

class User:
    def __init__(self, cookie:str):
        """Создаёт пользователя

        Args:
            cookie (str): Куки аутентификации, берётся из `User.login()`
        """        
        self.session = aiohttp.ClientSession(
            headers={'Accept': ' application/json, text/plain, */*', 'Cookie': cookie},
            timeout=aiohttp.ClientTimeout(total=100000000))


    async def submit(self, task:str, lang:str, code:str) -> dict:
        """Отправить код на проверку

        Args:
            task (str): Id задачи
            lang (str): код компилятора, можно взять из класса `Langs`
            code (str): сам код

        Returns:
            dict: ответ сервера, пример ответа:
            >>> {'error': 'Вы отправили копию предыдущего решения', 'tip': '', 'url': ''}
        """        
        f = io.BytesIO(bytes(code, encoding='utf-8'))
        f.name='file.txt'
        async with self.session.post(ENDPONT+'submit/do_submit', data={'langId': lang, 'taskId': task, 'sourceText':'', 'sourceFile':f}) as response:
            return json.loads(await response.text())

    async def get_rating(self) -> dict:
        """Получить общий рейтинг по туру

        Returns:
            dict: Ответ сервера
            >>> {'tours': [{'id': '11559', 'title': 'Тренировочный тур', 'isOpened': '1', 'position': '11558', 'tourModel': '1'}]}
        """        
        async with self.session.post(ENDPONT+'rating/rating?showFrozen=0', json={"selectedAttributes":[]}) as response:
            return await response.json()

    async def get_tour_report(self) -> dict:
        """Получить отчёт по туру

        Returns:
            _type_: Ответ сервера
            >>> {'display_time_and_memory': '0', 'model_code': 1, 'submits': [
            >>>    {'compiler': 'Visual C++ 2019','date': '2023-05-31 17:42:37', 'id': '943010', 'points': None, 'result_line': None, 'status': '1', 'taskModel': 'ICPC', 'task_id': '121962', 'task_title': '4. COVID-19: Карантин', 'testNumber': None, 'total': None}
            >>> ]}
        """  
        async with self.session.get(ENDPONT+'report/get_report') as response:
            return await response.json()

    async def submit_info(self) -> dict:
        """Получить параметры тура по отправке

        Returns:
            dict: Ответ сервера
            >>> {'elapsedTime': 21912, 'isEnabled': 1, 'isInfinite': 1, 'queueModel': 0,
            >>> 'langs': [{'id': 'mingw8.1c', 'title': 'MinGW64 C 8.1'}], 'submitLimits': [{'submitsLeft': 50, 'submitsTotal': 50, 'taskId': 121961}],
            >>> 'tasks': [{'id': '121961', 'title': '1. Шлю я за пакетом пакет...'}], 'tourTime': -28070250}
        """        
        async with self.session.get(ENDPONT+'submit/submit_info') as response:
            return await response.json()

    async def set_tour(self, tour:str) -> dict:
        """"Переключится" на тур (особенность нсутса)

        Args:
            tour (str): Id тура

        Returns:
            dict: Ответ сервера
            >>> {"entered":true}
        """        
        async with self.session.get(ENDPONT+'tours/enter', params={"tour": tour}) as response:
            return await response.text()

    async def list_tours(self) -> dict:
        """Список всех туров

        Returns:
            dict: Ответ сервера
            >>> {'tours': [{'id': '11559', 'title': 'Тренировочный тур', 'isOpened': '1', 'position': '11558', 'tourModel': '1'}]}
        """        
        async with self.session.get(ENDPONT+'tours/list',) as response:
            return await response.json()

    async def get_data(self) -> dict:
        """Получить данные аккаунта

        Returns:
            dict: Ответ сервера
            >>> {'user': {'id': 52653, 'email': 'emain@mail.ru', 'surname': 'fam', 'name': 'name', 'patronymic': 'sur', 'permissions': {'p_dev': '0'}}, 'olympiad': None, 'tour': None}
        """        
        async with self.session.get(ENDPONT+'common/system_data') as response:
            return await response.json()

    async def set_olympiad(self, olympiad:str):
        """"Переключится" на олимпиаду (особенность нсутса)

        Args:
            olympiad (str): Id тура

        Returns:
            str: Строка ошибки
        """  
        async with self.session.post(ENDPONT+'olympiads/enter', json={"olympiad": olympiad}) as response:
            return await response.text()

    async def register_olympiad(self, olympiad:str,team:str, city:str=None, school:str=None,group:str=None,surname:str=None,name:str=None,patronymic:str=None) -> str:
        """Зарегестирироваться на олимпиаду

        Args:
            olympiad (str): Id олимпиады
            team (str): Название команды
            city (str, optional): Город, рекомендуется существующий. Defaults to None.
            school (str, optional): Учебное заведение. Defaults to None.
            group (str, optional): Группа. Defaults to None.
            surname (str, optional): Фамилия. Defaults to None.
            name (str, optional): Имя. Defaults to None.
            patronymic (str, optional): Отчество. Defaults to None.

        Returns:
            str: Строка ошибки
        """        
        data={"olympiad": olympiad, "values": {"_usertitle": team, }, "invite": None}
        if city: data["values"]["_1"]=city
        if school: data["values"]["_2"]=school
        if group: data["values"]["_9"]=group
        if surname: data["values"]["_27"]=surname
        if name: data["values"]["_28"]=name
        if patronymic: data["values"]["_29"]=patronymic

        async with self.session.post(ENDPONT+'olympiads/register', json=data) as response:
            return await response.text()

    async def list_olympiads(self) -> dict:
        """Список всех олимпиад

        Returns:
            dict: Ответ сервера
            >>> {'registeredTo': [], 'canRegisterTo': [{'id': '201', 'title': 'ВКИ', 'teams': '621', 'tours': '25', 'cover_url': '/nsuts-new/nsuts_img/covers/olympiad.png', 'hasInvite': False}]}
        """        
        async with self.session.get(ENDPONT+'olympiads/list') as response:
            return await response.json()

    async def logout(self) -> dict:
        """Выйти из аккаунта и разорвать соединение

        Returns:
            dict: Ответ сервера
        """        
        async with self.session.post(ENDPONT+'logout') as response:
            data= await response.json()
        await self.session.close()
        return data

    @classmethod
    async def create(cls,surname:str,name:str,patronymic:str,email:str=None,password:str=None, email_sub='@mer.ci.nsu.ru') -> 'User':
        """Создать аккаунт пользователя
        Если аккаунт уже существует ничего не произойдёт
        
        Cокращение от
        >>> email, password = await User.register(f,i,o)
        >>> cookie=await User.login(email, password)
        >>> user = User(cookie)

        Args:
            surname (str): Фамилия
            name (str): Имя
            patronymic (str): Отчество
            email (str, optional): Имейл, если не задан, сгенериутся из ФИО
            password (str, optional): Пароль, если не задан, сгенериутся из ФИО
            email_sub (str, optional): Окончание автоматической почты. Defaults to '@mer.ci.nsu.ru'.

        Returns:
            User: аккаунт пользователя
        """        
        e,p = await cls.register(surname,name,patronymic,email,password, email_sub)
        cookie = await cls.login(e,p)
        return cls(cookie)

    @classmethod
    async def register(cls,surname:str,name:str,patronymic:str,email:str=None,password:str=None, email_sub='@mer.ci.nsu.ru') -> tuple[str,str]:
        """Регистация пользователя

        Args:
            surname (str): Фамилия
            name (str): Имя
            patronymic (str): Отчество
            email (str, optional): Имейл, если не задан, сгенериутся из ФИО
            password (str, optional): Пароль, если не задан, сгенериутся из ФИО
            email_sub (str, optional): Окончание автоматической почты. Defaults to '@mer.ci.nsu.ru'.

        Returns:
            tuple[str,str]: кортеж (имейл, пароль)
        """        
        login = translit(surname.lower() + name.lower()[0] + patronymic.lower()[0])
        if email is None: email=login+email_sub
        if password is None: password=login

        async with aiohttp.ClientSession() as session:
            async with session.post(ENDPONT+'register',
                    json={"email":email,"surname":surname,"name":name,"patronymic":patronymic,"password":password}) as response:
                return email,password

    @classmethod
    async def login(cls,email:str, password:str) -> str:
        """Вход в аккаунт

        Args:
            email (str): Имейл
            password (str): Пароль

        Raises:
            LoginFailedException: Если неправильный логин/пароль

        Returns:
            str: куки аутентификации
        """        
        async with aiohttp.ClientSession() as session:
            async with session.post(ENDPONT+'login',
                    json={"email":email,"password":password,"method":"internal"}) as response:
                if not response.headers.get('Set-Cookie'): raise LoginFailedException('Неверный логин или пароль')
                return response.headers['Set-Cookie'].split(';')[0]

