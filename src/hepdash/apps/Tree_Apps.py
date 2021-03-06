from dataclasses import dataclass
import itertools
import os

import yaml
import matplotlib.pyplot as plt
import streamlit as st

from hepdash.layouts.BiColumn import import_ROOT_file, PhysOb_Page_TwoColumn, MultiPage


default_colours = plt.rcParams['axes.prop_cycle'].by_key()['color']

"""
Tree Apps are designed to be used with ROOT TTrees, 
    with the projections of histograms out of TTrees and the rendering of the histograms handled automiatcally.


"""



def parse_config(yaml_file):
    assert os.path.isfile(yaml_file), "Config file not found"
    with open(yaml_file, 'r') as stream:
        data_loaded = yaml.safe_load(stream)
    return data_loaded


def create_input_object(index,name,ROOT_file_path,tree_name,**kwargs):

    """
    Wrapper for creating InputObject with additional (colour if non-specified)
    """


    colour=kwargs["colour"] if "colour" in kwargs else default_colours[index]
    return InputObject(name=name,
                ROOT_file_path=ROOT_file_path,
                tree_name=tree_name,
                colour=colour)


class InputObject:

    def __init__(self,name,ROOT_file_path,tree_name,colour,**kwargs):

        """
        A proxy for the ROOT file itself, containing the tree data stored once the ROOT file has been parsed
        """

        self.name = name
        self.ROOT_file_path = ROOT_file_path
        self.tree_name = tree_name
        self.tree = None
        self.colour = colour
        self.label = kwargs["label"] if "label" in kwargs else self.name



class Tree_Comparison_App:

    """
    Base class Tree comparison app
    Takes input_dictionary which contains names and filepaths of ROOT files

    Common two-column design, with option for which branches are rendered depending on which inherited class is used.
    """

    def __init__(self,input_dictionary):

        '''
        input dictionary should be of the form {name: [ROOT_file_path,tree_name])}
        '''
        self.list_of_input_objects = []

        for i,(k,v) in enumerate(input_dictionary.items()):
            io = create_input_object(index=i,name=k,ROOT_file_path=v["file_path"],tree_name=v["tree_name"],colour=v["colour"])
            self.list_of_input_objects.append(io)
        
        self.load()
        # self.check_trees_for_branches()

    def load(self):

        for v in self.list_of_input_objects:
            v.tree = import_ROOT_file(v.ROOT_file_path,v.tree_name)
        

    def check_trees_for_branches(self):

        for io in self.list_of_input_objects:
            assert all([branch_name in io.tree.keys() for branch_name in self.all_branches]), "Not all prerequisite branches found in tree"


    def make_multipage(self):

        MP = MultiPage()

        for page in self.object_pages:
            MP.add_page(page)

        MP.Build_MultiPage()

    



class Preset(Tree_Comparison_App):

    """
    Using preset branches on preset physics objects
    """

    physics_objects = ["el","mu","jet"]
    observable_branches = ["_pt","_eta","_phi","_e"]
    all_branches = [''.join(p) for p in itertools.product(physics_objects, observable_branches)]    

    def __init__(self,input_dictionary):
        super().__init__(input_dictionary) 
        self.check_trees_for_branches()

    @staticmethod
    def make_from_config(yaml_file):
        data_loaded = parse_config(yaml_file)
        return Preset(data_loaded)

    # @staticmethod
    def add_object_pages(self):
        muon        =  PhysOb_Page_TwoColumn(phys_ob="Muon",      input_objects=self.list_of_input_objects,  branches2plot=["mu_pt","mu_eta","mu_phi","mu_e"])
        electron    =  PhysOb_Page_TwoColumn(phys_ob="Electron",  input_objects=self.list_of_input_objects,  branches2plot=["el_pt","el_eta","el_phi","el_e"])
        jet         =  PhysOb_Page_TwoColumn(phys_ob="Jet",       input_objects=self.list_of_input_objects,  branches2plot=["jet_pt","jet_eta","jet_phi","jet_e"])

        self.object_pages = [muon,electron,jet]

        # Build MultiPage here 
        MP = MultiPage()
        for page in self.object_pages:
            MP.add_page(page)
        MP.Build_MultiPage()        





class Specific(Tree_Comparison_App):

    """
    For specifying particular branches (clustered or non-clustered)
    Unclustered branches can be given as a list
    """


    def __init__(self,input_dictionary,**kwargs):

        # self.imported_unclustered_branches = kwargs["unclustered_branches"] if "unclustered_branches" in kwargs and isinstance(kwargs["unclustered_branches"],list) else []
        # self.imported_clustered_branches   = kwargs["clustered_branches"]   if "clustered_branches"   in kwargs and isinstance(kwargs["clustered_branches"],dict)   else {}
        # self.all_branches = self.imported_unclustered_branches + self.imported_clustered_branches.values()
        # self.dic_of_requested_branches = {}

        # assert len

        super().__init__(input_dictionary)

    @staticmethod
    def make_from_config(yaml_file):
        data_loaded = parse_config(yaml_file)
        return Specific(data_loaded)

    @classmethod
    def parse_specifics(self,specifics_file):
        assert os.path.isfile(specifics_file), "Config file not found"
        with open(specifics_file, 'r') as stream:
            data_loaded = yaml.safe_load(stream)

        self.dic_of_requested_branches = {}
        
        for cat,br in data_loaded.items():
            self.dic_of_requested_branches[cat] = br.split(",")

        # self.imported_unclustered_branches = {"UNCATEGORISED" : dic_of_requested_branches["UNCATEGORISED"]}
        # self.imported_clustered_branches   = {(k,v) for (k,v) in dic_of_requested_branches.items() if k!="UNCATEGORISED"}

    def add_object_pages(self):

        self.object_pages = []
        for k,v in self.dic_of_requested_branches.items():
            Obj_Page = PhysOb_Page_TwoColumn(phys_ob=k,      
                                                input_objects=self.list_of_input_objects,  
                                                branches2plot=v)
            self.object_pages.append(Obj_Page)

        # Build MultiPage here 
        MP = MultiPage()
        for page in self.object_pages:
            MP.add_page(page)
        MP.Build_MultiPage()        


        









class General(Tree_Comparison_App):

    """
    For taking all branches (non-clustered)
    """

    # all_branches = None

    def get_all_common_branches(self):

        list_of_branches = [io.tree.keys() for io in self.list_of_input_objects]

        Output = set(list_of_branches[0])
        for l in list_of_branches[1:]:
            Output &= set(l)
        
        # Converting to list
        self.all_branches = list(Output)


    def __init__(self,input_dictionary,**kwargs):

        super().__init__(input_dictionary)
        self.get_all_common_branches()

    @staticmethod
    def make_from_config(yaml_file):
        data_loaded = parse_config(yaml_file)
        return General(data_loaded)

    def add_object_pages(self):
        the_page   =  PhysOb_Page_TwoColumn(phys_ob="All Branches",   input_objects=self.list_of_input_objects,  branches2plot=self.all_branches)
        the_page.Build()

  




