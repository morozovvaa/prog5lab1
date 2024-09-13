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
python -m http.server
```


4. Запуск файла activation_script.py
```sh
python -i activation_script.py
```

5. При попытке импорта файла ```myremotemodule.py```, в котором размещена наша функция ```myfoo```, сейчас будет выведено ```ModuleNotFoundError: No module named 'myremotemodule'```


6. Выполнение кода, добавив путь, где располагается модуль, приведет к срабатыванию "кастомного" ```URLLoader```.
```python
sys.path.append("http://localhost:8000")
```
![image](https://github.com/user-attachments/assets/5e393f1f-e02d-4670-8ff9-cf50f153d212)

![image](https://github.com/user-attachments/assets/2cc5f107-4ba6-4c5b-b16e-853922b530b5)




В ```path_hooks``` будет содержатся наша функция ```url_hook```. 

![image](https://github.com/user-attachments/assets/34793dce-7cb0-45c6-8bfd-85a720d2de6f)  


7. Вывод программы, при попытке импортировать модуль, если сервер не запущен
![image](https://github.com/user-attachments/assets/e60ba692-a058-4a68-b5a6-6dd1d8d1587a)


Запуск сервера
![image](https://github.com/user-attachments/assets/d14be88d-1faf-4bcf-85b9-a07c722fdf9a)  


![image](https://github.com/user-attachments/assets/68dba27f-04dd-4894-b844-cfe718d6e3b8)  

![image](https://github.com/user-attachments/assets/32c61473-65d8-4584-a03a-a49b83922143)  




8. Протестируйте работу удаленного импорта, используя в качестве источника модуля другие "хостинги" (например, gist, repl.it, heroku).


12. Задание про-уровня (\*\*\*): реализовать загрузку **пакета**, разобравшись с аргументами функции spec_from_loader и внутренним устройством импорта пакетов.





