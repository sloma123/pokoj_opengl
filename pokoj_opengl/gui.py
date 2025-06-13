import tkinter as tk
from tkinter import colorchooser
from furniture import Komoda, Stol, TV
from OpenGL.GLUT import glutPostRedisplay

def launch_gui(obiekty_ref, get_selected, set_selected, set_wall_color):
    root = tk.Tk() # Utworzenie głównego okna aplikacji
    root.title("Panel zarządzania meblami")
    root.attributes("-topmost", True)

    frame = tk.Frame(root)
    frame.pack(padx=20, pady=20)

    def add_obj(obj_type):
        if obj_type == "komoda":
            obj = Komoda([0.0, -0.95, 0.0])
            obiekty_ref.append(obj)
        elif obj_type == "stol":
            obj = Stol([0.0, -0.95, 0.0])
            obiekty_ref.append(obj)
        elif obj_type == "tv":
            selected = get_selected()
            if selected and selected.name == "komoda":
                # Dodaj tylko jeśli TV jeszcze nie został dodany do sceny
                if hasattr(selected, "attached_tv") and selected.attached_tv not in obiekty_ref:
                    obiekty_ref.append(selected.attached_tv)
                    glutPostRedisplay()

        elif obj_type == "lozko":
            from furniture import Lozko
            lozko = Lozko([0.0, -0.95, 0.0])
            obiekty_ref.append(lozko)
            obiekty_ref.append(lozko.attached_koldra)

        elif obj_type == "szafa":
            from furniture import Szafa
            obj = Szafa([0.0, -0.95, 0.0])
            obiekty_ref.append(obj)
        elif obj_type == "regal":
            from furniture import Regal
            obj = Regal([0.0, -0.95, 0.0])
            obiekty_ref.append(obj)
        else:
            return

        glutPostRedisplay()


    def delete_selected():
        obj = get_selected()
        if obj in obiekty_ref:
            # Jeśli usuwany obiekt to komoda – usuń też jej TV
            if hasattr(obj, "attached_tv") and obj.attached_tv in obiekty_ref:
                obiekty_ref.remove(obj.attached_tv)
            obiekty_ref.remove(obj)
            set_selected(None)
            glutPostRedisplay()


    def change_object_color():
        obj = get_selected()
        if obj:
            color_code = colorchooser.askcolor(title="Wybierz kolor obiektu")
            if color_code[0]:
                rgb_float = tuple(c / 255.0 for c in color_code[0])
                obj.color = rgb_float
                glutPostRedisplay()

    # --- UI Przycisków dodawania/usuń
    tk.Button(frame, text="Dodaj komodę", width=20, command=lambda: add_obj("komoda")).pack(pady=5)
    tk.Button(frame, text="Dodaj stół", width=20, command=lambda: add_obj("stol")).pack(pady=5)
    tk.Button(frame, text="Dodaj TV", width=20, command=lambda: add_obj("tv")).pack(pady=5)
    tk.Button(frame, text="Dodaj łóżko", width=20, command=lambda: add_obj("lozko")).pack(pady=5)
    tk.Button(frame, text="Dodaj szafę", width=20, command=lambda: add_obj("szafa")).pack(pady=5)
    tk.Button(frame, text="Dodaj regał", width=20, command=lambda: add_obj("regal")).pack(pady=5)

    tk.Label(frame, text="").pack()
    tk.Button(frame, text="Usuń zaznaczony obiekt", width=20, command=delete_selected).pack(pady=10)
    tk.Button(frame, text="Zmień kolor obiektu", width=20, command=change_object_color).pack(pady=5)


    # --- Sekcja zmiany koloru ścian ---
    def show_wall_color_controls():
        color_frame.pack(pady=5)

    def pick_color():
        color_code = colorchooser.askcolor(title="Wybierz kolor")
        if color_code[0]:
            rgb = tuple(map(int, color_code[0]))
            color_preview.config(bg=color_code[1])
            color_frame.rgb_selected = rgb

    def confirm_color():
        if hasattr(color_frame, "rgb_selected"):
            set_wall_color(color_frame.rgb_selected)
            glutPostRedisplay()
        color_frame.pack_forget()  # Ukryj panel po zatwierdzeniu

    tk.Button(frame, text="Zmień kolor ścian", width=20, command=show_wall_color_controls).pack(pady=5)

    # Ukryty kontener z przyciskami wyboru koloru
    color_frame = tk.Frame(frame)
    color_preview = tk.Label(color_frame, text="Podgląd", width=20, height=2, bg="#CCCCCC")
    color_preview.pack(pady=5)
    tk.Button(color_frame, text="Wybierz kolor", command=pick_color).pack(pady=5)
    tk.Button(color_frame, text="Zatwierdź", command=confirm_color).pack(pady=5)
    color_frame.pack_forget()

    root.mainloop() # Uruchomienie głównej pętli GUI
