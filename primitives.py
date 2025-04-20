import math

class GameObject:
    def __init__(self, game):
        self.game = game

    def update(self, dt, events):
        raise NotImplementedError()

    def draw(self, surf, offset = (0, 0)):
        raise NotImplementedError()

class Pose:
    def __init__(self, position, angle = 0):
        """ИНИЦИАЛИЗИРУЕМ ПОЗИЦИЮ
            Позиция -> двумерный кортеж (x,y)
            угол -> угол в градусах против часовой стрелки справа
        """
        self.set_position(position)
        self.angle = angle

    def set_x(self, new_x):
        self.x = new_x
    def set_y(self, new_y):
        self.y = new_y
    def set_position(self, position):
        self.x, self.y = position

    def set_angle(self,angle):
        self.angle = angle

    def get_position(self):
        return self.x, self. y

    def get_angle_of_position(self):
        return math.atan2(-self.y, self.x)

    def get_angle_randians(self):
        return self.angle*math.pi/180

    def get_unit_vector(self):
        """Возвращает единичный вектор равный углу в позиции"""

        unit_x = math.cos(self.get_angle_radians())
        unit_y = -math.sin(self.get_angle_radians())
        return unit_x, unit_y

    def get_weighted_position(self, weight):
        return self.x*weight, self.y*weight

    def add_position(self, position):
        add_x, add_y = position
        self.set_x(self.x + add_x)
        self.set_y(self.y + add_y)

    def add_angle(self, angle):
        self.set_angle(self.angle + angle)

    def rotate_position(self, angle):
        x = self.x*math.cos(angle*math.pi/180) - self.y*math.sin(angle*math.pi/180)
        y = -self.x*math.sin(angle*math.pi/180) - self.y*math.cos(angle*math.pi/180)
        self.set_position((x, y))
        

