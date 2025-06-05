# BRG-ZHCODE

BRG workshop at ZHCODE

## Prerequisites

### CAD

- Rhino 8

### Python Environment

- **Recommended:** [Miniforge](https://github.com/conda-forge/miniforge)
- **Alternative:** [Anaconda](https://www.anaconda.com/) or [Miniconda](https://docs.conda.io/en/latest/miniconda.html)

### Code Editor

[Visual Studio Code](https://code.visualstudio.com/) with the following extensions from Microsoft:

- Python
- Pylance
- C++ Extension Pack

### C++ Compiler Setup

*This is only needed on Friday...*

#### Windows

- Install [Visual Studio](https://visualstudio.microsoft.com/)  
- During installation, select **"Desktop development with C++"** workload

#### macOS

```bash
xcode-select --install
```

#### Ubuntu

```bash
sudo apt-get install build-essential
```

## Installation

We will repeat the installation process during the workshop.
However, it is useful to already test that the installed tools work properly.

If you are totally new to `conda`, please refer to the [getting started instructions](https://docs.conda.io/projects/conda/en/latest/user-guide/getting-started.html).

On Windows, use the `Anaconda Prompt` instead of the standard `Commdand Prompt` or `Windows Powershell` to run `conda` commands.
On Mac, you can just use the `Terminal`.

## Create an environment

Using `conda`, create an environment `zha-intro`, and install `python3.12` and `compas_occ` from `conda-forge`.

```bash
conda create -n zha-intro -c conda-forge python=3.12 compas_occ -y
```

## Activate the environment

You can have many environments in parallel.
Therefore, you need to activate the environment you want to use.

```bash
conda activate zha-intro
```

## Install packages

Except for `compas_occ`, the core packages of the COMPAS Framework can be installed directly from `PyPI` using the `compas_framework` meta package.

```bash
pip install "compas_framework>=0.1.3"
```

This will install

- `compas >= 2.13`
- `compas_cgal`
- `compas_gmsh`
- `compas_libigl`
- `compas_model`
- `compas_session`
- `compas_shapeop`
- `compas_viewer`

## Test the installation

Launch an interactive Python interpreter.

```bash
python
```

When the Python interpreter is active you will see the Python prompt (`>>>`).
Import some or all of the installed packages and print their version.

```bash
>>> import compas
>>> print(compas.__version__)
'2.13.0'
>>>
```

Exit the interpreter when you're done.

```bash
>>> exit()
```

## C++ / Python binding

- [Step-by-step tutorial.](https://docs.google.com/presentation/d/1HL4o8cadvuZlQDsdYlslzeDhDVvTUlPdk9zTSn5fsLA/edit?slide=id.g35f9a478f0a_0_5#slide=id.g35f9a478f0a_0_5)
