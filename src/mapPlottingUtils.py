from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import pandas as pd
# from src.countyDataExtractionUtils import findCountyLE

# Code heavily copied and influenced by
# http://shallowsky.com/blog/programming/plotting-election-data-basemap.html

"""
Description:
Input:
Output:
TODO:
"""





def getStateFPs(BM):
    """
    Description: Iterates through all states and grabs their stateFP ID. This is then used as an
        index to place the state in a list. This list can be then used by the counties_info FP ID
        info to snag state names.
    Input:
        BM (basemap object): Please refer to draw_us_map
    Output:
        stateFPs (list(str)) a list a state name is placed at it's FP index. 
    TODO:
    """
    MAXSTATEFP = 73
    stateFPs = [None] * MAXSTATEFP
    for state in BM.states_info:
        statefp = int(state["STATE"])# holds the FP ID for a state. County data uses these to map to states
        # Many states have multiple entries in m.states (because of islands).
        # Only add it once.
        if not stateFPs[statefp]:
            stateFPs[statefp] = state["NAME"]
    return(stateFPs)


def draw_us_map():
    """
    Description: Draws state and county boundaries on a map of the US. Reads ina file which 
        contains state and another that contains county level data.
    Input:
        None:
    Output:
        BM (basemap object): contains information on the states, counties, and their shape
            locations. You'll want to use this to update any counties with color data. BM has some
            important attributes. BM.sates_info[] is a list of dicts with the following important 
            information: NAME, AREA, PERIMETER as keys.
            BM.sates[] is a list of 2-tuples of numbers, not coordinates like
            (-745649.3757546246, 6074729.819906185). They're set up in such a way that the index of
            the a state in state_info[] is the index of the states shape tuples in BM.states[].
            BM also includes county information. BM.counties_info is a county level mirror of 
            BM.state_info. counties_info has no name for a state and instead relies on FP IDs. So 
            BM.counties_info[m]["STATEFP"] is an integer that corresponds to some state's
            BM.states_info[n]["STATE"].
        stateFPs (list(str)): State FP IDs can be used to index into stateFPs in order
            to get the corresponding state name.
    TODO:
        1) Make sure map county information andLE information years match
    """
    # Set the lower left and upper right limits of the bounding box:
    lllon = -119
    urlon = -64
    lllat = 22.0
    urlat = 50.5
    # and calculate a centerpoint, needed for the projection:
    centerlon = float(lllon + urlon) / 2.0
    centerlat = float(lllat + urlat) / 2.0
    height = 16*1.0
    width = 12*1.0
    fig = plt.figure(num=None, figsize=(height, width), dpi=300, facecolor='w', edgecolor='k')
    BM = Basemap(resolution='i',  # crude, low, intermediate, high, full
                llcrnrlon = lllon, urcrnrlon = urlon,
                lon_0 = centerlon,
                llcrnrlat = lllat, urcrnrlat = urlat,
                lat_0 = centerlat,
                projection='tmerc')
    # Read state boundaries.
    shp_info = BM.readshapefile('data/cartographyData/st99_d00', 'states',
                               drawbounds=True, color='lightgrey')

    # Read county boundaries
    shp_info = BM.readshapefile('data/cartographyData/cb_2015_us_county_500k/cb_2015_us_county_500k',
                               'counties',
                               drawbounds=True)
    stateFPs = getStateFPs(BM)
    return(BM, stateFPs)



def colorMap(BM, stateFPs, countyFpToLeDict):
    """
    Description: Colors counties on a map. Iterates through all counties and changes their color.
    Input:
        BM (basemap object): Please refer to draw_us_map
        stateFPs (list(str)): Please refer to draw_us_map
    Output:
        None:
    TODO:
        1) Sety individual county colors. Right now everything is set to blue, but you need
            to open and read the life expectancy data to get this information.
        2) handle alaska and Hawaii data. You need to draw counties for them and fix an issue
            where alaska being fucksy when you draw it.
    """





    ax = plt.gca() 
    for i, county in enumerate(BM.counties_info):
        countyname = county["NAME"]
        try:
            statename = stateFPs[int(county["STATEFP"])]
        except IndexError:
            print(countyname, "has out-of-index statefp of", county["STATEFP"])
            continue



        # The file has no results for Puerto Rico and Alaska.
        if statename in ["Puerto Rico", "Alaska", "Hawaii"]:
            # TODO there is data for alaska and hawaii but plotting them is difficult.
            # print("nothing for Alaska")
            continue

        if not statename:
            # print("No state for", countyname)
            continue



        countystate = "%s, %s" % (countyname, statename)
        try:
            ccolor = countyFpToLeDict[county["GEOID"]][1]
            # colAlpha = 1#float(countyFpToLeDict[county["GEOID"]][1])
            # colAlpha = 0
        except KeyError:
            print("No match for", countystate)
            continue
            # No exact match; try for a fuzzy match
            # colAlpha = 0
            # fuzzyname = fuzzy_find(countystate, county_colors.keys())
            # if fuzzyname:
            #     ccolor = county_colors[fuzzyname]
            #     county_colors[countystate] = ccolor
            # else:
            #     print("No match for", countystate)
            #     continue



        countyseg = BM.counties[i]
        # Move Hawaii and Alaska:
        # http://stackoverflow.com/questions/39742305/how-to-use-basemap-python-to-plot-us-with-50-states
        # Offset Alaska and Hawaii to the lower-left corner.
        if statename == 'Alaska':
        # Alaska is too big. Scale it down to 35% first, then transate it.
            countyseg = list(map(lambda xy: (0.25*xy[0] + 400000, 0.25*xy[1]-1000000), countyseg))
            # countyseg =countyseg
        elif statename == 'Hawaii':
            # countyseg = countyseg
            countyseg = list(map(lambda xy: (xy[0] + 6000000, xy[1]-1500000), countyseg))



        # countyseg = BM.counties[i]
        poly = plt.Polygon(countyseg, facecolor = ccolor)  # edgecolor="white"
        ax.add_patch(poly)
def showMap():
    """
    Description: Real simply. Shows the mape and chamges some title stuff.
    Input:
    Output:
    TODO:
    """
#     showMap()
    plt.title('US Counties', fontsize = 48)
    # Get rid of some of the extraneous whitespace matplotlib loves to use.
    plt.tight_layout(pad=0, w_pad=0, h_pad=0)
    plt.show()