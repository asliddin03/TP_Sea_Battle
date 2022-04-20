import global_variable as glob_var


def dotted_and_hit(fired_BL, comp_turn, diagonal_only=True):
    a, b = fired_BL
    x, y = 0, 11
    if comp_turn:
        a += 15
        x += 15
        y += 15
        glob_var.for_comp_to_shoot.add(fired_BL)
    glob_var.hit_Bl.add((a, b))
    for i in range(-1, 2):
        for j in range(-1, 2):
            if not diagonal_only and x < a + i < y and 0 < b + j < 11:
                glob_var.dotted.add((a+i, b+j))
                if comp_turn:
                    glob_var.dotted_to_shoot.add((fired_BL[0]+i, b+j))
    glob_var.dotted -= glob_var.hit_Bl