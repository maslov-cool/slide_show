import os
import sys

import pygame
import requests




def main(geocode):
    server_address = 'http://geocode-maps.yandex.ru/1.x/?'
    api_key = '8013b162-6b42-4997-9691-77b7074026e0'
    # Готовим запрос.
    geocoder_request = f'{server_address}apikey={api_key}&geocode={geocode}&format=json'

    # Выполняем запрос.
    response = requests.get(geocoder_request)
    if response:
        # Преобразуем ответ в json-объект
        json_response = response.json()

        # Получаем первый топоним из ответа геокодера.
        # Согласно описанию ответа, он находится по следующему пути:
        toponym = json_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"]
        # Полный адрес топонима:
        toponym_address = toponym["metaDataProperty"]["GeocoderMetaData"]["text"]
        # Координаты центра топонима:
        toponym_coodrinates = toponym["Point"]["pos"].split()
        # Печатаем извлечённые из ответа поля:
        return toponym_coodrinates
    else:
        print("Ошибка выполнения запроса:")
        print(geocoder_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")


def main_2(place):
    server_address = 'https://static-maps.yandex.ru/v1?'
    api_key = 'a3c5d4c5-d812-4e23-b8d0-bbcd1ce66cc1'
    ll_spn = f'll={','.join(main(place))}&spn=0.402,0.402'

    # Готовим запрос.

    map_request = f"{server_address}{ll_spn}&apikey={api_key}"
    response = requests.get(map_request)

    if not response:
        print("Ошибка выполнения запроса:")
        print(map_request)
        print("Http статус:", response.status_code, "(", response.reason, ")")
        sys.exit(1)

    # Запишем полученное изображение в файл.
    map_file = "map.png"
    with open(map_file, "wb") as file:
        file.write(response.content)
    return map_file


A = [
    "Париж", "Рим", "Киото", "Нью-Йорк", "Стамбул",
    "Барселона", "Дубай", "Прага", "Сидней", "Рио-де-Жанейро",
    "Лондон", "Пекин", "Мачу-Пикчу", "Марракеш", "Кейптаун"
]
# Инициализируем pygame
pygame.init()
screen = pygame.display.set_mode((600, 450))
img = main_2(A[0])
# Рисуем картинку, загружаемую из только что созданного файла.
screen.blit(pygame.image.load(img), (0, 0))
# Переключаем экран и ждем закрытия окна.
pygame.display.flip()
c = 0
running = True
while running:
    # внутри игрового цикла ещё один цикл
    # приема и обработки сообщений
    for event in pygame.event.get():
        # при закрытии окна
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            print(1)
            c += 1
            if c == len(A):
                c = 0
            img = main_2(A[c])
            screen.fill('black')
            # Рисуем картинку, загружаемую из только что созданного файла.
            screen.blit(pygame.image.load(img), (0, 0))
            pygame.display.flip()
pygame.quit()

# Удаляем за собой файл с изображением.
os.remove(img)
