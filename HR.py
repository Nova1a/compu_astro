#!/usr/bin/env python
# coding: utf-8

# In[ ]:


#Create a file and the HR diagram

import os
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

os.chdir("/path/to/all/the/data/Data") # Path to all the data

# Round function to bin the data
def round_off(number):
    return round(number * 4) / 4


def HR():
    
    # Star classification
    values = ['Pre_MS', 'Low_MS', 'MS', 'Hertzsprung_Gap (HG)','Red_Giant_Branch (RGB)',
              'Core_Helium_Burning', 'Asymptotic_Giant_Branch (AGB)','Second_AGB',
              'Helium_MS', 'Helium_HG', 'Helium_Giant_Branch', 'Helium_WD','Carbon_Oxygen_WD',
              'Oxygen_Neon_WD','NS', 'BH','Massless_SNR']

    # Step and columns
    step = pd.read_csv("/home/chema/Desktop/Astro&Cosmo/3rd/CA/HR_Again/step.csv")
    ab = ["L1[L*]","L2[L*]","TEFF1[K]","TEFF2[K]","K*1","K*2"]
    cd = ["L[L*]","Teff[K]","K*"]
    
    # "Walk" through all the folders and all the files
    for root, dirpath, filenames in os.walk(os.getcwd()): 
        for name in filenames: 
            
            # For binaries
            if name.startswith('binary.40'): 
                
                # Get the SC properties
                a = os.path.abspath(os.path.join(root, name))
                _,M = a.split("M")
                M,_,Z,___ = M.split("_")
                Z,_ = Z.split("/")
                Z = Z[1:]
                binary,time = name.split("_")
                time = int(time)
                M = int(M)
                Z = float(Z)
                
                # Find the step for time convertion
                b = step.loc[(step["MCLU"]==M) & (step["Z"]==Z)]
                b = float(pd.to_numeric(b['step']))
                time_myr = round_off(time/b)
                
                # Get the stars that will be part of the plot 
                if time_myr in (0,10,20,30,40,50,60,70,80,90,100):
                    
                    # Read the file
                    df = pd.read_csv(os.path.join(root, name),skiprows=1, delim_whitespace=True,
                                     names=ab, usecols=[24,25,26,27,32,33])
                    
                    # Add the SC properties
                    df.insert(0, column="TIME[Myr]", value=time_myr)
                    df.insert(0, column="MCLU", value=M)
                    df.insert(0, column="Z", value=Z)
                    
                    # Classify the stars depending on the condition
                    conditions1 = [(df['K*1'] == -1),(df['K*1'] == 0),(df['K*1'] == 1),(df['K*1'] == 2),
                                   (df['K*1'] == 3),(df['K*1'] == 4),(df['K*1'] == 5),(df['K*1'] == 6),
                                   (df['K*1'] == 7),(df['K*1'] == 8),(df['K*1'] == 9),(df['K*1'] == 10),
                                   (df['K*1'] == 11),(df['K*1'] == 12),(df['K*1'] == 13),(df['K*1'] == 14),
                                   (df['K*1'] == 15)]
                    conditions2 = [(df['K*2'] == -1),(df['K*2'] == 0),(df['K*2'] == 1),(df['K*2'] == 2),
                                   (df['K*2'] == 3),(df['K*2'] == 4),(df['K*2'] == 5),(df['K*2'] == 6),
                                   (df['K*2'] == 7),(df['K*2'] == 8),(df['K*2'] == 9),(df['K*2'] == 10),
                                   (df['K*2'] == 11),(df['K*2'] == 12),(df['K*2'] == 13),(df['K*2'] == 14),
                                   (df['K*2'] == 15)]
                    df['Star1'] = np.select(conditions1, values)
                    df['Star2'] = np.select(conditions2, values)
                    
                    # Drop unnecessary columns
                    df = df.drop(["K*1","K*2"],axis =1)
                    
                    # Create to frames so each rwo represents 1 star and not the whole binary
                    df1 = df[["Z","MCLU","TIME[Myr]","L1[L*]","TEFF1[K]","Star1"]]
                    df1.columns = ["Z","MCLU","TIME[Myr]","L[L*]","Teff[K]","Star"]
                    df2 = df[["Z","MCLU","TIME[Myr]","L2[L*]","TEFF2[K]","Star2"]]
                    df2.columns = ["Z","MCLU","TIME[Myr]","L[L*]","Teff[K]","Star"]
                    
                    # Create the HR file
                    df = pd.concat([df1,df2],ignore_index=True)                  
                    
                    # if file does not exist write header 
                    if not os.path.isfile('HR.csv'):
                        df.to_csv('HR.csv', index=False, header=True)
                        
                    # else it exists so append without writing the header
                    else: 
                        df.to_csv('HR.csv', index=False, mode="a", header=False)
                        
            # For single stars
            if name.startswith('single.40'): 
                
                # Get the SC properties
                a = os.path.abspath(os.path.join(root, name))
                _,M = a.split("M")
                M,_,Z,___ = M.split("_")
                Z,_ = Z.split("/")
                Z = Z[1:]
                binary,time = name.split("_")
                time = int(time)
                M = int(M)
                Z = float(Z)
                
                # Find the step for time convertion
                b = step.loc[(step["MCLU"]==M) & (step["Z"]==Z)]
                b = float(pd.to_numeric(b['step']))
                time_myr = round_off(time/b)
                
                # Get the stars that will be part of the plot 
                if time_myr in (0,10,20,30,40,50,60,70,80,90,100):
                    
                    # Read the file
                    df = pd.read_csv(os.path.join(root, name),skiprows=1, delim_whitespace=True, names=cd, usecols=[10,11,14])
                    
                    # Add the SC properties
                    df.insert(0, column="TIME[Myr]", value=time_myr)
                    df.insert(0, column="MCLU", value=M)
                    df.insert(0, column="Z", value=Z)
                    
                    # Classify the stars depending on the condition
                    conditions1 = [(df['K*'] == -1),(df['K*'] == 0),(df['K*'] == 1),(df['K*'] == 2),
                                   (df['K*'] == 3),(df['K*'] == 4),(df['K*'] == 5),(df['K*'] == 6),
                                   (df['K*'] == 7),(df['K*'] == 8),(df['K*'] == 9),(df['K*'] == 10),
                                   (df['K*'] == 11),(df['K*'] == 12),(df['K*'] == 13),(df['K*'] == 14),
                                   (df['K*'] == 15)]
                    df['Star'] = np.select(conditions1, values)
                    
                    # Drop unnecessary columns
                    df = df.drop(["K*"],axis =1)
                    
                    
                    # Create the HR file just as above
                    if not os.path.isfile('HR.csv'):
                        df.to_csv('HR.csv', index=False, header=True)
                    else:
                        df.to_csv('HR.csv', index=False, mode="a", header=False)
                        
                        
    return print("Files has been created :)")


def plot_HR():
    
    # Read the file for the plot
    HR = pd.read_csv('/home/chema/Desktop/Astro&Cosmo/3rd/CA/HR_Again/HR.csv')
    
    # Drop BH and NS
    HR = HR.drop(HR[(HR['Star'] == "BH")].index)
    HR = HR.drop(HR[(HR['Star'] == "NS")].index)

    # Sometimes was faster for plotting to drop lots of MS stars
    #HR = HR.drop(HR.loc[HR['Star'] == 'Low_MS'].sample(frac=0.90).index)
    #HR = HR.drop(HR.loc[HR['Star'] == 'MS'].sample(frac=0.90).index)

    # Plot
    plt.rcParams.update(plt.rcParamsDefault)
    sns.reset_defaults()
    sns.set_style("white")
    g=sns.relplot(data=HR, x='Teff[K]', y='L[L*]', hue='Z', col="TIME[Myr]",style="Star",
                      palette = sns.color_palette("colorblind", HR['Z'].nunique()).as_hex(),s=50,col_wrap=3)
    g.set(xscale='log')
    g.set(yscale='log')
    for ax in g.axes.ravel():
        ax.invert_xaxis()
    leg = g._legend
    leg.set_bbox_to_anchor([0.8, 0.125])
    plt.savefig('HR.png',bbox_inches='tight')
    
    # We simply didn't find how to make the labels bigger :(
    return plt.show()

HR()
plot_HR()

