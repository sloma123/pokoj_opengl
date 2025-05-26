from OpenGL.GL import *
from OpenGL.GLUT import *
from OpenGL.GLU import *
import numpy as np
import sys
from komoda import draw_komoda

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

# Lista obiektów z pozycją, rozmiarem, kolorem i rotacją
obiekty = [
    {"nazwa": "komoda", "pos": np.array([1.0, -0.5, 1.0]), "size": 1.0, "color": (0.6, 0.3, 0.2), "typ": "model", "rot": 0},
    {"nazwa": "stol",   "pos": np.array([0.0, -0.3, 0.0]), "size": 1.5, "color": (0.4, 0.2, 0.1), "typ": "cube", "rot": 0},
    {"nazwa": "tv",     "pos": np.array([-2.0, 0.0, -3.0]), "size": 1.0, "color": (0.0, 0.0, 0.0), "typ": "cube", "rot": 0}
]

selected_obj = None

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

    wall_color = (0.8, 0.8, 0.9)
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
        glPushMatrix()
        glTranslatef(*obj["pos"])
        glRotatef(obj.get("rot", 0), 0, 1, 0)  # obrót wokół osi Y
        if obj["typ"] == "cube":
            draw_cube(0, 0, 0, obj["size"], obj["color"])
        elif obj["typ"] == "model" and obj["nazwa"] == "komoda":
            draw_komoda()
        glPopMatrix()

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

def ray_hits_box(ray_origin, ray_dir, box_center, box_size):
    t_min = -np.inf
    t_max = np.inf
    bounds_min = box_center - box_size / 2
    bounds_max = box_center + box_size / 2
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

def mouse_click(button, state, x, y):
    global selected_obj
    if button == GLUT_LEFT_BUTTON and state == GLUT_DOWN:
        ray_origin, ray_dir = get_ray_from_mouse(x, y)
        for obj in obiekty:
            if ray_hits_box(ray_origin, ray_dir, obj["pos"], obj["size"]):
                selected_obj = obj
                break
    elif button == GLUT_LEFT_BUTTON and state == GLUT_UP:
        selected_obj = None

def mouse_drag(x, y):
    global selected_obj
    if selected_obj is not None:
        ray_origin, ray_dir = get_ray_from_mouse(x, y)
        t = (selected_obj["pos"][1] - ray_origin[1]) / ray_dir[1]
        point_on_plane = ray_origin + t * ray_dir

        half_size = selected_obj["size"] / 2
        min_x = -5 + half_size
        max_x = 5 - half_size
        min_z = -5 + half_size
        max_z = 5 - half_size

        # Zabezpieczenie przed "wchodzeniem" w ściany
        new_x = np.clip(point_on_plane[0], min_x, max_x)
        new_z = np.clip(point_on_plane[2], min_z, max_z)

        selected_obj["pos"][0] = new_x
        selected_obj["pos"][2] = new_z


def special_input(key, x, y):
    global selected_obj
    if selected_obj:
        if key == GLUT_KEY_LEFT:
            selected_obj["rot"] = (selected_obj["rot"] - 10) % 360
        elif key == GLUT_KEY_RIGHT:
            selected_obj["rot"] = (selected_obj["rot"] + 10) % 360

def timer(v):
    update_camera()
    glutPostRedisplay()
    glutTimerFunc(16, timer, 0)

def key_down(key, x, y):
    keys.add(key)
    if key == b'\x1b': sys.exit()

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
    glutCreateWindow(b"3D Pokoj z obiektami")
    init()
    glutDisplayFunc(display)
    glutKeyboardFunc(key_down)
    glutKeyboardUpFunc(key_up)
    glutPassiveMotionFunc(mouse_motion)
    glutMouseFunc(mouse_click)
    glutMotionFunc(mouse_drag)
    glutSpecialFunc(special_input)  # ⬅️ obsługa strzałek
    glutTimerFunc(0, timer, 0)
    glutMainLoop()

if __name__ == "__main__":
    main()
