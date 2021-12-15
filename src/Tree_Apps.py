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


class Tree_Comparison_App:

    """
    Base class Tree comparison app
    """

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



class Preset(Tree_Comparison_App):

    """
    Using preset branches on preset physics objects
    """

    physics_objects = ["el","mu","jet"]
    observable_branches = ["_pt","_eta","_phi","_e"]
    all_branches = [''.join(p) for p in itertools.product(physics_objects, observable_branches)]    

    def __init__(self,input_dictionary):
        super().__init__(input_dictionary) 


class Specific(Tree_Comparison_App):

    """
    For specifying particular branches (clustered or non-clustered)
    Unclustered branches can be given as a list
    """


    def __init__(self,input_dictionary,**kwargs):

        self.imported_unclustered_branches = kwargs["unclustered_branches"] if "unclustered_branches" in kwargs and isinstance(kwargs["unclustered_branches"],list) else []
        self.imported_clustered_branches   = kwargs["clustered_branches"]   if "clustered_branches"   in kwargs and isinstance(kwargs["clustered_branches"],dict)   else {}
        self.all_branches = self.imported_unclustered_branches + self.imported_clustered_branches.values()


        super().__init__(input_dictionary)


class General(Tree_Comparison_App):

    """
    For taking all branches (non-clustered)
    """

    all_branches = None

    def __init__(self,input_dictionary,**kwargs):

        super().__init__(input_dictionary)





