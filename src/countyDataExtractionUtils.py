import pandas as pd
import numpy as np 
import seaborn as sns; sns.set()



def findCountyLE(lifeExpDF, colOfInterest, colorStart, colorEnd):
    """
    Description: Finds all LEs for counties in the dataset and then assigns LEs to a color
        on a diverging color scale. 
    Input:
        lifeExpDF (pandas DF): A DF which contains FIPS, and LEs so they can be mapped to counties.
        leYear (str): The column string to look at for LEs. They have different years.
    Output:
        countyFpToLeDict (dict): Maps FIPS to a tuple of (name, color) where color are rgb values.
        LEs (list): A list of floats for LEs for every row of the DF
    TODO:
        1) Generalize a bit by adding in arguments for colos and number of buckets.
    """
    LEs = []
    # countyFpToLeDict = {}
    for row in lifeExpDF.iterrows():
        # print(row)
        lifeExp = row[1][colOfInterest]
        lifeExp = lifeExp
        lifeExp = lifeExp
        LEs.append(lifeExp)



    nBuckets = 11
    colorSpec = sns.diverging_palette(colorStart, colorEnd, n = (nBuckets + 1))
    _, bins = np.histogram(LEs, nBuckets)
    binAssignments = np.digitize(LEs, bins)



    countyFpToLeDict = {}
  
    for binAssignment, row in zip(binAssignments, lifeExpDF.iterrows()):
        # print(row)
        fip = str(row[1]["FIPS"]).zfill(5)
        if fip in countyFpToLeDict:
            print(countyFpToLeDict)
            print("*"*100)
            print(row)
            print("\n")
        lifeExp = row[1][colOfInterest]
        lifeExp = lifeExp
        lifeExp = lifeExp
        curColor = colorSpec[(binAssignment-1)]
        countyFpToLeDict[fip] = (row[1]["Location"], curColor)
        LEs.append(lifeExp)
    return(countyFpToLeDict, LEs, bins, colorSpec)