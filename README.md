# DEES_Python_course

This repository contains a series of [Jupyter](https://jupyter.org) notebooks designed to practice developing and applying Python across challenges in the Earth Sciences. There are so many courses now available to pick up core operations in Python, this course is targetted more at diving straight in and providing templates for common operations. 

[![DOI](https://zenodo.org/badge/233927415.svg)](https://zenodo.org/badge/latestdoi/233927415)

At the start of this course we will explain how you will access and interact with the course materials, but this repository also outlines multiple ways you can work with us from your own machine to running on free cloud services. 

<img src="images/Intro2.png" width="800"/>

# Table of contents
1. [Course overview](#Course-overview)
2. [Running the models](#Running)
     * 2a. [Using the University Jupyter-hub **(recommended for UoM students)**](#UoMhub)
     * 2b. [Using your own machine](#own)
     * 2c. [Using Binder](#Binder)
     * 2d. [Using Google Colab](#Colab)
3. [Folder structure and running the examples](#Folder-Structure)
4. [Expectations and pace of learning](#Expectations)
5. [Code of Conduct](#Code-of-Conduct)

## Course overview<a name="Course-overview"></a>

This course has been developed with the notion that learning any programming language is most effective when provided with domain relevant examples. However, it is also important to cover some basic/fundamental operations. In each notebook you will find a narrative that matches an associate lecture, though they should be able to provide learning material on their own. 

## Running the models<a name="Running"></a>

If you have not used a Jupyter notebook before, I would reccomend checking out the official [webpage](https://jupyter.org/). There is also information provided in the lectures associated with this course. There are multiple ways you can interact with a Jupyter notebook. The most flexible way is to open and interact with them on your own computer or via a Jupyter-hub instance. However, you can also start an instance of every notebook running in the cloud. We provide details below.

### 2(a). Using the University Jupyter-hub **(recommended for UoM students)**<a name="UoMhub"></a>

If you are a student at the University of Manchester, we will show you how to run this course on a University cluster. You will find these details on the Blackboard page of our course. This includes instructions on how to download all of the course material and install a few packages before we dive in.

### 2(b). Using your own machine<a name="own"></a>

Having a Python distribution on your own machine is attractive for a number of reasons, not least gaining familiarity with building projects in your own time. If you havent already, I would reccomend installing the Anaconda distribution. You can download a copy using [this link](https://www.anaconda.com/products/individual). That page will give you the option to download a version for Windows, Mac or Linux. Download the graphical installer and, typically, accept all options. Once you have installed this, now open a terminal. On Windows, go to the menu of options and find 'Anaconda Prompt' under the Anaconda folder. On a Mac, go to Finder -> Utilities -> Terminal. If on a Mac, when in this terminal when you type:

> Python

Do you see the reference to Anaconda? For example, you may see something *similar* to:

> Python 3.7.6 (default, Jan  8 2020, 20:23:39) [MSC v.1916 64 bit (AMD64)] :: Anaconda, Inc. on win32

Now we are going to create a virtual environment to run our notebooks in. Virtal environments are a great way of maintaining a 'work space' that is seperate to your default installation. For example, if you are going to start installing lots of bespoke modules, you may sometimes come across a clash of version numbers which then becomes tricky to maintain. In the worst case scenario, this would require a re-installation of Python. So lets create a virtual environment for our project. You can switch-on and switch-ff these virtual environments from the command line/terminal whenever you need them.

If you are on Windows, go back to the Anaconda prompt. If you are on a Mac or Linux, go back to ther terminal. First we need to clone this repository. We should use Git for this, becuase with Git you can keep pulling updates from this repository. If you do not already have Git installed on your machine, you can get it from the [download page](https://git-scm.com/downloads). Once you have installed this, at the prompt/terminal type:

> git clone https://github.com/loftytopping/DEES_programming_course.git

This will download the project to the location you are in already. You can change this location before running the above command, or move the folder later. Github also gives you the option to download a ZIP file of the entire project if you cannot, or do not want, to use Git. Once you have the project downloaded, open a command prompt/terminal and navigate to the project folder. We are now going to use the file 'environment.yml' to create a new virtual environment. Run the following command:

> conda env create -f environment.yml

You will see a number of packages being downloaded by the conda package manager which is part of the Anaconda distribution. Accept any requests and, when finished, you will see a message that resembles the following:

    To activate this environment, use
    
        $ conda activate DEES_python
    
    To deactivate an active environment, use
    
        $ conda deactivate
        
These are the commands for switching on/off this new virtual environment. Let's switch it on. Type the following in the command prompt/terminal:

> conda activate DEES_python

In the command prompt, you will see the name (DEES_programming_env) replace (base). Now we can start an interactive Jupyer notebook session. Still within the project folder, type the following:

> jupyter notebook

Can you see the project folders and files? You are good to go! Every time you now want to open the notebooks for this project, open either the Anaconda prompt or Terminal, activate the environment and then run the last command from within the project folder.

### 2(c). Binder <a name="Binder"></a>

If you do not, or cannot, run Python from your own machine we have provided the ability for you to interact with these files using Binder. The Binder project offers an easy place to share computing environments to everyone. It allows users to specify custom environments and share them with a [single link](https://jupyter.org/binder). Indeed, if you click the link below this will spin-up an individual session for you. Please bare in mind it can take a while to start, and if idle for a short period these sessions will stop. However you can download your notebook file during the session. Everytime you start a Binder link, it will start from scratch.

[![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/loftytopping/DEES_programming_course/HEAD)

### 2(d). Using Google Colab<a name="Colab"></a>

Google's Colab [Co-laboratory](https://colab.research.google.com) is a great platform for developing machine learning and data-science driven applications on the web. It provides access to free GPU resource (Graphics Processing Units). However it also allows us to run Jupyter notebooks from a Github repository *if you have a Google account*. If you can register or have an existing Google account, using Google Colab is a really nice experience. It will allow you to save individual files and projects to your Google Drive. It also meas you can access the course anywhere off campus without needing a VPN. By clicking on the Google Colab link it will take you to the Google Colab platform. The first thing you see will be some Python code, running in a Jupyter notebook. Click anywhere in the code block and then, to the left hand side, you will see a 'play' button. If you click this button Google Colab will run the code in there. This code essentially creates a new folder on your Google Drive and then mounts that drive before downloading the entire course. Once complete you can then run through the course material from your Google account. 

- [![Open notebook In Colab](https://colab.research.google.com/assets/colab-badge.svg)](https://colab.research.google.com/github/loftytopping/DEES_programming_course/blob/master/Setup_GoogleColab.ipynb)

## Repository structure and using Jupyter notebooks <a name="Folder-Structure"></a>

    .                           # Root folder of our repository
    ├── assessments             # Folder containing notebook templates for chosen assignment
    |------ data                  # Data used in assignment notebooks
    ├── data                    # Contains data used in Pandas examples 
    ├── images                  # Contains images for all notebooks
    ├── solutions               # Contains the same notebooks as in our root folder but with solutions
    |------ data                  # Data used in solutions notebooks
    |------ images                # images used in solutions notebooks
    ├── Practical 1.            # Individual notebook practicals
    ├── Practical 2. ....
    ├── LICENSE
    └── README.md
    
## Expectations and pace of learning<a name="Expectations"></a>

We cant teach everything Python or any programming language has to offer in this course, but we can given you a set of tools to begin your journey into the wonderful world of programming and data analysis in aerosol science. Please note that you should not feel pressured to complete every exercise in class. These practicals are designed for you to take outside of class and continue working on them. Proposed solutions to all exercises can be found in the 'solutions' folder. After reading the instructions and aims of any exercise, search the code snippets for a note that reads ------'INSERT CODE HERE'------ to identify where you need to write your code. These are often proposed solutions and you may have your own way of solving then. That is fine! Quite often in programming there are many ways to 'cut the cloth'. In this course we will not cover optimisation but try to stick to a 'Pythonic' way of solving things without sacrificing your learning path. 
    
## Code of Conduct<a name="Code-of-Conduct"></a>

Please note that this project is released with a Contributor Code of Conduct. By participating in this project you agree to abide by its [terms](code-of-conduct.md). 

## Disclaimer
Content is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU General Public License for more details.                                                                            You should have received a copy of the GNU General Public License along with this repository.  If not, see <http://www.gnu.org/licenses/>.            
