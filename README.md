# CPSC 525 Project
## CWE 502: Deserialization of Untrusted data

### Coding Portion

**Application**

This is a simple GUI graphing calculator written with Python, using PySide6 (Qt). The user can:
- Add and remove supported mathematical functions of x
- Group functions into separate pages / tabs.
- Save and load projects, containing currently open pages and their functions, using binary serialization.

Supported functions:
- Operations (+, -, *, /, ^)
- Trigonometric (sin, cos, tan, csc, sec, cot, asin, acos, atan)
- Logarithmic (log, log_, ln)
- Square root (sqrt)
- Factorial (!)
- Constants (pi, e)

** Note on order of operations and valid input **
- It's as you would expect for BEDMAS, but between `()` and `^`, the order is `()`->`!`->`function evaluation`->`^`.
- Essentially, this means that the `!` applies to what was immediately before it, and a `^` will evaluate after the function is computed.
- For example: `cos x!` is `cos(x!)`, and `cos x^2` is `(cos x)^2`
- You do not need to enter brackets; the application is able to tell when juxtaposition is multiplication and when it's an argument.
- Similarly to LaTeX commands, purely alphabetical strings will be considered as one token, so `cosx` is nonsense, but `cos x` is fine.

A fixed version of the app which uses JSON serialization instead of binary can be found on the `restructured-graphing` branch.

**Attack code**

This uses a socket-based server and client to copy the .pkl project file data from the app directory. 

The client is contained as executable code within an untrusted .pkl file, created by running `exploitexfil.py`. When loaded, it will connect to the server and send the contents of every .pkl file in the app directory.

The server, `demo/exfil-receiver.py`, can be run at any time, and will wait indefinitely for a connection. Once a connection is established, it will write the file data it receives to a new .pkl file in the server's local directory.

---
### Controls

- -/=: Zoom out/in
- 0: Reset graph view
- Arrow keys: Scroll graph

---

### Launching the Application

**Option 1: Running directly (Not applicable to university Linux servers)**

To run the application, PySide6 must first be installed.
```
$ pip install PySide6
```
Then, run app.py.
```
$ python app.py
```

**Option 2: Running through a virtual environment**

If you cannot install PySide6 directly using pip, as is the case on some Linux distributions and the MS computers, you can instead create a virtual environment.
```
$ cd CPSC_525_Project
$ python -m venv ./venv
$ source venv/bin/activate
(venv) $ pip install PySide6
(venv) $ python app.py
```

---
### Running the Attack Code

Run exploitexfil.py to create a file called `malicious.pkl`:
```
$ python exploitexfil.py
```

Before loading the newly created file, run exfil-receiver.py, located in demo. As a server, this must run alongside app.py.
```
$ python demo/exfil-receiver.py
```

This file contains code that can be executed if loaded by the app, done by clicking File > Open.
