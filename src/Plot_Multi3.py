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
import time

# Third-party imports
from streamlit import cli as stcli
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot
import boost_histogram as bh


@st.cache
def Generate_Histogram(num_bins,hist_range,df,normalise):
    bins = np.linspace(hist_range[0],hist_range[1],num_bins+1)
    h = bh.Histogram(bh.axis.Variable(bins))
    h.fill(df)
    if normalise:
        return h/h.sum()
    else:
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

    nb = st.slider('Number of bins',min_value=1,max_value=100,value=50,key=index)
    maxH,minH = Get_Extrema(df)

    #####

    # Switch statement to select correct histogram based on branch name
    if "_eta" in branch_name or "_phi" in branch_name:
        h = Angular_Histogram(nb,minH,maxH,df,index)
    else:
        h = EPT_Histogram(nb,minH,maxH,df,index)

    return h ,df



# class PolyHist:

#     d


def Plot_SingleHist(h,branch_name):

    fig,ax = plt.subplots()
    hep.histplot(h)
    plt.xlabel(branch_name)
    plt.ylabel("Number of events")
    st.pyplot(fig)


class PhysOb_Page:

    def __init__(self,phys_ob,dic_of_trees,branches2plot):
        self.phys_ob        = phys_ob
        self.dic_of_trees  = dic_of_trees
        self.branches2plot  = branches2plot

    def Build(self):

        st.write("## " + self.phys_ob)

        # Selects obs as the observable in question
        obs = st.selectbox("Choose an observable",self.branches2plot)

        dic_of_df = {}


        # Extract TBranches to DF and compute limits
        maxH_list , minH_list = [],[]

        # Automatically compute histogram bounds
        for tree_name,tree in self.dic_of_trees.items():
            t0 = time.time()
            df = tree[obs].array(library="pd")
            print(time.time()-t0)
            dic_of_df[tree_name] = df
            maxH,minH = Get_Extrema(df)
            maxH_list.append(maxH)
            minH_list.append(minH)
        max_HH, min_HH = max(maxH_list),min(minH_list)
        # print(max_HH,min_HH)
        # input()

        # Bin slider
        index = self.phys_ob+"_"+obs
        nb = st.slider('Number of bins',min_value=1,max_value=100,value=50,key=index)

        # Generate the bin edge slider based on observable type
        if "_eta" in obs or "_phi" in obs:
            hist_range = st.slider('Range of histogram',value=[minH,maxH],key=index)
        else:
            # Getting the binning to work well with slider
            nearest10k = lambda a: math.ceil(a/10e3)*10e3
            maxH = nearest10k(maxH)
            hist_range = st.slider('Range of histogram',value=[0.0,maxH/1e3],key=index)
            hist_range = tuple([1e3*x for x in hist_range])
        dic_of_hists = {}


        normalise = st.checkbox("Show normalised",value=True)
        for name,df in dic_of_df.items():
            t1 = time.time()
            h = Generate_Histogram(nb,hist_range,df,normalise=normalise)
            print(time.time()-t1)
            dic_of_hists[name] = h

        fig,ax = plt.subplots()
        [hep.histplot(h,yerr=False) for h in dic_of_hists.values()]
        st.pyplot(fig)



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

@st.cache(allow_output_mutation=True)
def import_files():
    t2=time.time()
    file1 = uproot.open("~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_particleLevel_even.root")
    tree1 = file1["particleLevel_even"]

    file2 = uproot.open("~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_reco_even.root")
    tree2 = file2["reco_even"]

    return tree1,tree2


def main():

    st.title("HEP-Dash")

    st.write("### Interactive HEP Visualisation!")

    # st.write("welcome to the first attempt at multi-page histogram Visualisation")

    # assert os.path.isfile(file_name), file_name+" not found"

    t2 = time.time()
    tree1,tree2 = import_files()
    print(time.time()-t2)

    # input_trees = {}
    # for imp in imported_
    input_trees = {"tree1":tree1,"tree2":tree2}

    # print(input_trees)
    # input()

    # Pass list of trees here
    muon        =  PhysOb_Page("Muon",input_trees,["mu_pt","mu_eta","mu_phi","mu_e"])
    electron    =  PhysOb_Page("Electron",input_trees,["el_pt","el_eta","el_phi","el_e"])#,"mu_eta"])

    MP = MultiPage()
    MP.add_page(muon)
    MP.add_page(electron)


    MP.Build_MultiPage()




if __name__ == '__main__':
    if st._is_running_with_streamlit:
        # file_name   = sys.argv[1]
        # tree_name   = sys.argv[2]
        # branch_name = sys.argv[3]
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]#,sys.argv[1],sys.argv[2]]#,sys.argv[3]]
        sys.exit(stcli.main())
