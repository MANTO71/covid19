# tick on mondays every week
import matplotlib.dates as mdates
import matplotlib.cbook as cbook
import matplotlib.pyplot as plt
import numpy as np
from datetime import datetime
import pandas as pd
from typing import Union, List

def createXYPlot(dfplot: pd.DataFrame,
                 x: str,
                 y: Union[str, List[str]],
                 today: str,
                 plots_folder: str,
                 figsize_x: int = 10,
                 figsize_y: int = 5,
                 xtitle: str = None,
                 ytitle: str = None,
                 dpis: int = 100,
                 bar: bool = False,
                 bar_width: float = 0.75,
                 bar_start: List[float] = None,
                 alpha: float = 1.0,
                 linewidth: float = 1.0,
                 savename: str = None,
                 title: str = None,
                 color: str = None,
                 start_date: str = None,
                 xlim: float = None,
                 days_interval: int = 4):
    
       
    if start_date is not None: dfplot = dfplot[pd.to_datetime(dfplot[x]) > datetime.strptime(start_date,'%Y-%m-%d')]

    dfplot = dfplot.sort_values(x).reset_index() 
    first_day = str(dfplot[x].tolist()[0])
    fig, ax = plt.subplots(figsize=(figsize_x, figsize_y),dpi=dpis)
    
    xindexes = [ x for x in dfplot.index  if (x + 1) % days_interval == 0]
    xlabels =  [ str(dfplot[x].tolist()[i]) for i in xindexes]

    i=0
    for y_name in y:
        x_data = dfplot.index
        y_data = np.array(dfplot[y_name])
        if bar:
            plt.bar(x_data + bar_start[i] * bar_width, y_data, width=bar_width, align="center", alpha=alpha, color=color, label=y_name)
        else:
            plt.plot(x_data, y_data, alpha=alpha, color=color, linewidth=linewidth, label=y_name)
        i+=1
        
    plt.grid(which="both")
    plt.legend(fontsize=12)
    
    if xtitle: 
        plt.xlabel(xtitle,fontsize=14)
    if ytitle:
        plt.ylabel(ytitle,fontsize=14)
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
    plt.yticks(fontsize=12)
    
    if savename:
        plt.savefig(f"{plots_folder}/{savename}",bbox_inches="tight")
    plt.show()
    plt.close()
    
    del(fig)