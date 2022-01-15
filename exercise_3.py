# Калькулятор
# Назначение: вычисление операций
# Входные данные: id
# Результаты: выполнение программы в соответсвии c заданиями
# Метод решения: построение на модуле tkinter

# Библиотеки
from tkinter import *
import math

root = Tk()  # Окно
root.title('Калькулятор - обычный режим')  # Заголовк окна
root.resizable(False, False)  # Убрать изменение размера экрана

f = "Arial 25"  # Шрифт текста
operations = []  # Список операций
memoryDict = {}  # Словарь чисел
tmpl1_n = 0  # Счётчик
tmpl0 = []  # Спикок для кнопок памяти в расширенном режиме
tmpl1 = []  # Спикок для меток в расширенном режиме
pos = 1.0  # Отслеживание позиции строк ввода
sp = ''  # Отслеживание пустых строк ввода


class BaseButtons:  # Класс кнопок

    def __init__(self):  # Создание полей
        self.text = Text(height=8, width=60)
        self.text.grid(row=0, column=0, columnspan=5, sticky='w,e', padx=10, pady=10)
        self.c_button = Button(text='< >', command=self.c_height, fg='White', bg='Red', font=f, bd=4)
        self.c_button.grid(row=4, sticky='w,e,n,s', column=1, padx=10, pady=10)
        self.am = Button(text='☰', command=self.c_relief, fg='White', bg='Red', font=f, bd=4, relief=RAISED)
        self.am.grid(row=4, sticky='w,e,n,s', column=0, padx=10, pady=10)
        self.text.insert(pos, '0')
        self.text.tag_add('input', 1.0, END)
        self.text.tag_config('input', justify=RIGHT, font=("Verdana", 20, 'bold'))

    def txt_format(self):  # Форматирование текста
        self.text.tag_add('input', 1.0, END)
        self.text.tag_config('input', justify=RIGHT, font=("Verdana", 20, 'bold'))
        self.text.see('end')

    def c_height(self):  # Изменение количества строк
        global pos
        the_id = self.error_check('ID')
        if the_id == 0:
            return
        else:
            self.text['height'] = id_func(the_id) * 2
            self.txt_format()

    def error_check(self, e_type):  # Провекра на наличие ошибок
        global pos
        if e_type == 'ID':
            the_id = self.text.get(pos, END).strip()
            if len(the_id) != 8:
                self.text.delete(1.0, END)
                self.text.insert(1.0, 'Wrong ID\n')
                self.txt_format()
                pos = 2.0
            else:
                return the_id
        if e_type == 'x/0':
            self.text.insert(pos, 'Error (x/0)\n')
            pos += 1
        if e_type == '√-x':
            self.text.insert(pos, 'Error (√-x)\n')
            pos += 1
        if e_type == 'ln':
            self.text.insert(pos, 'Error (x≤0)\n')
            pos += 1
        if e_type == 'damn+':
            self.text.insert(pos, 'Result too large')
            pos += 1
        if e_type == 'damn-':
            self.text.insert(pos, 'Result too small')
            pos += 1
        return 0

    def c_relief(self):  # Включение расширенного режима
        if self.am['relief'] == RAISED:
            if self.advanced_mode(1) == 0:
                return
            self.am['relief'] = SUNKEN
            root.title('Калькулятор - расширенный режим')
        else:
            self.advanced_mode(0)
            self.am['relief'] = RAISED
            root.title('Калькулятор - обычный режим')
        self.txt_format()

    def dot_insert(self, dot):  # Вставка точки
        global sp
        if self.text.get(pos, END).strip()[-1] == '.' or self.text.get(pos, END).strip()[-1] in operations:
            return 0  # Чтобы точка не ставилась после самой себя или оператора
        if len(operations) > 0:
            # Проверка на повторение точек в одном числе
            for i in self.text.get(pos, END).strip()[::-1]:
                if i == '.':
                    return 0
                elif i == operations[-1]:
                    break
        else:
            # Если опретора нет в тексте
            for i in self.text.get(pos, END).strip():
                if i == '.':
                    return 0
        txt = self.text.get(pos, END).strip()
        if pos != 1.0:
            sp = '\n'
        self.text.delete(pos, END)
        self.text.insert(pos, sp + txt + str(dot))
        self.txt_format()

    def digit_insert(self, digit):  # Вставка цифр
        global sp
        txt = self.text.get(pos, END).strip()
        if len(txt) == 17:  # Максимальное количество символов в строке
            return 0
        elif len(txt) == 1 and txt[0] == '0':  # Убираем изначальный 0
            txt = txt[1:]
        elif digit == '0':
            try:
                if txt[-2] == operations[-1] and txt[-1] == '0':  # Только один 0, если идёт первым после оператора
                    return 0
            except IndexError:  # Пропуск ошибки
                pass
        self.text.delete(pos, END)
        if pos != 1.0:
            sp = '\n'
        self.text.insert(pos, sp + txt + str(digit))
        self.txt_format()

    def operation_insert(self, op):  # Вставка операции
        global sp
        txt = self.text.get(pos, END).strip()
        try:
            # При нажатии на еще один оператор производится замена последнего
            if txt[-1] in operations or txt[-1] == '.' or txt[-1] == '%':
                txt = txt[:-1]
            if len(operations) > 0 and operations[-1] in txt and op != '%':
                if operations[0] == '-' and len(operations) <= 1:
                    pass
                else:
                    self.calculate()
                    txt = self.text.get(pos, END).strip()
                    operations.clear()
        except IndexError:
            pass
        if txt == '':
            txt += '0'
        if len(txt) == 1 and txt[0] == '0' and op == '-':  # Убираем изначальный 0
            txt = txt[1:]
        self.text.delete(pos, END)
        if pos != 1.0:
            sp = '\n'
        if op == 'x^ʸ':
            self.text.insert(pos, sp + txt + '^')
            op = op.replace(op, '^')
        elif op == 'CE':
            self.text.delete(pos, END)
            return 0
        elif op == 'x²':
            self.text.insert(pos, sp + txt + '^2')
            self.calculate()
        elif op == 'x³':
            self.text.insert(pos, sp + txt + '^3')
            self.calculate()
        elif op == '1/x':
            self.text.insert(pos, sp + '1/' + txt)
        elif op == '←':
            self.text.insert(pos, sp + txt[:-1])
        elif op == '√':
            self.advanced_format(txt, '√')
        elif op == 'ln':
            self.advanced_format(txt, 'ln')
        elif op == 'Dms':
            self.advanced_format(txt, 'Dms')
        elif op == 'sin':
            self.advanced_format(txt, 'sin')
        else:
            self.text.insert(pos, sp + txt + op)
        operations.append(op)
        if op == '←':
            operations.remove('←')
        self.txt_format()

    def calculate(self):  # Функция вычисления
        global pos
        txt = self.text.get(pos, END).strip()
        if txt[-1] in operations and txt[-1] != '%':
            txt = txt + txt[:-1]
        elif '^' in txt:
            txt = txt.replace('^', '**')
        elif '%' in txt:
            txt = advanced_calc_format(txt, '%')
        elif '√' in txt:
            txt = advanced_calc_format(txt, '√')
        elif 'ln' in txt:
            txt = advanced_calc_format(txt, 'ln')
        elif 'Dms' in txt:
            txt = advanced_calc_format(txt, 'Dms')
        elif 'sin' in txt:
            txt = advanced_calc_format(txt, 'sin')
        pos += 1.0
        self.text.insert(pos, '\n=\n')
        pos += 1.0
        if str(txt).count('.') > 2:
            self.text.insert(pos, str(txt) + '\n')
            pos += 1
        else:
            try:
                if txt == 'sqrt_e':
                    self.error_check('√-x')
                elif txt == 'ln_e':
                    self.error_check('ln')
                else:
                    result = str(round(eval(txt), 5))
                    if float(result) > 0 and len(result) > 17:
                        raise OverflowError
                    elif float(result) < 0 and len(result) > 17:
                        self.error_check('damn-')
                    else:
                        self.text.insert(pos, result)
            except ZeroDivisionError:
                self.error_check('x/0')
            except OverflowError:
                self.error_check('damn+')
        operations.clear()
        self.txt_format()

    def clear(self):  # Очищение экрана
        global pos, sp
        self.text.delete(1.0, END)
        self.text.insert(1.0, '0')
        pos = 1.0
        sp = ''
        operations.clear()
        self.txt_format()

    def minus_add(self):  # Вставка минуса перед числом
        global sp
        txt = self.text.get(pos, END).strip()
        ik = 0
        if txt[0] == '0' and len(txt) == 1:
            return
        # Проверка на наличие оператора в тексте
        for o in operations:
            if o in txt:
                ik += 1
        if ik == 0:
            if txt[0] == '-':
                txt = txt[1:]
            else:
                txt = '-' + txt
                operations.insert(0, '-')

        else:  # Все условия ниже предусматривают корректность вставки минуса перед числом
            if operations[-1] == '+':
                txt = txt.replace('+', '-')
                operations[-1] = '-'
            elif operations[-1] == '-':
                f_i = txt.rindex('-')
                txt = txt[:f_i] + '+' + txt[f_i + 1:]
                operations[-1] = '+'
            else:
                f_i = txt.index(operations[-1])
                if txt[-1] in operations:
                    if txt[0] == '-':
                        txt = txt[1:]
                    else:
                        txt = '-' + txt
                elif txt[f_i + 1] == '-':
                    txt = txt[:f_i] + txt[f_i] + txt[f_i + 2:]
                else:
                    txt = txt[:f_i] + txt[f_i] + '-' + txt[f_i + 1:]
        self.text.delete(pos, END)
        if pos != 1.0:
            sp = '\n'
        self.text.insert(pos, sp + txt)
        self.txt_format()

    def memory_btn(self, mb, ms='MS'):  # Работа с памятью
        global sp
        if pos != 1.0:
            sp = '\n'
        if mb == 'MC':  # Очищение памяти
            memoryDict.clear()
        elif mb == 'MR':  # Считывание памяти
            if ms not in memoryDict:
                pass
            else:
                self.text.delete(pos, END)
                self.text.insert(pos, sp + str(memoryDict[ms]))
        elif mb == 'MS':  # Сохранение в память
            txt = self.text.get(pos, END).strip()
            ik = 0
            # Проверка на наличие оператора в тексте
            for o in operations:
                if o in txt:
                    ik += 1
            if ik == 0:
                memoryDict[ms] = float(txt)
            else:
                f_i = txt.index(operations[-1])
                if txt[-1] == operations[-1]:
                    memoryDict[ms] = float(txt[:f_i])
                else:
                    memoryDict[ms] = float(txt[:f_i:-1])
        elif mb == 'M+':  # Прибавить к числу из памяти с ввода
            if ms not in memoryDict:
                return
            txt = self.text.get(pos, END).strip()
            ik = 0
            # Проверка на наличие оператора в тексте
            for o in operations:
                if o in txt:
                    ik += 1
            if ik == 0:
                memoryDict[ms] += float(txt)
            else:
                f_i = txt.index(operations[-1])
                if txt[-1] == operations[-1]:
                    memoryDict[ms] += float(txt[:f_i])
                else:
                    memoryDict[ms] += float(txt[:f_i:-1])
        elif mb == 'M-':  # Вычесть число из памяти с ввода
            if ms not in memoryDict:
                return
            txt = self.text.get(pos, END).strip()
            ik = 0
            # Проверка на наличие оператора в тексте
            for o in operations:
                if o in txt:
                    ik += 1
            if ik == 0:
                memoryDict[ms] -= float(txt)
            else:
                f_i = txt.index(operations[-1])
                if txt[-1] == operations[-1]:
                    memoryDict[ms] -= float(txt[:f_i])
                else:
                    memoryDict[ms] -= float(txt[:f_i:-1])
        self.txt_format()

    def advanced_mode(self, mode):  # Функия для перехода в расширенный режим
        global tmpl0, pos
        if mode == 1:
            the_id = self.error_check('ID')
            if the_id == 0:
                return 0
            cell_amount = id_func(the_id, 0)
            new_ops = ['%', '←', '1/x', 'x²', 'CE']
            n = 0
            bg = '#3f48cc'
            # Замена кнопок памяти в обычном режиме на новые операции
            for i in new_ops:
                if i == 'CE':
                    bg = 'Red'
                new_ops_button(i, bg).grid(row=5, sticky='w,e,n,s', column=n, padx=10, pady=10)
                n += 1
            l1 = Label(text="управление ячейками памяти", fg='#3f48cc', font=f, bd=4)
            l1.grid(row=4, column=5, columnspan=5, padx=10, pady=10)
            # Создание кнопок памяти в в зависимости от ID
            for mb_amount in range(0, cell_amount):
                tmp = 'l' + str(mb_amount)
                tmpl0.append(tmp)
                v_lb = Label(text=mb_amount + 1, fg='#3f48cc', font=f, bd=4)
                v_lb.grid(row=5 + mb_amount, column=11, padx=10, pady=10)
                tmpl0[mb_amount] = v_lb
                create_memory_buttons(5 + mb_amount, 5, mb_amount, 1)
            l2 = Label(text='KMM ' + the_id, fg='Grey', font=f, bd=4)
            l2.grid(row=0, column=5, columnspan=5, sticky='w,e', padx=10, pady=10)
            c = 5
            tmpl0.append(l1)
            tmpl0.append(l2)
            # Дополнительные функции расширенного режима
            for mo in ['ln', 'x³', 'Dms', 'sin']:
                math_ops_button(mo, 1).grid(row=1, column=c, sticky='w,e,n,s', padx=10, pady=10)
                c += 1
        else:
            # Удаление каждой кнопки по элементу
            for i in tmpl0:
                i.destroy()
            delete_buttons()
            create_memory_buttons()
            tmpl0.clear()

    def advanced_format(self, txt, a_op):  # Форматирование текста в расширенном режиме
        try:
            if operations[-1] in txt and operations[-1] != '-':
                if txt[-1] == operations[-1]:
                    txt = txt[:-1]
                else:
                    txt = txt[:txt.index(operations[-1]):-1]
            self.text.insert(pos, sp + a_op + txt)
            self.calculate()
        except IndexError:
            self.text.insert(pos, sp + a_op + txt)
            self.calculate()

    def add_key(self, event):  # Переход в расширенный режим по кнопке "F"(Используя собственный ID)
        if event.char == 'f':
            self.clear()
            self.digit_insert(70155302)
            self.c_relief()


def advanced_calc_format(txt, aon):  # Вычисление дополнительных функциий
    a_f = None
    if aon == 'sin':
        a_f = sin_func
    elif aon == 'ln':
        a_f = ln_func
    elif aon == 'Dms':
        a_f = dms_func
    elif aon == '√':
        a_f = sqrt_func
    elif aon == '%':
        return p_func(txt)
    n_txt = txt.replace(aon, aon[0])
    f_i = n_txt.index(aon[0])
    if f_i == 0:
        n_txt = str(a_f(float(n_txt[1:])))
    else:
        n_txt = n_txt[:f_i] + str(a_f(float(n_txt[f_i + 1:])))
    return str(n_txt)


def math_ops_button(np, mode=0):  # Свойства кнопкок дополнительного режима
    if mode == 0:  # В обычном режиме
        return Button(text=np, command=lambda: bb.operation_insert(np), fg='White', bg='DimGrey', font=f, bd=4)
    else:  # В расширенном режиме
        global tmpl1, tmpl1_n
        tmp = 'm' + np
        tmpl1.append(tmp)
        mab = Button(text=np, command=lambda: bb.operation_insert(np), fg='White', bg='DimGrey', font=f, bd=4)
        if np == 'Dms':
            mab['font'] = 'Arial 20'
        tmpl1[tmpl1_n] = mab
        tmpl1_n += 1
        return mab


def new_ops_button(np, bg):  # Создание кнопок с дополнительными функиями
    return Button(text=np, command=lambda: bb.operation_insert(np), fg='White', bg=bg, font=f, bd=4)


def p_func(txt):  # Вычисление процента
    if len(operations) < 2:
        return '0'
    if operations[-2] in txt:
        f_i = txt.index(operations[-2])
        f_i_p = txt.index('%')
        p = str(float(txt[f_i + 1:f_i_p]) / 100)
        txt_p = str(eval(txt[:f_i] + '*' + p))
        return str(txt[:f_i] + operations[-2] + txt_p)
    else:
        return '0'


def sqrt_func(x):  # Вычисление корня
    try:
        txt_c = math.sqrt(x)
        return txt_c
    except ValueError:
        return 'sqrt_e'


def sin_func(x):  # Вычисление синуса
    txt_c = math.sin(x)
    return txt_c


def ln_func(x):  # Вычисление натурального логорифма
    try:
        txt_c = math.log(x)
        return txt_c
    except ValueError:
        return 'ln_e'


def dms_func(dd):  # Переводит из десятичного вида в формат в градусы, минуты, секунды
    is_positive = dd >= 0
    dd = abs(dd)
    minutes, seconds = divmod(dd * 3600, 60)
    degrees, minutes = divmod(minutes, 60)
    degrees = degrees if is_positive else -degrees
    txt = ' '.join([str(round(degrees, 5)), str(round(minutes, 5)), str(round(seconds, 5))])
    return txt


bb = BaseButtons()  # Вызов класса

root.bind('<Key>', bb.add_key)  # Вызов события при нажатии кнопок


def id_recursion(id_name, id_len=8):  # Выполнение рекурсии
    if id_len == 0:
        return 0
    else:
        return str(eval(str(id_name[id_len - 1]) + '+' + str(id_recursion(id_name, id_len - 1))))


def id_func(id_name, str_amount=1):  # Подсчитывание строк цифрого дисплея
    if str_amount == 1:
        res = id_recursion(id_name)
        if len(res) > 1:
            while len(res) > 1:
                res = id_recursion(res, len(res))
        if res == '1':
            res = 10
    else:
        res = id_recursion(id_name[:3:-1], 3)
        if len(res) > 1:
            while len(res) > 1:
                res = id_recursion(res, len(res))
        if res == '1':
            res = 2
    return int(res)


def dot_button(dot):  # Свойства точки
    return Button(text=dot, command=lambda: bb.dot_insert(dot), fg='#034d97', bg='White', font=f, bd=4)


def digit_button(digit):  # Свойства кнопок обычного режима по цифре
    return Button(text=digit, command=lambda: bb.digit_insert(digit), fg='#034d97', bg='White', font=f, bd=4)


def operation_button(op):  # Свойства кнопок обычного режима по операции
    return Button(text=op, command=lambda: bb.operation_insert(op), fg='White', bg='DimGrey', font=f, bd=4)


def calc_button(equal):  # Свойства кнопоки вычисления
    return Button(text=equal, command=bb.calculate, fg='White', bg='#034d97', font=f, bd=4)


def clear_button(c):  # Свойства кнопоки очистки экрана
    return Button(text=c, command=bb.clear, fg='White', bg='Red', font=f, bd=4)


def minus_add_button(md):  # Свойства кнопоки очистки экрана
    return Button(text=md, command=bb.minus_add, fg='White', bg='DimGrey', font=f, bd=4)


def memory_number_button(mb, mb_num, mode):  # Свойства кнопок памяти
    if mode == 0:  # Создание в обычном режиме
        return Button(text=mb, command=lambda: bb.memory_btn(mb, mb_num), fg='White', bg='DimGrey', font=f, bd=4)
    else:  # Создание в расширенном режиме
        global tmpl1, tmpl1_n
        tmp = 'm' + mb
        tmpl1.append(tmp)
        mb_btn = Button(text=mb, command=lambda: bb.memory_btn(mb, mb_num), fg='White', bg='DimGrey', font=f, bd=4)
        tmpl1[tmpl1_n] = mb_btn
        tmpl1_n += 1
        return mb_btn


def delete_buttons():  # Удаление кнопок памяти при выходе из расширенного режима
    global tmpl1, tmpl1_n
    # Удаление каждой кнопки по элементу
    for i in tmpl1:
        i.destroy()
    tmpl1.clear()
    tmpl1_n = 0


# Кнопоки обычного режима
b0 = digit_button('0').grid(row=9, sticky='w,e,n,s', column=0, columnspan=2, padx=10, pady=10)
b1 = digit_button('1').grid(row=8, sticky='w,e,n,s', column=0, padx=10, pady=10)
b2 = digit_button('2').grid(row=8, sticky='w,e,n,s', column=1, padx=10, pady=10)
b3 = digit_button('3').grid(row=8, sticky='w,e,n,s', column=2, padx=10, pady=10)
b4 = digit_button('4').grid(row=7, sticky='w,e,n,s', column=0, padx=10, pady=10)
b5 = digit_button('5').grid(row=7, sticky='w,e,n,s', column=1, padx=10, pady=10)
b6 = digit_button('6').grid(row=7, sticky='w,e,n,s', column=2, padx=10, pady=10)
b7 = digit_button('7').grid(row=6, sticky='w,e,n,s', column=0, padx=10, pady=10)
b8 = digit_button('8').grid(row=6, sticky='w,e,n,s', column=1, padx=10, pady=10)
b9 = digit_button('9').grid(row=6, sticky='w,e,n,s', column=2, padx=10, pady=10)

# Кнопка - точка
bd = dot_button('.').grid(row=9, sticky='w,e,n,s', column=2, padx=10, pady=10)

# Операции обычного режима
op0 = operation_button('+').grid(row=9, sticky='w,e,n,s', column=3, padx=10, pady=10)
op1 = operation_button('-').grid(row=8, sticky='w,e,n,s', column=3, padx=10, pady=10)
op2 = operation_button('*').grid(row=7, sticky='w,e,n,s', column=3, padx=10, pady=10)
op3 = operation_button('/').grid(row=6, sticky='w,e,n,s', column=3, padx=10, pady=10)
op4 = operation_button('x^ʸ').grid(row=6, sticky='w,e,n,s', column=4, padx=10, pady=10)
op5 = operation_button('√').grid(row=7, sticky='w,e,n,s', column=4, padx=10, pady=10)

# Кнопка вычисления
calc_b = calc_button('=').grid(row=9, sticky='w,e,n,s', column=4, padx=10, pady=10)

# Кнопка очистки экрана
clear_b = clear_button('C').grid(row=4, sticky='w,e,n,s', column=4, padx=10, pady=10)

# Кнопка вставки минуса
minus_add_b = minus_add_button('+/-').grid(row=8, sticky='w,e,n,s', column=4, padx=10, pady=10)


# Кнопки памяти
def create_memory_buttons(r=5, c=0, mb_num=0, mode=0):
    memory_number_button('MC', str(mb_num), mode).grid(row=r, sticky='w,e,n,s', column=c, padx=10, pady=10)
    memory_number_button('MR', str(mb_num), mode).grid(row=r, sticky='w,e,n,s', column=c + 1, padx=10, pady=10)
    memory_number_button('MS', str(mb_num), mode).grid(row=r, sticky='w,e,n,s', column=c + 2, padx=10, pady=10)
    memory_number_button('M+', str(mb_num), mode).grid(row=r, sticky='w,e,n,s', column=c + 3, padx=10, pady=10)
    memory_number_button('M-', str(mb_num), mode).grid(row=r, sticky='w,e,n,s', column=c + 4, padx=10, pady=10)


create_memory_buttons()

root.mainloop()
