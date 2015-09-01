# pyprel

Python print elegant

# introduction

This module provides Python rendering functionality. It can render a dictionary such that it is displayed with indentations for illustration of hierarchy:

```
sample information:
  name: ttH
  generator: pythia8
  cross section: 0.055519
  variables:
    zappo_n: 9001
    trk_n: 147
  number of events: 124883
  k factor: 1.0201
  ID: 169888
```

It can render and display logos:

```
                  ____      _            _____ _                                
                 / ___|___ | | ___  _ __|  ___| | _____      __                 
                | |   / _ \| |/ _ \| '__| |_  | |/ _ \ \ /\ / /                 
                | |__| (_) | | (_) | |  |  _| | | (_) \ V  V /                  
                 \____\___/|_|\___/|_|  |_|   |_|\___/ \_/\_/               
```

It can center blocks of text for terminal output (such as in a way shown for the logo above). It can render segment displays:

```
 _     _  _     _  _  _  _  _ 
| |  | _| _||_||_ |_   ||_||_|
|_|  ||_  _|  | _||_|  ||_| _|
```

It can render and display tables of various specified widths and column widths with various text wrapping features and delimiters:

```
|---------------------------------------------------|
|heading 1                |heading 2                |
|---------------------------------------------------|
|some text                |some more text           |
|---------------------------------------------------|
|lots and lots and lots   |some more text           |
|and lots and lots of text|                         |
|---------------------------------------------------|
```

```
                         |---------------------------|                          
                         |heading 1    |heading 2    |                          
                         |---------------------------|                          
                         |some text    |some more    |                          
                         |             |text         |                          
                         |---------------------------|                          
                         |lots and lots|some more    |                          
                         |and lots and |text         |                          
                         |lots and lots|             |                          
                         |of text      |             |                          
                         |---------------------------|                         
```

```
||----------------------------------------------------||
||heading 1                ||heading 2                ||
||----------------------------------------------------||
||some text                ||some more text           ||
||----------------------------------------------------||
||lots and lots and lots   ||some more text           ||
||and lots and lots of text||                         ||
||----------------------------------------------------||
```

```
|-----------------------------------------------------------------------------|
|heading 1                |heading 2                |heading 3                |
|-----------------------------------------------------------------------------|
|some text                |some more text           |even more text           |
|-----------------------------------------------------------------------------|
|lots and lots and lots   |some more text           |some more text           |
|and lots and lots of text|                         |                         |
|-----------------------------------------------------------------------------|
```

```
|---------------------------------------------------------------------------|
|heading 1         |heading 2         |heading 3         |heading 4         |
|---------------------------------------------------------------------------|
|some text         |some more text    |even more text    |yeah more text    |
|---------------------------------------------------------------------------|
|lots and lots and |some more text    |some more text    |some more text    |
|lots and lots and |                  |                  |                  |
|lots of text      |                  |                  |                  |
|---------------------------------------------------------------------------|
```

It can provide color palettes, extend them and save images of them:

![](images/palette_1.png)
![](images/palette_2.png)
![](images/palette_3.png)
![](images/palette_4.png)
![](images/palette_5.png)
![](images/palette_6.png)
![](images/palette_7.png)

# prerequisites

## pyfiglet

```Bash
sudo pip install pyfiglet
```
