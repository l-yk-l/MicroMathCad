import function
import gif_drawer
from importlib import reload
# import gif_drawer2

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

import tkinter as tk

# Style
font_size = 12

fig, ax = plt.subplots()
ax.grid()
plt.xlim([-0.6, 10.6])
plt.ylim([-1.2, 1.2])

gifs_counter = 0

# Charts initialization
# sin1 = function.Sinusoid(plt, ax)
# sin1.set_color('blue')

# sin2 = function.Sinusoid(plt, ax, -1.0)
# sin2.set_color('red')

# sin3 = function.Sinusoid(plt, ax, 0.1)
# sin3.set_color('purple')

# sin4 = function.Sinusoid(plt, ax, -0.1)
# sin4.set_color('#7FFFD4')

# objects = [sin1, sin2, sin3, sin4]
victim = function.Victim(plt, ax, start_x=0, start_y=0, direction=30, speed=0.5, max_angle_of_rotation=10)
hunter1 = function.Hunter(plt, ax, start_x=-4, start_y=2, direction=90, speed=0.7, max_angle_of_rotation=10)
victim.add_hunter(hunter1)
hunter1.set_victim(victim)
objects = [victim, hunter1]


# Functions
def on_closing():
    for canvas_item in canvas.get_tk_widget().find_all():
        canvas.get_tk_widget().delete(canvas_item)
    root.quit()


# def add_k():
#     for obj in objects:
#         obj.k += 0.1
#     labelK.configure(text=f"k = {round(objects[0].k, 1)}")
#
#
# def sub_k():
#     for obj in objects:
#         obj.k -= 0.1
#     labelK.configure(text=f"k = {round(objects[0].k, 1)}")


def start():
    for obj in objects:
        obj.isPaused = False


def pause():
    for obj in objects:
        obj.isPaused = True


def stop_save():
    for obj in objects:
        obj.isPaused = True
    # Визуализация прогресса сохранения гифки (очень тормозит процесс сохранения)
    # drawer = gif_drawer2.Modal(root)
    # drawer.draw_history(objects=objects, x_lim=[-0.6, 10.6], y_lim=[-1.2, 1.2])
    # top = tk.Toplevel(root)
    # top.geometry('250x100')
    # top.attributes('-disabled', True)
    # top.focus_set()
    # top.transient(root)
    # top.grab_set()
    #
    # top_label = tk.Label(top, text="Пожалуйста, подождите", font=('Arial Bold', font_size))
    # top_label.place(relx=.5, rely=.5, anchor="center", height=30, width=200, bordermode=tk.OUTSIDE)
    # top.update()

    gif_drawer.draw_history(objects=objects)
    reload(gif_drawer)
    # top.destroy()


root = tk.Tk()
root.title('Симуляция преследования')
header = tk.Label(root, text="Анимация графика", font=('Arial Bold', font_size))
header.grid(column=0, row=0, columnspan=5)

filler_column_1 = tk.Label(root, text="", padx=10)
filler_column_1.grid(column=0, row=0)

canvas = FigureCanvasTkAgg(fig, master=root)
canvas.get_tk_widget().grid(column=1, row=1, columnspan=3, rowspan=18)

filler_column_2 = tk.Label(root, text="", padx=5)
filler_column_2.grid(column=4, row=0)

# btnSub = tk.Button(
#     root,
#     text="k-0.1",
#     command=sub_k,
#     font=12,
#     padx=30,
# )
# btnSub.grid(column=5, row=18)

# labelK = tk.Label(root, text="qwe", font=('Arial Bold', font_size))
# labelK.grid(column=5, row=16)

# btnAdd = tk.Button(
#     root,
#     text="k+0.1",
#     command=add_k,
#     font=12,
#     padx=30,
# )
# btnAdd.grid(column=5, row=17)

btnStart = tk.Button(
    root,
    text="Старт",
    command=start,
    font=12,
    padx=30,
)
btnStart.grid(column=5, row=1)

btnPause = tk.Button(
    root,
    text="Пауза",
    command=pause,
    font=12,
    padx=30,
)
btnPause.grid(column=5, row=2)

btnStopSave = tk.Button(
    root,
    text="Сохранить gif",
    command=stop_save,
    font=12,
    padx=30,
)
btnStopSave.grid(column=5, row=3)

filler_column_3 = tk.Label(root, text="", padx=10)
filler_column_3.grid(column=6, row=0)


animations = []
for item in objects:
    gen = item.data_gen()
    animations.append(animation.FuncAnimation(fig, item.update, gen, interval=20, blit=False))

root.protocol("WM_DELETE_WINDOW", on_closing)
root.mainloop()
