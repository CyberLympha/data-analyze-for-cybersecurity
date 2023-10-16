import my_module as mm
import pytest

name = 'Ivan'
surname = 'Ivanov'
position = 'engineer'
age = 35

def test_create_employee():
    employee = mm.Employee(name, surname, position, age)

    assert employee.name == name
    assert employee.surname == surname
    assert employee.position == position
    assert employee.age == age

    assert employee.salary == 50000
    assert employee.currency == 'rub'

    employee = mm.Employee(name, surname, position, age, currency='usd', salary=100)
    assert employee.salary == 100
    assert employee.currency == 'usd'

def test_employee_attributes():
    employee = mm.Employee(name, surname, position, age)

    assert getattr(employee, "_Employee__salary") == 50000
    assert getattr(employee, "_Employee__age") == age
    assert getattr(employee, "_Employee__currency") == 'rub'


# @pytest.mark.xfail(raises=AttributeError)
# def test_employee_write_attributes():
#     employee = mm.Employee(name, surname, position, age)

#     assert getattr(employee, "_Employee__salary") == 50000
#     assert getattr(employee, "_Employee__age") == age


#     assert employee.salary == 10
#     assert employee.currency == 10

def test_convert_currency():
    employee = mm.Employee(name, surname, position, age)

    assert employee.convert_currency(90, 'rub', 'usd') == 1
    assert employee.convert_currency(1, 'rub', 'rub') == 1

def test_change_currency():
    employee = mm.Employee(name, surname, position, age, salary=90000)
    employee.change_currency('usd')
    
    assert employee.salary == employee.convert_currency(90000, 'rub', 'usd')

    employee.change_currency('usddd')

    assert employee.salary == employee.convert_currency(90000, 'rub', 'usd')

def test_age():
    assert getattr(mm.Employee, '_Employee__AGE_LIMITS') == 75

    employee = mm.Employee(name, surname, position, 70)
    assert employee._is_meeting_standards(70) == True

    employee = mm.Employee(name, surname, position, 80)
    assert employee._is_meeting_standards(80) == False

    employee = mm.Employee(name, surname, position, 130)
    assert employee is None

    employee = mm.Employee(name, surname, position, 10)
    assert employee is None

    employee = mm.Employee(name, surname, position, 30.0)
    assert employee is None

    employee = mm.Employee(name, surname, position, 30)
    employee.age = 120
    assert employee.age == 30

def test_salary():
    employee = mm.Employee(name, surname, position, 30, salary=90)
    assert employee.salary == 90

    employee = mm.Employee(name, surname, position, 30, salary=-90)
    assert employee is None

def test_eq():
    employee1 = mm.Employee(name, surname, position, 30, salary=100)
    employee2 = mm.Employee(name, surname, position, 30, salary=90)

    assert employee1 == employee2

    employee2 = mm.Employee(name, surname, position, 31, salary=90)
    assert employee1 != employee2

    assert employee1 != 10


def test_manager():
    manager = mm.Manager(name, surname, position, age)
    assert manager.salary == 70000

    engineer = mm.Engineer(name, surname, position, age)

    manager.add_engineer(engineer)

    assert engineer in manager.engineers

def test_engineer():
    engineer = mm.Engineer(name, surname, position, 80)
    assert engineer._is_meeting_standards(80) == False

    engineer = mm.Engineer(name, surname, position, 70)
    assert engineer._is_meeting_standards(70) == False

    engineer = mm.Engineer(name, surname, position, 60)
    assert engineer._is_meeting_standards(60) == True

    manager = mm.Manager(name, surname, position, age)
    manager.add_engineer(engineer)

    assert engineer.manager == manager



    
