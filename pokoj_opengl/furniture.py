
from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import pywavefront

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
        self.draw_geometry()
        if self.is_selected:
            glPushAttrib(GL_ENABLE_BIT)
            glDisable(GL_LIGHTING)
            glColor3f(1.0, 0.0, 0.0)
            glLineWidth(3.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
            glScalef(self.size * 1.01, self.size * 1.01, self.size * 1.01)
            glutWireCube(1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopAttrib()
        glPopMatrix()

    def draw_geometry(self):
        glPushMatrix()
        glScalef(self.size, self.size, self.size)
        glDisable(GL_LIGHTING)
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




class Stol(Furniture):
    def __init__(self, pos):
        super().__init__("stol", pos, 1.0, (0.4, 0.2, 0.1))
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/TableAndChair.obj',
            collect_faces=True,
            create_materials=True
        )

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(*self.pos)
        #glScalef(0.8, 0.8, 0.8)  # zwiększona skala

        glDisable(GL_LIGHTING)
        glColor3f(*self.color)

        for mesh in self.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.model.vertices[vertex_i])
            glEnd()
        glPopMatrix()



class Regal(Furniture):
    def __init__(self, pos):
        super().__init__("regal", pos, 1.0, (0.7, 0.5, 0.3))
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/oak_bookshelf.obj',
            collect_faces=True,
            create_materials=True
        )

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(0, 0, 0)
        glScalef(0.01, 0.01, 0.01)
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)  # <-- Użyj dynamicznego koloru

        for mesh in self.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.model.vertices[vertex_i])
            glEnd()

        glPopMatrix()


class Szafa(Furniture):
    def __init__(self, pos):
        super().__init__("szafa", pos, 1.0, (0.6, 0.4, 0.3))
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/Wardrobe.obj',
            collect_faces=True,
            create_materials=True
        )

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(0, 0, 0)
       # glScalef(0.01, 0.01, 0.01)
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)

        for mesh in self.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.model.vertices[vertex_i])
            glEnd()

        glPopMatrix()


class Lozko(Szafa):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "lozko"
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/Bed.obj',
            collect_faces=True,
            create_materials=True
        )

class Koldra(Lozko):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "koldra"
        self.color = (1.0, 1.0, 1.0)  # kolor biały, możesz zmienić
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/koldra.obj',
            collect_faces=True,
            create_materials=True
        )

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(0, 0.1, 0)  # przesunięcie lokalne o 0.1 w górę
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)

        for mesh in self.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.model.vertices[vertex_i])
            glEnd()
        glPopMatrix()


class Komoda(Szafa):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "komoda"
        self.color = (0.2, 0.4, 0.8)
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/SideTable.obj',
            collect_faces=True,
            create_materials=True
        )

class TV(Szafa):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "tv"
        self.color = (0.0, 0.0, 0.0)
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/FlatScreenTelevision.obj',
            collect_faces=True,
            create_materials=True
        )
    def draw_geometry(self):
        glPushMatrix()
        glScalef(0.5, 0.5, 0.5)  # ewentualne skalowanie
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)

        for mesh in self.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.model.vertices[vertex_i])
            glEnd()
        glPopMatrix()

    