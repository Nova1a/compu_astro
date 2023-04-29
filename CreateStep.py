# Walks through all files and gets the step to convert the time from NB units to Myr
import os
import pandas as pd

os.chdir("/path/to/all/the/data/Data") # Path to all the data

def step_csv():
    lo=[]
    for (dirpath, dirnames, filenames) in os.walk(os.getcwd()): # "Walk" through all the folders and all the files
        for filename in filenames:
            if filename.startswith('binary.40'):
                a = os.path.abspath(os.path.join(dirpath, filename))
                _,M = a.split("M")
                M,_,Z,___ = M.split("_")
                Z,_ = Z.split("/")
                Z = Z[1:]
                Z = float(Z)
                binary,time = filename.split("_")
                time = int(time)
                M = int(M)
                data = {'Z': Z,
                        'MCLU': M,
                       'TIME[NB]':time}
                df = pd.DataFrame(data, index=[0])
                lo.append(df)
    
    step = pd.concat(lo,axis=0)
    step = step.groupby(['Z', 'MCLU'])['TIME[NB]'].max().reset_index()
    step["step"] = step["TIME[NB]"]/100 
    step = step.drop(["TIME[NB]"],axis=1)
    step.columns = ["Z","MCLU","step"]
    step.to_csv('step.csv', index=False)
    return print("File has been created :)")

step_csv()
