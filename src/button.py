from tkinter import Variable
import global_variable as variables
import pygame


pygame.init()


class button:
    """
    Создает кнопки и печатает пояснительное сообщение для них
    ----------
    Атрибуты:
        __title (str): Название кнопки (заголовок)
        __message (str): пояснительное сообщение для печати на экране
        __x_start (int): горизонтальное смещение, с которого начинается кнопка рисования
        __y_start (int): смещение по вертикали, с которого начинается кнопка рисования
        rect_for_draw (tuple): прямоугольник кнопки, который нужно нарисовать
        rect (pygame Rect): объект pygame Rect
        __rect_for_button_title (tuple): прямоугольник внутри кнопки для печати текста в нем
        __color (tuple): цвет кнопки
    ----------
    Методы:
    draw_button(): Рисует кнопку в виде цветного прямоугольника
    change_color_on_hover(): Рисует кнопку в виде прямоугольника зеленого цвета.
    print_message_for_button(): Выводит пояснительное сообщение рядом с кнопкой
    """
    def __init__(self, x_ofs, button1):
        self.__tl = button1
        self.__tl_w, self.__tl_h = variables.font.size(self.__tl)
        self.__button_w = self.__tl_w + variables.block_sz
        self.__button_h = self.__tl_h + variables.block_sz
        self.__x = x_ofs + variables.block_sz
        self.__y = variables.upp_margin + 4 * \
            variables.block_sz + self.__button_h
        self.draw = self.__x, self.__y - 20, self.__button_w - 40, self.__button_h
        self.rect = pygame.Rect(self.draw)
        self.__button_tl = self.__x + self.__button_w // 2 - self.__tl_w // 2 - \
            20, self.__y + self.__button_h // 2 - self.__tl_h // 2 - 20
        self.__cl = variables.L_GRAY

    def Draw(self, cl=None):
        """
        Рисует кнопку в виде цветного прямоугольника
        Аргументы:
            цвет (tuple): цвет кнопки. По умолчанию значение равно None
        """
        if not cl:
            cl = self.__cl
        pygame.draw.rect(variables.screen, cl, self.draw)
        text = variables.font.render(
            self.__tl, True, variables.RED)
        variables.screen.blit(text, self.__button_tl)

    def change_cl(self):
        """
        Рисует кнопку в виде прямоугольника
        """
        coor = pygame.mouse.get_pos()
        if self.rect.collidepoint(coor):
            self.Draw(variables.GR)
