# spheriod-mesh-generate
Spheroid Mesh Generation and Visualization

# Prerequisites

* (Anaconda)[https://www.anaconda.com/] or (miniconda)[https://docs.conda.io/en/latest/miniconda.html]
* 
# Setup
Install prerequisites such as `numpy`, `plotly`, `moviepy`, and `scipy`

```sh
conda create -n "astro" python=3.9 --file requirements.txt
conda activate astro
```

## Start a jupyter notebook
```sh
jupyter notebook globe_mesh_uv.ipynb
```

## Generate .html file from the notebook
```sh
jupyter nbconvert --to html globe_mesh_uv.ipynb

jupyter nbconvert --execute --to html /path/to/example.ipynb --HTMLExporter.theme=dark

jupyter nbconvert --Exporter.preprocess_cell=[\"nbconvert_preprocess.RemoveCellsWithNoTags\"] --ClearOutputPreprocessor.enabled=True --to notebook --output=mesh_pt_1 globe_mesh_uv.ipynb

jupyter nbconvert --Exporter.preprocessors=[\"preprocess.PP\"] --ClearOutputPreprocessor.enabled=True --to html --output=mesh_pt_3 globe_mesh_uv.ipynb

jupyter nbconvert --Exporter.preprocessors=[\"from nbconvert.preprocessors import Preprocessor as pre
class PP(pre):
    def preprocess(self, nb, r):
        nb.cells = [c for i, c in enumerate(nb.cells) if i in {1,2,3}]
        return nb, r\"]
--ClearOutputPreprocessor.enabled=True --to html --output=mesh_pt_3 globe_mesh_uv.ipynb
```