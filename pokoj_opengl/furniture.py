from OpenGL.GL import *
from OpenGL.GLUT import *
import numpy as np
import pywavefront


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
        self.model = None
        self.scale_factor = 1.0
        self.model_center = np.zeros(3)
        self.model_min = np.zeros(3)
        self.model_size = np.ones(3)

    def get_bounding_box_size(self):
        return self.model_size * self.scale_factor * 1.01

    def get_box_offset(self):
        offset = -self.model_min.copy()
        offset[1] += self.model_center[1] - self.model_min[1]
        return offset * self.scale_factor

    def compute_model_bounds(self):
        all_vertices = np.array(self.model.vertices)
        min_bounds = np.min(all_vertices, axis=0)
        max_bounds = np.max(all_vertices, axis=0)
        self.model_center = (min_bounds + max_bounds) / 2
        self.model_min = min_bounds
        self.model_size = max_bounds - min_bounds

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
            glTranslatef(*self.get_box_offset())
            glScalef(*(self.model_size * self.scale_factor * 1.01))
            glutWireCube(1.0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
            glPopAttrib()

        glPopMatrix()

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(*(-self.model_min * self.scale_factor))
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)
        for mesh in self.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.model.vertices[vertex_i])
            glEnd()
        glPopMatrix()

    def get_bounds(self):
        offset = self.get_box_offset()
        min_corner = self.pos + offset
        max_corner = min_corner + self.model_size * self.scale_factor * 1.01
        return min_corner, max_corner

    def contains_ray(self, ray_origin, ray_dir):
        t_min = -np.inf
        t_max = np.inf
        bounds_min, bounds_max = self.get_bounds()
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
        self.compute_model_bounds()

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(*(-self.model_min * self.scale_factor))
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
        self.compute_model_bounds()


    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(*(-self.model_min * self.scale_factor))
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)
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
        self.compute_model_bounds()

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(*(-self.model_min * self.scale_factor))
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
        self.compute_model_bounds()

class Koldra(Lozko):
    def __init__(self, pos):
        super().__init__(pos)
        self.name = "koldra"
        self.color = (1.0, 1.0, 1.0)
        self.model = pywavefront.Wavefront(
            'C:/Users/Gosia/projekt_obiektowka_gosia_ola/pokoj_opengl/pokoj_opengl/models/koldra.obj',
            collect_faces=True,
            create_materials=True
        )
        self.compute_model_bounds()

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(*(-self.model_min * self.scale_factor))
        glTranslatef(0, 0.1, 0)
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
        self.compute_model_bounds()

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
        self.compute_model_bounds()

    def draw_geometry(self):
        glPushMatrix()
        glTranslatef(*(-self.model_min * self.scale_factor))
        #glScalef(0.5, 0.5, 0.5)
        glDisable(GL_LIGHTING)
        glColor3f(*self.color)
        for mesh in self.model.mesh_list:
            glBegin(GL_TRIANGLES)
            for face in mesh.faces:
                for vertex_i in face:
                    glVertex3f(*self.model.vertices[vertex_i])
            glEnd()
        glPopMatrix()
