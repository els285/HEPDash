# Histogram Apps

'''
Histogram apps could have General or Specific varieties
Pull histograms from ROOT file
Compile into app
'''

import streamlit as st
import uproot
import matplotlib.pyplot as plt
import mplhep as hep
import sys
from streamlit import cli as stcli

from hepdash.layouts.BiColumn import import_ROOT_file, PhysOb_Page_TwoColumn, MultiPage
from hepdash.histograms.design import HEP_histogram_design_parameters




def create_input_object(index,name,ROOT_file_path,list_of_hist_names,**kwargs):

    """
    Wrapper for creating InputObject with additional (colour if non-specified)
    """

    colour=kwargs["colour"] if "colour" in kwargs else default_colours[index]
    return InputObject(name=name,
                ROOT_file_path=ROOT_file_path,
                list_of_hist_names=list_of_hist_names,
                colour=colour)


class InputObject:

    def __init__(self,name,ROOT_file_path,list_of_hist_names,colour,**kwargs):

        """
        A proxy for the ROOT file itself, containing the tree data stored once the ROOT file has been parsed
        """

        self.name = name
        self.ROOT_file_path = ROOT_file_path
        self.list_of_hist_names = list_of_hist_names
        self.dic_of_histograms = {}
        self.colour = colour
        self.label = kwargs["label"] if "label" in kwargs else self.name

    def import_hists(self):

        file = uproot.open(self.ROOT_file_path)

        # If empty list passed, use all the histograms in the file
        if not self.list_of_hist_names:
            self.list_of_hist_names = file.keys()

        # Get the intersection of the list of hists in file and hists asked for
        loadable_histogram_names = list(set(file.keys()).intersection(self.list_of_hist_names))

        # Get the histograms
        for hn in loadable_histogram_names:
            self.dic_of_histograms[hn] = file[hn]
            



class Histogram_App:

    def __init__(self,input_dictionary):

        # Load input objects which contain the information on the ROOT files
        self.list_of_input_objects = []

        for i,(k,v) in enumerate(input_dictionary.items()):
            io = create_input_object(index=i,name=k,ROOT_file_path=v["file_path"],list_of_hist_names=v["list_of_hist_names"],colour=v["colour"])
            io.import_hists()
            self.list_of_input_objects.append(io)

        self.get_common_hist_names()


 
    def get_common_hist_names(self):
               # Get the common histograms in all input_objects
        all_names = [list(io.dic_of_histograms.keys()) for io in self.list_of_input_objects]
            
        self.common_histogram_names = set(all_names[0])
        for s in all_names[1:]:
            self.common_histogram_names.intersection_update(s)



    def Build_BiColumn_Page(self):

        # Initialsie the streamlit web-app object
        st.set_page_config(layout='wide')
        st.title("HEP Dash")
        col1, col2, col3 = st.columns([2,1,4])

        with col1:
            hist_name = st.selectbox("Choose an observable",self.common_histogram_names)

        with col3:

            hep.style.use(HEP_histogram_design_parameters["experiment"])
            fig,ax = plt.subplots()

            for io in self.list_of_input_objects:
                hep.histplot(io.dic_of_histograms[hist_name],color=io.colour)

            fig.set_size_inches(6,5)    
            ax.set_xlabel(hist_name,labelpad=0,fontsize=14)
            ax.set_ylabel("Unnormalised Number of Events",fontsize=14)

            HEP_histogram_design_parameters["HEP experiment label"].text(HEP_histogram_design_parameters["HEP label text"],ax=ax,loc=1)

            st.pyplot(fig)



def main():

    input_dic = {"file1": {"file_path":"/home/ethan/Documents/ttZ/MadGraph ttZ SpinCorrelation Studies/nov10_pp2ttZ/output_nov10_pp2ttZ_spinON.root" ,"list_of_hist_names": [] , "colour":"blue" },
                "file2": {"file_path":"/home/ethan/Documents/ttZ/MadGraph ttZ SpinCorrelation Studies/nov10_pp2ttZ/output_nov10_pp2ttZ_spinOFF.root"          ,"list_of_hist_names": []           , "colour":"red" }}

    App1 = Histogram_App(input_dic)

    App1.Build_BiColumn_Page()


if __name__ == '__main__':
    if st._is_running_with_streamlit:
        # file_name   = sys.argv[1]
        # tree_name   = sys.argv[2]
        # branch_name = sys.argv[3]
        main()
    else:
        sys.argv = ["streamlit", "run", sys.argv[0]]#,sys.argv[1],sys.argv[2]]#,sys.argv[3]]
        sys.exit(stcli.main())
