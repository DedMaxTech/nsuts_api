import asyncio
import pprint

from nsuts import User, Langs

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