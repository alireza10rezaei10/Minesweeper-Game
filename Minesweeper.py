# imports ---------------------------------------------------

import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle, Circle
from matplotlib.animation import FuncAnimation
import random
from time import sleep


# configs ---------------------------------------------------

mine_count = 10
figsize = 5


# building our fiqure ---------------------------------------

fig = plt.figure(figsize=(figsize, figsize))
ticks = [x for x in range(0, 10)]
surf = fig.subplots()
plt.xlim([0, 10])
plt.ylim([0, 10])
plt.xticks(ticks)
plt.yticks(ticks)
surf.grid(True, lw=5)


# classes ---------------------------------------------------

class Target:
    _all = {}
    hidden_targets = 100
    game_over = False

    def __init__(self, x, y, row, col):
        self.x = x
        self.y = y
        self.is_mine = False
        self.has_flag = False
        self.flag_text = surf.text(x=x+0.35, y=y+0.35, s='?',
                                   fontsize=15, visible=False,
                                   color='green')
        self.hide = True
        self.number = 0
        self.neighbours = None
        self.row = row
        self.col = col

    def click(self, mouse_x=-50, mouse_y=-50, button='LEFT', from_neighbour=False):
        # mige ini ke seda zadan man bodam ya na?
        if self.hide:
            if self.me(mouse_x, mouse_y) or from_neighbour:
                if button == 'LEFT':
                    if self.is_mine:
                        Target.game_over = True
                        for t in Target._all.values():
                            t.show()

                    else:
                        self.show()
                        if self.number == 0:
                            self.click_on_neighbours()

                else:
                    self.show(button='RIGHT')

    def me(self, mouse_x, mouse_y):
        if mouse_x < self.x+1 and mouse_x > self.x and mouse_y < self.y+1 and mouse_y > self.y:
            return True
        else:
            return False

    def show(self, button='LEFT'):
        if button == 'LEFT':

            if self.has_flag:
                self.has_flag = False
                self.flag_text.set_visible(self.has_flag)

            if self.is_mine:
                surf.add_patch(Circle(
                    xy=[self.x+0.5, self.y+0.5],
                    radius=0.3
                ))
            elif self.number != 0:
                surf.text(
                    x=self.x+0.35,
                    y=self.y+0.35,
                    s=self.number
                )
            else:
                surf.add_patch(Rectangle(
                    xy=[self.x, self.y],
                    width=1,
                    height=1,
                    color='gray'
                ))

            self.hide = False
            Target.hidden_targets -= 1

        if button == 'RIGHT':
            self.has_flag = not self.has_flag
            self.flag_text.set_visible(self.has_flag)

    def find_neighbours(self):
        # find neighbour cells
        row, col = self.row, self.col
        neighbours = []

        # left up right down
        if col != 0:
            neighbours.append(f'{row}-{col-1}')
        if row != 0:
            neighbours.append(f'{row-1}-{col}')
        if col != 9:
            neighbours.append(f'{row}-{col+1}')
        if row != 9:
            neighbours.append(f'{row+1}-{col}')

        # left-up and left-down
        if col != 0:
            if row != 0:
                neighbours.append(f'{row-1}-{col-1}')
            if row != 9:
                neighbours.append(f'{row+1}-{col-1}')

        # right-up and right-down
        if col != 9:
            if row != 0:
                neighbours.append(f'{row-1}-{col+1}')
            if row != 9:
                neighbours.append(f'{row+1}-{col+1}')

        self.neighbours = [Target._all[n] for n in neighbours]

    def find_number(self):
        if not self.is_mine:
            for neighbour in self.neighbours:
                if neighbour.is_mine:
                    self.number += 1

    def click_on_neighbours(self):
        for neighbour in self.neighbours:
            if neighbour.hide:
                if neighbour.number == 0:
                    neighbour.click(from_neighbour=True)
                else:
                    neighbour.show()


# building targets ------------------------------------------

col = 0
for x in range(10):
    row = 0
    for y in range(10):
        Target._all[f'{row}-{col}'] = Target(x=x, y=y, row=row, col=col)
        row += 1
    col += 1

for target in Target._all.values():
    target.find_neighbours()


# puting mines ---------------------------------------------

mine_targets = random.sample(list(Target._all.values()), 10)
for target in mine_targets:
    target.is_mine = True


# finding numbers ------------------------------------------

for target in Target._all.values():
    target.find_number()


# handeling click events -----------------------------------

def on_click(event):
    if event.xdata != None:
        for t in Target._all.values():
            t.click(mouse_x=event.xdata, mouse_y=event.ydata,
                    button=event.button.name)


cid = fig.canvas.mpl_connect('button_press_event', on_click)


# add animations ------------------------------------------


def update(frame):
    if Target.hidden_targets == 10 and not Target.game_over:
        print('you won...')

    if Target.game_over:
        print('you lost...')


anim = FuncAnimation(fig, update, interval=200)
plt.show()
