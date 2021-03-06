import os 
import esda
import math
import folium
import leafmap
import numpy as np 
import pandas as pd
import seaborn as sbn
import libpysal as lps
import geopandas as gpd
import streamlit as st
import plotly.express as px
from matplotlib import colors
import matplotlib.pyplot as plt
from folium.plugins import HeatMap
from folium.plugins import MarkerCluster

def read_dati_bes(path):
    
    '''
    Through this function the excel file:
    * is read and imported;
    * is reduce by dropping unuseful columns     
    '''

    df = pd.read_excel(path)
    df.drop(columns = ['Unnamed: 0', 'DOMINIO', 'CODICE', 'SESSO', 'FONTE'], inplace = True)

    return df 


def provinces_BES(df, Anomalous_Regions, Sud_Sardinia, Macro_Areas, Italy, Regions):

    '''
    Due to the difference in annotation between the BES_Indicator data and the ones of ISTAT,
    there is the need to change some of the names of the provinces.
    Firstly, we should brake the dataset of BES Indicators in order to separate regions and macro areas,
    NB: We have to check that there are NO differences between regions'names
    Secondly, we have to omologate the names of the two dataset.
    NB: There are substantial differences mainly involving Sardinia, where ISTAT's Sud-Sardegnia contains BES'S Sud-Sardegna, Medio-Campidano, Carbonia-Iglesias, Ogliastra and Olbia-Tempio.
    '''

    #all_territories = df.TERRITORIO.unique().tolist()
    #return set(all_territories) - set(Regions) - set(Anomalous_Regions) - set(Sud_Sardinia) - set(Macro_Areas) - set(Italy)
    all_territories = df.TERRITORIO.unique().tolist()
    territories =  set(all_territories) - set(Regions) - set(Anomalous_Regions) - set(Sud_Sardinia) - set(Macro_Areas) - set(Italy)
    territories = list(territories)
    territories.sort()
    return territories

def regions_BES(Regions):
    '''
    Due to the difference in annotation between the BES_Indicator data and the ones of ISTAT,
    there is the need to change some of the names of the regions.
    '''

    new_regions = []
    for reg in Regions:
        if reg =="Valle d'Aosta":
            new_regions.append("Valle d'Aosta/Vall??e d'Aoste")
        elif reg == 'Trentino-Alto Adige':
            new_regions.append("Trentino-Alto Adige/S??dtirol")
        elif reg == 'Friuli Venezia Giulia':
            new_regions.append('Friuli-Venezia Giulia')
        else:
            new_regions.append(reg)
    
    return new_regions


def mod_col_geo(geodf):
    
    '''
    This function drops useless columns to the geodataframe and rename one of its column
    '''
    
    geodf.drop(columns=['COD_RIP','COD_REG'], inplace = True)
    geodf.rename(columns={'DEN_REG':'Reg'}, inplace = True) #CHANGE
    
    return geodf

def get_regions_names(geodf):  # Make sense to have it ? Check notebook

    '''
    This function returns a list of all the regions names according to the ISTAT standard
    NB there are some differences among the names used by ISTAT and the ones used for the BES indicators 
    '''

    return  geodf.Reg.unique().tolist()  # CHANGE 

def sort_reset_index_geo(geo_df):

    '''
    The geodaframe is sorted and its indeces are reset
    (This will be useful when the main dataframe will be converted into a geopandas dataframe)
    '''
    geo_df.sort_values(by = ['Prov'], inplace = True) # DEN_UTS
    geo_df.reset_index(inplace = True)

    return geo_df

def order_df(df, BES_Territories):

    '''
    The daframe is:
    * reduced in order to have coherence with the geodatafrmae which considers less provinces than the one of bes (actually, the geodatraframe respects the actual division of Italy into provinces)
    * sorted
    * its indeces are reset
    (This will be useful when the main dataframe will be converted into a geopandas dataframe)
    '''

    prov_df =  df[df['TERRITORIO'].isin(BES_Territories)]

    if len(prov_df) > 3:
        prov_df.sort_values(by=['TERRITORIO'],inplace = True)
        
    
    prov_df.set_index('TERRITORIO', inplace = True)

    return prov_df


def clean_prov_geo(geo_prov, provinces):
      
  geo_prov.drop(columns = ['COD_RIP','COD_REG',	'COD_PROV',	'COD_CM',	'COD_UTS',	'DEN_PROV',	'DEN_CM', 'TIPO_UTS'])
  geo_prov.sort_values(by = 'DEN_UTS', inplace = True)
  geo_prov.DEN_UTS = provinces
  geo_prov.set_index('DEN_UTS', inplace = True)
  
  return geo_prov

def order_df_regions(geodf, BES_Territories):
    '''
    This function modifies the geodaframe in order to have the same nomenclature for both the df and the geodf.
    This step  is needed in order to merge the two at the next step.
    '''
    
    geodf['Reg'] = BES_Territories #CHANGE
    geodf.sort_values(by= ['Reg'], inplace = True)
    geodf.set_index('Reg', inplace = True )
    
    return geodf

def aggregate_macros(geodf):
    
    '''
    The data regarding BES indicators refer to just three macroareas insted of 6 as in the ISTAT dataset. 

    Hence, there is the need to marge the areas in order have 3 main areas

    1.   North : Piemonte, Valle d'Aosta/Vall??e d'Aoste, Lombardia, Liguria, Trentino-Alto Adige/S??dtirol, Veneto, Friuli-Venezia Giulia, Emilia-Romagna
    2.   Centre: Toscana, Umbria, Marche, Lazio
    3.   South(& Islands): Abruzzo, Molise, Campania, Puglia, Basilicata, Calabria, Sicilia, Sardegna  
    '''

    Territorio = ['Nord', 'Nord', 'Centro', 'Mezzogiorno', 'Mezzogiorno']
    geodf['TERRITORIO'] = Territorio
    geodf = geodf.to_crs(epsg=4326).dissolve(by='TERRITORIO')
    geodf.drop(columns = ['DEN_RIP'])
    geodf.sort_values(by = ['COD_RIP'], inplace = True)

    return geodf

def from_df_to_gdf(df, geo_df):

    '''
    With this function we convert the dataframe containing the statistics we are interested in into a geodaframe. 
    This allows us to use all the functionalities of a geopandas dataframe such us doing plots.
    '''

    df['Shape_Leng'] = geo_df['Shape_Leng']
    df['Shape_Area'] = geo_df['Shape_Area']
    df['geometry'] = geo_df['geometry']
    df = gpd.GeoDataFrame(df)

    return df



def get_title_(file_name):

    '''
    This function provides the title to plots 
    '''

    title = file_name.strip('.xlsx')
    title = title.split('-')
    title = title[0].upper() + ' ' + title[1] + ' ' + title[2]

    return title 

def get_labels_(df):
    
    return df.iloc[0]['INDICATORE'] + '\n' + '(' + df.iloc[0]['UNITA_MISURA'] + ')'

def static_choroplet(df, variable, title_):

    '''
    With this function is it possible to create a static Choroplet map 
    Additional feature that can be added are ad-hoc colormaps, and a scheme for the division of the classes.
    '''
    
    miss_df = df[df[variable].isna()]
    df.dropna(subset = [variable], inplace = True)
    if len(df) > 3:
        df = look_for_anomalies2(df, variable)
    ax = df.plot(column=variable,
                                cmap="OrRd", edgecolor = "darkgrey", 
                                linewidth = 0.9,legend=True,figsize=(14,14),
                                scheme="equal_interval",
                                k=5)
    if len(miss_df) > 0 : 
        miss_df.plot(color = 'gray', ax = ax)
    ax.set_axis_off()
    ax.set_title(title_)
    plt.show()
    fig = ax.figure
    return fig   # modifica 24/04 


def dynamic_choroplet(df, title_, measure):
    
    '''
    With this function it is possible to create an interactive choropletmap
    '''

    fig = px.choropleth(df,
                   geojson=df.geometry,
                   locations=df.index, # maybe this should be changed for provinces 
                   color=measure,
                    title = title_)
    fig.update_geos(fitbounds="locations", visible=False)
    #fig.show()
    return fig



def folium_interactive_map(df, var, file_name, indicator):
    '''
    
    '''
    

    # Create the folium map 
    m10=folium.Map(location=[41.9027835,12.4963655],tiles='openstreetmap',zoom_start=5)

    df = look_for_anomalies2(df, var)
    df.to_crs(4326, inplace = True)

    
    folium.Choropleth(
    geo_data = df.to_json(),
    data = df,
    columns=['TERRITORIO', var],
    key_on='feature.properties.TERRITORIO',
    #key_on = 'feature.properties.id',
    fill_color='Oranges', 
    fill_opacity=0.6, 
    line_opacity=1,
    nan_fill_color='black',
    legend_name= get_title_(file_name),
    smooth_factor=0).add_to(m10)


    
    #add the feature
    folium.features.GeoJson(df,
                        name='Labels',
                        style_function=lambda x: {'color':'transparent','fillColor':'transparent','weight':0},
                        tooltip=folium.features.GeoJsonTooltip(fields=[var],
                                                                aliases = [indicator], #Substitute with the indicator of the df
                                                                labels=True,
                                                                sticky=False
                                                                            )
                       ).add_to(m10)
    

    return m10

def look_for_anomalies2(df,var):

    i = 0
    in_set = set()

    for el in df[var].values:
        if type(el) == str or math.isnan(el): 
            
            in_set.add(i)
    
        i += 1 

    df.reset_index(inplace=True)
    df.drop(list(in_set), inplace = True)   
    
    
    return df

 


def look_for_anomalies(df, var):
    
    df[var] = df[var].fillna(np.nan)

    i = 0 
    in_set = set()
    for el in df[var]:
    
        if type(el) == str:
            in_set.add(i)
            
    
        i += 1  

    if len(in_set) == 0 :
        return  df

    else: 
        df_2 = df.reset_index()
        for ind in in_set:
            #print(df_2.iloc[ind].TERRITORIO)
            #print(type(df_2.iloc[ind].TERRITORIO))
            df.drop(index = df_2.iloc[ind].TERRITORIO, inplace = True) 
    
    return df


def read_csv_shp(path):

    _full_df_ = gpd.GeoDataFrame(crs = 4326, columns = ['name', 'lat', 'lon'])
    lats = []
    lons = []
    names = []
    list_files = os.listdir(path)
    list_files_ = []


    for file_ in list_files:
        if file_.endswith('.csv'):
            list_files_.append(file_)
        elif file_.endswith('.shp'):
            list_files_.append(file_)


    for _file_ in list_files_:
        
        if _file_.endswith('.csv'):
            _df_ = pd.read_csv(path + '/' + _file_)
            if len(_df_) > 0:
                _df_['geometry'] = gpd.GeoSeries.from_wkt(_df_['geometry'])
                _geodf_ = gpd.GeoDataFrame(_df_, crs = 4326)
        
        elif _file_.endswith('.shp'):
            _geodf_ = gpd.read_file(path + '/' + _file_)
        lats.extend(_geodf_.geometry.centroid.to_crs(4326).y)
        lons.extend(_geodf_.geometry.centroid.to_crs(4326).x)

        if 'name' in _geodf_.columns:
            names.extend(_geodf_.name)
        else: 
            names.extend(['Missing'] * len(_geodf_.geometry.centroid.to_crs(4326).x))
    

    new_names = []
    for n in names: 
        if type(n) != str:
            new_names.append('Missing')
        else:
            new_names.append(n)
    

    _full_df_['lat'] = lats
    _full_df_['lon']= lons
    _full_df_['name'] = new_names

    return _full_df_

def getMarker(lat,lon, message,inconstyle):
    marker = folium.Marker(location=[lat,lon],
                         popup=message,
                         icon=inconstyle)
    return marker


def marker_plot(df, logo : str):
    m5=folium.Map(location=[41.9027835,12.4963655],tiles='openstreetmap',zoom_start=6)
    for index, row in df.iterrows():
        #icon=folium.Icon(color='purple',prefix='fa',icon='arrow-circle-down')
        icon=folium.features.CustomIcon(logo, icon_size=(34,34))
        marker = getMarker(row['lat'],row['lon'],row['name'], icon)

        marker.add_to(m5)
    
    return  m5

def marker_cluster(df, logo:str):

    m6=folium.Map(location=[41.9027835,12.4963655],tiles='openstreetmap',zoom_start=6)
    marker_cluster = MarkerCluster().add_to(m6)
    for index, row in df.iterrows():
        #icon=folium.Icon(color='purple',prefix='fa',icon='arrow-circle-down')
        icon=folium.features.CustomIcon(logo, icon_size=(34,34))
        message = '<strong>sezione:'+ str(row['name'])
        #tip = message + '<br/>' + row['via']
        marker = getMarker(row['lat'],row['lon'],message, icon)
        #add to marker cluster 
        marker.add_to(marker_cluster)
    
    
    return m6

def heatmap_plot(df):

    m7 = folium.Map(location=[41.9027835,12.4963655],tiles='openstreetmap',zoom_start=6)
    data = df[['lat','lon']]
    HeatMap(data.values).add_to(m7)


    return m7

def title_folium_map(map, title:str):
    title = ''
    title_html = '''
             <h3 align="center" style="font-size:16px"><b>{}</b></h3>
             '''.format(title)   

    map = folium.Map(location=[27.783889, -97.510556],
               zoom_start=12)

    map.get_root().html.add_child(folium.Element(title_html))

    return map 

def line_chart_plotly(Bes_df, to_hide_1, to_hide_2, to_hide_3, titolo = ''):
    df_plotly = pd.DataFrame(columns = ['TERRITORIO', 'MISURA', 'ANNO'])
    #if len(df_plotly) > 1:
    territorio = []
    misura = []
    _anno_ = []
    for i in range(len(Bes_df)):
        for j in range(4,20):
                
            if j < 10:
                anno = 'V_200' + str(j)
            else:
                anno = 'V_20' + str(j)
                    
            anno_ = int(anno[2:])
            territorio.append(Bes_df.iloc[i]['TERRITORIO'])
            misura.append(Bes_df.iloc[i][anno])
            _anno_.append(anno_)

        
        
    df_plotly['TERRITORIO'] = territorio
    df_plotly['ANNO'] = _anno_
    df_plotly['MISURA'] = misura


    to_hide_1.extend(to_hide_2)
    to_hide_1.extend(to_hide_3)
    fig = px.line(df_plotly, x = 'ANNO', y = 'MISURA', color = 'TERRITORIO', title = titolo)
    fig.for_each_trace(lambda trace: trace.update(visible="legendonly") 
            if trace.name in to_hide_1 else ())
        
        
    return fig
    
    #else:
        #return ('There are not enough data to produce a line chart')

def autocorrelation(path: str, df_prov: gpd.GeoDataFrame, Reg_df : gpd.GeoDataFrame, var : str):
    '''
    '''
    df_prov.to_crs(4326, inplace = True)
    Reg_df.to_crs(4326, inplace = True)
    df_prov2 = look_for_anomalies(df_prov, var)
    if len(df_prov2[var]) == 0:
        return 'It is not possible to compute autocorrelation'
    df_prov2 = df_prov2.reset_index()
    prova_df = gpd.sjoin(Reg_df, 
                          df_prov2, how='inner', predicate='contains')
    prova_df2 = prova_df.reset_index()
    median_val = prova_df2[var].groupby([prova_df2['Reg']]).mean()
    prova_df2 = prova_df.merge(median_val, on = 'Reg')
    df = prova_df2
    wq =  lps.weights.Queen.from_dataframe(df)
    wq.transform = 'r'
    var = var + '_y'
    y = df[var]
    yb = 1 * (y > y.median()) # convert back to binary
    wq =  lps.weights.Queen.from_dataframe(df)
    wq.transform = 'b'
    np.random.seed(12345)
    #jc = esda.join_counts.Join_Counts(yb, wq)
    mi = esda.moran.Moran(y, wq)
    fig_1 = plt.figure(figsize=(10, 4))
    sbn.kdeplot(mi.sim, shade=True)
    plt.vlines(mi.I, 0, 1, color='r')
    plt.vlines(mi.EI, 0,1)
    plt.xlabel("Moran's I")
    #sbn.kdeplot(jc.sim_bb, shade=True)
    #plt.vlines(jc.bb, 0, 0.075, color='r')
    #plt.vlines(jc.mean_bb, 0,0.075)
    #plt.xlabel('BB Counts')
    st.write('We obtain Moran\'s index = ', str(mi.p_sim))
    if mi.p_sim > 0.05:
        return 'There is no statistical correlation: Moran\'s Index = ' + str(mi.p_sim)
    else: 
        st.pyplot(fig_1)
    spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
    li = esda.moran.Moran_Local(y, wq)
    sig = 1 * (li.p_sim < 0.05)
    hotspot = 1 * (sig * li.q==1)
    coldspot = 3 * (sig * li.q==3)
    doughnut = 2 * (sig * li.q==2)
    diamond = 4 * (sig * li.q==4)
    spots = hotspot + coldspot + doughnut + diamond
    labels = [spot_labels[i] for i in spots]
    hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
    fig_2, ax = plt.subplots(1, figsize=(9, 9))
    df.assign(cl=labels).plot(column='cl', categorical=True, \
            k=2, cmap=hmap, linewidth=0.1, ax=ax, \
            edgecolor='white', legend=True)
    ax.set_axis_off()
    plt.title('Local Autocorrelation: Hot Spots, Cold Spots, and Spatial Outliers')
    

    return fig_2
    

def representative_point(df:gpd.GeoDataFrame):

    return df.geometry.representative_point().to_crs(4326)



def df_ranking(prova_mac, indicatori):
    ranking = pd.DataFrame(columns=indicatori)
    row = []
    for territorio in prova_mac:
        for ind in prova_mac[territorio]:
            row.append(sum(prova_mac[territorio][ind]))

        row.append(territorio)    
        series = pd.Series(row, index = ranking.columns)
        ranking = ranking.append(series, ignore_index= True)

        row = []
    ranking.set_index('TERRITORIO', inplace = True)
    return ranking