# DEES_Python_course

This repository contains a series of [Jupyter](https://jupyter.org) notebooks designed to practice developing and applying Python across challanges in the Earth Sciences. There are so many courses now available to pick up core operations in Python, this course is targetted more at diving straight in and providing templates for common operations.

<img src="images/Introduction.png" width="800"/>

Please check the project wiki page for more information on updates and planned releases should you wish to follow this repository outside of the University module. This project is licensed under the terms of the Creative Commons (CC) License v3.0, as provided with this repository. 

# Table of contents
1. [Course overview](#Course-overview)
2. [Dependencies and running examples](#Dependencies)
     * 2a. [The current course (2020)](#Course-note)
     * 2b. [Using your own machine](#Own)
3. [Folder structure and running the examples](#Folder-Structure)
4. [Expectations and pace of learning](#Expectations)
5. [Code of Conduct](#Code-of-Conduct)

## Course overview<a name="Course-overview"></a>

This course has been developed with the notion that learning Python is best when provided with domain relevant examples. However it is also important to cover some basic/fundamental operations. In each notebook you will find a narrative that matches each weekly lecture, whilst also walking you through a series of exercises that not only reaffirm the new skills being developed, but serve as a reference point for further practicals as we move through the course.

First, you will need to clone this repository into a local folder. Create a folder on your machine, and then run the following command from a command prompt:

git clone. xxx

## Dependencies and running examples <a name="Dependencies"></a>

The material provided has been built in the [Anaconda Python 3.7 environment](https://www.anaconda.com/download/#macos). [Assimulo](http://www.jmodelica.org/assimulo). Apart from one mapping package we use, Cartopy, the vanilla installation of the Anaconda environment should provide you with all of the modules we will be using, namely:
 
#### Used modules:

Module        |  Note
------------- | -------------
[matplotlib](https://matplotlib.org/)    |  A plotting package
[numpy](https://www.scipy.org/scipylib/download.html)         |  A numerical package designed for efficient operations
[pandas](https://pandas.pydata.org/)        |  A module dedicated to data structures and data analysis tools.
[scipy](https://www.scipy.org)         |  (pronounced “Sigh Pie”) is a Python-based ecosystem of open-source software for mathematics, science, and engineering
[time](https://docs.scipy.org/doc/numpy/f2py/)  |  A module for checking duration, introducing time-dependent operations etc
[Seaborn](https://seaborn.pydata.org)  |  data visualization library based on matplotlib
[Scikit Learn](https://scikit-learn.org/stable/)  |  A module dedicate to developing and deploying machine learning functions
 
### The current course (2020) <a name="Course-note"></a>

Most of the large University clusters will allow you to run the provided notebooks by issuing the following command in a command prompt

> jupyter notebook

This should ideally be run in the same directory your notebook files are.

**Important note for the 2020 course**: We have been allocated a cluster with a specific environment which will require you to use the following command, **in the Anaconda prompt**, to run our jupyter notebooks.

> jupyter-notebook --notebook-dir .\ --NotebookApp.token='' --NotebookApp.password=''

You can find the Anaconda prompt in the menu of applications in Windows. You will also need to make sure you clone this repository into your P:\ drive if you want to keep working on modified files in-between sessions. If not, you will have to re-clone this repository everytime. To access your P:\ drive you simply need to type P:\ in the command prompt. We will show you in class how to clone to your P:\ drive.

Please note you might find it easier to issue this command in the directory where you have cloned this repository, but you should be able to navigate to find them. Once you issue this command you should find a web browser takes you to the default home page which will look like the following figure:

<img src="images/Home_page_example.png" width="800"/>

From here you will then be able to click on any of the jupyter notebooks, or folders, to access the material you are interested in.

### Using your own machine <a name="Own"></a>

As noted above, this course is designed to work within the recent Anaconda environment which will work on Windows/Mac/Linux. Depending on your operating system you can install this by downloading the relevant installation script from the [Anaconda webpage](https://www.anaconda.com/distribution/). For the practical on geospatial plotting we also use a package called [Cartopy](https://scitools.org.uk/cartopy/docs/latest/). The Anaconda environment also comes with its own package manager and the following command 'should' install this additional package for you:

> conda install cartopy

Once this has been installed, you can then start working through the notebooks provided by running the following command in the root folder of this repository:

> jupyter notebook

## Repository structure and using Jupyter notebooks <a name="Folder-Structure"></a>

    .                           # Root folder of our repository
    ├── assessments             # Folder containing notebook templates for chosen assignment
    |------ data                  # Data used in assignment notebooks
    ├── data                    # Contains data used in Pandas examples 
    ├── images                  # Contains images for all notebooks
    ├── solutions               # Contains the same notebooks as in our root folder but with solutions
    |------ data                  # Data used in solutions notebooks
    |------ images                # images used in solutions notebooks
    ├── Practical 1. Introduction to data types and numerical operations.ipynb         # Individual notebook practicals
    ├── Practical 2. ....
    ├── LICENSE
    └── README.md
    
## Expectations and pace of learning<a name="Expectations"></a>

We cant teach everything Python has to offer in this course, but we can given you a set of tools to begin your journey into the wonderful world of programming and data analysis. Please note that you should not feel pressured to complete every exercise in class. These practicals are designed for you to take outside of class and continue working on them. Proposed solutions to all exercises can be found in the 'solutions' folder. After reading the instructions and aims of any exercise, search the code snippets for a note that reads ------'INSERT CODE HERE'------ to identify where you need to write your code. These are often proposed solutions and you may have your own way of solving then. That is fine! Quite often in programming there are many ways to 'cut the cloth'. In this course we will not cover optimisation but try to stick to a 'Pythonic' way of solving things without sacrificing your learning path. 
    
## Code of Conduct<a name="Code-of-Conduct"></a>

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its [terms](code-of-conduct.md). 
