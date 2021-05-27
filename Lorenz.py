import numpy as np, pygame as pg, timeit

pg.init()
pg.display.set_caption("Lorenz Attractor")

xmax = 1920  # width of the window/map
ymax = 1080  # height of the window/map
scr = pg.display.set_mode((xmax, ymax))

## Attractor Parameters
rho = 28.0
sigma = 10.0
beta = 8.0 / 3.0
dt = 0.002

class Particle():
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z


def convect(particle):
    dxdt = sigma*(particle.y-particle.x)
    dydt = particle.x*(rho-particle.z)-particle.y
    dzdt = particle.x*particle.y - beta*particle.z

    return dxdt*dt, dydt*dt, dzdt*dt


## initialize particles
particles = []
rangee = 50
for i in range(rangee):
    particles.append(Particle(0.99+np.random.randint(1000)/50000, 0.99+np.random.randint(1000)/50000, 0.99+np.random.randint(1000)/50000))

running = 1
theta = 0
toc = timeit.default_timer()
while running:
    tic = timeit.default_timer()
    # print(tic-toc)
    darken_percent = .01
    dark = pg.Surface(scr.get_size()).convert_alpha()
    dark.fill((0, 0, 0, darken_percent * 255))
    scr.blit(dark, (0, 0))

    # theta += 2*np.pi*(tic-toc)/100000

    ## convecting each particle over one time step
    for i in range(len(particles)):
        subject = particles[i]
        dx, dy, dz = convect(subject)

        screen_x, screen_y = subject.x*np.cos(theta)+subject.z*np.sin(theta), subject.y

        pos1 = (screen_x*15+xmax/2, screen_y*15+ymax/2)

        subject.x = subject.x + dx
        subject.y = subject.y + dy
        subject.z = subject.z + dz

        red = min(130+dx**2*60, 254)
        green = min(max(100+dy**2*60,0),254)
        blue = min(130+dz**2*50, 254)

        colours = (red, green, blue)

        screen_x, screen_y = subject.x * np.cos(theta) + subject.z * np.sin(theta), subject.y

        pos2 = (screen_x*15+xmax/2, screen_y*15+ymax/2)

        # pg.draw.circle(scr, colours, pos2, 1)
        pg.draw.line(scr, colours, pos1, pos2, 2)

    for event in pg.event.get():
        # Stay in main loop until pygame.quit event is sent
        if event.type == pg.QUIT:
            running = 0
        elif event.type == pg.KEYDOWN:
            # Escape key, end sim
            if event.key == pg.K_ESCAPE:
                running = 0

    pg.display.flip()

pg.quit()