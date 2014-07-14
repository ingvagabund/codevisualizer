## About

**codevisualizer** is a tool helping you to visualize C source code.

What it basically does is to
* allow you to comment source code,
* add own folds
* mark keywords with a label
* add needinfo label
* create database of keywords for all files or any file individually

without changing the code itself. This is usefull for stable upstream codes 
that does not change often. This is not a tool for very rapidly changing
source codes.

**Through folds you can**
* merge lines of code (even blocks) as one semantic action
* hide unnecesary parts of code

E.g. code for initialization can be grouped into one fold and hidden
(needed only when debugging some init probles for example). The aim is to
show only those parts of code, that are essential for quick walkthrough of the code.

**Through keyword database you can**
* add your own explanation or meaning of keyword
* label important keywords throughout the source code

E.g. add whatis text for system/library calls from man page section 3 or
choose diffrent explanation suited for problem you are solving

![Code visualization](https://raw.githubusercontent.com/ingvagabund/codevisualizer/master/examples/example.png)

## Installation
Clone the repo into a directory. ~/codevisualizer prefered but can be basically anything.

   ```$ git clone https://github.com/ingvagabund/codevisualizer.git
   ```

In the directory run

   ```$ make
   $ sudo make install
   ```

## QuickGuide

Description of all options, visualization file format and keywords database is in man page
	$ man visualize

Visualization file example:

   ```#### reading config file ####
   827:needinfo:namestore:list of items of config file
   843:comment:~/.manpath
   846:comment:read config file only once
   850:fold:866:1:read config file from ~/.manpath or user file (user_config_file) through option
   851:comment:NULL if called from manpath
   862:highlight:add_to_dirlist (config, 1):parses config file and calls add functions
   ```

keyworddb example:

   ```#### man-db general functions ####
   get_manpath:get all possible man paths (optionally with systems)
   add_nls_manpaths:each  path in manpath replace by itself plus prepended its locale paths (locale = languages like fr,de,...)
   locale_manpath:to each path in manpath prepend its localized paths
   ```

## Launch it
Already prepared example from man-db source codes

   ```$ visualize --dest=examples examples/manp.c
   ```

Running with --debug will show you the resulting html file and the visualization process

   ```$ visualize --dest=examples examples/manp.c --debug
   ```

