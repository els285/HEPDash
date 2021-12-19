import matplotlib.pyplot as plt
import mplhep as hep
import hist
import numpy as np
from hist.intervals import ratio_uncertainty
import boost_histogram as bh
import uproot
import functools
import operator
import math
 



class PyHist_Object:

    '''
    A basic wrapper for storing a boost-histogram and associated bin errors
    Also required to contain specific plotting information e.g. colour and legend label
    '''

    def __init__(self,Histogram,errors,**kwargs):

        self.Histogram = Histogram 
        self.errors_up = errors[1]
        self.errors_down = errors[0]
        # self.colour "black"
        # self.label = ""

        self.Set_Features(**kwargs)

    def Set_Features(self,**kwargs):

        self.colour = kwargs["colour"] if "colour" in kwargs else "black"
        self.label  = kwargs["label"]  if "label"  in kwargs else ""



class Histogram_Wrapper:

    ''' 
    Larger wrapper for Boost-Histogram object generated from Uproot parsing of ROOT file 
    Contains methods for extracting histogram from Uproot file and constructing boost-histogram 
    Stores the above PyHist_Objects for both normalised and unnormalised cases
    '''

    def __init__(self,df,**kwargs):

        # self.TTree = ttree
        # self.branch_name = branch_name
        self.number_of_bins = 26
        self.normalise = kwargs["normalise"] if "normalise" in kwargs else True

        # Plot features
        self.colour = kwargs["colour"] if "colour" in kwargs else None
        self.label  = kwargs["label"]  if "label"  in kwargs else None

        # Extract histogram for Uproot file TTree
        self.df = df

        self.Generate_Binning(kwargs)


        compute_errors = lambda errors: [np.sqrt(boost_hist.variances()),np.sqrt(boost_hist.variances())]

        # Generate boost_histogram, and wrap with errors
        boost_hist = bh.Histogram(bh.axis.Variable(self.binning))
        boost_hist.fill(self.df)
        boost_hist_errors = compute_errors(boost_hist)
        self.UnNorm_Hist = PyHist_Object(boost_hist,boost_hist_errors,colour=self.colour,label=self.label)
       
       # Generate normalised histogram, and wrap with errors
        if self.normalise:
            norm_boost_hist    = self.normalise_boost_histogram(boost_hist)
            norm_boost_hist_errors = compute_errors(norm_boost_hist)
            self.Norm_Hist = PyHist_Object(norm_boost_hist,norm_boost_hist_errors,colour=self.colour,label=self.label)

        # self.UnNorm_Hist.colour,self.Norm_Hist.colour = self.colour,self.colour


    def Generate_Binning(self,kwargs):
        if "binning" in kwargs:
            self.AutoBin = False
            self.binning = kwargs["binning"]

        else:
            self.AutoBin = True
            num_bins = kwargs["number_of_bins"] if "number_of_bins" in kwargs else self.number_of_bins
            maxH,minH = float(math.ceil(df.max())),float(math.floor(df.min()))
            self.binning = np.linspace(minH,maxH,num_bins)


    def Change_Defaults(self,**kwargs):

        self.number_of_bins = kwargs["number_of_bins"] if "number_of_bins" in kwargs else self.number_of_bins



    @staticmethod
    def normalise_boost_histogram(orig_boost_hist):

        ''' Recommended method for normalising histogram'''

        norm_boost_hist = orig_boost_hist.copy()    

        area = functools.reduce(operator.mul, norm_boost_hist.axes.widths)
        factor = np.sum(norm_boost_hist.view())
        view = norm_boost_hist.view() / (factor * area)

        for i,x in enumerate(view):  
            norm_boost_hist[i]=x

        print(norm_boost_hist.sum())

        return norm_boost_hist


