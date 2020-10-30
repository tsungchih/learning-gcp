# learning-gcp
This repository embraces all my learning history in terms of GCP.

## How to initiate docs directory by means of Sphinx

When initiating the `docs` directory by means of Sphinx, we can use `sphinx-quickstart`.

```shell
$ sphinx-quickstart 
欢迎使用 Sphinx 3.2.1 快速配置工具。

Please enter values for the following settings (just press Enter to
accept a default value, if one is given in brackets).

Selected root path: .

You have two options for placing the build directory for Sphinx output.
Either, you use a directory "_build" within the root path, or you separate
"source" and "build" directories within the root path.
> 独立的源文件和构建目录（y/n） [n]: n

The project name will occur in several places in the built documentation.
> 项目名称: ProjectName
> 作者名称: George, T. C. Lai
> 项目发行版本 []: 

If the documents are to be written in a language other than English,
you can select a language here by its language code. Sphinx will then
translate text that it generates into that language.

For a list of supported codes, see
https://www.sphinx-doc.org/en/master/usage/configuration.html#confval-language.
> 项目语种 [en]: 

创建文件 /Users/george/Documents/projects/python/learning-gcp/gcp-bigtable/docs-test/conf.py。
创建文件 /Users/george/Documents/projects/python/learning-gcp/gcp-bigtable/docs-test/index.rst。
创建文件 /Users/george/Documents/projects/python/learning-gcp/gcp-bigtable/docs-test/Makefile。
创建文件 /Users/george/Documents/projects/python/learning-gcp/gcp-bigtable/docs-test/make.bat。

完成：已创建初始目录结构。

You should now populate your master file /Users/george/Documents/projects/python/learning-gcp/gcp-bigtable/docs-test/index.rst and create other documentation
source files. Use the Makefile to build the docs, like so:
   make builder
where "builder" is one of the supported builders, e.g. html, latex or linkcheck.
```

After having finished the above procedure, we have the following structure in the `docs` directory.

```shell
.
├── Makefile
├── _build
├── _static
├── _templates
├── conf.py
├── index.rst
└── make.bat
```

As a result of using src-layout, we need to make following least changes to the `conf.py`.

```python
# Add src directory to the python path
sys.path.insert(0, os.path.abspath('../src'))
```

We can also add some more necessary extensions for Sphinx to use, such as those listed as follows.

```python
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.autosummary",
    "sphinx.ext.doctest",
    "sphinx.ext.intersphinx",
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.napoleon",
]
```

We can then add `.rst` documents in `docs` directory. The content would be like

```python
.. automodule:: <MODULE_NAME>
  :members:
  :show-inheritance:
```