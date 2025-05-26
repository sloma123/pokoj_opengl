import tkinter as tk
from tkinter import colorchooser
from furniture import Komoda, Stol, TV
from OpenGL.GLUT import glutPostRedisplay

def launch_gui(obiekty_ref, get_selected, set_selected, set_wall_color):
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

    def change_wall_color():
        picker = tk.Toplevel(root)
        picker.title("Wybierz kolor ścian")

        color_var = tk.StringVar()

        def pick_color():
            color_code = colorchooser.askcolor(title="Wybierz kolor")
            if color_code[0]:
                rgb = tuple(map(int, color_code[0]))
                picker.rgb_selected = rgb
                color_preview.config(bg=color_code[1])

        def confirm():
            if hasattr(picker, "rgb_selected"):
                set_wall_color(picker.rgb_selected)
                glutPostRedisplay()
            picker.destroy()

        color_preview = tk.Label(picker, text="Podgląd", width=20, height=2)
        color_preview.pack(pady=5)

        tk.Button(picker, text="Wybierz kolor", command=pick_color).pack(pady=5)
        tk.Button(picker, text="Zatwierdź", command=confirm).pack(pady=10)

    tk.Button(frame, text="Dodaj komodę", width=20, command=lambda: add_obj("komoda")).pack(pady=5)
    tk.Button(frame, text="Dodaj stół", width=20, command=lambda: add_obj("stol")).pack(pady=5)
    tk.Button(frame, text="Dodaj TV", width=20, command=lambda: add_obj("tv")).pack(pady=5)

    tk.Label(frame, text="").pack()

    tk.Button(frame, text="Usuń zaznaczony obiekt", width=20, command=delete_selected).pack(pady=10)
    tk.Button(frame, text="Zmień kolor ścian", width=20, command=change_wall_color).pack(pady=5)

    root.mainloop()
