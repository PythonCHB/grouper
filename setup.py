from setuptools import setup, find_packages

long_description = open("README.md").read()

setup(name='grouper',
      version="0.0.1",
      author="Christopher H Barker",
      author_email="PythonCHB@gmail.com",
      description="Prototype for a special dict for groupby operations",
      long_description=long_description,
      long_description_content_type="text/markdown",
      url="https://github.com/PythonCHB/grouper",
      packages=find_packages(),
      classifiers=("Programming Language :: Python :: 3",
                   "License :: OSI Approved :: BSD2 License",
                   "Operating System :: OS Independent",
                   ),
      )
