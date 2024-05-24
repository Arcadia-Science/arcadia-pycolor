# arcadia-pycolor

Tools for using the Arcadia color palettes and figure style guide in Python.  
This package automatically generate color palettes and color maps for use with Matplotlib.

## Installation

TODO: write installation instructions once the package is hosted on PyPI.

## Usage

See [this notebook](usage_example.ipynb) for examples of how to use the color palettes and color maps in this package.

## Development

We use poetry to manage dependencies and packaging. First, create a new conda environment and install poetry:

```bash
conda create -n arcadia-pycolor -f envs/dev.yml
conda activate arcadia-pycolor
```

Then, install dependencies:

```bash
poetry install --no-root
```

Finally, install the package in editable mode:

```bash
pip install -e .
```

## Publishing

To publish a new version of the package, first update the version number in `pyproject.toml`. Then, build the package and upload the build artifacts to the PyPI test server:

```bash
make test-publish
```

The build artifacts are written to `dist/` directory. 

You can then install the package from the test server using:

```bash
pip install --index-url https://test.pypi.org/simple/ arcadia-pycolor
```

If everything looks good, publish the package to the real PyPI server:

```bash
make publish
```
