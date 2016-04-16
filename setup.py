from setuptools import setup

from bars import __version__


setup(name="bars",
      version=__version__,
      description="A command-line interface that loads a CSV file and outputs "
                  "a bar chart.",
      long_description=open("README.rst").read(),
      url="https://github.com/flother/bars",
      classifiers=[
          "Development Status :: 4 - Beta",
          "Environment :: Console",
          "Intended Audience :: Developers",
          "Intended Audience :: Science/Research",
          "Intended Audience :: System Administrators",
          "License :: OSI Approved :: MIT License",
          "Natural Language :: English",
          "Programming Language :: Python :: 3",
          "Topic :: Utilities",
      ],
      modules=["bars"],
      entry_points={
          "console_scripts": ["bars=bars:main"],
      },
      install_requires=[
          "agate==1.3.1",
          "click==6.6",
      ])
