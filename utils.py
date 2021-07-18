# tick on mondays every week
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd

def createXYPlot(dfplot,
                 y,
                 today,
                 plots_folder,
                 x="giorno",
                 xtitle=None,
                 dpis=100,
                 bar=False,
                 barWidth=0.75,
                 barStart=None,
                 alpha=1.0,
                 linewidth=1.0,
                 savename=None,
                 title=None,
                 color=None,
                 color_avg="orange",
                 fitGauss=False, 
                 startDate=None,
                 xLim=None,
                 yticks=None,
                 daysInterval = 4):
    
       
    if startDate is not None: dfplot = dfplot[pd.to_datetime(dfplot[x]) > datetime.strptime(startDate,'%Y-%m-%d')]

    dfplot = dfplot.sort_values(x).reset_index() 
    first_day = str(dfplot[x].tolist()[0])
    fig, ax = plt.subplots(figsize=(12,6),dpi=dpis)
    
    xindexes = [ x for x in dfplot.index  if (x + 1) % daysInterval == 0]
    xlabels =  [ str(dfplot[x].tolist()[i]) for i in xindexes]

    i=0
    for y_name in y:
        x_data = dfplot.index
        y_data = np.array(dfplot[y_name])
        if bar:
            plt.bar(x_data+barStart[i]*barWidth, y_data, width=barWidth, align="center", alpha=alpha, color=color, label=y_name)
        else:
            plt.plot(x_data, y_data, alpha=alpha, color=color, linewidth=linewidth, label=y_name)
        try:
            y_data_mean = np.array(dfplot[y+"_media_7"])
            plt.plot(x_data, y_data_mean,"-",color=color_avg,linewidth=2.5)
        except:
            pass
        i+=1
        
    plt.grid(which="both")
    plt.legend(fontsize=12)
    
    if xtitle: 
        plt.xlabel(xtitle,fontsize=14)
    if title: 
        plt.title(title,fontsize=16)
    # format the coords message box
    ax.format_xdata = mdates.DateFormatter('%Y-%m-%d')
    plt.xticks(xindexes, 
               labels=xlabels, 
               fontsize=12,
               rotation=50, 
               rotation_mode="anchor", 
               verticalalignment = "top",
               horizontalalignment = "right")
    plt.yticks(yticks,fontsize=12)
    if savename:
        plt.savefig(f"{plots_folder}/{savename}",bbox_inches="tight")
    plt.show()
    plt.close()
    
    del(fig)