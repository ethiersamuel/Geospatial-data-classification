As I talked about during the interview, here at Ecometrica, we make every candidate complete a programming test to better evaluate them for the skill set we are hiring for.

I have attached a python file called classify.py with 2 numpy arrays containing simplified geospatial data:

- LANDCOVER: the type of landcover at a given x,y pixel coordinate
- CARBON: carbon stocks in the soil, covering an area within the coordinates described by LANDCOVER

I want you to write a command-line program that does a "classification" operation with the data: calculate the average (mean) for each type of landcover in our given carbon area.
That is, the average carbon values grouped by landcover type. The print out the result (ideally nicely formatted).

Additionally, the program should accept two optional arguments:

- "landcover": If present, only do the calculation for that given type of landcover. An appropriate error message should be displayed if the given value is not a valid landcover type.
- "stddev": If present, also calculate the standard deviation (in addition to the average).

Your output should look similar to the following (the exact format is up to you):

```
$ python classify.py
Landcover Type                 Mean carbon
----------------------------   -----------
water                               0
evergreen needleleaf forest        -
...

$ python classify.py --landcover croplands --stdev
Landcover Type                 Mean carbon    SD carbon
----------------------------   -----------    ---------
croplands                           101            5

```

Please use Python 3.5+.  Your program should pass the tests in the included tests.py file (with pytest), and should pass pylint with the attached .pylintrc file.

The tests.py file contains rudimentary tests to help you confirm that your program is working as expected.  Feel free to add additional tests for your specific implementation of this exercise, but this is NOT obligatory.

Please write your program in the "classify.py" file and send it back to me once you are finished. Be sure to add to the requirements.txt file if you use any third-party libraries.

