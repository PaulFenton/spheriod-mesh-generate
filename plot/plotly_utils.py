import io 
from PIL import Image
import numpy as np
import plotly.graph_objects as go
import moviepy.editor as mpy
from scipy.spatial.transform import Rotation as R

def show_poly_3d(nodes=None, polys=None, show_nodes=False):
    '''
    Makes a basic invokation of __plot to show a single frame
    '''
    fig = __plot(nodes=nodes, polys=polys, t=0, show_nodes=show_nodes)
    fig.show()
    return

def create_poly_3d_gif(filepath, nodes=None, polys=None, fps=15, duration=8, show_nodes=False):
    '''
    Creates a gif using moviepy from frames built using plotly
    '''

    def make_frame(t):
        return __plotly_fig2array(__plot(nodes=nodes, polys=polys, t=t, fps=fps, duration=duration, show_nodes=show_nodes))

    gif_output_file = filepath
    animation = mpy.VideoClip(make_frame, duration=duration)
    animation.write_gif(gif_output_file, fps=15, loop=0, opt="OptimizePlus", fuzz=10)
    animation.close()

    # forcing garbage collection here seems to account for a 'bug' in moviepy loop count encoding
    import gc
    del animation
    gc.collect()

    return

def __plotly_fig2array(fig):
    '''
    Convert plotly figure into an 2x2 array of RGB bytes
    '''
    fig_bytes = fig.to_image(format="png", scale=1.0)
    buf = io.BytesIO(fig_bytes)
    img = Image.open(buf)
    return np.asarray(img)


def __plot(nodes=None, polys=None, t=0, fps=15, duration=8, show_nodes=False):
    '''
    Creates a plotly figure for a single frame, displaying nodes with scatter3d and
    nodes + polygons with mesh3d
    '''
    assert nodes is not None, "nodes is a required parameter"
    if polys is None:
        show_nodes = True  # always show nodes if there are no polys

    # rotate the polygon on each frame
    frame = t*fps
    max_frame = fps * duration
    p = ((frame - 1) / (max_frame))
    roll = -(2*np.pi/8) * p
    pitch = -np.sin( 2*np.pi * p + 0.321) * (np.pi / 32)
    rotated = R.from_rotvec([pitch, 0.0, roll]).apply(nodes)

    # populate the plot's contents
    data = []
    if polys is not None:
        data.append(__get_mesh3d(rotated, polys))
    if show_nodes:
        data.append(__get_node_scatter3d(rotated))

    # initialize the plot
    fig = go.Figure(data=data)
    fig['layout']['margin'] = dict(l=0, r=0, b=0, t=0)
    fig["layout"]["height"] = 400
    fig["layout"]["width"] = 400

    # configure the plot's axes
    hide_axis_params = {
        'title': '',
        'autorange': False,
        'showgrid': False,
        'zeroline': False,
        'showline': False,
        'ticks': '',
        'showticklabels': False,
        'backgroundcolor': "rgba(0, 0, 0, 0)",
        'showbackground': True,
    }
    fig["layout"]["scene"] = {
      'aspectmode': 'cube',
      'xaxis': {
          **hide_axis_params,
          'range': [np.min(nodes[:,0]), np.max(nodes[:,0])*1.1]
        },
      'yaxis':{
          **hide_axis_params,
          'range': [np.min(nodes[:,1]), np.max(nodes[:,1])*1.1]
       },
      'zaxis': {
          **hide_axis_params,
          'range': [np.min(nodes[:,2]), np.max(nodes[:,2])*1.1]
        }
    }

    # configure the camera to be more zoomed in
    fig["layout"]["scene_camera"] = {
      'up': dict(x=0, y=0, z=0.8),
      'center': dict(x=0, y=0, z=0.0),
      'eye': dict(x=0.8, y=0.8, z=0.8)
    }

    return fig


def __get_mesh3d(nodes, polys, color=None):
    '''
    Constructs a plotly mesh3d object from a list of nodes and polygons
    '''
    i, j, k = zip(*polys)

    # determine colormap settings
    if color is None:
        colormap_settings = {
            'colorscale': [[0, '#010095'], [1, '#1F56FF']],
            'intensity': [c%2 for c in range(len(i))]
        }
    else:
        colormap_settings = {
            'colorscale': [[0, color]],
            'intensity': 0
        }

    return go.Mesh3d(
        **colormap_settings,
        x=nodes[:,0],
        y=nodes[:,1],
        z=nodes[:,2],
        intensitymode='cell',
        flatshading=True,
        i=i,
        j=j,
        k=k,
        showscale=False
    )


def __get_node_scatter3d(nodes):
    '''
    Constructs a plotly scatter3d object from a list of nodes
    '''
    return go.Scatter3d(
        x=nodes[:,0],
        y=nodes[:,1],
        z=nodes[:,2],
        mode ='markers', 
        marker = dict(
            size = 3,
            color = '#CC0000',
            opacity = 0.7
        )
    )