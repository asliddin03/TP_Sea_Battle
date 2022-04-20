from asyncio import FastChildWatcher
from cmath import rect
from button import button
import global_variable as variables
from draw import draw, ships
from dotted_and_hit import dotted_and_hit
import pygame
import random

pygame.init()

st_game = variables.l_margin + 10 * variables.block_sz
st_button = button(st_game, "START GAME")

def sign():
    list = [variables.font.render("COMPUTER", True, variables.RED), variables.font.render("HUMAN", True, variables.RED)]
    for i in range(len(list)):
        variables.screen.blit(list[i], (variables.l_margin + (5 + 15 * i) * variables.block_sz - list[i].get_width() //
                          2, variables.upp_margin - variables.block_sz//2 - int(variables.block_sz / 1.5)))

def shoot(set_to_shoot):
    pygame.time.delay(700)
    comp_fired = random.choice(tuple(set_to_shoot))
    variables.ava_to_fire_set.discard(comp_fired)
    return hit_or_miss(comp_fired, variables.H_ships_w, True)

def hit_or_miss(fired_BL, oppo_ships_list, comp_turn):
    for i in oppo_ships_list:
        if fired_BL in i:
            dotted_and_hit(
                fired_BL, comp_turn)
            pos = oppo_ships_list.index(i)
            if len(i) == 1:
                dotted_and_hit(fired_BL, comp_turn)
            i.remove(fired_BL)
            if comp_turn:
                variables.last_hits.append(fired_BL)
                variables.human.ships_set.discard(fired_BL)
                update_around_comp_hit(fired_BL)
            else:
                variables.computer.ships_set.discard(fired_BL)
            if not i:
                draw.destroyed_ships(pos, oppo_ships_list, comp_turn)
                if comp_turn:
                    variables.last_hits.clear()
                    variables.around_hit_set.clear()
                else:
                    variables.destroyed_ships.append(variables.computer.ships[pos])
            return True
    if not comp_turn:
        variables.dotted.add(fired_BL)
    else:
        variables.dotted.add((fired_BL[0] + 15, fired_BL[1]))
        variables.dotted_to_shoot.add(fired_BL)
    if comp_turn:
        update_around_comp_hit(fired_BL, False)
    return False

def update_around_comp_hit(fired_BL, computer_hits=True):
    if computer_hits and fired_BL in variables.around_hit_set:
        new_hit_set = set()
        def add(x, y):
            new_hit_set.add((x, y))
        for i in range(len(variables.last_hits)-1):
            if variables.last_hits[i][0] == variables.last_hits[i+1][0]:
                if 1 < variables.last_hits[i][1]:
                    add(variables.last_hits[i][0], variables.last_hits[i][1] - 1)
                if 1 < variables.last_hits[i+1][1]:
                    add(variables.last_hits[i][0], variables.last_hits[i+1][1] - 1)
                if variables.last_hits[i][1] < 10:
                    add(variables.last_hits[i][0], variables.last_hits[i][1] + 1)
                if variables.last_hits[i+1][1] < 10:
                    add(variables.last_hits[i][0], variables.last_hits[i+1][1] + 1)
            elif variables.last_hits[i][1] == variables.last_hits[i+1][1]:
                if 1 < variables.last_hits[i][0]:
                    add(variables.last_hits[i][0] - 1, variables.last_hits[i][1])
                if 1 < variables.last_hits[i+1][0]:
                    add(variables.last_hits[i+1][0] - 1, variables.last_hits[i][1])
                if variables.last_hits[i][0] < 10:
                    add(variables.last_hits[i][0] + 1, variables.last_hits[i][1])
                if variables.last_hits[i+1][0] < 10:
                    add(variables.last_hits[i+1][0] + 1, variables.last_hits[i][1])
        variables.around_hit_set = new_hit_set
    
    elif computer_hits and fired_BL not in variables.around_hit_set:
        x, y = fired_BL
        if 1 < x:
            variables.around_hit_set.add((x - 1, y))
        if 1 < y:
            variables.around_hit_set.add((x, y - 1))
        if x < 10:
            variables.around_hit_set.add((x+1, y))
        if y < 10:
            variables.around_hit_set.add((x, y+1))
    elif not computer_hits:
        variables.around_hit_set.discard(fired_BL)

    variables.around_hit_set -= variables.dotted_to_shoot
    variables.around_hit_set -= variables.for_comp_to_shoot
    variables.ava_to_fire_set -= variables.around_hit_set
    variables.ava_to_fire_set -= variables.dotted_to_shoot

def Draw_hit_Bl(hit_Bl):
    for block in hit_Bl:
        x1 = variables.block_sz * (block[0]-1) + variables.l_margin
        y1 = variables.block_sz * (block[1]-1) + variables.upp_margin
        pygame.draw.line(variables.screen, variables.BL, (x1, y1),(x1+variables.block_sz, y1+variables.block_sz), variables.block_sz//7)
        pygame.draw.line(variables.screen, variables.BL, (x1, y1+variables.block_sz),(x1+variables.block_sz, y1), variables.block_sz//7)

def show_mess(mess, r, w_f = variables.font):
    mess_w, mess_h = w_f.size(mess)
    mess_r = pygame.Rect(r)
    x = mess_r.centerx - mess_w /2
    y = mess_r.centery - mess_h /2
    backgr_r = pygame.Rect(x - variables.block_sz /2, y, mess_w + variables.block_sz, mess_h)
    mess_blit = w_f.render(mess, True, variables.RED)
    variables.screen.fill(variables.WH, backgr_r)
    variables.screen.blit(mess_blit, (x, y))

def main():
    variables.screen.fill(variables.WH)
    f = True
    draw.grid()
    sign()
    draw.ship(variables.human.ships)
    rect_button = (650, 352, 194, 72)
    game_over = False
    comp_turn = False
    while f:
        st_button.Draw()
        st_button.change_cl()
        pygame.display.update()
        m = pygame.mouse.get_pos()
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                f = False
            elif i.type == pygame.MOUSEBUTTONDOWN and st_button.rect.collidepoint(m):
                f = False
        pygame.display.update()
        variables.screen.fill(variables.WH, (650, 332, 154, 72))

    while not game_over:
        for i in pygame.event.get():
            if i.type == pygame.QUIT:
                game_over = True
            elif not comp_turn and i.type == pygame.MOUSEBUTTONDOWN:
                x, y = i.pos
                if 100 <= x <= 600 and 80 <= y <= 580:
                    if (variables.l_margin < x < variables.l_margin + 10*variables.block_sz) and (variables.upp_margin < y < variables.upp_margin + 10*variables.block_sz):
                        fired_BL = ((x - variables.l_margin) // variables.block_sz + 1,
                                        (y - variables.upp_margin) // variables.block_sz + 1)
                    comp_turn = not hit_or_miss(
                        fired_BL, variables.ship_w, comp_turn)

        if comp_turn:
            if variables.around_hit_set:
                comp_turn = shoot(variables.around_hit_set)
            else:
                comp_turn = shoot(variables.ava_to_fire_set)

        draw.dotted(variables.dotted)
        Draw_hit_Bl(variables.hit_Bl)
        draw.ship(variables.destroyed_ships)
        if not variables.computer.ships_set:
            show_mess("YOU WIN!", (0, 0, variables.size[0], variables.size[1]), variables.gameover_f)
        if not variables.human.ships_set:
            show_mess("YOU LOSE!", (0, 0, variables.size[0], variables.size[1]), variables.gameover_f)
            draw.ship(variables.computer.ships)
        pygame.display.update()

main()
pygame.quit()
