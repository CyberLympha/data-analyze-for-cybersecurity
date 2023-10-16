class Employee:
    '''Базовый класс для работы с сотрудниками'''
    __AGE_LIMITS = 75

    def __new__(cls, *args, **kwargs):
        """ 
        При создании объекта класса должен проверяться возраст 
        объекта, если возраст не проходит - класс не создается
        (создание класса происходит только тогда, когда __new__
        возвращает ссылку на объект класса)
        """
        
        age = args[3]
        salary = kwargs.get('salary', 1)

        if type(salary) not in [int, float] or salary < 0:
            print('Некорректное значение ЗП, объект не создан')  
            return
        
        if type(age) != int or age > 120 or age < 18:
            print('Некорректное значение возраста, объект не создан')  
            return
        
        return super().__new__(cls)

    def __init__(
            self, name, surname, 
            position, age, 
            salary=50000, currency='rub'
            ):
        """
        инициализатор класса.
        __атрибут - приватный атрибут
        _атрибут - защищенный атрибут
        атрибут - публичный атрибут
        """
                
        self.name = name
        self.surname = surname
        self.position = position
        self.__age = age
        self.__salary = salary
        self.__currency = currency

        if not self._is_meeting_standards(age):
            print("Возраст сотрудника не удовлетворяет корп.стандартам")

    # ниже прописаны сеттеры и геттеры для атрибутов класса,
    # которые позволяют управлять доступом для них.

    @property
    def age(self):
        return self.__age
    
    @age.setter
    def age(self, new_age):
        if not self._is_meeting_standards(new_age):
            print('Не удовл. стандартам')  

        if type(new_age) == int and 18 <= new_age < 120:
            self.__age = new_age
        else:
            print('Некорректное значение возраста')  

    @property
    def salary(self):
        return self.__salary
    
    @salary.setter
    def salary(self, value):
        if type(value) not in [int, float] or value < 0:
            print('Некорректное значение ЗП')  
            return
        self.__salary = value

    @property
    def currency(self):
        return self.__currency

    @staticmethod
    def convert_currency(value,
                         cur_currency,
                         req_currency):   
        """_
        А это статический метод, у него нет доступа к атрибутам объекта и 
        класса, зато он может работать как калькулятор валют
        """
        exchange_rate = {
            'rub': 1,
            'usd': 90,
            'eur': 100
        }

        # Пересчет курса валют
        rate = (exchange_rate[cur_currency] /
                exchange_rate[req_currency])
        
        return value * rate

    def change_currency(self, currency_new):

        if self.currency != currency_new:
            try:
                # обработчик мы написали, чтобы отлавливать
                # случаи, в которых у нас нет данных о курсе
                # валюты, в которую мы переводим
                self.salary = self.convert_currency(
                    self.salary,
                    self.currency,
                    currency_new
                )
                self.__currency = currency_new

            except KeyError:
                print('Недопустимое имя валют(ы)')

    @classmethod
    def _is_meeting_standards(cls, age):
        """
        Это метод класса, т.к. нам нужен доступ к атрибуту класса __AGE_LIMITS
        """
        return age < cls.__AGE_LIMITS
    
    def __str__(self):
        """
        Магический метод для реализации функции str()
        применительно к объекту класса
        """
        return f"{self.name} {self.surname}"
    
    def __eq__(self, other):
        """
        Магический метод для сравнения объектов класса
        """
        if not isinstance(other, Employee):
            return False

        return (
                self.name == other.name and
                self.surname == other.surname and
                self.age == other.age and
                self.position == other.position
            )
    
    def __call__(self):
        """
        Магический метод, который определяет поведение класса при
        обращении к нему как к функции, через ()
        """
        print(f"Сотрудник {self.name} уже бежит к вам")

    

class Engineer(Employee):
    __AGE_LIMITS = 65

    def __init__(self, *args, **kwargs):
        # Мы никак не меняем аргументы при инициализации,
        # но нам нужно создать атрибут manager, поэтому нам
        # нужен инициализатор, поэтому мы должны добавить 
        # вызов вышестоящего инициализатора с пробросом
        # всех параметров
        super().__init__(*args, **kwargs)

        self.manager = None

    @classmethod
    def _is_meeting_standards(cls, age):
        # нам нужно переопределить метод, чтобы он работал 
        # с атрибутом класса Engineer
        return age < cls.__AGE_LIMITS
    
    def give_premium(self):
        premium = self.salary * 0.1
        print(f"{self.position} {self.name} {self.surname} получил премию в размере {premium} {self.currency}")

        return premium
    

class Manager(Employee):

    def __init__(self, *args, salary=70000, **kwargs):
        super().__init__(*args, salary, **kwargs)
        self.engineers = list()

    def add_engineer(self, engineer):
        if engineer not in self.engineers:
            self.engineers.append(engineer)
            engineer.manager = self

    def give_premium(self):
        premium = sum([engineer.salary for engineer in self.engineers]) * 0.08
        print(f"{self.position} {self.name} {self.surname} получил премию в размере {premium} {self.currency}")
        return sum([engineer.salary for engineer in self.engineers]) * 0.15

    def change_salary(self, new_salary, currency=None):
        old_salary = self.salary
        self.salary = new_salary

        if currency is not None and currency != self.currency:
            old_salary = self.convert_currency(
                old_salary, self.currency, currency)
            self.currency = currency

        if (new_salary - old_salary) / old_salary > 0.5:
            print("Подозрение на коррупционные схемы!")