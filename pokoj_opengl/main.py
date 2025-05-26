from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import sys

from furniture import Komoda, Stol, TV

# Kamera
camera_pos = np.array([0.0, 1.0, 5.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw, pitch = -90.0, 0.0
keys = set()
last_x, last_y = 400, 300
first_mouse = True
speed = 0.1
sensitivity = 0.2

# Kolor ścian (RGB 0–1)
wall_color = [0.8, 0.8, 0.9]

# Obiekty
obiekty = [
    Komoda([1.0, -0.5, 1.0]),
    Stol([0.0, -0.3, 0.0]),
    TV([-2.0, 0.0, -3.0])
]

selected_obj = None
dragging = False

def init():
    glEnable(GL_DEPTH_TEST)
    glClearColor(0.5, 0.7, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 800 / 600, 0.1, 100.0)

def draw_room():
    glColor3f(0.6, 0.4, 0.2)
    glPushMatrix()
    glTranslatef(0, -1, 0)
    glScalef(10, 0.1, 10)
    glutSolidCube(1)
    glPopMatrix()

    glColor3f(0.9, 0.9, 0.9)
    glPushMatrix()
    glTranslatef(0, 2.5, 0)
    glScalef(10, 0.1, 10)
    glutSolidCube(1)
    glPopMatrix()

    for pos, scale in [((-5, 0.75, 0), (0.1, 3.5, 10)), ((5, 0.75, 0), (0.1, 3.5, 10)),
                       ((0, 0.75, -5), (10, 3.5, 0.1)), ((0, 0.75, 5), (10, 3.5, 0.1))]:
        glColor3f(*wall_color)
        glPushMatrix()
        glTranslatef(*pos)
        glScalef(*scale)
        glutSolidCube(1)
        glPopMatrix()

def draw_furniture():
    for obj in obiekty:
        obj.is_selected = (obj == selected_obj)
        obj.draw()

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
    if b'w' in keys: camera_pos += front * speed
    if b's' in keys: camera_pos -= front * speed
    if b'a' in keys: camera_pos -= right * speed
    if b'd' in keys: camera_pos += right * speed

def get_ray_from_mouse(x, y):
    viewport = glGetIntegerv(GL_VIEWPORT)
    modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
    projection = glGetDoublev(GL_PROJECTION_MATRIX)
    win_x = x
    win_y = viewport[3] - y
    near_point = gluUnProject(win_x, win_y, 0.0, modelview, projection, viewport)
    far_point = gluUnProject(win_x, win_y, 1.0, modelview, projection, viewport)
    ray_origin = np.array(near_point)
    ray_dir = np.array(far_point) - ray_origin
    ray_dir /= np.linalg.norm(ray_dir)
    return ray_origin, ray_dir

def check_collision(pos1, size1, pos2, size2):
    min1 = np.array(pos1) - size1 / 2
    max1 = np.array(pos1) + size1 / 2
    min2 = np.array(pos2) - size2 / 2
    max2 = np.array(pos2) + size2 / 2
    return (
        max1[0] > min2[0] and min1[0] < max2[0] and
        max1[1] > min2[1] and min1[1] < max2[1] and
        max1[2] > min2[2] and min1[2] < max2[2]
    )

def mouse_click(button, state, x, y):
    global selected_obj, dragging
    if button == GLUT_LEFT_BUTTON:
        if state == GLUT_DOWN:
            ray_origin, ray_dir = get_ray_from_mouse(x, y)
            hit_obj = None
            for obj in obiekty:
                if obj.contains_ray(ray_origin, ray_dir):
                    hit_obj = obj
                    break
            if hit_obj is not None:
                selected_obj = None if selected_obj == hit_obj else hit_obj
                dragging = True
            else:
                selected_obj = None
        elif state == GLUT_UP:
            dragging = False

def mouse_drag(x, y):
    global selected_obj, dragging
    if selected_obj is not None and dragging:
        ray_origin, ray_dir = get_ray_from_mouse(x, y)
        t = (selected_obj.pos[1] - ray_origin[1]) / ray_dir[1]
        point_on_plane = ray_origin + t * ray_dir
        half_size = selected_obj.size / 2
        new_x = np.clip(point_on_plane[0], -5 + half_size, 5 - half_size)
        new_z = np.clip(point_on_plane[2], -5 + half_size, 5 - half_size)
        proposed_pos = np.array([new_x, selected_obj.pos[1], new_z])

        for obj in obiekty:
            if obj is not selected_obj and check_collision(proposed_pos, selected_obj.size, obj.pos, obj.size):
                return
        selected_obj.pos[0], selected_obj.pos[2] = new_x, new_z

def special_input(key, x, y):
    global selected_obj
    if selected_obj:
        if key == GLUT_KEY_LEFT:
            selected_obj.rotation = (selected_obj.rotation - 10) % 360
        elif key == GLUT_KEY_RIGHT:
            selected_obj.rotation = (selected_obj.rotation + 10) % 360

def timer(v):
    update_camera()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def key_down(key, x, y):
    keys.add(key)
    if key == b'\x1b':
        sys.exit()

def key_up(key, x, y):
    keys.discard(key)

def mouse_motion(x, y):
    global yaw, pitch, camera_front, last_x, last_y, first_mouse
    if first_mouse:
        last_x, last_y = x, y
        first_mouse = False
    dx, dy = x - last_x, last_y - y
    last_x, last_y = x, y
    yaw += dx * sensitivity
    pitch += dy * sensitivity
    pitch = max(-89.0, min(89.0, pitch))
    rad_yaw, rad_pitch = np.radians(yaw), np.radians(pitch)
    camera_front[:] = np.array([
        np.cos(rad_yaw) * np.cos(rad_pitch),
        np.sin(rad_pitch),
        np.sin(rad_yaw) * np.cos(rad_pitch)
    ]) / np.linalg.norm(camera_front)

def set_selected(obj):
    global selected_obj
    selected_obj = obj

def set_wall_color(rgb_tuple):
    global wall_color
    wall_color = [c / 255.0 for c in rgb_tuple]

def start_gl():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Pokoj z obiektami")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(key_down)
    glutKeyboardUpFunc(key_up)
    glutPassiveMotionFunc(mouse_motion)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_drag)
    glutSpecialFunc(special_input)
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    import threading
    import gui

    gl_thread = threading.Thread(target=start_gl)
    gl_thread.daemon = True
    gl_thread.start()

    gui.launch_gui(obiekty, lambda: selected_obj, lambda obj: set_selected(obj), set_wall_color)
