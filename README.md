# Test

Build environment: `conda env create -f environment.yml`.
Run tests: `python test_all.py`.

Test results on Dell laptop: 
```
...
Ran 232 tests in 2.802s
```

Note:

Python version is 3.4 according to section "What you need for this book" in preface:

> You will need to have Python 3.3 or 3.4 installed and running.

For PIL is incompatible with Python 3.4, [Pillow](https://github.com/python-pillow/Pillow)
is used instead.

------

Original *Readme.txt*:

How to Execute the Code:

1) Extract the Code Bundle at your desired location

2) Use the Python Command Prompt or use the Windows Command Prompt as per your Operating System and go to the lacation where 
   you have the Code Bundle placed.

3) If you are using the Windows Command Prompt type "DIR" and Enter and observe whether all the Directories that are
   there in the folder of the Chapters folder are being read, for eg, Chapter_1, Chapter_2 and so on.

4) Then type "python test_all.py" and check whether you are getting any error as an output, if not then it should display something
   like the following as an output:
   ....................................................................................................................................
..................................................................................................
----------------------------------------------------------------------
Ran 230 tests in 10.955s

5) If you get the preceding as the output then you can test the Code files individually even though the above output tests all the
   example Code file at once.

