# HEP Dash

Designed to take ROOT TTrees and build interactive web-browser-based notebooks.

Possibly use streamlit, dash more advanced?

Think about functionality and optimal use case...

Most up-to-date functionality so far is the `make_premade_comparison_app.py` function. `make_general_comparison_app.py` has also been created.


![alt text](examples/example_fig.png "Title")

For effective README exhibiting features of the app, use this site to create screen recordings: https://gifcap.dev/

## Features

Histograms can be manipulated and downloaded.



## Installation


### Github
Feel free to clone the directory. Preferred: install via `pip` through:
```bash
python3 -m pip install git+https://github.com/ethansimpson285/HEPDash.git
```

### Other
From PyPi - not uploaded.



## From Trees

Generate and deploy a HEP-Dash app using ROOT TTrees! HEP-Dash automatically handles the histogram construction, projection and rendering.

Pass any number of ROOT files with specified TTrees

There are several varieties of 
* General - App will diplay histograms for each branch common to all the ROOT TTrees given.
* Preset - App will display (pT,eta,phi,E) histograms for electron, muon and jet objects.
* Specific - App will display histograms specified by the user.


## From Histograms

Display and manipulate ROOT histograms (maybe other types?) through a HEP-Dash app!


## Additional Information on Code
The current implementation selects branches and projects into histograms each time the streamlit app flow is updated (i.e. every time a button is pressed). This was found to be faster than storing all branches and accessing them when necessary. However, for larger scale presentation of multiple histograms, this will possibly become necessary...
