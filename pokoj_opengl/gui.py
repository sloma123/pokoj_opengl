import tkinter as tk
from furniture import Komoda, Stol, TV
from OpenGL.GLUT import glutPostRedisplay

def launch_gui(obiekty_ref, get_selected, set_selected):
    root = tk.Tk()
    root.title("Panel zarządzania meblami")

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    def add_obj(obj_type):
        if obj_type == "komoda":
            obj = Komoda([0.0, -0.5, 0.0])
        elif obj_type == "stol":
            obj = Stol([0.0, -0.5, 0.0])
        elif obj_type == "tv":
            obj = TV([0.0, -0.5, 0.0])
        else:
            return
        obiekty_ref.append(obj)
        glutPostRedisplay()

    def delete_selected():
        obj = get_selected()
        if obj in obiekty_ref:
            obiekty_ref.remove(obj)
            set_selected(None)
            glutPostRedisplay()

    tk.Button(frame, text="Dodaj komodę", width=20, command=lambda: add_obj("komoda")).pack(pady=5)
    tk.Button(frame, text="Dodaj stół", width=20, command=lambda: add_obj("stol")).pack(pady=5)
    tk.Button(frame, text="Dodaj TV", width=20, command=lambda: add_obj("tv")).pack(pady=5)

    tk.Label(frame, text="").pack()

    tk.Button(frame, text="Usuń zaznaczony obiekt", width=20, command=delete_selected).pack(pady=10)

    root.mainloop()
