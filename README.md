# arcadia-pycolor

This repo contains a Python package called `arcadia_pycolor` that provides tools for using the Arcadia color palettes and for styling Matplotlib figures to comply with Arcadia's style guide.

## Installation

The package is hosted on PyPI and can be installed using pip:

```bash
pip install arcadia-pycolor
```

## Usage

Please see [the quickstart guide](docs/quickstart.md) for an introduction to the package and how to use it to style Matplotlib and seaborn plots.

For detailed documentation about the package and links to example plots, see the [documentation README](docs/README.md).

## Development

### Environment setup

We use poetry to manage dependencies and packaging. First, create a new conda environment and install poetry:

```bash
conda create -n arcadia-pycolor -f envs/dev.yml
conda activate arcadia-pycolor
```

Then, install dependencies, including the development dependencies:

```bash
poetry install --no-root --with=dev
```

Finally, install the package in editable mode:

```bash
pip install -e .
```

### Testing

We use pytest for testing. The tests are found in the `arcadia_pycolor/tests/` subpackage. To run the tests, simply run `pytest` from the root directory of the repository.

Some of the tests generate plots whose correctness is difficult to validate programmatically. Therefore, when changes are made to the style defaults or to the auto-styling methods in `arcadia_pycolor.mpl`, it is important to manually inspect these plots to verify that no unintended changes have been introduced. To do so, there is a custom `--output-dirpath` pytest option that can be used to save the test plots to a local directory. For example, to save the test plots to a directory called `test-outputs`, run:

```bash
pytest --output-dirpath ./test-outputs
```

The directory passed to `--output-dirpath` will be created if it does not already exist and will be overwritten if it does exist. The test plots will be saved in this directory as PDF files with the same names as the test functions that generated them. The tests are parametrized by the pre-defined figure sizes in `arcadia_pycolor.style_defaults`, so there will be one file for each test and each figure size.

Hint: you can use pytest's `-k` option to filter the tests that are run if you only need to generate certain plots. This can be convenient for faster feedback during development. For example, to run only the tests that generate barplots, run:

```bash
pytest -k barplots --output-dirpath ./test-outputs
```

### Updating the Jupyter notebooks

Some of the documentation is in the form of Jupyter notebooks. The inline graphical outputs of these notebooks are part of the documentation, so these notebooks are committed to the repo with their outputs included. It is therefore important to keep the notebook outputs up-to-date by re-running all of the notebooks when changes are made to the package.

Run the makefile command `execute-all-notebooks` to execute all the notebooks. This 1) ensures that the notebooks execute without errors and 2) updates their outputs in-place. Then, commit any modified notebooks to the repo.

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
