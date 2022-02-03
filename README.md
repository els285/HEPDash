# HEP Dash

**Welcome to HEPDash...**
#Death2theTBrowser

Designed to take ROOT TTrees and build interactive, web-based histogram dashboards!
Effortlessly create interactive histograms from ROOT TTrees or pre-existing histograms, and share easily.



![alt text](examples/example_fig.png "Title")

For effective README exhibiting features of the app, use this site to create screen recordings: https://gifcap.dev/

## Features

Histograms can be manipulated and downloaded.


## Installation


### Github
Install via `pip` through:
```bash
python3 -m pip install git+https://github.com/ethansimpson285/HEPDash.git
```

Alternatively, feel free to clone this git.

<hr style="border:2px solid gray"> </hr>


## Build From TTrees

Generate and deploy a HEP-Dash app using ROOT TTrees! HEP-Dash automatically handles the histogram construction, projection and rendering. Pass any number of ROOT files with specified TTrees, and select a variety of dashboard options.

For set a set of ROOT files with specified TTrees, you have several options to choose from:
* General - Dashboard will diplay histograms for each branch common to all the ROOT TTrees given.
* Preset - Dashboard will display (pT,eta,phi,E) histograms for electron, muon and jet objects - if they exist.
* Specific - App will display histograms specified by the user. A config file 

Requires a `config.yml` file to run, which contains the information on each ROOT sample.

To run:

```bash
python3 -m hepdash.make_tree -mode <option> --config config1.yml 
```
where `option` corresponds to one of the three options above.

An example config file may look like:
```yaml
# Config File 1

FILE1:
  name: particle_level
  file_path: ~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_particleLevel_even.root
  tree_name: particleLevel_even
  colour: blue
  label: pL

FILE2:
  name: reco_level
  file_path: ~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_reco_even.root
  tree_name: reco_even
  colour: red
  label: nominal
```

If you wish to run the `Specific` option, an additional arugment is required `--specifics specific_branches.yml`, where this YAML config file contains information on the branches you wish to run, for example:

```yaml
UNCATEGORISED: jet_pt,jet_eta,jet_phi
CAT1: el_pt,el_eta
CAT2: mu_pt,mu_eta
 ```

### Development Notes
* General - Built in 0.0.4, histogram image does not fit on screen.
* Preset  - Built in 0.0.3, works.
* Specific - Built and works in 0.1.0

## From Histograms

Display and manipulate ROOT histograms (maybe other types?) through a HEP-Dash app!


## Additional Information on Code
The current implementation selects branches and projects into histograms each time the streamlit app flow is updated (i.e. every time a button is pressed). This was found to be faster than storing all branches and accessing them when necessary. However, for larger scale presentation of multiple histograms, this will possibly become necessary...
