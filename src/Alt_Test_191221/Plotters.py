# Various plotters
import mplhep as hep
from hist.intervals import ratio_uncertainty
import matplotlib.pyplot as plt
from matplotlib.lines import Line2D



from Histogram_Classes import PyHist_Object, Histogram_Wrapper



def Compute_Ratio(hist1,hist2):

    ratio_hist = hist1/hist2
    ratio_uncertainties = ratio_uncertainty(hist1.view(),hist2.view(),"poisson-ratio")
    return PyHist_Object(ratio_hist,ratio_uncertainties)#[0],ratio_uncertainties[1])


def standard_plot(dic_of_hists,normalise):

    hep.style.use("ATLAS")
    fig,ax = plt.subplots()
    fig.set_size_inches(6,6)
    if normalise:
        [hep.histplot(h.Norm_Hist.Histogram,yerr=False) for h in dic_of_hists.values()]
    else:
        [hep.histplot(h.UnNorm_Hist.Histogram,yerr=True) for h in dic_of_hists.values()]

    legend_elements = [Line2D([0],[0],color=h.colour,lw=2,label=h.label) for h in dic_of_hists.values()]
    ax.legend(handles=legend_elements)#, loc='center')

    return fig



def ratio_only_plot(dic_of_hists,normalise,divisor_histogram):
    hep.style.use("ATLAS")
    fig,ax = plt.subplots()
    fig.set_size_inches(6,6)    

    legend_elements = []            

    for n,h in dic_of_hists.items():
        if normalise:
            ratio_obj = Compute_Ratio(h.Norm_Hist.Histogram,divisor_histogram.Norm_Hist.Histogram)
        else:
            ratio_obj = Compute_Ratio(h.UnNorm_Hist.Histogram,divisor_histogram.UnNorm_Hist.Histogram)                                               
        hep.histplot(ratio_obj.Histogram,yerr=False,ax=ax)

        legend_elements.append(Line2D([0],[0],color=h.colour,lw=2,label=h.label))
    ax.legend(handles=legend_elements)#, loc='center')

    return fig

def combined_plot(dic_of_hists,normalise,divisor_histogram):
    fig, (ax, rax) = plt.subplots(2, 1, figsize=(6,6), gridspec_kw=dict(height_ratios=[3, 1], hspace=0.1), sharex=True)
    fig.set_size_inches(6,6)

    legend_elements = []
    
    for n,h in dic_of_hists.items():
        if normalise:
            hep.histplot(h.Norm_Hist.Histogram,yerr=False,ax=ax)
            ratio_obj = Compute_Ratio(h.Norm_Hist.Histogram,divisor_histogram.Norm_Hist.Histogram)
            hep.histplot(ratio_obj.Histogram,yerr=False,ax=rax)
        else:
            hep.histplot(h.UnNorm_Hist.Histogram,yerr=False,ax=ax)
            ratio_obj = Compute_Ratio(h.UnNorm_Hist.Histogram,divisor_histogram.UnNorm_Hist.Histogram)
            hep.histplot(ratio_obj.Histogram,yerr=False,ax=rax)   

        legend_elements.append(Line2D([0],[0],color=h.colour,lw=2,label=h.label))
    ax.legend(handles=legend_elements)#, loc='center')

    return fig                              