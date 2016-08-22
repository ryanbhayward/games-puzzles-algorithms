# Technical Overview

This document aims to provide a gentle technical introduction to the tools used in this project, as well as the rationale behind each tool's inclusion.

## The Command-line Environment

If you have never used an UNIX-like operating system before, this course may be your first time interacting with a command-line environment. The command-line environment is really made up of two parts, the *terminal emulator*, which provides basic input and output capabilities, and the *shell*, which provides an interactive command-line interface.

For example, a fresh installation of Ubuntu will be using `GNOME Terminal` as its terminal emulator, and the `Bourne again shell` (more commonly referred to as `Bash`) as its shell.

When we start our terminal program, we are really first starting the terminal emulator, and then invoking our user's shell, which lets us interact with the system.

On an UNIX-like system, the file system is organized as a hierarchical tree. Internal nodes of the tree are called directories (equivalent to folders in other operating systems), and the leaves of the tree are files. At the root of the tree is the `/` directory, which all other directories lie beneath. When we talk about where to find some file or directory, we will refer to its *path* in the file system. This path tells us which directories to follow starting from the root in order to find what we're looking for. For example, the path `/usr/local/bin/program` tells us, starting from the root directory, `/`, to enter the `usr` directory, and then the `bin` directory, and from here we can find `program`.

When the shell is started, we will find ourselves in the user's *home directory*. This home directory is meant to contain all of the user's personal files. Usually, the user's home directory can be found at `/home/username/`, where `username` is the user's username.

To issue a command through the shell, the normal syntax is to type the name of the command, followed by any arguments. For example, `ls ./` will invoke the `ls` command, which lists directory contents, with the argument `./`, which signifies the current directory. Many commands also feature optional arguments called 'long options' and 'short options', which are invoked by adding specified arguments prefaced by either '--' or '-'. For example, to see a detailed listing of the current directory contents, with human readable output, we could issue `ls -l --human-readable`, or `ls -l -h`. These two commands are equivalent, and indeed short options are so named because they are usually one or two letter abbreviations for an equivalent long option.

To navigate around the file system, we will make use of the `ls` and `cd` commands. `ls` lists the directory contents, and `cd` changes the directory. For example, starting from our user's home directory, we might issue `ls`, and see the following:

`documents/ pictures/ downloads/ desktop/`

Now, if we wanted to enter the `documents` directory, we would issue `cd documents`. This command will change our current directory from `/home/username/` to `/home/username/documents/`.

All of the built-in commands, and many additional commands, have manual pages which we can access with the `man` command. For example, to see how to use `cd`, we can issue `man cd` to read its manual. The *man pages* have an explanation of what the command is, the available options, and usually also include usage examples. If you're ever unsure of how to use a command, the man page is a good place to start, and you can also usually find lots of examples and tutorials online.

There are many tutorials and introductions to the command-line interface and common tools available on UNIX-like systems, and so we will omit a full treatment here.


[//]: # "TODO: Provide references for simple bash usage and commands."


At this point, you might be wondering why we bother using a command-line environment instead of sticking to a graphical user interface (GUI) for everything we do. In short, we use the command-line environment because it provides more flexibility and power than a GUI. With a GUI, we are limited to the functionality that the GUI's programmers have provided. By contrast, a command-line environment gives us the freedom to compose different tools and to write scripts to perform complex tasks. In UNIX-like systems, we can use *pipes* in our commands to feed the output of one command as the input to another. This allows us to chain commands together, forming a 'pipeline' which processes data. For more complex functionality, we can write *shell scripts* that describe sequences of commands to run, and which we can then re-use many times. This gives us the power to combine many different tools using a common interface, the command-line, that might be very difficult or even impossible if we limited ourselves to only using GUIs.

## Programming Languages

This project primarily makes use of two programming languages, Python and JavaScript.

### Python

Python is a high-level general-purpose programming language. Python has several features that made it our main choice of programming language for this course.

Firstly, the standard Python interpreters are available for every major operating system, and the Python standard library provides good abstractions for many standard operations, which makes it very easy to write portable code that will run in most environments.

Secondly, Python provides a very powerful interactive environment through its REPL (Read-Eval-Print-Loop). This interactive environment makes it very easy to play and experiment with your programs. It also offers the means to very easily interact with the programs we will be providing as part of the course while they are running in order to better understand them.

Lastly, Python makes it very easy to write clear and concise code that is easy to read and understand. Generally, it is easier to write clean and readable code in Python than in lower level languages which provide less abstraction from the underlying machine. This is because Python automatically handles many lower level details such as memory management while also providing high level abstractions which form the building blocks of our programs.

To run a Python program, we simply issue `python program.py`, where `program.py` is the name of our Python program.

To start the Python REPL, we can issue `python`. To start the interactive environment after running a Python program, we can use the `-i` argument, and issue `python -i program.py`. After the program is finished running, we will enter the Python REPL and will be able to interact with anything that the program has brought into scope.

### JavaScript



## Tools

We use a variety of tools as part of the project. In this section, we will briefly go over some of the tools we are using, providing an explanation of the purpose of each.

### GNU Make

One of the key concepts of software development is taking tedious and repetitive tasks and automating them so that we are able to recreate the effect of the task while having software accomplish it for us.

An example of such a task that we would like to automate is building software projects from source files. As the size of a project grows, building it can become extremely complex. To manage this complexity, we would like to be able to specify once how to build the project, and then use the specification to build the project in the same way in the future. Luckily, several tools exist which allow use to do this.

*GNU Make* is a tool which lets us specify how to build software from its source files. The specification is written in what is called a *makefile*, which is a file the tool uses to build the software. Simply put, a makefile consists of a set of rules. Each rule has a further set of dependencies, and then a list of instructions to follow. When we invoke a rule, Make first looks to make sure that each of the rule's dependencies has already been built. If not, Make recursively builds each dependency. Once all dependencies have been satisfied, Make then executes the instructions we have specified for that rule. This system lets us specify how to build complex software projects by composing simple sets of rules for each piece of the software we are building.

In this project, we use make to handle installing our software, cleaning up after ourselves, and to run tests, among other things. Once we are in a directory which contains a makefile, we can run Make.

To run the default rule for the makefile:

`make`

To install our software:

`make install`

To remove our software:

`make clean`

To run tests:

`make test`

For more information about GNU Make and makefiles, see:

[https://www.gnu.org/software/make/]()

### git

When we collaborate on software, we usually want some way to track what changes are being made, and who's making them. Additionally, we would like to be able to compare our current software to past versions, and to be able to retrieve those past versions if necessary.

We accomplish these goals by using a *version control system*. For this project, our version control system of choice is git. git was originally developed as a version control system for use in developing the Linux kernel, but since its creation it has seen widespread use among many software developers. The website that the code for this course is hosted on, [https://github.com](), is one of several popular websites used for hosting git repositories.

git is a fully-featured software project, and as such we will not cover it here. If you'd like to learn more about git and how to use it, you might find the following resources helpful.

For git itself:

[https://git-scm.com/]()

[https://git-scm.com/book/en/v2]()

For using GitHub:

[https://help.github.com/categories/bootcamp/]()

### Package Managers

When developing software, it is often useful to be able to re-use software that others have already written. Software written for the purpose of being used to help develop other software is usually referred to as a *library*. This project uses several software libraries, which we call *dependencies* of the project. We call them dependencies since our project depends on these libraries being installed on the system in order to function. Sometimes, software libraries have dependencies themselves, and then it is possible for these dependencies to have further dependencies, and so on.

Manually managing the dependencies of a software package is tedious, and can also be error-prone. Consider the case where we are using a library which is pinned to a specific version of another library. We would first have to know that this dependency existed, and then have to make sure the exact version of the dependency was installed on our system. Now suppose we were using a second library which had the same dependency, but was pinned to a different version of the software. In this case, we would have to make sure that we had *both* versions of the dependency installed, and further, we would need to make sure that each library we were using actually linked to the correct version of the dependency at build-time.

To manage this complexity, we use *package managers*. Software libraries are *packaged* when they are released, and these *packages* keep track of the dependencies needed for the library, which are in turn packages themselves. When we install a package with a package manager, it checks if the dependencies for that package are already installed on the system. If not, it installs their dependencies, which might involve installing the dependencies for thos packages, and so on. The package also describes which versions of the dependency are valid to use with the package, and the package manager will handle having multiple versions of the same software installed on the system.

In this project we use several package managers. We will give a brief overview of each of them.

#### pip

[pip](https://pip.pypa.io/en/stable/) is a package manager for installing software packages written in Python. Many of the packages installed by pip can be found in the [Python Package Index](https://pypi.python.org/pypi/) also referred to as PyPi.

##### Installation

[https://packaging.python.org/installing/#install-pip-setuptools-and-wheel]()

##### Usage

To install a package:

`pip install <package>`

To upgrade a package:

`pip install --upgrade <package>`

To remove a package:

`pip uninstall <package>`

See also: [https://pip.pypa.io/en/stable/quickstart/]()

#### npm

[npm](https://www.npmjs.com/) is a package manager for the [Node.js](https://nodejs.org/en/) runtime environment.

##### Installation

[https://docs.npmjs.com/getting-started/installing-node]()

##### Usage

To install a package locally:

`npm install <package>`

To update a package locally:

`npm update <package>`

To uninstall a package locally:

`npm uninstall <package>`

To install a package globally (needed for command-line tools):

`npm install -g <package>`

To update a package globally:

`npm update -g <package>`

To uninstall a package globally:

`npm uninstall -g <package>`

See also: [https://docs.npmjs.com/]()

#### bower

[bower](https://bower.io/) is a package manager for front-end web development.

##### Installation (Requires npm)

`npm install -g bower`

##### Usage

To install a package:

`bower install <package>`

To update a package:

`bower update <package>`

To uninstall a package:

`bower uninstall <package>`

See also: [https://bower.io/docs/api/]()

### virtual environments

When using Python, it is usually the case that we would like to make use of third party software libraries. Sometimes, we would also like to have multiple versions of the same library installed, or it may be that we have a conflicting dependency on a software package between two different projects we're working on.

To solve this problem, we use what is called a *virtual environment* to keep our dependencies separate. When we create a virtual environment, hereafter referred to as a *virtualenv*, we are creating a seperate installation directory under the namespace of the virtualenv. This means that once the virtualenv is activated, any packages we install, remove, or update will only affect that one particular virtualenv, and not the entire system. This has major benefits when we are working on multiple projects at the same time, or may be sharing our system with multiple people.

To create a virtualenv, we issue:

`virtualenv ENV`

Here, `ENV` is the name of the virtualenv. Once we issue this command, it creates a directory called `ENV`, which contains the files needed to activate the virtualenv, and also will contain all the files needed for any packages we install.

After creating the virtualenv, we can activate it:

`source ENV/bin/activate`

After invoking this command, we are now in the virtualenv. From this point forward, any package changes we make using `pip` will only affect the virtualenv, and not the rest of our system.

To exit the virtualenv, we simply run:

`deactivate`

This deactivates the virtualenv, and lets us use our system's installed Python again.

For more information, see: [https://virtualenv.pypa.io/en/stable/]()
