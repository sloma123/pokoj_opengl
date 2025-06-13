from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import sys

from furniture import Komoda, Stol, TV, Regal, Szafa, Lozko, Koldra, LampkaStojaca

camera_pos = np.array([0.0, 1.6, 4.0])
camera_front = np.array([0.0, 0.0, -1.0])
camera_up = np.array([0.0, 1.0, 0.0])
yaw, pitch = -90.0, 0.0
keys = set()
last_x, last_y = 400, 300
first_mouse = True
speed = 0.1
sensitivity = 0.2

wall_color = [0.8, 0.8, 0.9]

komoda = Komoda([2.6, -0.95, 1.0])
lozko = Lozko([2.5, -0.95, -2.5])
lampka = LampkaStojaca([-1.0, -0.95, 1.5])

obiekty = [
    lozko,
    lozko.attached_koldra,
    Szafa([-2.5, -0.95, 2.2]),
    Regal([-3.5, -0.95, -3.5]),
    Stol([-0.55, -0.5, -2.9]),
    komoda,
    komoda.attached_tv,
    lampka
]

selected_obj = None
dragging = False

def init():
    glEnable(GL_DEPTH_TEST)
    glEnable(GL_LIGHTING)
    glEnable(GL_LIGHT0)
    glEnable(GL_NORMALIZE)
    glShadeModel(GL_SMOOTH)

    glClearColor(0.5, 0.7, 1.0, 1.0)
    glMatrixMode(GL_PROJECTION)
    gluPerspective(60, 800 / 600, 0.1, 100.0)

    light_pos = [0.0, 2.45, 0.0, 1.0]
    glLightfv(GL_LIGHT0, GL_POSITION, light_pos)
    glLightfv(GL_LIGHT0, GL_AMBIENT, [0.3, 0.3, 0.3, 1.0])    # tło
    glLightfv(GL_LIGHT0, GL_DIFFUSE, [2.0, 2.0, 2.0, 2.0])   # główna jasność
    glLightfv(GL_LIGHT0, GL_SPECULAR, [0.5, 0.5, 0.5, 1.0])   # połysk
    glLightf(GL_LIGHT0, GL_CONSTANT_ATTENUATION, 1.0)
    glLightf(GL_LIGHT0, GL_LINEAR_ATTENUATION, 0.1)
    glLightf(GL_LIGHT0, GL_QUADRATIC_ATTENUATION, 0.03)


    glEnable(GL_LIGHT1)  # Lampka stojąca – światło dodatkowe

def draw_room():
    glEnable(GL_LIGHTING)

    # PODŁOGA – ciepły kolor, dobre odbicie światła
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.6, 0.4, 0.2, 1.0])
    glMaterialfv(GL_FRONT_AND_BACK, GL_SPECULAR, [0.4, 0.35, 0.3, 1.0])
    glMaterialf(GL_FRONT_AND_BACK, GL_SHININESS, 40.0)
    glNormal3f(0.0, 1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-4, -1, -4)
    glVertex3f( 4, -1, -4)
    glVertex3f( 4, -1,  4)
    glVertex3f(-4, -1,  4)
    glEnd()

    # SUFIT
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [0.9, 0.9, 0.9, 1.0])
    glNormal3f(0.0, -1.0, 0.0)
    glBegin(GL_QUADS)
    glVertex3f(-4, 2.5, -4)
    glVertex3f(-4, 2.5,  4)
    glVertex3f( 4, 2.5,  4)
    glVertex3f( 4, 2.5, -4)
    glEnd()

    # ŚCIANY
    glMaterialfv(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE, [*wall_color, 1.0])
    for normal, verts in [
        ([1.0, 0.0, 0.0],  [(-4, -1, -4), (-4, 2.5, -4), (-4, 2.5, 4), (-4, -1, 4)]),     # lewa
        ([-1.0, 0.0, 0.0], [(4, -1, -4), (4, -1, 4), (4, 2.5, 4), (4, 2.5, -4)]),         # prawa
        ([0.0, 0.0, 1.0],  [(-4, -1, -4), (4, -1, -4), (4, 2.5, -4), (-4, 2.5, -4)]),     # tylna
        ([0.0, 0.0, -1.0], [(-4, -1, 4), (-4, 2.5, 4), (4, 2.5, 4), (4, -1, 4)]),         # przednia
    ]:
        glNormal3f(*normal)
        glBegin(GL_QUADS)
        for v in verts: glVertex3f(*v)
        glEnd()

    # LAMPA SUFITOWA – świecąca kula
    glPushMatrix()
    glTranslatef(0.0, 2.45, 0.0)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [1.0, 1.0, 0.8, 1.0])
    glNormal3f(0.0, -1.0, 0.0)
    glutSolidSphere(0.1, 20, 20)
    glMaterialfv(GL_FRONT_AND_BACK, GL_EMISSION, [0.0, 0.0, 0.0, 1.0])  # reset emisji
    glPopMatrix()


def draw_furniture():
    for obj in obiekty:
        obj.is_selected = (obj == selected_obj)
        if hasattr(obj, "attached_koldra"):
            obj.attached_koldra.is_selected = (obj == selected_obj)
        obj.draw()

def display():
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_MODELVIEW)
    glLoadIdentity()
    center = camera_pos + camera_front
    gluLookAt(*camera_pos, *center, *camera_up)

    # światło lampki stojącej (GL_LIGHT1)
    if lampka.is_on:
        glEnable(GL_LIGHT1)
        bulb_pos = lampka.pos + np.array([0.0, 1.85, 0.0])
        glLightfv(GL_LIGHT1, GL_POSITION, [*bulb_pos, 1.0])

        # CIEPŁE I INTENSYWNE ŚWIATŁO
        glLightfv(GL_LIGHT1, GL_AMBIENT, [0.08, 0.05, 0.03, 1.0])
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [0.95, 0.7, 0.4, 1.0])
        glLightfv(GL_LIGHT1, GL_SPECULAR, [0.3, 0.2, 0.1, 1.0])


        # KIERUNEK W DÓŁ
        glLightfv(GL_LIGHT1, GL_SPOT_DIRECTION, [0.0, -1.0, 0.0])
        glLightf(GL_LIGHT1, GL_SPOT_CUTOFF, 60.0)
        glLightf(GL_LIGHT1, GL_SPOT_EXPONENT, 6.0)

        # OSŁABIENIE – dla większego zasięgu
        glLightf(GL_LIGHT1, GL_CONSTANT_ATTENUATION, 0.5)
        glLightf(GL_LIGHT1, GL_LINEAR_ATTENUATION, 0.02)
        glLightf(GL_LIGHT1, GL_QUADRATIC_ATTENUATION, 0.005)
    else:
        glDisable(GL_LIGHT1)




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

def check_collision(obj1, obj2):
    min1 = obj1.pos + obj1.bounds_min - obj1.center_offset
    max1 = obj1.pos + obj1.bounds_max - obj1.center_offset
    min2 = obj2.pos + obj2.bounds_min - obj2.center_offset
    max2 = obj2.pos + obj2.bounds_max - obj2.center_offset
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
                    hit_obj = obj.parent if obj.name == "koldra" and hasattr(obj, "parent") else obj
                    break
            selected_obj = None if selected_obj == hit_obj else hit_obj
            dragging = True if hit_obj else False
        elif state == GLUT_UP:
            dragging = False

def mouse_drag(x, y):
    global dragging, selected_obj
    if selected_obj is None or not dragging: return
    ray_origin, ray_dir = get_ray_from_mouse(x, y)
    if abs(ray_dir[1]) < 1e-6: return
    t = (selected_obj.pos[1] - ray_origin[1]) / ray_dir[1]
    point_on_plane = ray_origin + t * ray_dir
    margin = 0.0
    if selected_obj.name == "lozko": margin = 1.0
    elif selected_obj.name == "stol": margin = 0.4
    elif selected_obj.name == "szafa": margin = 0.5
    half_size = selected_obj.size / 2
    new_x = np.clip(point_on_plane[0], -4 + half_size + margin, 4 - half_size - margin)
    new_z = np.clip(point_on_plane[2], -4 + half_size + margin, 4 - half_size - margin)
    original_pos = selected_obj.pos.copy()
    selected_obj.pos[0] = new_x
    selected_obj.pos[2] = new_z
    for obj in obiekty:
        if obj is not selected_obj and check_collision(selected_obj, obj):
            selected_obj.pos = original_pos
            return

def special_input(key, x, y):
    global selected_obj
    if selected_obj and selected_obj.name != "tv":
        if key == GLUT_KEY_LEFT:
            selected_obj.rotation = (selected_obj.rotation - 10) % 360
        elif key == GLUT_KEY_RIGHT:
            selected_obj.rotation = (selected_obj.rotation + 10) % 360

def timer(v):
    update_camera()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def key_down(key, x, y):
    if key == b'\x1b': sys.exit()
    if key == b'l': lampka.is_on = not lampka.is_on
    keys.add(key)

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
    pitch = np.clip(pitch + dy * sensitivity, -89.0, 89.0)
    rad_yaw, rad_pitch = np.radians(yaw), np.radians(pitch)
    camera_front[:] = np.array([
        np.cos(rad_yaw) * np.cos(rad_pitch),
        np.sin(rad_pitch),
        np.sin(rad_yaw) * np.cos(rad_pitch)
    ])

def set_selected(obj): global selected_obj; selected_obj = obj
def set_wall_color(rgb_tuple): global wall_color; wall_color = [c / 255.0 for c in rgb_tuple]

def start_gl():
    glutInit()
    glutInitDisplayMode(GLUT_DOUBLE | GLUT_RGB | GLUT_DEPTH)
    glutInitWindowSize(800, 600)
    glutCreateWindow(b"3D Pokoj z lampka")
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
    gui.launch_gui(obiekty, lambda: selected_obj, set_selected, set_wall_color)
