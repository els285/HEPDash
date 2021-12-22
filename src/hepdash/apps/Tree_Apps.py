from dataclasses import dataclass
import itertools
import yaml
import os
import matplotlib.pyplot as plt
import streamlit as st

from hepdash.layouts.BiColumn import import_ROOT_file


default_colours = plt.rcParams['axes.prop_cycle'].by_key()['color']

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

    @staticmethod
    def make_from_config(yaml_file):
        data_loaded = parse_config(yaml_file)
        return Specific(data_loaded)



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
        return Specific(data_loaded)

  




