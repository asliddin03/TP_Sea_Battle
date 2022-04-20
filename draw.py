import global_variable as glob_var
from dotted_and_hit import dotted_and_hit
import pygame
import random
pygame.init()

 
class draw:
    def ship(ships_coor_list):
        for i in ships_coor_list:
            ship = sorted(i)
            x_s = ship[0][0]
            y_s = ship[0][1] 
            ship_w = glob_var.block_sz * len(ship)
            ship_h = glob_var.block_sz
            if len(ship) > 1 and ship[0][0] == ship[1][0]:
                ship_w, ship_h = ship_h, ship_w
            x = glob_var.block_sz * (x_s - 1) + glob_var.l_margin
            y = glob_var.block_sz * (y_s - 1) + glob_var.upp_margin
            if ships_coor_list == glob_var.human.ships:
                x += 15 * glob_var.block_sz
            pygame.draw.rect(glob_var.screen, glob_var.BL, ((x, y), (ship_w, ship_h)), width=glob_var.block_sz//10)

    def grid():
        let = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
        num = ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10']
        for i in range(11):
            list = [[0, i * glob_var.block_sz, 10 * glob_var.block_sz, i * glob_var.block_sz], [i * glob_var.block_sz, 0, i * glob_var.block_sz, 10 * glob_var.block_sz],
                            [15 * glob_var.block_sz, i * glob_var.block_sz, 25 * glob_var.block_sz, i * glob_var.block_sz], [(i + 15) * glob_var.block_sz, 0, (i + 15) * glob_var.block_sz, 10 * glob_var.block_sz]]
            for j in list:
                pygame.draw.line(glob_var.screen, glob_var.BL, (glob_var.l_margin + j[0], glob_var.upp_margin + j[1]),(glob_var.l_margin + j[2], glob_var.upp_margin + j[3]), 2)
            if i < 10:
                num_ver = glob_var.font.render(num[i], True, glob_var.BL)
                let_hor = glob_var.font.render(let[i], True, glob_var.BL)
                num_ver_width = num_ver.get_width()
                num_ver_height = num_ver.get_height()
                let_hor_width = let_hor.get_width()
                glob_var.block_sz1 = glob_var.block_sz // 2
                num_ver_width1 = num_ver_width // 2
                num_ver_height1 = num_ver_height // 2
                let_hor_width1 = let_hor_width // 2
                list1 = [[num_ver, -glob_var.block_sz1 - num_ver_width1, i * glob_var.block_sz + glob_var.block_sz1 - num_ver_height1], [let_hor, i * glob_var.block_sz + glob_var.block_sz1 - let_hor_width1, 10 * glob_var.block_sz + 5],
                                                                            [num_ver, -glob_var.block_sz1 - num_ver_width1 + 15 * glob_var.block_sz, i * glob_var.block_sz + glob_var.block_sz1 - num_ver_height1],
                                                                                                    [let_hor, (i + 15) * glob_var.block_sz + glob_var.block_sz1 - let_hor_width1, 10 *glob_var.block_sz + 5]]
                for j in list1:
                    glob_var.screen.blit(j[0], (glob_var.l_margin + j[1], glob_var.upp_margin + j[2]))

    def dotted(dotted):
        for i in dotted:
            pygame.draw.circle(glob_var.screen, glob_var.BL, (glob_var.block_sz*(
                i[0]-0.5)+glob_var.l_margin, glob_var.block_sz*(i[1]-0.5)+glob_var.upp_margin), glob_var.block_sz//5)

    def destroyed_ships(pos, oppo_ships_list, comp_turn, diagonal_only=False):
        if oppo_ships_list == glob_var.ship_w:
            ships_list = glob_var.computer.ships
        elif oppo_ships_list == glob_var.H_ships_w:
            ships_list = glob_var.human.ships
        ship = sorted(ships_list[pos])
        for i in range(-1, 1):
            dotted_and_hit(ship[i], comp_turn, diagonal_only)




class ships(draw):
    def __init__(self):
        self.ava_Bl = set((a, b)for a in range(1, 11) for b in range(1, 11))
        self.ships_set = set()
        self.ships = self.grid()

    def create_ship(self, num_Bl, ava_Bl):
        ship_coor = []
        x_y = random.randint(0, 1)
        str_rev = random.choice((-1, 1))
        x, y = random.choice(tuple(ava_Bl))
        for _ in range(num_Bl):
            ship_coor.append((x, y))
            if not x_y:
                str_rev, x = self.add_ship(
                    x, str_rev, x_y, ship_coor)
            else:
                str_rev, y = self.add_ship(
                    y, str_rev, x_y, ship_coor)
        ship = set(ship_coor)
        if ship.issubset(self.ava_Bl):
            return ship_coor
        return self.create_ship(num_Bl, ava_Bl)

    def add_ship(self, coor, str_rev, x_y, ship_coor):
        if (coor <= 1 and str_rev == -1) or (coor >= 10 and str_rev == 1):
            str_rev *= -1
            return str_rev, ship_coor[0][x_y] + str_rev
        else:
            return str_rev, ship_coor[-1][x_y] + str_rev

    def add_new_ship(self, ship):
         self.ships_set.update(ship)

    def update_ava_Bl(self, ship):
        for i in ship:
            for j in range(-1, 2):
                for m in range(-1, 2):
                    if 0 < (i[0]+j) < 11 and 0 < (i[1]+m) < 11:
                        self.ava_Bl.discard((i[0]+j, i[1]+m))

    def grid(self):
        ships_coor = []
        for i in range(1, 5):
            for _ in range(5-i):
                ship = self.create_ship(i, self.ava_Bl)
                ships_coor.append(ship)
                self.add_new_ship(ship)
                self.update_ava_Bl(ship)
        return ships_coor
