# Лабораторная работа 1. Реализация удаленного импорта

Разместите представленный ниже код локально на компьютере и реализуйте механизм удаленного импорта. 
Продемонстрируйте в виде скринкаста или в текстовом отчете с несколькими скриншотами работу удаленного импорта.


1. Создание файла ```myremotemodule.py```, который будет импортироваться, в папке ```rootserver```, со следующим кодом:
```python
def myfoo():
    author = "Diana" 
    print(f"{author}'s module is imported")
```

2. Создание файла ```activation_script.py``` с содержимым функций ```url_hook``` и классов ```URLLoader```, ```URLFinder```


3. Запуск сервера http в каталоге ```rootserver``` с файлом ```myremotemodule.py``` 
```sh
python3 -m http.server
```


4. Запуск файла activation_script.py
```sh
python3 -i activation_script.py
```

5. При попытке импорта файла ```myremotemodule.py```, в котором размещена наша функция ```myfoo```, сейчас будет выведено ```ModuleNotFoundError: No module named 'myremotemodule'```


6. Выполнение кода, добавив путь, где располагается модуль, приведет к срабатыванию "кастомного" ```URLLoader```.
```python
sys.path.append("http://localhost:8000")
```

В ```path_hooks``` будет содержатся наша функция ```url_hook```. 



![image](https://github.com/user-attachments/assets/d14be88d-1faf-4bcf-85b9-a07c722fdf9a)
![image](https://github.com/user-attachments/assets/b49d2e01-ea16-49c8-873d-e88cbc53b7eb)
![image](https://github.com/user-attachments/assets/34793dce-7cb0-45c6-8bfd-85a720d2de6f)



8. Протестируйте работу удаленного импорта, используя в качестве источника модуля другие "хостинги" (например, gist, repl.it, heroku). 
9. Переписать содержимое функции url_hook, класса URLLoader с помощью модуля ```requests``` (см. комменты).
10. Задание со звездочкой (\*): реализовать обработку исключения в ситуации, когда хост (где лежит модуль) недоступен.
11. Задание про-уровня (\*\*\*): реализовать загрузку **пакета**, разобравшись с аргументами функции spec_from_loader и внутренним устройством импорта пакетов.





