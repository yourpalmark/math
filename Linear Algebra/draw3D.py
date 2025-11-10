from math import sqrt

import numpy as np

import matplotlib
import matplotlib.pyplot as plt
from matplotlib.ticker import MultipleLocator
from mpl_toolkits.mplot3d import Axes3D, proj3d
from mpl_toolkits.mplot3d.art3d import Poly3DCollection

__all__ = ["Point3D", "Points3D", "Line3D", "Arrow3D", "draw3D"]

class Point3D():
    def __init__(self, x, y, z, color='black', label=None):
        self.x = x
        self.y = y
        self.z = z
        self.color = color
        self.label = label

class Points3D():
    def __init__(self, *points, color='black'):
        length = len(points)
        points = list(map(process_pt, points, [color]*length))
        self.points = list(points)
        self.color = color

class Line3D():
    def __init__(self, start_point, end_point, color='gray', linestyle='solid'):
        self.start_point = start_point
        self.end_point = end_point
        self.color = color
        self.linestyle = linestyle

class Arrow3D():
    def __init__(self, head, tail=(0,0,0), color='red', linestyle='solid', head_length=0.2, head_radius=0.08, head_resolution=24):
        self.head = head
        self.tail = tail
        self.color = color
        self.linestyle = linestyle
        self.head_length = head_length
        self.head_radius = head_radius
        self.head_resolution = head_resolution

def process_pt(pt, color):
    length = len(pt)
    x, y, z, col, label = 0, 0, 0, color, None
    if length > 0:
        x = pt[0]
        if length > 1:
            y = pt[1]
            if length > 2:
                z = pt[2]
                if length > 3:
                    col = pt[3]
                    if length > 4:
                        label = pt[4]
    return Point3D(x, y, z, color=col, label=label)
    
def extract_vectors_3D(objects):
    for obj in objects:
        if type(obj) == Point3D:
            yield (obj.x, obj.y, obj.z)
        elif type(obj) == Points3D:
            for p in obj.points:
                yield (p.x, p.y, p.z)
        elif type(obj) == Line3D:
            yield obj.start_point
            yield obj.end_point
        elif type(obj) == Arrow3D:
            yield obj.head
            yield obj.tail
        else:
            raise TypeError("Unrecognized object: {}".format(obj))

def draw_segment(ax, start, end, color="black", linestyle='solid'):
    all_x, all_y, all_z = [[start[i],end[i]] for i in range(0,3)]
    ax.plot(all_x, all_y, all_z, color=color, linestyle=linestyle)

def set_translucent_panes(ax, dark_mode, pane_alpha=0.15):
    if dark_mode:
        pane_color = 'white'
        edge_color = 'white'
    else:
        pane_color = 'black'
        edge_color = 'black'
    
    rgba = matplotlib.colors.to_rgba(pane_color, pane_alpha)
    edge_rgba = matplotlib.colors.to_rgba(edge_color, 1)

    # Make the overall axes face transparent so panes aren't masked by it
    ax.set_facecolor((1, 1, 1, 0))

    for axis in (ax.xaxis, ax.yaxis, ax.zaxis):
        pane = getattr(axis, "pane", None)
        if pane is not None:
            pane.fill = True
            pane.set_facecolor(rgba)
            pane.set_edgecolor(edge_rgba)
            pane.set_alpha(pane_alpha)

def draw3D(*objects, origin=False, axes=True, axes_labels=False, ticks=True, tick_labels=True, grid=False, grid_size=(1,1,1), dark_mode=True, width=6, dpi=100, nice_aspect_ratio=True, save_as=None, azim=None, elev=None, depthshade=True):

    if dark_mode:
        plt.style.use('dark_background')
        axes_color = 'white'
    else:
        plt.style.use('default')
        axes_color = 'black'

    fig = plt.figure(figsize=(width, width), dpi=dpi)
    ax = fig.add_subplot(111, projection='3d')
    
    ax.view_init(elev=elev,azim=azim)
    
    # Set up grid with custom properties
    ax.grid(grid)
    if grid:
        # Set grid line properties for each axis
        ax.xaxis._axinfo["grid"]["color"] = (1, 1, 1, 0.2) if dark_mode else (0, 0, 0, 0.2)
        ax.yaxis._axinfo["grid"]["color"] = (1, 1, 1, 0.2) if dark_mode else (0, 0, 0, 0.2)
        ax.zaxis._axinfo["grid"]["color"] = (1, 1, 1, 0.2) if dark_mode else (0, 0, 0, 0.2)

    if grid_size:
        ax.xaxis.set_major_locator(MultipleLocator(grid_size[0]))
        ax.yaxis.set_major_locator(MultipleLocator(grid_size[1]))
        ax.zaxis.set_major_locator(MultipleLocator(grid_size[2]))
    
    set_translucent_panes(ax, dark_mode=dark_mode)
    
    all_vectors = list(extract_vectors_3D(objects))
    if origin:
        all_vectors.append((0,0,0))
    all_x, all_y, all_z = zip(*all_vectors)

    max_x, min_x = max(0,*all_x), min(0,*all_x)
    max_y, min_y = max(0,*all_y), min(0,*all_y)
    max_z, min_z = max(0,*all_z), min(0,*all_z)

    x_size = max_x-min_x
    y_size = max_y-min_y
    z_size = max_z-min_z

    # Grid
    rx = max(max_x - min_x, 1e-9)
    ry = max(max_y - min_y, 1e-9)
    rz = max(max_z - min_z, 1e-9)

    margin=0.1
    
    pad_x = rx * margin
    pad_y = ry * margin
    pad_z = rz * margin

    auto_xlim = (min_x - pad_x, max_x + pad_x)
    auto_ylim = (min_y - pad_y, max_y + pad_y)
    auto_zlim = (min_z - pad_z, max_z + pad_z)

    ax.set_xlim(auto_xlim)
    ax.set_ylim(auto_ylim)
    ax.set_zlim(auto_zlim)

    if axes_labels:
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.set_zlabel('z')

    x0, x1 = ax.get_xlim()
    y0, y1 = ax.get_ylim()
    z0, z1 = ax.get_zlim()
    
    if axes:
        draw_segment(ax, (x0, 0, 0), (x1, 0, 0), color=axes_color)
        draw_segment(ax, (0, y0, 0), (0, y1, 0), color=axes_color)
        draw_segment(ax, (0, 0, z0), (0, 0, z1), color=axes_color)

    if origin:
        ax.scatter([0],[0],[0], color=axes_color, marker='x', depthshade=depthshade)

    # Objects
    for obj in objects:
        if type(obj) == Point3D:
            ax.scatter(obj.x, obj.y, obj.z, color=obj.color, depthshade=depthshade)
        elif type(obj) == Points3D:
            all_x = [p.x for p in obj.points]
            all_y = [p.y for p in obj.points]
            all_z = [p.z for p in obj.points]
            all_colors = [p.color for p in obj.points]
            all_labels = [p.label for p in obj.points]
            ax.scatter(all_x, all_y, all_z, color=all_colors, depthshade=depthshade)
        elif type(obj) == Line3D:
            draw_segment(ax, obj.start_point, obj.end_point, color=obj.color, linestyle=obj.linestyle)
        elif type(obj) == Arrow3D:
            head, tail = obj.head, obj.tail
            length = sqrt((head[0]-tail[0])**2 + (head[1]-tail[1])**2 + (head[2]-tail[2])**2)
            color, linestyle = obj.color, obj.linestyle
            head_length, head_radius, head_resolution = obj.head_length, obj.head_radius, obj.head_resolution
            
            start = np.asarray(tail, float)
            d = np.asarray(head, float)
            n = np.linalg.norm(d)
            if n == 0:
                raise ValueError("direction vector must be non-zero")
            d = d / n
        
            shaft_end = start + d * (length - head_length)
            tip = start + d * length
        
            # shaft
            draw_segment(ax, start, shaft_end, color=color, linestyle=linestyle)
        
            # orthonormal basis around d
            up = np.array([0., 0., 1.]) if abs(d[2]) < 0.999 else np.array([0., 1., 0.])
            a = np.cross(d, up); a /= np.linalg.norm(a)
            b = np.cross(d, a)
        
            # cone base ring
            theta = np.linspace(0, 2*np.pi, head_resolution, endpoint=False)
            base_center = shaft_end
            ring = [base_center + head_radius*(np.cos(t)*a + np.sin(t)*b) for t in theta]
        
            # triangular faces to tip
            faces = [[ring[i], ring[(i+1)%head_resolution], tip] for i in range(head_resolution)]
            ax.add_collection3d(Poly3DCollection(faces, color=color))
        else:
            raise TypeError("Unrecognized object: {}".format(obj))
    
    if not tick_labels:
        ax.set_xticklabels([])
        ax.set_yticklabels([])
        ax.set_zticklabels([])
    
    if not ticks:
        ax.set_xticks([])
        ax.set_yticks([])
        ax.set_zticks([])

    # Size
    if nice_aspect_ratio:
        ax.set_box_aspect([1.0, 1.0, 1.0])  # Equal aspect ratio for 3D
        fig.set_size_inches(width, width, forward=True)
    else:
        ax.set_box_aspect(None)
        w, h = fig.get_size_inches()
        scale = width/w
        fig.set_size_inches(width, h * scale, forward=True)
        fig.set_dpi(dpi)
    
    if save_as:
        plt.savefig(save_as, dpi=fig.dpi)

    plt.show()


