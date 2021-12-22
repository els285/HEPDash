# Various plotters
import mplhep as hep
from hist.intervals import ratio_uncertainty
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D


from hepdash.histograms.Histogram_Classes import PyHist_Object, Histogram_Wrapper
from hepdash.histograms.design import HEP_histogram_design_parameters


def Compute_Ratio(hist1,hist2):

    """
    Compute ratio dividies two boost_histogram hists
    Computes the ratio_uncertainties through hist.intervals method, though this seems to cause issue
    """

    ratio_hist = hist1/hist2
    ratio_uncertainties = ratio_uncertainty(hist1.view(),hist2.view(),"poisson-ratio")
    return PyHist_Object(ratio_hist,ratio_uncertainties)#[0],ratio_uncertainties[1])


def standard_plot(dic_of_hists,normalise,xaxis_label):

    """
    standard_plot() displays the (normalised or unnormalised) histograms 
    """

    hep.style.use(HEP_histogram_design_parameters["experiment"])
    fig,ax = plt.subplots()
    fig.set_size_inches(6,6)

    HEP_histogram_design_parameters["HEP experiment label"].text(HEP_histogram_design_parameters["HEP label text"],ax=ax,loc=1)

    if normalise:
        [hep.histplot(h.Norm_Hist.Histogram,yerr=False,color=h.colour) for h in dic_of_hists.values()]
        ax.set_ylabel('Number of Events (Normalised)',fontsize=16)
    else:
        [hep.histplot(h.UnNorm_Hist.Histogram,yerr=True,color=h.colour) for h in dic_of_hists.values()]
        ax.set_ylabel('Number of Events (Unnormalised)',fontsize=16)

    if any([x in xaxis_label for x in ["p_{T}","E"]]):
        ax.set_xlabel(xaxis_label,labelpad=20)
    else:
        ax.set_xlabel(xaxis_label,labelpad=0)


    # Legend
    legend_elements = [Line2D([0],[0],color=h.colour,lw=2,label=h.label) for h in dic_of_hists.values()]
    ax.legend(handles=legend_elements)#, loc='center')

    return fig



def ratio_only_plot(dic_of_hists,normalise,divisor_histogram,xaxis_label):

    """
    ratio_only_plot() displays the ratios of any histograms with respect to one of them
    """

    hep.style.use(HEP_histogram_design_parameters["experiment"])
    fig,ax = plt.subplots()
    fig.set_size_inches(6,6)    

    HEP_histogram_design_parameters["HEP experiment label"].text(HEP_histogram_design_parameters["HEP label text"],ax=ax,loc=1)


    legend_elements = []            

    for n,h in dic_of_hists.items():
        if normalise:
            ratio_obj = Compute_Ratio(h.Norm_Hist.Histogram,divisor_histogram.Norm_Hist.Histogram)
        else:
            ratio_obj = Compute_Ratio(h.UnNorm_Hist.Histogram,divisor_histogram.UnNorm_Hist.Histogram)                                               
        hep.histplot(ratio_obj.Histogram,yerr=False,ax=ax,color=h.colour)

        legend_elements.append(Line2D([0],[0],color=h.colour,lw=2,label=h.label))
    ax.legend(handles=legend_elements)#, loc='center')

    if any([x in xaxis_label for x in ["p_{T}","E"]]):
        ax.set_xlabel(xaxis_label,labelpad=20)
    else:
        ax.set_xlabel(xaxis_label,labelpad=0)    
    ax.set_ylabel('Ratio w.r.t. ' + divisor_histogram.belongs2,fontsize=16)

    return fig


def combined_plot(dic_of_hists,normalise,divisor_histogram,xaxis_label):

    """
    combined_plot() generates a figure made up of two subplots
    The top plot shows the histogram,
    the bottom plot displays the ratios with respect to a chosen histogram
    """


    hep.style.use(HEP_histogram_design_parameters["experiment"])
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)
    fig.set_size_inches(6,6)

    HEP_histogram_design_parameters["HEP experiment label"].text(HEP_histogram_design_parameters["HEP label text"],ax=ax,loc=1)

    legend_elements = []
    
    for n,h in dic_of_hists.items():
        if normalise:
            hep.histplot(h.Norm_Hist.Histogram,yerr=False,ax=ax,color=h.colour)
            ratio_obj = Compute_Ratio(h.Norm_Hist.Histogram,divisor_histogram.Norm_Hist.Histogram)
            hep.histplot(ratio_obj.Histogram,yerr=False,ax=rax,color=h.colour)
            ax.set_ylabel('Number of Events (Normalised)',fontsize=14)
        else:
            hep.histplot(h.UnNorm_Hist.Histogram,yerr=False,ax=ax,color=h.colour)
            ratio_obj = Compute_Ratio(h.UnNorm_Hist.Histogram,divisor_histogram.UnNorm_Hist.Histogram)
            hep.histplot(ratio_obj.Histogram,yerr=False,ax=rax,color=h.colour)   
            ax.set_ylabel('Number of Events (Unormalised)',fontsize=14)

        legend_elements.append(Line2D([0],[0],color=h.colour,lw=2,label=h.label))
    ax.legend(handles=legend_elements)#, loc='center')

    if any([x in xaxis_label for x in ["p_{T}","E"]]):
        rax.set_xlabel(xaxis_label,labelpad=20)
    else:
        rax.set_xlabel(xaxis_label,labelpad=0)    
    
    rax.set_ylabel('Ratio w.r.t. ' + divisor_histogram.belongs2,fontsize=12)


    return fig                                  