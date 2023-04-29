#!/usr/bin/env python
# coding: utf-8

# In[43]:


# Create a file and the Lagrangian radii plots
import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns


os.chdir("/path/to/all/the/data/Data") # Path to all the data

def round_off(number):
    return round(number * 2) / 2

def R_L():
    
    step = pd.read_csv("step.csv")

    # "Walk" through all the folders and all the files
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()): 
        for filename in filenames:
            
            # Grab the Lagrangian radii with the lagr.7 files
            if filename.endswith('lagr.7'):
                a = os.path.abspath(os.path.join(dirpath, filename))
            
                # Extract the SC info from the path/file
                _,M = a.split("M")
                M,_,Z = M.split("_")
                Z,_ = Z.split("/")
                Z = Z[1:]
                Z = float(Z)
                M = int(M)
                df = pd.read_csv(a, header = 1, delim_whitespace=True, usecols=[0,11,19])
            
                # Find the step for time conversation
                b = step.loc[(step["MCLU"]==M) & (step["Z"]==Z)]
                b = float(pd.to_numeric(b['step']))          
            
                # Add the SC properties
                df.insert(0, column="Z", value=Z)
                df.insert(0, column="MCLU", value=M)
                df.insert(0, column="TIME[Myr]", value=round_off(df["TIME"]/b))
                df = df.drop(["TIME"],axis =1)
            
                # Create the files for the rc and rh
                rc = df[["TIME[Myr]","MCLU","Z","<RC"]]
                rc.columns = ["TIME[Myr]","MCLU","Z","<RC"]
                rh = df[["TIME[Myr]","MCLU","Z","5.00E-01"]]
                rh.columns = ["TIME[Myr]","MCLU","Z","5.00E-01"]
            
                # if file does not exist write header 
                if not os.path.isfile('rc.csv'):
                    rc.to_csv('rc.csv',index=False, header=True)
                    
                # else it exists so append without writing the header 
                else: 
                    rc.to_csv('rc.csv', index=False, mode="a", header=False)
                
                
                # Same for rh    
                if not os.path.isfile('rh.csv'):
                    rh.to_csv('rh.csv', index=False, header=True)
                else:
                    rh.to_csv('rh.csv', index=False ,mode="a", header=False)
                    
    return print("Files have been created :)")

def plot_R_L():
    
    # Read both the files for the rc and rh
    rc = pd.read_csv("rc.csv")
    rh = pd.read_csv("rh.csv")
    
    # Get the median values for the radii
    rc = rc.groupby(["TIME[Myr]","Z"])["<RC"].median().reset_index()
    rh = rh.groupby(["TIME[Myr]","Z"])["5.00E-01"].median().reset_index()
    
    # Plot
    fig, axs = plt.subplots(ncols=2)
    fig.set_size_inches(24, 10)
    
    # Colorlind palette
    color_pal = sns.color_palette("colorblind", len(rc["Z"].unique())).as_hex()
    
    # rc line
    sns.lineplot(data=rc,x="TIME[Myr]" ,y="<RC", hue="Z", palette=color_pal, ax = axs[0],
                 legend=False,linewidth=4.5)
   
    # rh line
    sns.lineplot(data=rh,x="TIME[Myr]" ,y="5.00E-01", hue="Z", palette=color_pal,
                 ax = axs[1],linewidth=4.5)
    
    # Create a pink like that scales like t**2/3
    x=np.linspace(6,100,100)
    y = 2.5 + 0.06*x**(2/3)
    df = pd.DataFrame(y, columns=['2/3'])
    df["TIME[Myr]"] = x
    sns.lineplot(data=df,x="TIME[Myr]" ,y="2/3", ax =axs[1], linewidth=4.5,color="#cc78bc" ,linestyle='--')
    
    # Define sizes and adjustments
    ax2 = fig.add_axes([.72, .18, .15, .25])
    ax2 = sns.lineplot(data=rh,x="TIME[Myr]" ,y="5.00E-01", hue="Z", palette=color_pal,
                       linewidth=2.5,legend=False)
    ax2.set_ylabel("$r_{h} [pc]$", fontsize = 18)
    ax2.set_xlabel("", fontsize = 1)
    ax2.text(2.5, .82, 'TIME[Myr]', fontsize = 18)
    ax2.tick_params(axis='x', labelsize=18)
    ax2.tick_params(axis='y', labelsize=18)
    ax2.set_xlim(0,6)
    ax2.set_ylim(0.8,1.3)
    leg = axs[1].legend(title="Z",fontsize = 25,title_fontsize='25',loc='best')
    for line in leg.get_lines():
        line.set_linewidth(4.5)
    axs[0].set_ylabel("$r_{c} [pc]$", fontsize=25)
    axs[1].set_ylabel("$r_{h} [pc]$",fontsize=25)
    axs[0].set_xlabel("TIME[Myr]", fontsize=25)
    axs[1].set_xlabel("TIME[Myr]",fontsize=25)
    axs[0].set_xlim(0,105)
    axs[1].set_xlim(0,105)
    axs[0].tick_params(axis='x', labelsize=25)
    axs[0].tick_params(axis='y', labelsize=25)
    axs[1].tick_params(axis='x', labelsize=25)
    axs[1].tick_params(axis='y', labelsize=25)
    plt.text(0.5, 1.950, '$\propto t^{2/3}$', c="#cc78bc", fontsize=25,rotation=30)
    sns.move_legend(axs[1], "upper center", bbox_to_anchor=(-.18, -0.11),
                    ncol=4,fontsize = 25,title_fontsize='25')
    
    # Save figure
    plt.savefig('R_lag.png',dpi=300,bbox_inches = 'tight')
    
    return plt.show()

R_L()
plot_R_L()


# In[ ]:




