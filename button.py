import global_variable
import pygame


pygame.init()


class button:

    def __init__(self, x_ofs, button1):
        self.__tl = button1
        self.__tl_w, self.__tl_h = global_variable.font.size(self.__tl)
        self.__button_w = self.__tl_w + global_variable.block_sz
        self.__button_h = self.__tl_h + global_variable.block_sz
        self.__x = x_ofs + global_variable.block_sz
        self.__y = global_variable.upp_margin + 4 * \
            global_variable.block_sz + self.__button_h
        self.draw = self.__x, self.__y - 20, self.__button_w - 40, self.__button_h
        self.rect = pygame.Rect(self.draw)
        self.__button_tl = self.__x + self.__button_w // 2 - self.__tl_w // 2 - \
            20, self.__y + self.__button_h // 2 - self.__tl_h // 2 - 20
        self.__cl = global_variable.RB

    def Draw(self, cl=None):
        if not cl:
            cl = self.__cl
        pygame.draw.rect(global_variable.screen, cl, self.draw)
        text = global_variable.font.render(
            self.__tl, True, global_variable.L_GRAY)
        global_variable.screen.blit(text, self.__button_tl)

    def change_cl(self):
        coor = pygame.mouse.get_pos()
        if self.rect.collidepoint(coor):
            self.Draw(global_variable.GR)
