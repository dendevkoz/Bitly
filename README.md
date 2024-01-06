# Обрезка ссылок с помощью Битли
Данное приложение сокращает ссылки и ведет подсчет переходов по коротким ссылкам.

## Функция main
Эта функция определяет что нужно сделать с введенной ссылкой.
Внутри функции происходит проверка: 1) если введенная ссылка является длинной, то запускается функция для сокращения, 
2) если ссылка короткая, то функция выводит колличество переходов по этой ссылке.


### Функция shorten_link
Функция возвращает сокращенную переданную ссылку.
>Пример вывода функции shorten_link (рисунок 1).
+ ![Screenshot_1](https://github.com/dendevkoz/Bitly/blob/main/screenshot/Screenshot_1.png)


### Функция count_clicks
Функция возвращает колличество переходов по сокращенной ссылке.
>Пример вывода функции count_clicks (рисунок 2).
+ ![Screenshot_2](https://github.com/dendevkoz/Bitly/blob/main/screenshot/Screenshot_2.png)


### Функция is_bitlink
Функция проверяет является ли переданная ссылка сокращенной.


## Как установить
### Пакет python-dotenv
Для того что бы ваши ключи были защищены, вым понадобится небольшой пакет python-dotenv.
>Установка и использование пакета python-dotenv (рисунок 3).
+ ![Screenshot_3](https://github.com/dendevkoz/Bitly/blob/main/screenshot/Screenshot_3.png)

Он считывает пары ключ-значение из файла .env, и загружает необходимые вашему приложению переменные среды.
>Пример файла .env (рисунок 4).
+ ![Screenshot_4](https://github.com/dendevkoz/Bitly/blob/main/screenshot/Screenshot_4.png)

### Файл requirements.txt
В данном файле прописаны библиотеки и их версии, которые понадобятся для работы программы.
Python3 должен быть уже установлен. 
Затем используйте `pip` (или `pip3`, есть конфликт с Python2) для установки зависимостей:
```
pip install -r requirements.txt
```
### Как использовать

```python
import requests
import os
from dotenv import load_dotenv
import argparse


def shorten_link(long_url, headers):
    url = "https://api-ssl.bitly.com/v4/bitlinks"
    payload = {"long_url": long_url}
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    bitlink = response.json()["id"]
    return bitlink


def count_clicks(bitlink, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{bitlink}/clicks/summary"
    response = requests.get(url, headers=headers)
    response.raise_for_status()
    clicks_count = response.json()["total_clicks"]
    return clicks_count


def is_bitlink(user_url, headers):
    url = f"https://api-ssl.bitly.com/v4/bitlinks/{user_url}"
    response = requests.get(url, headers=headers)
    return response.ok


def main(user_url):
    load_dotenv()
    headers = {"Authorization": f"Bearer {os.environ['BITLY_KEY']}"}
    if is_bitlink(user_url, headers):
        try:
            print("По вашей ссылке прошли", count_clicks(user_url, headers), "раз(а)")
        except requests.exceptions.HTTPError:
            print("Введена некорректная сокращенная ссылка")
    else:
        try:
            print("Битлинк", shorten_link(user_url, headers))
        except requests.exceptions.HTTPError:
            print("Введена неверная ссылка")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("user_url", type=str, help="The program works with this site")
    args = parser.parse_args()
    main(args.user_url)

```

>Пример файла .env (рисунок 4).
+ ![Screenshot_4](https://github.com/dendevkoz/Bitly/blob/main/screenshot/Screenshot_5.png)


### Цель проекта

Код написан в образовательных целях на онлайн-курсе для веб-разработчиков [dvmn.org](https://dvmn.org/).
