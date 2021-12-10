import itertools
from Plot_Multi_2columnB import import_ROOT_file
import streamlit as st

from dataclasses import dataclass

@dataclass
class InputObject:
    name: str
    ROOT_file_path: str
    tree_name: str 
    tree: any 


class Premade_Tree_Comparison_App:

    """
    The Premade_Tree_Comparison_App is a class for generating a streamlit-based web app for comparing the contents of TTrees in separate ROOT files
    The Premade class has pre-defined branches to project out, which must appear in all ROOT files.
    Intention: the TBrowser() extension: for visual inspection of branches in NTuples
    The app will be split by object and observable
    Pulls out all common branches in the ROOT files, or a specified sub-set
    """

    physics_objects = ["el","mu","jet"]
    observable_branches = ["_pt","_eta","_phi","_e"]
    all_branches = [''.join(p) for p in itertools.product(physics_objects, observable_branches)]

    def __init__(self,input_dictionary):

        '''
        input dictionary should be of the form {name: [ROOT_file_path,tree_name])}
        '''
        self.list_of_input_objects = []

        for k,v in input_dictionary.items():
            io = InputObject(k,v[0],v[1],None)
            self.list_of_input_objects.append(io)
        
        self.load()
        self.check_trees_for_branches()

    def load(self):

        for v in self.list_of_input_objects:
            v.tree = import_ROOT_file(v.ROOT_file_path,v.tree_name)

    def check_trees_for_branches(self):

        for io in self.list_of_input_objects:
            assert all([branch_name in io.tree.keys() for branch_name in self.all_branches]), "Not all prerequisit branches found in tree"
