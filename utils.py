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
                 error = False,
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
        if error: 
            y_err = np.array(dfplot["err_" + y_name])
            print
        else:
            y_err=None
        if bar:
            plt.bar(x_data + bar_start[i] * bar_width, 
                         y_data, 
                         yerr=y_err,
                         xerr=None,
                         width=bar_width, 
                         align="center", 
                         alpha=alpha, 
                         color=color, 
                         label=y_name,
                         error_kw={"capsize":1.5,"elinewidth":1}
                   )
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
    
    
    
def get_efficacy(df: pd.DataFrame, z_value=1.645):
    
    for vax_status in ["1st_dose", "2nd_dose", "no_vax"]:
        
        df[f"ev_{vax_status}_per_100k"] =  np.round((1e5) * df[f"event_{vax_status}"]/df[f"pop_{vax_status}"],3)
            
        p = df[f"event_{vax_status}"]/df[f"pop_{vax_status}"]
        q = 1 - p
        N = df[f"pop_{vax_status}"]
        df[f"err_ev_{vax_status}_per_100k"] = z_value * (1e5) * np.sqrt(p*q) / np.sqrt(N)
        
        
    for vax_status in ["1st_dose", "2nd_dose"]:
        df[f"efficacy_{vax_status}"] =  np.round(1 - df[f"ev_{vax_status}_per_100k"]/df["ev_no_vax_per_100k"],3)
        
        df.replace([-np.inf], 0, inplace=True)
        
        A = 1 - df[f"ev_{vax_status}_per_100k"]
        B = df["ev_no_vax_per_100k"]
        sA = df[f"err_ev_{vax_status}_per_100k"]
        sB = df[f"err_ev_no_vax_per_100k"]
        f = df[f"efficacy_{vax_status}"]
        df[f"err_efficacy_{vax_status}"] = z_value * np.round(np.abs(f) * np.sqrt((sA/A)**2 + (sB/B)**2),3)
            
        df[f"arr_{vax_status}"] = (df[f"ev_no_vax_per_100k"] - df[f"ev_{vax_status}_per_100k"])/(1e5)
        df[f"nntv_{vax_status}"] = 1/df[f"arr_{vax_status}"]
    
    return df