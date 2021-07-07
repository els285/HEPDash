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
import math

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
    # print(file.__dict__["_keys"][0].__dict__)
    # input()
    tree=file[tree_name]
    caz=tree[branch_name].array(library="pd") # Parse the TTree to a Panda dataframe

    @st.cache
    def Generate_Histogram(num_bins,hist_range,df):
        bins = np.linspace(hist_range[0],hist_range[1],nb+1)
        h = bh.Histogram(bh.axis.Variable(bins))
        h.fill(df)
        return h

    def Get_Extrema(df):
        import math
        return float(math.ceil(df.max())),float(math.floor(df.min()))

    #Streamlit suffers from the problem of being slow to generate a slider for histogram extrema which are very large values 
    #This is problematic for pT and eta
    

    def EPT_Histogram(nb,minH,maxH,caz):
        nearest10k = lambda a: math.ceil(a/10e3)*10e3
        maxH = nearest10k(maxH)
        hist_range = st.slider('Range of histogram',value=[0.0,maxH/1e3])
        hist_range = tuple([1e3*x for x in hist_range])
        return Generate_Histogram(nb,hist_range,caz)

    def Angular_Histogram(nb,minH,maxH,caz):
        hist_range = st.slider('Range of histogram',value=[minH,maxH])
        return Generate_Histogram(nb,hist_range,caz)


    st.title("Interactive Histogram")

    if st.checkbox("Display events"):
        st.write(caz)

    nb = st.slider('Number of bins',min_value=1,max_value=100,value=50)

    maxH,minH = Get_Extrema(caz)

    # Switch statement to select correct histogram based on branch name
    if "_eta" in branch_name or "_phi" in branch_name:
        h = Angular_Histogram(nb,minH,maxH,caz)
    else:
        h = EPT_Histogram(nb,minH,maxH,caz)

    ### Plotting

    fig,ax = plt.subplots()
    hep.histplot(h)
    plt.xlabel(branch_name)
    plt.ylabel("Number of events")
    st.pyplot(fig)

    # if st.button("Reset"):
    #     nb = 50
    #     hist_range = [minH,maxH]




if __name__ == '__main__':
    if st._is_running_with_streamlit:
        file_name   = sys.argv[1]
        tree_name   = sys.argv[2]
        branch_name = sys.argv[3]
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0],sys.argv[1],sys.argv[2],sys.argv[3]]
        sys.exit(stcli.main())