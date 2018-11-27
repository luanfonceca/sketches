# Author: Berin
# Sketches repo: https://github.com/berinhard/sketches

from random import choice, shuffle
from save_frames import save_video_frames
import json


WHITE = color(235, 235, 235, 130)
BLACK = color(27, 27, 27)


COLORS = None
def get_color_palette():
    global COLORS

    if not COLORS:
        with open("data/1000.json") as fd:
            colors = json.load(fd)
            COLORS = choice(colors)

    return COLORS

MIN_RADIUS = 50
MAX_RADIUS = 200

class Bokeh(object):

    def __init__(self):
        self.radius = 1
        self.x = choice(range(width))
        self.y = choice(range(height))
        self.velocity = PVector(2, 2)
        self.color = choice(get_color_palette())
        self.skip_step = random(0.2, 0.7)

    @property
    def dead(self):
        return self.radius > MAX_RADIUS

    def move(self, ref_point):
        direction = PVector(self.x, self.y)
        direction.sub(ref_point)
        direction.normalize()
        diff = height / direction.dist(PVector(self.x, self.y))
        direction.mult(2 * diff)
        self.x += self.velocity.x * direction.x
        self.y += self.velocity.y * direction.y

    def update(self, ref_point):
        self.move(ref_point)
        self.radius += 1

    def display(self):
        r = red(self.color)
        g = green(self.color)
        b = blue(self.color)
        a = map(self.radius, MIN_RADIUS, MAX_RADIUS, 100, 20)

        if random(1) > self.skip_step:
            return
        stroke(color(r, g, b, a))

        for r in range(10, self.radius, 50):
            ellipse(self.x, self.y, r, r)

bokeh_list = []

def setup():
    global px, py

    fullScreen()
    background(BLACK)
    colorMode(RGB, 100)
    #frameRate(24)
    noCursor()
    noFill()
    strokeWeight(2)

    px = random(1) * width
    py = random(1) * height

def draw():
    #background(BLACK)
    global bokeh_list, px, py, COLORS

    ref_point = PVector(px, py)

    bokeh_list.append(Bokeh())
    bokeh_list.append(Bokeh())
    bokeh_list = sorted(
        [b for b in bokeh_list if not b.dead],
        key=lambda b: b.radius,
    )
    for bokeh in bokeh_list:
        bokeh.display()
        bokeh.update(ref_point)

    #save_video_frames(24, 60 * 10)t



def keyPressed():
    global COLORS, bokeh_list
    if key == 'n':
        background(BLACK)
        COLORS = None
        global px, py
        px = random(1) * width
        py = random(1) * height
        bokeh_list = []
    elif key == 's':
        saveFrame("##########.png")