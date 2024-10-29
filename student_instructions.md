# Hands-On Optics Calculations - Setup Instructions
---

During the Hands-On Optics Calculations, we will use **Python3** and [`Xsuite`](https://xsuite.readthedocs.io/en/latest/).

`Xsuite` is a collection of python packages for the simulation of the beam dynamics in particle accelerators. 

> **Important:** we kindly ask you to go through this document **before coming** to CAS, such as to **prepare yourself**  for the course. We will explain in the following sections how to install all necessary software on your laptop. **A basic knowledge of Python is assumed**. If you are not familiar with Python, you can find a few resources to fill the gap in the following sections. Do not worry about the theory of Optics Calculations for the moment (it will be discussed in details during the school), just focus on Python and the installation.

After [a short introduction](#a-very-short-introduction-to-python), we will focus on the [software setup](#software-setup). 
Finally, in [appendix](#appendix-python-packages), you will find links and cheatsheets for the most common Python packages that will be used during the course.



---
# A very short introduction to Python
You can find several nice courses, videos and resources on the internet. Here you have a couple of suggestions you can find on YouTube:

<p align="center">
<a href=http://www.youtube.com/watch?v=kqtD5dpn9C8><img src="http://img.youtube.com/vi/kqtD5dpn9C8/0.jpg" alt="Python for Beginners - Learn Python in 1 Hour" width="40%"/></a> 
&nbsp;&nbsp;&nbsp;&nbsp;
<a href=http://www.youtube.com/watch?v=rfscVS0vtbw><img src="http://img.youtube.com/vi/rfscVS0vtbw/0.jpg" alt="Learn Python - Full Course for Beginners" width="40%"/></a>
</p>

### Test Python on a web page

If you are not familiar with Python and you have not installed it on your laptop, you can start playing with simple python snippets on the web (e.g., [CoLab](https://colab.research.google.com/drive/1Pk-UPE2-OCA2UCFIunqDwxXmQi9Yvp-C?usp=sharing), a Google account is needed).


You can test the following commands:

```python
import numpy as np

# Matrix definition
Omega=np.array([[0, 1],[-1,0]])
M=np.array([[1, 0],[1,1]])

# Sum and multiplication of matrices
Omega - M.T @ Omega @ M
# M.T means the "traspose of M".

# Function definition
def Q(f=1):
    return np.array([[1, 0],[-1/f,1]])

# Eigenvalues and eigenvectors
np.linalg.eig(M)
```
You can compare and check your output with the ones [here](000_example.ipynb).

---
# Software Setup

In this section, we will explain how to install Python locally on your laptop. 

> We suggest not to use CoLab (or other remote servers) during the hands-on since there could be problem with the internet connection.
 
There are many ways to use Python on your laptop.  You can use it from the terminal, from the browser with Jupyter/JupyterLab or in an Integrated Developer Environment, [IDE](https://www.google.com/search?q=most+popular+python+ide). During the lectures and the Hands-on, we will use Python and JupyterLab.


JupyterLab is a user-friendly environment to work with Python. 
You can find an overview on JupyterLab [here](https://jupyterlab.readthedocs.io/en/stable/).


## Installation

We suggest installing **Xsuite** following the instructions of the [Basic Installation](https://xsuite.readthedocs.io/en/latest/installation.html#basic-installation). There you will find the procedures to install it on Linux, Mac and Windows Operating Systems (OS). For Windows OS, please use the Windows Subsystem for Linux, [WSL](https://en.wikipedia.org/wiki/Windows_Subsystem_for_Linux).


Then please install the additional packages with

```bash
pip install matplotlib ipywidgets jupyter jupyterlab sympy
```

After the installation, launch JupyterLab and then test that everything works.

## Launch Jupyter


1. Launch JupyterLab from your terminal:

    ```bash
    jupyter lab
    ```

2. Follow the instructions given in the terminal. You should end-up on your default browser with a page similar to this [image](https://ipython-books.github.io/pages/chapter03_notebook/06_jupyterlab_files/home.png).

This will be your **working directory**. 

3. Start playing with Python! Please make sure to go throw all the [000_example.ipynb](000_example.ipynb) to familiarize with the typical Python concepts that will be used during the course, but also to verify your installation. 

<!-- If you happen to experience any problem, please check to have installed the whole anaconda distribution. Alternatively, you can try to go back to your terminal, and install each single (or missing) package independently, e.g.:

```python
pip install numpy matplotlib seaborn scipy ipywidgets jupyter jupyterlab sympy cpymad PyNAFF
``` -->

5. If you are not familiar with Python, you can start playing with simple python snippets. For example, have a look at the following [examples/PythonBasic.ipynb](examples/PythonBasic.ipynb) (courtesy of *Simon Albright*).


6. **Just before the start of the course**, we will ask you to download the **latest version** of the [hands-on lattice exercises](./exercises/Exercises.pdf) (even better, the whole repository) in your **working directory**.

<!-- 7. **Optional:** instead of running Jupyter lab within a browser, you can try to install and the [jupyterlab-desktop](https://github.com/jupyterlab/jupyterlab-desktop) application. -->

---
## Appendix: Python Packages

You can leverage python's capability by exploring a galaxy of packages. Below you can find the most useful for our course (focus mostly on `numpy` and `matplotlib`) and some very popular ones. 

### The *numpy* package
To get familiar with the *numpy* package, have a look at the following [summary poster](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Numpy_Python_Cheat_Sheet.pdf).
You can google many other resources, but the one presented of the poster covers the set of instructions you should be familiar with.

### The *matplotlib* package
To get familiar with the *matplotlib* package, have a look at the following [summary poster](https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Python_Matplotlib_Cheat_Sheet.pdf).

### The *linalg* module
To get familiar with the Linear Algebra (linalg) package, have a look at the following [summary poster](
https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Python_SciPy_Cheat_Sheet_Linear_Algebra.pdf).

### The *pandas* package (optional)
To get familiar with the *pandas* package, have a look at the following [summary poster](
https://s3.amazonaws.com/assets.datacamp.com/blog_assets/PandasPythonForDataScience.pdf).

### The *seaborn* package (optional)
To get familiar with the *seaborn* package, have a look at the following [summary poster](
https://s3.amazonaws.com/assets.datacamp.com/blog_assets/Python_Seaborn_Cheat_Sheet.pdf).

### The *sympy* package (optional)
To get familiar with the *sympy* package, have a look at the following [summary poster](http://daabzlatex.s3.amazonaws.com/9065616cce623384fe5394eddfea4c52.pdf).

