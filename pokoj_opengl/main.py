from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
from load_objects import *
import numpy as np
import sys
import pygame
import pywavefront
import pygame
from pygame.locals import *
import pywavefront

# Pozycja i orientacja kamery
camera_pos = np.array([0.0, 1.0, 5.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw, pitch = -90.0, 0.0

# Sterowanie
keys = set()
last_x, last_y = 400, 300
first_mouse = True
speed = 0.1
sensitivity = 0.2

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 800 / 600, 0.1, 100.0)

def draw_cube(x, y, z, size, color):
    glPushMatrix()
    glTranslatef(x, y, z)
    glScalef(size, size, size)
    glColor3f(*color)
    glutSolidCube(1)
    glPopMatrix()

def draw_room():
    # Podłoga
    glColor3f(0.6, 0.4, 0.2)
    glPushMatrix()
    glTranslatef(0, -1, 0)
    glScalef(10, 0.1, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Sufit
    glColor3f(0.9, 0.9, 0.9)
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    glScalef(10, 0.1, 10)
    glutSolidCube(1)
    glPopMatrix()

    # Ściany
    wall_color = (0.8, 0.8, 0.9)
    for pos, scale in [((-5, 0.75, 0), (0.1, 3, 10)), ((5, 0.75, 0), (0.1, 3, 10)),
                       ((0, 0.75, -5), (10, 3, 0.1)), ((0, 0.75, 5), (10, 3, 0.1))]:
        glColor3f(*wall_color)
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(*scale)
        glutSolidCube(1)
        glPopMatrix()

def draw_furniture():
    draw_cube(0, -0.3, 0, 1.5, (0.4, 0.2, 0.1))  # Stół
    draw_cube(2, -0.5, 2, 1.0, (0.6, 0.3, 0.2))  # Szafka
    draw_cube(-2, 0.0, -3, 1.0, (0.0, 0.0, 0.0))  # Telewizor

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()

    center = camera_pos + camera_front
    gluLookAt(*camera_pos, *center, *camera_up)

    draw_room()
    draw_furniture()

    glutSwapBuffers()

def update_camera():
    global camera_pos
    front = camera_front / np.linalg.norm(camera_front)
    right = np.cross(front, camera_up)
    right /= np.linalg.norm(right)

    if b'w' in keys:
        camera_pos[:] += front * speed
    if b's' in keys:
        camera_pos[:] -= front * speed
    if b'a' in keys:
        camera_pos[:] -= right * speed
    if b'd' in keys:
        camera_pos[:] += right * speed

def timer(v):
    update_camera()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def key_down(key, x, y):
    keys.add(key)
    if key == b'\x1b':  # ESC
        sys.exit()

def key_up(key, x, y):
    keys.discard(key)

def mouse_motion(x, y):
    global yaw, pitch, camera_front, last_x, last_y, first_mouse

    if first_mouse:
        last_x, last_y = x, y
        first_mouse = False

    dx = x - last_x
    dy = last_y - y
    last_x, last_y = x, y

    dx *= sensitivity
    dy *= sensitivity

    yaw += dx
    pitch += dy
    pitch = max(-89.0, min(89.0, pitch))

    rad_yaw = np.radians(yaw)
    rad_pitch = np.radians(pitch)

    front = np.array([
        np.cos(rad_yaw) * np.cos(rad_pitch),
        np.sin(rad_pitch),
        np.sin(rad_yaw) * np.cos(rad_pitch)
    ])
    camera_front[:] = front / np.linalg.norm(front)

def main():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Pokoj z ruchem FPS (WASD + mysz)")
    init()

    glutDisplayFunc(display)
    glutKeyboardFunc(key_down)
    glutKeyboardUpFunc(key_up)
    glutPassiveMotionFunc(mouse_motion)
    glutTimerFunc(0, timer, 0)

    glutMainLoop()

if __name__ == "__main__":
    main()
