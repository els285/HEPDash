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


@st.cache
def Generate_Histogram(num_bins,hist_range,df):
    bins = np.linspace(hist_range[0],hist_range[1],num_bins+1)
    h = bh.Histogram(bh.axis.Variable(bins))
    h.fill(df)
    return h

def Get_Extrema(df):
    import math
    return float(math.ceil(df.max())),float(math.floor(df.min()))

#Streamlit suffers from the problem of being slow to generate a slider for histogram extrema which are very large values 
#This is problematic for pT and eta


def EPT_Histogram(nb,minH,maxH,df,index):
    nearest10k = lambda a: math.ceil(a/10e3)*10e3
    maxH = nearest10k(maxH)
    hist_range = st.slider('Range of histogram',value=[0.0,maxH/1e3],key=index)
    hist_range = tuple([1e3*x for x in hist_range])
    return Generate_Histogram(nb,hist_range,df)

def Angular_Histogram(nb,minH,maxH,df,index):
    hist_range = st.slider('Range of histogram',value=[minH,maxH],key=index)
    return Generate_Histogram(nb,hist_range,df)



def Branch2Hist(tree,branch_name,index):
    df = tree[branch_name].array(library="pd")
    if st.checkbox("Display events for "+ branch_name):
        st.write(df)
    nb = st.slider('Number of bins',min_value=1,max_value=100,value=50,key=index)
    maxH,minH = Get_Extrema(df)

    # Switch statement to select correct histogram based on branch name
    if "_eta" in branch_name or "_phi" in branch_name:
        h = Angular_Histogram(nb,minH,maxH,df,index)
    else:
        h = EPT_Histogram(nb,minH,maxH,df,index)

    return h 

def Plot_SingleHist(h,branch_name):

    fig,ax = plt.subplots()
    hep.histplot(h)
    plt.xlabel(branch_name)
    plt.ylabel("Number of events")
    st.pyplot(fig)


class PhysOb_Page:

    def __init__(self,phys_ob,tree,branches2plot):
        self.phys_ob        = phys_ob
        self.tree           = tree
        self.branches2plot  = branches2plot

    def Build(self):

        st.write("# " + self.phys_ob)

        obs = st.selectbox("Choose an observable",self.branches2plot)

        st.write("## "+obs)

        h = Branch2Hist(self.tree,obs,self.phys_ob+"_"+obs)
        Plot_SingleHist(h,obs)


class MultiPage:

    def __init__(self) -> None:
        self.dic_of_pages = {}

    def add_page(self,page_object):
        self.dic_of_pages[page_object.phys_ob] = page_object

    def Build_MultiPage(self):
        # Build the multipage format and the selection box
        list_of_pages = self.dic_of_pages.keys()
        page = st.sidebar.selectbox("Physics Object Selection",list(self.dic_of_pages.values()),format_func = lambda page: page.phys_ob)
        page.Build()


def main():

    st.title("HEP-Dash: Interactive ROOT File Visualisation!")

    # st.write("welcome to the first attempt at multi-page histogram Visualisation")

    assert os.path.isfile(file_name), file_name+" not found"
    file = uproot.open(file_name)

    tree=file[tree_name]

    muon=PhysOb_Page("Muon",tree,["mu_pt","mu_eta"])
    electron=PhysOb_Page("Electron",tree,["el_phi"])#,"mu_eta"])

    MP = MultiPage()
    MP.add_page(muon)
    MP.add_page(electron)


    MP.Build_MultiPage()




if __name__ == '__main__':
    if st._is_running_with_streamlit:
        file_name   = sys.argv[1]
        tree_name   = sys.argv[2]
        # branch_name = sys.argv[3]
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0],sys.argv[1],sys.argv[2]]#,sys.argv[3]]
        sys.exit(stcli.main())
