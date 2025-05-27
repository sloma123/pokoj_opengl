from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np

class Furniture:
    def __init__(self, name, pos, size, color, rotation=0):
        self.name = name
        self.pos = np.array(pos, dtype=np.float32)
        self.size = size
        self.color = color
        self.rotation = rotation
        self.is_selected = False

    def draw(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        glRotatef(self.rotation, 0, 1, 0)

        # Rysowanie bryły
        self.draw_geometry()

        # Podświetlenie zaznaczenia
        if self.is_selected:
            glPushAttrib(GL_ENABLE_BIT)
            glDisable(GL_LIGHTING)
            glColor3f(1.0, 0.0, 0.0)  # czerwony
            glLineWidth(3.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE) # tryb linii
            glScalef(self.size * 1.01, self.size * 1.01, self.size * 1.01)
            glutWireCube(1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopAttrib()

        glPopMatrix()

    def draw_geometry(self):
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
            if abs(ray_dir[i]) < 1e-8: # Sprawdzenie, czy promień jest równoległy do osi, porównanie z małą wartośćią przez float
                if ray_origin[i] < bounds_min[i] or ray_origin[i] > bounds_max[i]:
                    return False
            else:
                # Obliczanie przecięcia promienia z granicami obiektu
                t1 = (bounds_min[i] - ray_origin[i]) / ray_dir[i] # promień przecina początek obiektu
                t2 = (bounds_max[i] - ray_origin[i]) / ray_dir[i] # promień przecina koniec obiektu
                t_min = max(t_min, min(t1, t2)) 
                t_max = min(t_max, max(t1, t2))
                if t_max < t_min: #promień nie przecina obiektu
                    return False
        return True

class Komoda(Furniture):
    def __init__(self, pos):
        super().__init__("komoda", pos, 1.0, (0.2, 0.4, 0.8))

class Stol(Furniture):
    def __init__(self, pos):
        super().__init__("stol", pos, 1.5, (0.4, 0.2, 0.1))

class TV(Furniture):
    def __init__(self, pos):
        super().__init__("tv", pos, 1.0, (0.0, 0.0, 0.0))
