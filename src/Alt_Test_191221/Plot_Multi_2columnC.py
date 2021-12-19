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
import pickle
from collections import namedtuple
import functools
import operator

# Third-party imports
from streamlit import cli as stcli
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import mplhep as hep
import uproot
import boost_histogram as bh

# Own imports
from Histogram_Classes import PyHist_Object, Histogram_Wrapper
from Plotting_Histograms import make_both_plot,make_ratio_only_plot,make_standard_plot
import Plotters




def normalise_boost_histogram(boost_hist):

    area = functools.reduce(operator.mul, boost_hist.axes.widths)
    factor = np.sum(boost_hist.view())
    view = boost_hist.view() / (factor * area)

    for i,x in enumerate(view):  
        boost_hist[i]=x

    return boost_hist


@st.cache
def Generate_Histogram(num_bins,hist_range,df,normalise):
    bins = np.linspace(hist_range[0],hist_range[1],num_bins+1)
    h = bh.Histogram(bh.axis.Variable(bins))
    h.fill(df)
    if normalise:
        return normalise_boost_histogram(h)
    else:
        return h

# @st.cache
def generate_wrapped_histogram(num_bins,hist_range,df,**kwargs):
    binning = np.linspace(hist_range[0],hist_range[1],num_bins)
    Wrapped_Hist = Histogram_Wrapper(df,binning=binning,colour="red" ,label="reco")
    return Wrapped_Hist






def Get_Extrema(df):
    import math
    return 

#Streamlit suffers from the problem of being slow to generate a slider for histogram extrema which are very large values 
#This is problematic for pT and eta


def EPT_Histogram(nb,minH,maxH,df,index):
    nearest10k = lambda a: math.ceil(a/10e3)*10e3
    maxH = nearest10k(maxH)
    hist_range = st.slider('Range of histogram',value=[0.0,maxH/1e3],key=index,step=10.0)
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



def RootHist_2_boosthist(histogram_name):

    '''Some converstion through uproot(?) to boost_histogram'''

    pass

# class PolyHist:

#     d


def Plot_SingleHist(h,branch_name):

    fig,ax = plt.subplots()
    hep.histplot(h)
    plt.xlabel(branch_name)
    plt.ylabel("Number of events")
    st.pyplot(fig)


def extrema_from_dfs(list_of_dfs):
    
    maxH_list , minH_list = [],[]
    # get_extrema = lambda get_extrema df: float(math.ceil(df.max())),float(math.floor(df.min()))
    for df in list_of_dfs:
        maxH_list.append(float(math.ceil(df.max())))
        minH_list.append(float(math.floor(df.min())))
    max_HH, min_HH = max(maxH_list),min(minH_list)
    Extrema = namedtuple('Extrema','min max')
    return Extrema(min_HH,max_HH) 


from hist.intervals import ratio_uncertainty

def Compute_Ratio(hist1,hist2):

    ratio_hist = hist1/hist2
    ratio_uncertainties = ratio_uncertainty(hist1.view(),hist2.view(),"poisson-ratio")
    return PyHist_Object(ratio_hist,ratio_uncertainties)#[0],ratio_uncertainties[1])


class PhysOb_Page:

    def __init__(self,phys_ob,dic_of_trees,branches2plot):
        self.phys_ob        = phys_ob
        self.dic_of_trees   = dic_of_trees
        self.branches2plot  = branches2plot
        self.plot_types     = {"ratio only":make_ratio_only_plot,
                                "standard":make_standard_plot,
                                "standard+ratio":make_both_plot}

    def Build(self):

        st.write("## " + self.phys_ob)

        # Selects obs as the observable in question
        obs = st.selectbox("Choose an observable",self.branches2plot)


        chosen_plot_type = st.selectbox("Plot type:",self.plot_types.keys())
        plot_function = self.plot_types[chosen_plot_type]

        if chosen_plot_type=="ratio only" or chosen_plot_type=="standard+ratio":
            divisor_name =  st.selectbox("Histogram divisor" , self.data_object.list_of_input_objects.keys())
            # divisor = self.dic_of_trees[divisor_name]
  

        # Initialise list of DataFrames
        dic_of_df = {}

        # Extract TBranches to DF and compute limits
        maxH_list , minH_list = [],[]

        # Automatically compute histogram bounds
        for tree_name,tree in self.dic_of_trees.items():
            df = tree[obs].array(library="pd")
            dic_of_df[tree_name] = df
        extrema = extrema_from_dfs(dic_of_df.values())


        # Bin slider
        index = self.phys_ob+"_"+obs

        nb = st.slider('Number of bins',min_value=1,max_value=100,value=50,key=index)

        # Generate the bin edge slider based on observable type
        if "_eta" in obs or "_phi" in obs:
            hist_range = st.slider('Range of histogram',value=[extrema.min,extrema.max],key=index)
        else:
            # Getting the binning to work well with slider
            nearest10k = lambda a: math.ceil(a/10e3)*10e3
            maxH = nearest10k(exterma.max)
            hist_range = st.slider('Range of histogram',value=[0.0,maxH/1e3],key=index)
            hist_range = tuple([1e3*x for x in hist_range])

        dic_of_hists = {}

        normalise = st.checkbox("Show normalised",value=True)


        # Loop over the dataframes and generate the histograms
        for name,df in dic_of_df.items():
            h = generate_wrapped_histogram(nb,hist_range,df,normalise=normalise,colour=colour,label=label)
            dic_of_hists[name] = h


        # Get the divisor histogram, using the dictionary of histograms and the key specified
        if chosen_plot_type=="ratio only" or chosen_plot_type=="standard+ratio":
            divisor_histogram = dic_of_hists[divisor_name]  

        plot_function = make_standard_plot
        # fig = make_standard_plot(dic_of_hists=dic_of_hists,divisor=divisor_histogram)

        fig,ax = plt.subplots()
        [hep.histplot(h.UnNorm_Hist.Histogram,yerr=True) for h in dic_of_hists.values()]
        st.pyplot(fig)
        print("should now be visible")


class PhysOb_Page_TwoColumn:


    def __init__(self,phys_ob,input_object,branches2plot):
            self.phys_ob        = phys_ob
            self.data_object   = input_object
            self.branches2plot  = branches2plot
            self.plot_types     = {"ratio only":make_ratio_only_plot,
                                    "standard":make_standard_plot,
                                    "standard+ratio":make_both_plot}


    def Build(self):

        col1, col2, col3 = st.columns([2,1,4])

        # Page initialised with defaults
        page_data = {"observable":self.branches2plot[0], # Defines default branch
                     "plot_type"  :make_standard_plot,
                     "num_bins": 50,
                     "hist_range":None,
                     "normalise": False}


        with col1:
            st.write("## " + self.phys_ob)

            # Set page_data with streamlit widgets
            page_data["observable"] = st.selectbox("Choose an observable",self.branches2plot)
            index = self.phys_ob+"_"+page_data["observable"]            
            chosen_plot_type        = st.selectbox("Plot type:",self.plot_types.keys())
            page_data["plot_type"]  = self.plot_types[chosen_plot_type]
            page_data["normalise"]  = st.checkbox("Show normalised",value=True)
            page_data["num_bins"]   = st.slider('Number of bins',min_value=1,max_value=100,value=50,key=index)

            if chosen_plot_type=="ratio only" or chosen_plot_type=="standard+ratio":
                divisor_name =  st.selectbox("Histogram divisor" , [io.name for io in self.data_object.list_of_input_objects])#self.data_object.list_of_input_objects.keys())

            # for io in self.data_object.list_of_input_objects:
            dic_of_df = {io.name: io.observables[page_data["observable"]] for io in self.data_object.list_of_input_objects}
            
            extrema=extrema_from_dfs(dic_of_df.values())

            # Generate the bin edge slider based on observable type
            if "_eta" in page_data["observable"] or "_phi" in page_data["observable"]:
                hist_range = st.slider('Range of histogram',value=[extrema.min,extrema.max],key=index)
            else:
                # Getting the binning to work well with slider
                nearest10k = lambda a: math.ceil(a/10e3)*10e3
                maxH = nearest10k(extrema.max)
                hist_range = st.slider('Range of histogram',value=[0.0,maxH/1e3],key=index,step=10.0)
                hist_range = tuple([1e3*x for x in hist_range])
            page_data["hist_range"] = hist_range


        with col3:

            # Generate the histograms
            dic_of_hists = {}

            for io in self.data_object.list_of_input_objects:
                h = generate_wrapped_histogram(page_data["num_bins"],page_data["hist_range"],io.observables[page_data["observable"]],
                                                normalise=page_data["normalise"],
                                                colour=io.colour,
                                                label=io.label)
                dic_of_hists[io.name] = h

                # Get the divisor histogram, using the dictionary of histograms and the key specified
            # Get the divisor histogram, using the dictionary of histograms and the key specified
            if chosen_plot_type=="ratio only" or chosen_plot_type=="standard+ratio":
                divisor_histogram = dic_of_hists[divisor_name]  

            label_text = "Internal"

            if chosen_plot_type=="standard":
                fig=Plotters.standard_plot(dic_of_hists,page_data["normalise"])                    

            if chosen_plot_type=="ratio only":
                fig=Plotters.ratio_only_plot(dic_of_hists,page_data["normalise"],divisor_histogram)

            if chosen_plot_type=="standard+ratio":
                fig=Plotters.combined_plot(dic_of_hists,page_data["normalise"],divisor_histogram)


            st.pyplot(fig)            
            # label = hep.atlas.text(label_text,ax=ax,loc=1)
            # import plotly.express as px
            # fig = px.histogram(df, x="x",nbins=50)


# class PhysOb_Page_MultiObs:


class MultiPage:

    def __init__(self) -> None:
        self.dic_of_pages = {}

    def add_page(self,page_object):
        self.dic_of_pages[page_object.phys_ob] = page_object

    def Build_MultiPage(self):
        # Build the multipage format and the selection box
        list_of_pages = self.dic_of_pages.keys()

        page_name = st.sidebar.selectbox("Physics Object Selection",[str(x) for x in self.dic_of_pages])#list(self.dic_of_pages.values()))#,format_func = lambda page: page.phys_ob)
        # input()
        self.dic_of_pages[page_name].Build()
        

@st.cache(allow_output_mutation=True)
def import_files():
    t2=time.time()
    file1 = uproot.open("~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_particleLevel_even.root")
    tree1 = file1["particleLevel_even"]

    file2 = uproot.open("~/Documents/Qualification_Task/TTbar_Samples/ttbar_dec15_reco_even.root")
    tree2 = file2["reco_even"]
    print("here")

    return tree1,tree2



@st.cache(allow_output_mutation=True)
def import_ROOT_file(file_path,tree_name):
    return uproot.open(file_path)[tree_name]


def primary():

    st.set_page_config(layout='wide')

    st.title("HEP Dash")

    # st.write("### Interactive HEP Visualisation!")

    t2 = time.time()
    tree1,tree2 = import_files()
    print(time.time()-t2)

    # input_trees = {}
    # for imp in imported_
    input_trees = {"tree1":tree1,"tree2":tree2}

    # Pass list of trees here
    muon        =  PhysOb_Page_TwoColumn("Muon",input_trees,["mu_pt","mu_eta","mu_phi","mu_e"])
    electron    =  PhysOb_Page_TwoColumn("Electron",input_trees,["el_pt","el_eta","el_phi","el_e"])#,"mu_eta"])

    print("Pages written")

    MP = MultiPage()
    MP.add_page(muon)
    MP.add_page(electron)


    MP.Build_MultiPage()


def main():

    st.set_page_config(layout='wide')

    st.title("HEP Dash")

    # st.write("### Interactive HEP Visualisation!")

    t2 = time.time()
    tree1,tree2 = import_files()
    print(time.time()-t2)

    # input_trees = {}
    # for imp in imported_
    input_trees = {"tree1":tree1,"tree2":tree2}

    # input()

    # Pass list of trees here
    muon        =  PhysOb_Page_TwoColumn("Muon",input_trees,["mu_pt","mu_eta","mu_phi","mu_e"])
    electron    =  PhysOb_Page_TwoColumn("Electron",input_trees,["el_pt","el_eta","el_phi","el_e"])#,"mu_eta"])

    print("Pages written")

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
