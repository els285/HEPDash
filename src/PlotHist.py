"""
    HEP Dashboard 1
    Ethan Simpson

For plotting single histograms in a streamlit web-app, with controls for binning
and histogram range.

Run either through python3 or streamlit commands:
```python3 PlotHist.py <file_name> <tree_name> <branch_name>```
or
```streamlit run <file_name> <tree_name> <branch_name>```


This script is specfically designed to not use ROOT,
but therefore requires a number of third-party dependencies:
    - numpy = defining arrays
    - matplotlib = pyplot back-end
    - streamlit = generates web-app
    - uproot = parses ROOT file
    - boost_histogram = alternative to ROOT histogram
    - mplhep = for plotting

"""
# Standard imports
import sys
import os

# Third-party imports
from streamlit import cli as stcli
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot
import boost_histogram as bh


def main():

    assert os.path.isfile(file_name), file_name+" not found"
    file = uproot.open(file_name)

    tree=file[tree_name]
    caz=tree[branch_name].array(library="pd")

    @st.cache
    def Generate_Histogram(num_bins,hist_range,df):
        bins = np.linspace(hist_range[0]*1e3,hist_range[1]*1e3,nb+1)
        h = bh.Histogram(bh.axis.Variable(bins))
        h.fill(df)
        return h

    st.title("Interactive Histogram")

    nb = st.slider('Number of bins',min_value=1,max_value=100,value=12)
    hist_range = st.slider('Range of histogram',value=[0.0,500.0])

    h=Generate_Histogram(nb,hist_range,caz)
    fig,ax = plt.subplots()
    hep.histplot(h)
    st.pyplot(fig)


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        file_name   = sys.argv[1]
        tree_name   = sys.argv[2]
        branch_name = sys.argv[3]
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3]]
        sys.exit(stcli.main())
