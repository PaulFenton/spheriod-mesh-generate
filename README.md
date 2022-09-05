# spheriod-mesh-generate
Spheroid Mesh Generation and Visualization Utilities. Accompanying blog post: https://fentonsoftware.com/generating-spheroidal-meshes-in-python/

# Prerequisites

* [Anaconda](https://www.anaconda.com/) or [miniconda](https://docs.conda.io/en/latest/miniconda.html)

# Setup
Install prerequisites such as `numpy`, `plotly`, `moviepy`, and `scipy`, and others via `conda`.

```sh
conda create -n "astro" python=3.9 --file requirements.txt
conda activate astro
```

## Start the jupyter notebook
```sh
jupyter notebook globe_mesh_uv.ipynb
```

Run through the notebook to generate interactive 3D charts and .gifs like this:

![Gif example](./image/uv_spheroid_full.gif)

Use comments to toggle between the plotting utils to generate 3D charts (`show_poly_3d()`) or
.gifs (`create_poly_3d_gif()`):
```py
show_poly_3d(<...>)
#create_poly_3d_gif(<...>)
```
