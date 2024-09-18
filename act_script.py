import re
import sys
import requests
import types
import time
from importlib.abc import PathEntryFinder
from importlib.util import spec_from_loader

def url_hook(some_str):
    if not some_str.startswith(("http", "https")):
        raise ImportError
    try:
        response1 = requests.get(some_str)
        response1.raise_for_status()
        names_data = response1.text
        # Найдем все директории на главной странице
        package_dirs = re.findall(r"href=\"([a-zA-Z_][a-zA-Z0-9_]*)/\"", names_data)
        names = set(package_dirs)

        packnames = []  # Список для хранения названий пакетов

        for package_dir in names:
            # Загружаем содержимое директории
            pack_url = f"{some_str}/{package_dir}/"
            response2 = requests.get(pack_url)
            response2.raise_for_status()
            pack_data = response2.text
            # Ищем __init__.py в директории
            pack_dir = re.findall(r"href=\"(__init__.py*)\"", pack_data)
            if pack_dir:  # Проверка, найдено ли __init__.py
                packnames.append(package_dir)  # Добавление имени пакета в список
                # Ищем модули в директории пакета
                module_list = re.findall(r"href=\"([a-zA-Z_][a-zA-Z0-9_]*\.py)\"", pack_data)
                modnames = {module[:-3] for module in module_list}  # Удаление .py
                return URLFinder(pack_url, modnames)
    except requests.exceptions.RequestException as e:
        print(f"Ошибка при запросе: {e}")
        return None


sys.path_hooks.append(url_hook)  # Добавляем url_hook в sys.path_hooks


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

    def create_module(self, spec):
        return types.ModuleType(spec.name)

    def exec_module(self, module):
        max_retries = 3
        retry_delay = 1
        for attempt in range(1, max_retries + 1):
            try:
                response = requests.get(self.url)
                response.raise_for_status()
                if response.status_code == 200:
                    source = response.text
                    code = compile(source, self.url, mode="exec")
                    exec(code, module.__dict__)
                    return
            except requests.exceptions.RequestException as e:
                print(f"Ошибка при загрузке модуля с URL {self.url}: {e}")
                print(f"Попытка {attempt} из {max_retries}.")
                if attempt < max_retries:
                    time.sleep(retry_delay)
                    retry_delay *= 2
                else:
                    print(f"Превышено количество попыток загрузки модуля.")


