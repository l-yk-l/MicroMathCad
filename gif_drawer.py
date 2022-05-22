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


def __update_all(n, *args):
    min_x_lim = min(args[0][:n+1])
    min_y_lim = min(args[1][:n+1])
    max_x_lim = max(args[0][:n+1])
    max_y_lim = max(args[1][:n+1])
    for i in range(3, len(args), 3):
        min_x_lim = min(min_x_lim, min(args[i][:n+1]))
        min_y_lim = min(min_y_lim, min(args[i+1][:n+1]))
        max_x_lim = max(max_x_lim, max(args[i][:n+1]))
        max_y_lim = max(max_y_lim, max(args[i+1][:n+1]))
    plt.xlim([min_x_lim - 10, max_x_lim + 10])
    plt.ylim([min_y_lim - 10, max_y_lim + 10])
    for i in range(0, len(args), 3):
        __update(n, args[i], args[i+1], args[i+2])


def draw_history(objects):
    global __N

    n = len(objects[0].x_history)
    __N = n

    fig, ax = plt.subplots()
    ax.grid()

    lines = []
    for obj in objects:
        print(len(obj.x_history))
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

    victim = objects[0]
    min_x_lim = victim.x_history[1]
    min_y_lim = victim.y_history[1]
    max_x_lim = victim.x_history[1]
    max_y_lim = victim.y_history[1]
    for hunter in victim.hunters:
        min_x_lim = min(min_x_lim, hunter.x_history[1])
        min_y_lim = min(min_y_lim, hunter.y_history[1])
        max_x_lim = max(max_x_lim, hunter.x_history[1])
        max_y_lim = max(max_y_lim, hunter.y_history[1])
    plt.xlim([min_x_lim - 10, max_x_lim + 10])
    plt.ylim([min_y_lim - 10, max_y_lim + 10])

    anim = animation.FuncAnimation(fig, __update_all, n, fargs=f_args, interval=20, blit=False)
    anim.save('gifs/' + __get_filename(), writer='pillow')
    plt.close()
