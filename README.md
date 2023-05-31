# Апи `olympic.nsu.ru`

Это небольшой _неофициальный_ модуль для работы с апи `NSUts`, полученый методом реверс инженеринга. Каждый метод задокументирован при помощи docstring, так что документация и все методы находится прямо в модуле

Вот небольшой пример использование (`example.py`)

```python
import asyncio
import pprint

from api import User, Langs

async def main():
    # Более приятный вывод словарей
    print = pprint.pprint
    
    # Создание и вход в аккаунт
    f,i,o='Иванов Иван Иванович'.split(' ')
    email, password = await User.register(f,i,o)
    cookie=await User.login(email, password)
    user = User(cookie)
    await user.logout()
    
    # Или 
    user = await User.create(f,i,o)

    # список олимпиад
    print(await user.list_olympiads())
    # зарегестрироваться на олимпиады
    print(await user.register_olympiad('201',f+i+o,'Новосибирск', 'ВКИ НГУ', '111a1', f,i,o))
    # "переключится" на олимпиаду (это особенность нсутса)
    await user.set_olympiad('201')
    # список туров в олимпиаде
    print(await user.list_tours())
    # "переключится" на тур (это особенность нсутса)
    await user.set_tour('11871')
    # отправить код
    print(await user.submit('121962', Langs.vcc2019, '''
                            #include <stdio.h>
                            int main() {
                                printf("Hello, nsuts!");
                            }'''))

    # выйти с аккаунта + закрыть сессию
    await user.logout()
    
# Асинхронный запуск
asyncio.run(main())
```

## ДИСКЛЕЙМЕР

Создано исключительно в образовательный целях, **ни в коем случае не пытайтесь дудосить или брутфорсить** `nsuts`

## Установка

* Скачиваем репозиторий
* Устанавливаем питон если ещё нет
* Уставливаем `aiohttp` для асинхронных запросов

    ```bash
    pip install aiohttp
    ```

* Запускаем

    ```bash
    python example.py
    ```

## Список всех методов

Подробное описание всех аргументов смотрите в докстрингах

* ```python
  User.submit(self, task: str, lang: str, code: str) -> dict
  ```

  Отправить код на проверку

* ```python
  User.get_rating(self) -> dict
  ```

  Получить общий рейтинг по туру

* ```python
  User.get_tour_report(self) -> dict
  ```

  Получить отчёт по туру

* ```python
  User.submit_info(self) -> dict
  ```

  Получить параметры тура по отправке

* ```python
  User.set_tour(self, tour: str) -> dict
  ```

  "Переключится" на тур (особенность нсутса)

* ```python
  User.list_tours(self) -> dict
  ```

  Список всех туров

* ```python
  User.get_data(self) -> dict
  ```

  Получить данные аккаунта

* ```python
  User.set_olympiad(self, olympiad: str)
  ```

  "Переключится" на олимпиаду (особенность нсутса)

* ```python
  User.register_olympiad(self, olympiad: str, team: str, city: str = None, school: str = None, group: str = None, surname: str = None, name: str = None, patronymic: str = None) -> str
  ```

  Зарегестирироваться на олимпиаду

* ```python
  User.list_olympiads(self) -> dict
  ```

  Список всех олимпиад

* ```python
  User.logout(self) -> dict
  ```

  Выйти из аккаунта и разорвать соединение

* ```python
  User.create(cls, surname: str, name: str, patronymic: str, email: str = None, password: str = None, email_sub='@mer.ci.nsu.ru') -> 'User'
  ```

  Создать аккаунт пользователя

* ```python
  User.register(cls, surname: str, name: str, patronymic: str, email: str = None, password: str = None, email_sub='@mer.ci.nsu.ru') -> tuple[str, str]
  ```

  Регистация пользователя

* ```python
  User.login(cls, email: str, password: str) -> str
  ```

  Вход в аккаунт
