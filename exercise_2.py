# Банковские счета
# Назначение: работа со счётом
# Входные данные: операция, имя, сумма
# Результаты: выполнение программы в соответсвии c заданиями
# Метод решения: построение на модуле tkinter

from tkinter import *

root = Tk()

bank_IDs = {'Filinskii': 70155302}  # Начальный счёт


# ==================== Функции для работы со счетами ====================

def deposit(name, value):  # Зачислить на счёт
    if name in bank_IDs:
        bank_IDs[name] += value
    else:
        bank_IDs[name] = value


def withdraw(name, value):  # Снать со счёта
    if name in bank_IDs:
        bank_IDs[name] -= value
    else:
        bank_IDs[name] = -value


def balance(name):  # Показать баланс
    if name in bank_IDs:
        text2.insert(1.0, name + " " + str(bank_IDs[name]) + '\n' * 2)
    elif name == '0':
        for k, v in bank_IDs.items():
            kv = str(k) + ":" + str(v) + ";"
            text2.insert(1.0, kv + '\n' * 2)
    elif name not in bank_IDs:
        text2.insert(1.0, "NO CLIENT" + '\n' * 2)


def transfer(name1, name2, value):  # Перевод счёта
    if name1 in bank_IDs:
        if name2 in bank_IDs:
            bank_IDs[name2] += value
            bank_IDs[name1] -= value
        else:
            bank_IDs[name2] = value
            bank_IDs[name1] -= value
    else:
        if name2 in bank_IDs:
            bank_IDs[name2] += value
            bank_IDs[name1] = -value
        else:
            bank_IDs[name2] = value
            bank_IDs[name1] = -value


def income(p):  # Начислить проценты
    for name in bank_IDs:
        if bank_IDs[name] >= 0:
            bank_IDs[name] += int(bank_IDs[name] * int(p) / 100)


# =======================================================================
def calculate():  # Вычисление
    txt = text1.get(1.0, END)
    tpl = []
    n = 0
    j = 0
    txt = txt.replace("BALANCE \n", "BALANCE 0\n")
    t = txt.split()
    # Создаём список с операциями
    for tj in t:
        if "DEPOSIT" == tj:
            tmp = 't' + str(n)
            tpl.append(tmp)
            tpl[n] = (t[0 + j], t[1 + j], int(t[2 + j]))
            n += 1
            j += 3
        elif "WITHDRAW" == tj:
            tmp = 't' + str(n)
            tpl.append(tmp)
            tpl[n] = (t[0 + j], t[1 + j], int(t[2 + j]))
            n += 1
            j += 3
        elif "BALANCE" == tj:
            tmp = 't' + str(n)
            tpl.append(tmp)
            tpl[n] = (t[0 + j], t[1 + j])
            n += 1
            j += 2
        elif "TRANSFER" == tj:
            tmp = 't' + str(n)
            tpl.append(tmp)
            tpl[n] = (t[0 + j], t[1 + j], t[2 + j], int(t[3 + j]))
            n += 1
            j += 4
        elif "INCOME" == tj:
            tmp = 't' + str(n)
            tpl.append(tmp)
            tpl[n] = (t[0 + j], t[1 + j])
            n += 1
            j += 2
    count = 0
    # Выполняем операции
    for tl in tpl:
        if count <= 20:
            if "DEPOSIT" in tl:
                deposit(tl[1], int(tl[2]))
            elif "WITHDRAW" in tl:
                withdraw(tl[1], int(tl[2]))
            elif "BALANCE" in tl:
                balance(tl[1])
            elif "TRANSFER" in tl:
                transfer(tl[1], tl[2], int(tl[3]))
            elif "INCOME" in tl:
                income(tl[1])
            count += 1
        else:
            text2.insert(1.0, "Too many commands" + '\n' * 2)
            text2.tag_add('err', 1.0, '1.end')
            text2.tag_config('err', justify=CENTER, font=("Impact", 24, 'bold'))
            break


def delete_text1():  # Удапение текста на левом окне
    text1.delete(1.0, END)


def delete_text2():  # Удаление текста на правом окне
    text2.delete(1.0, END)


# ==================== Оформление интерфейса ====================

l_input = LabelFrame(text="Input")
l_output = LabelFrame(text="Output")

text1 = Text(l_input, width="50")
text2 = Text(l_output, width='50')

l_input.pack(side=LEFT)
l_output.pack(side=LEFT)

text1.pack(side=LEFT)
text2.pack(side=LEFT)

scroll1 = Scrollbar(l_input, command=text1.yview)
scroll2 = Scrollbar(l_output, command=text2.yview)

scroll1.pack(side=LEFT, fill=Y)
scroll2.pack(side=LEFT, fill=Y)

text1.config(yscrollcommand=scroll1.set)
text2.config(yscrollcommand=scroll2.set)

Button(text="Calculate", command=calculate, font="Arial 30").pack(side=LEFT)
Button(l_input, text="Clear", command=delete_text1, font="Arial 20").pack(side=BOTTOM)
Button(l_output, text="Clear", command=delete_text2, font="Arial 20").pack(side=BOTTOM)

# ===============================================================

root.mainloop()
