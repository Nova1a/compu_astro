#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

os.chdir("/path/to/all/the/data/Data") # Path to all the data


# Constants
Mdot = 2e30 #kg
G = 6.67e-11 #m3/kg/s2
au = 1.49e11 #m
erg = 1e-7 #Joule


# Round function to bin the data
def round_off(number):
    return round(number * 4) /4



def create_files():
    
    step = pd.read_csv("/path/step.csv")
    columns = ["NAME1", "NAME2","M1[M*]","M2[M*]","SEMI[AU]"]

    # "Walk" through all the folders and all the files
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()):
        for filename in filenames:
        
            # For binaries
            if filename.startswith('binary.40'):
                a = os.path.abspath(os.path.join(dirpath, filename))
            
                # Extract the SC info from the path/file
                _,M = a.split("M")
                M,_,Z,___ = M.split("_")
                Z,_ = Z.split("/")
                Z = Z[1:]
                Z = float(Z)
                binary,time = filename.split("_")
                time = int(time)
                M = int(M)
            
                # Read the file
                df = pd.read_csv(a,skiprows=1, delim_whitespace=True, names=columns, usecols=[0,1,3,4,18])
            
                # Find the step for time conversation
                b = step.loc[(step["MCLU"]==M) & (step["Z"]==Z)]
                b = float(pd.to_numeric(b['step']))
                time_myr = round_off(time/b)
                df.insert(0, column="TIME[Myr]", value=time_myr)
            
                # Add the SC properties
                df.insert(0, column="Z", value=Z)
                df.insert(0, column="MCLU", value=M)
            
                # Calculate the Binding Energy
                df["EBIN"] = (df["M1[M*]"]*df["M2[M*]"]/(df["SEMI[AU]"]))
                df["EBIN"] = df["EBIN"]*(G*(Mdot**2)/(2*au*erg))
                df = df.sort_values(by=["Z","MCLU","TIME[Myr]","NAME1"], ascending=True)
                df = df.drop(["M1[M*]","M2[M*]","SEMI[AU]"],axis =1)
            
                # Total number of stars in the binaries
                N = len(df.index)
                df["NB"] = N*2 
            
                # Discriminate between primordial and non-primordial 
                df["NB_P"] = np.where(((df["NAME1"]+1) %2 == 0),
                                      np.where((df["NAME2"] == df["NAME1"]+1),
                                               np.where((df["NAME1"] < df["NB"]),
                                                        1,0),
                                               0),0) # 1 = primordial, 0 = non-primordial
            
                # Total number of primordial binaries
                df["P"] = len(df[df["NB_P"]==1])
                NB_P = df["P"].max()
            
            
                # Create both the binding energy and the ratio files
                binding_energy = df.groupby(["MCLU","TIME[Myr]","Z","NB_P"])["EBIN"].sum().reset_index()
                data = {'Z': Z,
                        'MCLU': M,
                        'TIME[Myr]':time_myr,
                        'NB_P': NB_P/N}
                ratio = pd.DataFrame(data, index=[0])
            
            
                # if file does not exist write header 
                if not os.path.isfile('binding_energy.csv'):
                    binding_energy.to_csv('binding_energy.csv',index=False, header=True)
                    
                # else it exists so append without writing the header 
                else: 
                    binding_energy.to_csv('binding_energy.csv', index=False, mode="a", header=False)
                
                
                # Same for the ratio    
                if not os.path.isfile('ratio.csv'):
                    ratio.to_csv('ratio.csv', index=False, header=True)
                else:
                    ratio.to_csv('ratio.csv', index=False ,mode="a", header=False)
                    
    return print("Files has been created :)")


def plot_binding_energy():
    
    # Read the binding_energy file
    Z = pd.read_csv('/home/chema/Desktop/Astro&Cosmo/3rd/CA/FinalFinal/BBE/binding_energy.csv')
    Z = Z.sort_values(by=["Z","MCLU","TIME[Myr]"], ascending=True)
    #print(Z)
    
    # Get the median of all the simulations for each time, metallicity and type of binary
    Z = Z.groupby(["TIME[Myr]","Z","NB_P"])["EBIN"].median().reset_index()
    
    # Colorblind palette
    palette = sns.color_palette("colorblind", len(Z["Z"].unique())).as_hex()
    
    # Plot
    fig, ax1 = plt.subplots()
    fig.set_size_inches(12,10)
    ax1 = sns.lineplot(data=Z,x="TIME[Myr]" ,y="EBIN", hue="Z",style="NB_P" ,palette=palette,linewidth=4.5)
    handles, labels = ax1.get_legend_handles_labels()
    leg = ax1.legend(fontsize = 25,title_fontsize='25',loc='best')
    for line in leg.get_lines():
        line.set_linewidth(4.5)
    ax1.xaxis.get_ticklocs(minor=True)
    ax1.minorticks_on()
    plt.ylabel("$E_{b}$[ergs]", fontsize=25)
    plt.yscale("log")
    plt.xlabel("TIME[Myr]", fontsize=25)
    plt.xticks(fontsize=25)
    plt.yticks(fontsize=25)
    
    # Change the limits to have a "Zoom" of the plot
    plt.xlim(0,5)
    
    # Add a vertical line
    plt.axvline(x = 1.75, color = 'b', label = 'core-collapse')
    plt.yscale("log")
    
    #Save figure
    plt.savefig('binding_energy.png',dpi = 300,bbox_inches = 'tight')
    
    return plt.show()


def plot_ratio():
    
    # Read the file for the ratio
    M = pd.read_csv("ratio.csv")
    M = M.sort_values(by=["Z","MCLU","TIME[Myr]"], ascending=True)
    #print(M)
    
    #Get the median of all the simulations for each time and metallicity
    M = M.groupby(["TIME[Myr]","Z",])["NB_P"].median().reset_index()
    
    # Fontsizes
    a=18
    b=25
    
    # Colorblinf palette
    color_pal = sns.color_palette("colorblind", len(M["Z"].unique())).as_hex()
    
    #Plot
    fig, ax1 = plt.subplots()
    fig.set_size_inches(12,10)
    ax1 = sns.lineplot(data=M,x="TIME[Myr]" ,y="NB_P", hue="Z", palette=color_pal,linewidth=4.5)
    leg = ax1.legend(title="Z",fontsize = b,title_fontsize='25',loc='best')
    for line in leg.get_lines():
        line.set_linewidth(4.5)
    ax2 = fig.add_axes([.25, .5, .40, .35])
    ax2 = sns.lineplot(data=M,x="TIME[Myr]" ,y="NB_P", hue="Z", palette=color_pal,linewidth=3.5 ,legend=False)
    ax2.text(0.78, 0.565, 'TIME[Myr]', fontsize = a)
    ax2.set_ylabel("% Primordial Binaries", fontsize = a)
    
    # "Zoom" for the small plot
    ax2.set_xlim(0,2)
    ax2.set_ylim(0.55,1)
    ax2.set_xlabel("")
    
    # More plot
    ax1.set_xlim(0,105)
    ax1.set_ylabel("% Primordial Binaries",fontsize = b)
    ax1.set_xlabel("TIME[Myr]",fontsize = b)
    ax1.tick_params(axis='x', labelsize=b)
    ax1.tick_params(axis='y', labelsize=b)
    ax2.tick_params(axis='x', labelsize=a)
    ax2.tick_params(axis='y', labelsize=a)
    
    # Save figure
    plt.savefig('ratio_primordial.png',dpi = 300,bbox_inches = 'tight')
    
    return plt.show()



#create_files()
#plot_binding_energy()
#plot_ratio()

