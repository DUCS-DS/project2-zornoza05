# gen_art_v2.py           Basic generative art demo v2           Simmons Feb '23

import random, math, pygame


def radians(degrees):
    """convert degrees to radians"""
    return math.pi / 180 * degrees


def blue(scale=0.8):
    """return the rgb of a shade of blue"""
    assert 0 <= scale <= 1, f"scale must be between 0 and 1 inclusive, not {scale}"
    num = int(scale * 255)
    return (num // 2, 2 * num // 3, num)


class Node:
    def __init__(self, x, y, speed, angle):
        """create a node"""
        self.x = x
        self.y = y
        self.speed = speed
        self.angle = angle
        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed

    def move(self):
        """move the node"""
        self.x = self.x + self.dx
        self.y = self.y + self.dy

    def draw(self):
        """draw the node to the screen"""
        pygame.draw.circle(screen, blue(), (int(self.x), int(self.y)), node_radius)

    def reflect(self):
        """reflect off a boundary of the screen"""
        if self.x > winwidth - node_radius:  # right edge
            self.x = 2 * (winwidth - node_radius) - self.x
            self.angle = -self.angle
        elif self.x < node_radius:  # left edge
            self.x = 2 * node_radius - self.x
            self.angle = -self.angle
        if self.y > winheight - node_radius:  # bottom edge
            self.y = 2 * (winheight - node_radius) - self.y
            self.angle = math.pi - self.angle
        elif self.y < node_radius:  # top edge
            self.y = 2 * node_radius - self.y
            self.angle = math.pi - self.angle
        self.dx = math.sin(self.angle) * self.speed
        self.dy = math.cos(self.angle) * self.speed


winwidth = 800  # width of window
winheight = 600  # height of window
background = (5, 5, 5)  # this is close to black

# set generative parameters
num_nodes = 400
node_radius = 0
thresh = 1800

# initialize pygame
screen = pygame.display.set_mode((winwidth, winheight))
clock = pygame.time.Clock()
pygame.init()
pygame.display.set_caption("Triangles v2")
pygame.event.set_allowed([pygame.QUIT, pygame.KEYUP, pygame.KEYDOWN])

# create nodes
nodes = []
for i in range(num_nodes):
    x = random.randint(0, winwidth)
    y = random.randint(0, winheight)
    speed = random.randint(150, 200) / 600
    angle = radians(random.randint(0, 359))
    nodes.append(Node(x, y, speed, angle))

def getx(node):
    return node.x    

# the game loop: (press q to quit)
quit = False
while not quit:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            quit = True
            break
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_q:
                quit = True
                break
    if quit:
        break

    screen.fill(background)
    for node in nodes:
        node.move()
        node.reflect()
        node.draw()

    nodes = sorted(nodes, key = getx)    

    for i, node1 in enumerate(nodes):
        x1, y1 = node1.x, node1.y
        for node2 in nodes[i + 1 : i + 20]:
            x2, y2 = node2.x, node2.y
            d_squared = (x1 - x2) ** 2 + (y1 - y2) ** 2
            if d_squared < thresh:
                pygame.draw.aaline(
                    screen, blue((thresh - d_squared) / thresh), (x1, y1), (x2, y2)
                )

    clock.tick(60)
    pygame.display.flip()
    print(clock.get_fps())

pygame.quit()
