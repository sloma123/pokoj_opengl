from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
#from komoda import draw_komoda

class Furniture:
    def __init__(self, name, pos, size, color, rotation=0):
        self.name = name
        self.pos = np.array(pos, dtype=np.float32)
        self.size = size
        self.color = color
        self.rotation = rotation

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glRotatef(self.rotation, 0, 1, 0)
        self.draw_geometry()
        glPopMatrix()

    def draw_geometry(self):
        # domyślny sześcian
        glPushMatrix()
        glScalef(self.size, self.size, self.size)
        glColor3f(*self.color)
        glutSolidCube(1)
        glPopMatrix()

    def contains_ray(self, ray_origin, ray_dir):
        t_min = -np.inf
        t_max = np.inf
        bounds_min = self.pos - self.size / 2
        bounds_max = self.pos + self.size / 2
        for i in range(3):
            if abs(ray_dir[i]) < 1e-8:
                if ray_origin[i] < bounds_min[i] or ray_origin[i] > bounds_max[i]:
                    return False
            else:
                t1 = (bounds_min[i] - ray_origin[i]) / ray_dir[i]
                t2 = (bounds_max[i] - ray_origin[i]) / ray_dir[i]
                t_min = max(t_min, min(t1, t2))
                t_max = min(t_max, max(t1, t2))
                if t_max < t_min:
                    return False
        return True

class Komoda(Furniture):
    def __init__(self, pos):
        super().__init__("komoda", pos, 1.0, (0.2, 0.4, 0.8))  # niebieska komoda


class Stol(Furniture):
    def __init__(self, pos):
        super().__init__("stol", pos, 1.5, (0.4, 0.2, 0.1))

class TV(Furniture):
    def __init__(self, pos):
        super().__init__("tv", pos, 1.0, (0.0, 0.0, 0.0))
