from OpenGL.GL import *
from OpenGL.GLUT import *

def draw_cube():
    vertices = [
        [0,0,0], [0,0,1], [1,0,1], [1,0,0],
        [0,1,0], [0,1,1], [1,1,1], [1,1,0]
    ]
    faces = [
        [0,1,2,3], [4,5,6,7], [1,5,6,2],
        [0,4,7,3], [3,2,6,7], [0,1,5,4]
    ]
    glBegin(GL_QUADS)
    for face in faces:
        for vertex in face:
            glVertex3fv(vertices[vertex])
    glEnd()

def draw_komoda():
    # Korpus – jasny brąz
    glPushMatrix()
    glColor3f(0.8, 0.5, 0.2)  # <-- ustawienie koloru KORPUSU
    glTranslatef(0.0, -0.5, -2.5)
    glScalef(1.5, 1.0, 0.5)
    draw_cube()
    glPopMatrix()

    # Uchwyt 1 – ciemny szary
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)  # <-- ustawienie koloru UCHWYTU
    glTranslatef(-0.3, -0.1, -2.0)
    glScalef(0.1, 0.2, 0.05)
    draw_cube()
    glPopMatrix()

    # Uchwyt 2 – ciemny szary
    glPushMatrix()
    glColor3f(0.3, 0.3, 0.3)
    glTranslatef(0.4, -0.1, -2.0)
    glScalef(0.1, 0.2, 0.05)
    draw_cube()
    glPopMatrix()
