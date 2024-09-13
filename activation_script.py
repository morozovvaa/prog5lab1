import re
import sys
import requests
import types
import time

def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError
    try:
        response = requests.get(some_str)
        response.raise_for_status()
        data = response.text
        filenames = re.findall("[a-zA-Z_][a-zA-Z0-9_]*.py", data)
        modnames = {name[:-3] for name in filenames}
        return URLFinder(some_str, modnames)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при загрузке модуля с URL {some_str}: {e}")
        return None

sys.path_hooks.append(url_hook)  # Добавляем url_hook в sys.path_hooks

from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader


class URLFinder(PathEntryFinder):
    def __init__(self, url, available):
        self.url = url
        self.available = available

    def find_spec(self, name, target=None):
        if name in self.available:
            origin = "{}/{}.py".format(self.url, name)
            loader = URLLoader(origin)  # Передаем URL-адрес в URLLoader
            return spec_from_loader(name, loader, origin=origin)

        else:
            return None


class URLLoader:
    def __init__(self, url):
        self.url = url

    def create_module(self, spec):  # Добавляем метод create_module
        return types.ModuleType(spec.name)  # Создаем новый модуль

    def exec_module(self, module):
        max_retries = 3  # Максимальное количество попыток
        retry_delay = 1  # Начальная задержка
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(self.url)
                response.raise_for_status()
                source = response.text
                code = compile(source, self.url, mode="exec")
                exec(code, module.__dict__)
                return  # Успешная загрузка, выходим из цикла
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при загрузке модуля с URL {self.url}: {e}")
                print(f"Попытка {attempt} из {max_retries}.")
                if attempt < max_retries:
                    time.sleep(retry_delay)  # Экспоненциальная задержка
                    retry_delay *= 2  # Удваиваем задержку для следующей попытки
                else:
                    print(f"Превышено количество попыток загрузки модуля.")
