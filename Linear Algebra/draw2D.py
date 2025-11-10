from math import ceil, floor, sqrt

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.pyplot import xlim, ylim

__all__ = ["Point2D", "Points2D", "Line2D", "Arrow2D", "draw2D"]

class Point2D():
    def __init__(self, x, y, color='black', label=None):
        self.x = x
        self.y = y
        self.color = color
        self.label = label

class Points2D():
    def __init__(self, *points, color='black'):
        length = len(points)
        points = list(map(process_pt, points, [color]*length))
        self.points = list(points)
        self.color = color

class Line2D():
    def __init__(self, start_point, end_point=(0,0), color='gray', linestyle='solid', label=None):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.linestyle = linestyle
        self.label = label

class Arrow2D():
    def __init__(self, head, tail=(0,0), color='red', linestyle='solid', label=None):
        self.head = head
        self.tail = tail
        self.color = color
        self.linestyle = linestyle
        self.label = label

def process_pt(pt, color):
    length = len(pt)
    x, y, col, label = 0, 0, color, None
    if length > 0:
        x = pt[0]
        if length > 1:
            y = pt[1]
            if length > 2:
                col = pt[2]
                if length > 3:
                    label = pt[3]
    return Point2D(x, y, color=col, label=label)
    
def extract_vectors_2D(objects):
    for obj in objects:
        if type(obj) == Point2D:
            yield (obj.x, obj.y)
        elif type(obj) == Points2D:
            for p in obj.points:
                yield (p.x, p.y)
        elif type(obj) == Line2D:
            yield obj.start_point
            yield obj.end_point
        elif type(obj) == Arrow2D:
            yield obj.head
            yield obj.tail
        else:
            raise TypeError("Unrecognized object: {}".format(obj))

def get_label_xy(start_point, end_point=None):
    x1, y1 = start_point
    
    if end_point is not None:
        x2, y2 = end_point
        mx, my = (x1+x2)/2, (y1+y2)/2
        vx, vy = (x2-x1), (y2-y1)
    else:
        mx, my = x1, y1
        vx, vy = x1, y1

    # perpendicular offset by delta
    norm = (vx**2 + vy**2)**0.5 or 1.0
    nx, ny = -vy/norm, vx/norm
    delta = 0.2  # data-units
    
    if end_point is not None:
        lx, ly = mx + delta*nx, my + delta*ny
    else:
        lx, ly = x1, my + delta*ny
    
    yield lx
    yield ly

def draw2D(*objects, origin=False, axes=True, axes_labels=False, ticks=True, tick_labels=True, grid=True, grid_size=(1,1), dark_mode=True, width=6, dpi=100, nice_aspect_ratio=True, save_as=None):

    fig = plt.gcf()
    
    if dark_mode:
        plt.style.use('dark_background')
        axes_color = 'white'
    else:
        plt.style.use('default')
        axes_color = 'black'
    
    all_vectors = list(extract_vectors_2D(objects))
    all_x, all_y = zip(*all_vectors)

    max_x, min_x = max(0,*all_x), min(0,*all_x)
    max_y, min_y = max(0,*all_y), min(0,*all_y)

    x_size = max_x-min_x
    y_size = max_y-min_y
    
    # Grid
    x_padding = max(ceil(0.05 * x_size), grid_size[0])
    y_padding = max(ceil(0.05 * y_size), grid_size[1])

    def round_up_to_multiple(val,size):
        return floor((val + size) / size) * size

    def round_down_to_multiple(val,size):
        return -floor((-val - size) / size) * size

    plt.xlim(floor((min_x - x_padding) / grid_size[0]) * grid_size[0],
            ceil((max_x + x_padding) / grid_size[0]) * grid_size[0])
    plt.ylim(floor((min_y - y_padding) / grid_size[1]) * grid_size[1],
            ceil((max_y + y_padding) / grid_size[1]) * grid_size[1])

    if origin:
        plt.scatter([0],[0], color=axes_color, marker='x', zorder=3)

    ax = plt.gca()
    
    if not tick_labels:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
    
    if not ticks:
        ax.set_xticks([])
        ax.set_yticks([])
    else:
        ax.set_xticks(np.arange(plt.xlim()[0],plt.xlim()[1],grid_size[0]))
        ax.set_yticks(np.arange(plt.ylim()[0],plt.ylim()[1],grid_size[1])) 
    
    if grid:
        plt.grid(True, alpha=0.4)
        
    ax.set_axisbelow(True)

    if axes_labels:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
    
    if axes:
        ax.axhline(linewidth=2, color=axes_color, zorder=1)
        ax.axvline(linewidth=2, color=axes_color, zorder=1)

    # Objects
    for obj in objects:
        if type(obj) == Point2D:
            plt.scatter(obj.x, obj.y, color=obj.color, zorder=4)
            if obj.label is not None:
                lx, ly = get_label_xy((obj.x, obj.y))
                plt.annotate(obj.label, (lx, ly), xytext=(lx, ly), ha='center')
        elif type(obj) == Points2D:
            all_x = [p.x for p in obj.points]
            all_y = [p.y for p in obj.points]
            all_colors = [p.color for p in obj.points]
            all_labels = [p.label for p in obj.points]
            plt.scatter(all_x, all_y, color=all_colors, zorder=4)
            for i, txt in enumerate(all_labels):
                if txt is not None:
                    lx, ly = get_label_xy((all_x[i], all_y[i]))
                    plt.annotate(txt, (lx, ly), xytext=(lx, ly), ha='center')
        elif type(obj) == Line2D:
            x1, y1 = obj.start_point
            x2, y2 = obj.end_point
            plt.plot([x1,x2],[y1,y2], color=obj.color, linestyle=obj.linestyle, zorder=2)
            if obj.label is not None:
                lx, ly = get_label_xy(obj.start_point, obj.end_point)
                plt.annotate(obj.label, xy=(lx, ly), xytext=(lx, ly), ha='center')
        elif type(obj) == Arrow2D:
            head, tail = obj.head, obj.tail
            head_length = (xlim()[1] - xlim()[0]) / 20.
            length = sqrt((head[0]-tail[0])**2 + (head[1]-tail[1])**2)
            new_length = length - head_length
            new_y = (head[1] - tail[1]) * (new_length / length)
            new_x = (head[0] - tail[0]) * (new_length / length)
            ax.arrow(tail[0], tail[1], new_x, new_y,
                head_width=head_length/1.5, head_length=head_length,
                fc=obj.color, ec=obj.color, ls=obj.linestyle, zorder=3)
            if obj.label is not None:
                lx, ly = get_label_xy(tail, head)
                ax.annotate(obj.label, xy=(lx, ly), xytext=(lx, ly), ha='center')
        else:
            raise TypeError("Unrecognized object: {}".format(obj))
    
    # Size
    current_size = fig.get_size_inches()
    
    if nice_aspect_ratio:
        coords_height = (ylim()[1] - ylim()[0])
        coords_width = (xlim()[1] - xlim()[0])
        fig.set_size_inches(width, width * coords_height / coords_width)
        fig.set_dpi(dpi)
    else:
        ratio = current_size[0]/width
        fig.set_size_inches(width, current_size[1]/ratio)
        fig.set_dpi(dpi)

    if save_as:
        plt.savefig(save_as, dpi=fig.dpi)
    
    plt.show()


