import matplotlib.pyplot as plt
import matplotlib.animation as animation

from datetime import datetime

import tkinter as tk
import tkinter.ttk as ttk

# import main


class Modal(object):
    def __init__(self, root):
        self.root = root
        self.__N = 0
        self.__flag = True
        self.top = None
        self.top_label = None
        self.prog_bar = None

    def __init_modal(self):
        self.top = tk.Toplevel(self.root)
        self.top.geometry('250x100')
        self.top.attributes('-disabled', True)
        self.top.focus_set()
        self.top.transient(self.root)
        self.top.grab_set()

        self.top_label = tk.Label(self.top, text="Пожалуйста, подождите")
        self.top_label.place(relx=.5, rely=.5, anchor="s", height=30, width=140, bordermode=tk.OUTSIDE)

        self.prog_bar = ttk.Progressbar(self.top, orient='horizontal', mode='determinate', maximum=self.__N, value=0)
        self.prog_bar.place(relx=.5, rely=.5, anchor="n", height=30, width=230, bordermode=tk.OUTSIDE)

        self.top.update()
        self.prog_bar['value'] = 0
        self.top.update()

    def set_progress(self, progress):
        self.prog_bar['value'] = progress
        self.top.update()
        if self.prog_bar['value'] >= self.__N - 1:
            self.top.destroy()

    @staticmethod
    def __get_filename():
        filename = datetime.now()
        filename = str(filename).split('.')[0]
        filename = filename.replace(' ', '_')
        filename = filename.replace(':', '-')
        filename += '.gif'
        return filename

    def __update(self, n, x, y, line):
        if n == self.__N - 1:
            self.__flag = False
        if self.__flag:
            line.set_xdata(x[:n+1])
            line.set_ydata(y[:n+1])
            if x[n] >= 10:
                plt.xlim([x[n] - 10.6, x[n] + 0.6])

    def __update_all(self, n, *args):
        for i in range(0, len(args), 3):
            self.__update(n, args[i], args[i+1], args[i+2])
        self.set_progress(n)

    def draw_history(self, objects, x_lim=(-2, 102), y_lim=(-2, 102)):
        n = len(objects[0].x_history)
        self.__N = n
        self.__init_modal()

        fig, ax = plt.subplots()
        ax.grid()

        lines = []
        for obj in objects:
            [line] = ax.step(obj.x_history[0], obj.y_history[0])
            if obj.color:
                line.set_color(obj.color)
            lines.append(line)

        f_args = []
        for i in range(len(objects)):
            f_args.append(objects[i].x_history)
            f_args.append(objects[i].y_history)
            f_args.append(lines[i])
        f_args = tuple(f_args)

        plt.xlim(x_lim)
        plt.ylim(y_lim)

        anim = animation.FuncAnimation(fig, self.__update_all, n, fargs=f_args, interval=20, blit=False)
        anim.save('gifs/' + self.__get_filename(), writer='pillow')
