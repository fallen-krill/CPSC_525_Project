# CPSC 525 Project
## CWE 502: Deserialization of Untrusted data

### Coding Portion

`todo: high level description of your code and exploit (~1 paragraph, can be bulleted)`

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
### Running the Attack Code (Warning: Flashing Lights)

Run exploitexfil.py to create a file called `malicious.pkl`:
```
$ python exploitexfil.py
```

Before loading the newly created file, run exfil-receiver.py, located in demo. As a server, this must run alongside app.py.
```
$ python demo/exfil-receiver.py
```

This file contains code that can be executed if loaded by the app, done by clicking File > Open.

---

Run the attack code (Flashing window):
```
$ python exploitwindow.py
```
A file called `malicious.pkl` should appear if the script runs successfully.

This file contains code that can be executed if loaded by the app, done by clicking File > Open.