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

## Releasing the package on PyPI

Releasing a new version of the package on PyPI requires API tokens for the test and real PyPI servers. You can find these tokens in your PyPI account settings. Copy `.env.copy` to `.env` and add your tokens to this file.

When you're ready to release a new version of the package, first update the version number in `pyproject.toml`. This should be done in a standalone PR. Note that we use semantic versioning in which the versions have the form `MAJOR.MINOR.PATCH`. See [here](https://semver.org/) for more. Once the PR is merged, create a new git tag for the new version. In the example below, we're releasing version 0.1.0. __Make sure your local git repository is up-to-date before creating the tag!__

```bash
git tag -a v0.1.0 -m "Release version 0.1.0"
git push origin v0.1.0
```

Then, build the package and upload the build artifacts to the PyPI test server:

```bash
make test-publish
```

This command calls `poetry build` to build the package and then `poetry publish` to upload the build artifacts to the test server.

Note: the build artifacts are also written to the `dist/` directory. 

Check that you can install the package from the test server:

```bash
pip install --index-url https://test.pypi.org/simple/ arcadia-pycolor
```

If everything looks good, build and publish the package to the real PyPI server:

```bash
make publish
```

Finally, check that you can install the package from the real PyPI server:

```bash
pip install arcadia-pycolor
```
