# Towers of hanoi
# Назначение: переместить диски с 1 башни на 3, не нарушая правил
# Входные данные: id
# Результаты: выполнение программы в соответсвии с заданиями
# Метод решения: рекурсия

# Библиотеки
from tkinter import *
import random

root = Tk()  # Окно
root.title('Towers of hanoi')  # Заголовк окна
root.resizable(False, False)  # Убрать изменение размера экрана

# id = 70155302(5)
id_py = '33303300'  # Используемый id

c = Canvas(width=1280, height=720, bg='Grey')
c.pack()


class BaseFigure:  # Класс создающий базовые объекты
    # ==================== Переменные класса ====================
    x1 = 50
    y1 = 630
    x2 = 1230
    y2 = 650
    towers = []

    # ===========================================================

    def __init__(self, ccc):  # Передача канваса классу
        self.c = ccc

    def fig_config(self):  # Цвет башен и основания
        self.c.itemconfig('b', fill='Sienna', outline='SaddleBrown', width=3)

    def create_base(self):  # Создание башен с основанием
        self.c.create_rectangle(self.x1, self.y1, self.x2, self.y2, tag='b')
        self.x1 = 100
        self.x2 = 120
        self.y1 = 630
        self.y2 = 150
        # Создание башен
        for cc in range(8):
            tmp = 't' + str(cc)
            self.towers.append(tmp)
            t = self.c.create_rectangle(self.x1, self.y1, self.x2, self.y2, tag='b')
            self.c.create_text((self.x1 + self.x2) / 2, self.y2 - 20, text=8 - cc, font='Arial 20')
            self.towers[cc] = t, self.x1, self.x2, self.y1, (self.x2 - self.x1) / 2
            self.x1 = self.x2 + (self.x2 - self.x1) / 2 + 122
            self.x2 = self.x1 + 20
        self.fig_config()
        self.c.create_text(200, 670, text='~3 секунды на 100k итерациий', font='Arial  15', fill='DarkSlateGrey')


class DiscFigure:  # Класс для дисков
    # ==================== Переменные класса ====================
    disc_am = {}
    disc_db = {}
    t_num = 8
    t_iter = 0
    d_num = 9
    d_start = {}
    towers = BaseFigure.towers
    n_r = 0
    tt = 8
    y_iter = 1
    iter_count = 0
    loc_iter = 0
    it_1, it_2, it_3 = 0, 0, 0
    f_iter = 0
    pr_s = -1
    stop_now = 0
    p_used = 0
    end = 1
    b_used = 0
    last_d = None
    last_t = None
    lx = 0
    ly = 0
    # ===========================================================
    l1 = Label(text="Итерация " + str(iter_count), anchor=CENTER)  # Надпись с кол-вом операций
    l1.configure(width=20, bg="White")
    c.create_window(990, 679, window=l1)
    # ==================== Поля ввода ====================
    e1 = Entry(justify=CENTER)
    e1.configure(width=12)
    e1_win = c.create_window(510, 670, window=e1)

    e2 = Entry(justify=CENTER)
    e2.configure(width=12)
    e2_win = c.create_window(600, 670, window=e2)

    e3 = Entry(justify=CENTER)
    e3.configure(width=12)
    e3_win = c.create_window(690, 670, window=e3)

    e4 = Entry(justify=CENTER)
    e4.configure(width=12)
    e4_win = c.create_window(780, 670, window=e4)

    e1.insert(0, id_py[:2])
    e2.insert(0, id_py[2:4])
    e3.insert(0, id_py[4:6])
    e4.insert(0, id_py[6:])

    # =====================================================

    def __init__(self, ccc, id_py_id):  # Создание полей
        self.e = None
        self.c = ccc
        self.id = str(id_py_id)

    def disc_amount(self):  # Кол-во дисков на каждую башню
        i_k = 8
        # Подсчёт дисков на башне
        for i in self.id:
            tmp = 'tower' + str(i_k)
            self.disc_am[tmp] = int(i)
            i_k -= 1

    def disc_create(self):  # Создание дисков
        self.disc_amount()
        # Для каждой башни создаем определённое кол-во дисков
        for tower in self.disc_am.values():
            y1 = self.towers[self.t_iter][3]
            y2 = y1 - 12
            self.d_num = 9
            tmp = 'tower' + str(self.t_num)
            self.disc_db[tmp] = []
            self.d_start[tmp] = []
            # Для каждого диска задаём определённые св-ва
            for disc in range(int(tower)):
                d_x1, d_x2 = self.disc_x('x1'), self.disc_x('x2')
                disc_n = self.c.create_rectangle(d_x1, y1, d_x2, y2)
                disc_t = self.c.create_text(d_x1 - 10, y1, anchor='se', text=self.len_c(), font='Arial 10')
                d = [disc_n, disc_t, d_x1, d_x2, y1]  # Диск, надпись, x1, x2, y1
                d_str = [str(disc_n), str(disc_t), str(d_x1), str(d_x2), str(y1), str(y2)]  # Диск, надпись, x1, x2, y1
                self.disc_tag(disc_n)
                self.disc_db[tmp].append(d)
                self.d_start[tmp].append(d_str)
                y1 = y2
                y2 -= 12
                self.d_num -= 1
            self.t_num -= 1
            self.t_iter += 1
        t__ = 'Общее кол-во итераций в данной генерации = '
        t___ = str(self.max_iter())
        c.create_text(50, 45, text=t__ + t___, anchor=W, font='Arial  15', fill='DarkSlateGrey')

    def len_c(self):  # Расчёт диаметра диска
        return (lambda m, n: m * 10 + n)(self.t_num, self.d_num)

    def disc_x(self, x=None):  # Координаты иксов
        if x == 'x1':
            return self.towers[self.t_iter][1] - self.len_c() / 2
        elif x == 'x2':
            return self.towers[self.t_iter][2] + self.len_c() / 2

    def disc_tag(self, disc_n):  # Генерирование цветов
        def r(): return random.randint(0, 255)  # Вместо лямбды (PEP 8: E731)

        bg = '#%02X%02X%02X' % (r(), r(), r())
        fg = '#%02X%02X%02X' % (r(), r(), r())
        self.c.itemconfig(disc_n, fill=bg, outline=fg, width=2)

    def disc_btn(self, cmd):  # Функия, при нажатии на кнопки
        if cmd == 's':  # Начало
            self.start_pos()
        if self.end == 1:
            self.start_pos()
        if cmd == 'p1':
            self.e = self.e1
            if self.p_used == 1:
                self.start_pos()
            self.percent_iter()
        elif cmd == 'p2':
            self.e = self.e2
            if self.p_used == 1:
                self.start_pos()
            self.percent_iter()
        elif cmd == 'p3':
            self.e = self.e3
            if self.p_used == 1:
                self.start_pos()
            self.percent_iter()
        elif cmd == 'p4':
            self.e = self.e4
            if self.p_used == 1:
                self.start_pos()
            self.percent_iter()
        elif cmd == 'e':  # Окончание
            self.stop_now = 0
            if self.b_used == 1:
                c.move(self.last_d, 0, self.ly + 500)
                c.move(self.last_t, 0, self.ly + 500)
            self.disc_op()

    def percent_iter(self):  # Процентная итерация
        p = self.e.get()
        try:
            if int(p) > 100:
                self.start_pos()
                return
        except ValueError:
            return
        if p == '100':
            self.disc_op()
        if p[0] == '0':
            p = p[1]
        if p == '0':
            self.start_pos()
        else:
            self.pr_s = self.max_iter() * (int(p) / 100)
            self.disc_op()
            self.l1['text'] = 'Итерация ' + str(round(self.pr_s, 4))
            self.p_used = 1

    def max_iter(self):  # Общее кол-во итераций
        another_count = 8
        sq_ = 0
        while another_count - 2 != -1:
            if another_count == 2:
                another_count = 3
            t1 = self.disc_am['tower{}'.format(another_count)]
            t2 = self.disc_am['tower{}'.format(another_count - 1)]
            t3 = self.disc_am['tower{}'.format(another_count - 2)]
            n1 = t1 + t2 + t3
            n2 = t2 + t3
            n3 = t3
            tmp_it_1 = 2 ** n1 - 1
            tmp_it_2 = 2 ** n2 - 1
            tmp_it_3 = 2 ** n3 - 1
            sq_ += tmp_it_3 + tmp_it_2 + tmp_it_1
            if another_count == 4:
                self.disc_am['tower{}'.format(another_count - 1)] = 0
            self.disc_am['tower{}'.format(another_count - 2)] += t1 + t2
            another_count -= 2
        return sq_

    def disc_op(self):  # Передвижение дисков
        # На каждые 3 башни выполняем перемещение дисков с начала до конца
        while self.tt - 2 != -1:
            if self.tt == 2:
                self.tt = 3
            t1 = len(self.disc_db['tower{}'.format(self.tt)])
            t2 = len(self.disc_db['tower{}'.format(self.tt - 1)])
            t3 = len(self.disc_db['tower{}'.format(self.tt - 2)])
            n1 = t1 + t2 + t3
            n2 = t2 + t3
            n3 = t3
            self.it_1 = 2 ** n1 - 1
            self.it_2 = 2 ** n2 - 1
            self.it_3 = 2 ** n3 - 1
            if t1 == 0 and t2 == 0:
                pass
            elif t2 == 0 and t3 == 0:
                self.hanoi_default(n1, self.tt, self.tt - 2)
            elif t3 == 0:
                self.hanoi_t2(n1, n2, self.tt - 1, self.tt)
            else:
                self.hanoi_t3(n1, n2, n3, self.tt - 2, self.tt - 1)
            self.tt -= 2
            if self.stop_now == 1:
                break
        self.l1['text'] = "Итерация " + str(self.iter_count)

    def hanoi_t3(self, n1, n2, n3, start, end):  # Рекурсия перемещения дисков с 3 на 2 башни
        if n3 == 1:
            if self.stop_now == 1:
                return
            self.disc_move(start, end)
        else:
            other = (self.tt + (self.tt - 1) + (self.tt - 2)) - (start + end)
            self.hanoi_t3(n1, n2, n3 - 1, start, other)
            if self.stop_now == 1:
                return
            self.disc_move(start, end)
            self.hanoi_t3(n1, n2, n3 - 1, other, end)
        self.loc_iter += 1
        if self.loc_iter == self.it_3:
            self.loc_iter = 0
            self.hanoi_t2(n1, n2, self.tt - 1, self.tt)

    def hanoi_t2(self, n1, n2, start, end):  # Рекурсия перемещения дисков с 2 на 1 башни
        if n2 == 1:
            if self.stop_now == 1:
                return
            self.disc_move(start, end)
        else:
            other = (self.tt + (self.tt - 1) + (self.tt - 2)) - (start + end)
            self.hanoi_t2(n1, n2 - 1, start, other)
            if self.stop_now == 1:
                return
            self.disc_move(start, end)
            self.hanoi_t2(n1, n2 - 1, other, end)
        self.loc_iter += 1
        if self.loc_iter == self.it_2:
            self.loc_iter = 0
            self.hanoi_default(n1, self.tt, self.tt - 2)

    def hanoi_default(self, n, start, end):  # Рекурсия перемещения дисков для стандартных (с 1 на 3) ханойских башен
        if self.stop_now == 1:
            return
        if n == 1:
            self.disc_move(start, end)  # Перемещаем самый большой диск на башне
        else:
            # Башня, на которую можно переместить диск от начала
            other = (self.tt + (self.tt - 1) + (self.tt - 2)) - (start + end)
            # Перемещаем его, уменьшая кол-во дисков на начальной башне
            self.hanoi_default(n - 1, start, other)
            if self.stop_now == 1:
                return
            # Вызов функции перемещения
            self.disc_move(start, end)
            # Теперь тоже самое, перемещая диски с промежуточной башни на конечную
            self.hanoi_default(n - 1, other, end)

    def disc_move(self, start, end):  # Перемещение дисков
        between = 0
        if self.iter_count + 1 == int(self.pr_s):
            if isinstance(self.pr_s, float):
                between = 1
        disc_o = int(self.disc_db['tower' + str(start)][-1][0])
        text_o = int(self.disc_db['tower' + str(start)][-1][1])
        pos_x_s = (self.disc_db['tower' + str(start)][-1][2] + self.disc_db['tower' + str(start)][-1][3]) / 2
        pos_y_s = self.disc_db['tower' + str(start)][-1][4]
        if not self.disc_db['tower' + str(end)]:
            pos_x_e = (self.towers[8 - end][1] + self.towers[8 - end][2]) / 2
            pos_x_e -= (self.disc_db['tower' + str(start)][-1][3] + self.disc_db['tower' + str(start)][-1][2]) / 2
            pos_y_e = self.towers[8 - end][3]
            pos_x_move = pos_x_e
            pos_y_move = pos_y_e - pos_y_s
        else:
            pos_x_e = (self.disc_db['tower' + str(end)][-1][2] + self.disc_db['tower' + str(end)][-1][3]) / 2
            pos_y_e = self.disc_db['tower' + str(end)][-1][4]
            pos_x_move = pos_x_e - pos_x_s
            pos_y_move = (pos_y_e - pos_y_s) - 12
        if between == 1:
            pos_x_move /= 2
            pos_y_move = -500
            self.lx = pos_x_move
            self.ly = pos_y_move
            self.b_used = 1
            self.last_d = disc_o
            self.last_t = text_o
        c.move(disc_o, pos_x_move, pos_y_move)
        c.move(text_o, pos_x_move, pos_y_move)
        self.disc_db['tower' + str(start)][-1][2] += pos_x_move
        self.disc_db['tower' + str(start)][-1][3] += pos_x_move
        self.disc_db['tower' + str(start)][-1][4] += pos_y_move
        self.disc_db['tower' + str(end)].append(self.disc_db['tower' + str(start)][-1])
        self.disc_db['tower' + str(start)].pop(-1)
        self.disc_am['tower' + str(start)] -= 1
        self.disc_am['tower' + str(end)] += 1
        self.iter_count += 1
        if self.iter_count == int(self.pr_s):
            self.stop_now = 1

    def start_pos(self):  # Возращение дисков на изначальное положение
        s_obj_coord = {}
        s_obj_t_coord = []
        # Берём значения из словаря
        for v in self.d_start.values():
            if not v:
                continue
            # Добавление в список объектов диска и текста, которые были в начале
            for val in v:
                s_obj_coord[int(val[0])] = val[2:]
                s_obj_t_coord.append(int(val[1]))
        n_obj_coord = []
        n_obj_t_coord = []
        # Для каждого ключа и его значения
        for k, v in self.disc_db.items():
            if not v:
                continue
            # Добавление в список объектов диска и текста
            for val in v:
                n_obj_coord.append(int(val[0]))
                n_obj_t_coord.append(int(val[1]))
        i_k = 0
        # Берём из каждого объекта координату, которая была в начале
        for o in n_obj_coord:
            x1 = s_obj_coord[o][0]
            y1 = s_obj_coord[o][2]
            x2 = s_obj_coord[o][1]
            y2 = s_obj_coord[o][3]
            c.coords(n_obj_coord[i_k], x1, y1, x2, y2)
            c.coords(n_obj_t_coord[i_k], float(x1) - 10, y1)
            i_k += 1
        self.disc_db = {}
        self.disc_am = {}
        # Для каждого ключа и его значения
        for k, v in self.d_start.items():
            n_l = []
            if not v:
                self.disc_db[k] = []
                self.disc_am[k] = 0
                continue
            # Для каждого элемента из списка диска
            for val in v:
                n_l.append([float(item) for item in val])
            self.disc_db[k] = n_l
            self.disc_am[k] = len(v)
        self.tt = 8
        self.iter_count = 0
        self.l1['text'] = 'Итерация 0'
        self.stop_now = 0
        self.f_iter = 0
        self.pr_s = 0
        self.b_used = 0
        self.p_used = 0


BaseFigure(c).create_base()  # Создание шпинделей
df = DiscFigure(c, id_py)  # Вызвов класса
df.disc_create()  # Создание дисков

# ==================== Кнопки ====================

b1 = Button(text="Начало", command=lambda: df.disc_btn('s'), anchor=CENTER)
b1.configure(width=10, activebackground="#33B5E5")
b1_win = c.create_window(420, 680, window=b1)

b2 = Button(text="П.1", command=lambda: df.disc_btn('p1'), anchor=CENTER)
b2.configure(width=10, activebackground="#33B5E5")
b2_win = c.create_window(510, 700, window=b2)

b3 = Button(text="П.2", command=lambda: df.disc_btn('p2'), anchor=CENTER)
b3.configure(width=10, activebackground="#33B5E5")
b3_win = c.create_window(600, 700, window=b3)

b4 = Button(text="П.3", command=lambda: df.disc_btn('p3'), anchor=CENTER)
b4.configure(width=10, activebackground="#33B5E5")
b4_win = c.create_window(690, 700, window=b4)

b5 = Button(text="П.4", command=lambda: df.disc_btn('p4'), anchor=CENTER)
b5.configure(width=10, activebackground="#33B5E5")
b5_win = c.create_window(780, 700, window=b5)

b6 = Button(text="Окончание", command=lambda: df.disc_btn('e'), anchor=CENTER)
b6.configure(activebackground="#33B5E5")
b6_win = c.create_window(870, 680, window=b6)

# ================================================

root.mainloop()
