import matplotlib.pyplot as plt
import matplotlib.animation as animation
from datetime import datetime


__N = 0
__flag = True


def __get_filename():
    filename = datetime.now()
    filename = str(filename).split('.')[0]
    filename = filename.replace(' ', '_')
    filename = filename.replace(':', '-')
    filename += '.gif'
    return filename


def __update(n, x, y, line):
    global __flag
    if n == __N-1:
        __flag = False
    if __flag:
        line.set_xdata(x[:n+1])
        line.set_ydata(y[:n+1])
        if x[n] >= 10:
            plt.xlim([x[n] - 10.6, x[n] + 0.6])


def __update_all(n, *args):
    for i in range(0, len(args), 3):
        __update(n, args[i], args[i+1], args[i+2])


def draw_history(objects, x_lim=(-2, 102), y_lim=(-2, 102)):
    global __N

    n = len(objects[0].x_history)
    __N = n

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

    anim = animation.FuncAnimation(fig, __update_all, n, fargs=f_args, interval=20, blit=False)
    anim.save('gifs/' + __get_filename(), writer='pillow')
