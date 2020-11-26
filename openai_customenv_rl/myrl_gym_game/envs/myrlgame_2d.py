import pygame
import math

screen_width = 1500
screen_height = 800
checkpoints = ((1200, 660), (1250, 120), (190, 200), (1030, 270), (250, 475), (650, 690))

class Car:
    def __init__(self, car_image, map_image, car_starting_position):
        self.surface = pygame.image.load(car_image)
        self.map = pygame.image.load(map_image)
        self.surface = pygame.transform.scale(self.surface, (100, 100))
        self.rotate_surface = self.surface
        self.pos = car_starting_position
        self.angle = 0
        self.speed = 0
        self.center = [self.pos[0] + 50, self.pos[1] + 50]
        self.radars = []
        self.radars_for_draw = []
        self.is_alive = True
        self.current_check = 0
        self.prev_distance = 0
        self.cur_distance = 0
        self.goal = False
        self.check_flag = False
        self.distance = 0
        self.time_spent = 0

        # we have 5 radars, their angles are -90, -45, 0, 45, 90
        for d in range(-90, 120, 45):
            self.check_radar(d)

        # we need to create those 5 radars
        for d in range(-90, 120, 45):
            self.check_radar_for_draw(d)

    def draw(self, screen):
        screen.blit(self.rotate_surface, self.pos)

    def draw_collision(self, screen):
        for i in range(4):
            x = int(self.four_points[i][0])
            y = int(self.four_points[i][1])
            pygame.draw.circle(screen, (255, 255, 255), (x, y), 5)

    def draw_radar(self, screen):
        for r in self.radars_for_draw:
            pos, dist = r
            pygame.draw.line(screen, (0, 255, 0), self.center, pos, 1)
            pygame.draw.circle(screen, (0, 255, 0), pos, 5)

    def check_collision(self):
        self.is_alive = True
        for p in self.four_points:
            if self.map.get_at((int(p[0]), int(p[1]))) == (255, 255, 255, 255):
                self.is_alive = False
                break

    def check_radar(self, degree):

        # initially the length is 0 because the radar will start searching from minimum distance which is 0.

        len = 0

        # There are 5 radars, if the car is at 0 angle, in other words, if the car is straight then
        # the degrees of those 5 radars are radar 1 : 90 or 450, radar 2: 45 or 405, radar 3: 0 or 360, radar 4: 315, radar 5: 270
        # 360 - (0 + (-90)) == 450, 360 - (0 + (-45)) == 405, 360 - (0 + (0)) == 360, 360 - (0 + (45)) == 315, 360 - (0 + (90)) == 270 .

        # print(math.radians(450))
        # print(math.radians(405))
        # print(math.radians(360))
        # print(math.radians(315))
        # print(math.radians(270))
        #
        # 7.853981633974483
        # 7.0685834705770345
        # 6.283185307179586
        # 5.497787143782138
        # 4.71238898038469
        #
        # print(math.cos(7.85))
        # print(math.cos(7.06))
        # print(math.cos(6.28))
        # print(math.cos(5.49))
        # print(math.cos(4.71))
        #
        # 0.003981623454079739
        # 0.7131500886813729
        # 0.9999949269133752
        # 0.701579055431586
        # -0.0023889781122815386

        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        # Until there is a white area, which means outside of the road, we will increase the length of the distance to search for. Our radar
        # can search for within maximum distance 10. So, if the length is greater than  300 , then we will not search because our radar can not detect
        # anything outside that distance and 300 / 30 is 10 .

        while not self.map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
            len = len + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars.append([(x, y), dist])

    def check_radar_for_draw(self, degree):
        len = 0
        x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
        y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        while not self.map.get_at((x, y)) == (255, 255, 255, 255) and len < 300:
            len = len + 1
            x = int(self.center[0] + math.cos(math.radians(360 - (self.angle + degree))) * len)
            y = int(self.center[1] + math.sin(math.radians(360 - (self.angle + degree))) * len)

        dist = int(math.sqrt(math.pow(x - self.center[0], 2) + math.pow(y - self.center[1], 2)))
        self.radars_for_draw.append([(x, y), dist])

    def check_checkpoint(self):
        p = checkpoints[self.current_check]
        self.prev_distance = self.cur_distance
        dist = get_distance(p, self.center)
        if dist < 70:
            self.current_check += 1
            self.prev_distance = 9999
            self.check_flag = True
            if self.current_check >= len(checkpoints):
                self.current_check = 0
                self.goal = True
            else:
                self.goal = False

        self.cur_distance = dist

    def update(self):
        #check speed
        self.speed -= 0.5
        if self.speed > 10:
            self.speed = 10
        if self.speed < 1:
            self.speed = 1

        # Rotate the image if turn left or right
        self.rotate_surface = rot_center(self.surface, self.angle)

        # check if the car is at the edge of the screen
        self.pos[0] += math.cos(math.radians(360 - self.angle)) * self.speed
        if self.pos[0] < 20:
            self.pos[0] = 20
        elif self.pos[0] > screen_width - 120:
            self.pos[0] = screen_width - 120

        self.pos[1] += math.sin(math.radians(360 - self.angle)) * self.speed
        if self.pos[1] < 20:
            self.pos[1] = 20
        elif self.pos[1] > screen_height - 120:
            self.pos[1] = screen_height - 120

        self.distance += self.speed
        self.time_spent += 1

        # caculate 4 collision points
        self.center = [int(self.pos[0]) + 50, int(self.pos[1]) + 50]
        len = 40
        left_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 30))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 30))) * len]
        right_top = [self.center[0] + math.cos(math.radians(360 - (self.angle + 150))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 150))) * len]
        left_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 210))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 210))) * len]
        right_bottom = [self.center[0] + math.cos(math.radians(360 - (self.angle + 330))) * len, self.center[1] + math.sin(math.radians(360 - (self.angle + 330))) * len]
        self.four_points = [left_top, right_top, left_bottom, right_bottom]

class MyGame2D:
    # The following function will be called from the __init__ and the reset function in custom_env.py file
    def __init__(self):
        pygame.init()
        # set GUI screen
        self.screen = pygame.display.set_mode((screen_width,screen_hight))
        # set timer
        self.clock = pygame.time.Clock()
        # set style of the text to display on screen
        self.font = pygame.font.SysFont('Arial', 30)
        # Initialize a car object by passing car image and road image
        self.car = Car('car.png', 'map.png', [700,650])
        self.game_speed = 60
        self.mode = 0

    def observe(self):
        # return state
        radars = self.car.radars
        print("radars :", radars)
        ret = [0, 0, 0, 0, 0]
        for i, r in enumerate(radars):
            ret[i] = int(r[1] / 30)

        return tuple(ret)

    def action_to_take(self, action):
        if action == 0:
            self.car.speed += 2 # move forward
        if action == 1:
            self.car.angle += 5 # turn right
        elif action == 2:
            self.car.angle -= 5 # turn left

        self.car.update()
        self.car.check_collision()
        self.car.check_checkpoint()

        # This is important, we need to clear the previous observation.
        # Because the car's angle may have changed in the new state. If we
        # Update on the previous observation, we may not get the correct new x,y coordinates and dist of the radars.
        self.car.radars.clear()

        # Now create new radars to take new observation from the car's new state.
        for d in range(-90, 120, 45):
            self.car.check_radar(d)

    def evaluate(self):
        reward = 0
        """
        if self.car.check_flag:
            self.car.check_flag = False
            reward = 2000 - self.car.time_spent
            self.car.time_spent = 0
        """
        if not self.car.is_alive:
            reward = -10000 + self.car.distance

        elif self.car.goal:
            reward = 10000
        return reward

    def view(self):
        # draw game
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_m:
                    self.mode += 1
                    self.mode = self.mode % 3

        self.screen.blit(self.car.map, (0, 0))

        if self.mode == 1:
            self.screen.fill((0, 0, 0))

        self.car.radars_for_draw.clear()
        for d in range(-90, 120, 45):
            self.car.check_radar_for_draw(d)

        pygame.draw.circle(self.screen, (255, 255, 0), check_point[self.car.current_check], 70, 1)
        self.car.draw_collision(self.screen)
        self.car.draw_radar(self.screen)
        self.car.draw(self.screen)

        text = self.font.render("Press 'm' to change view mode", True, (255, 255, 0))
        text_rect = text.get_rect()
        text_rect.center = (screen_width / 2, 100)
        self.screen.blit(text, text_rect)

        pygame.display.flip()
        self.clock.tick(self.game_speed)

def get_distance(p1, p2):
    return math.sqrt(math.pow((p1[0] - p2[0]), 2) + math.pow((p1[1] - p2[1]), 2))

# Rotate the image but do not change the center and size of the image.
def rot_center(image, angle):
    orig_rect = image.get_rect()
    rot_image = pygame.transform.rotate(image, angle)
    rot_rect = orig_rect.copy()
    # update the center of the rotated image rectangle after the rotation
    rot_rect.center = rot_image.get_rect().center
    # subsurface gets you a surface that represents a rectangular section of a larger surface.
    # The subsurface function creates a new surface that references its parent
    rot_image = rot_image.subsurface(rot_rect).copy()
    return rot_image







