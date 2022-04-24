import esda
import pickle
import seaborn as sbn 
import streamlit as st
import geopandas as gpd 
import pandas as pd 
import matplotlib as plt
from functions2 import * 
from Testo_Indicatore import * 
from PIL import Image
from matplotlib import colors
from streamlit_folium import folium_static
import streamlit.components.v1 as components



# Path where are stored the shape files
Reg_Path = 'Limiti/Lim/Reg01012021/Reg01012021_WGS84.shp'
Prov_Path = 'Limiti/Lim/ProvCM01012021/ProvCM01012021_WGS84.shp'
Macro_Path = 'Limiti/Lim/RipGeo01012021/RipGeo01012021_WGS84.shp'
# Read the shape files and create the geodataframes
# One for each territorial division (Macroareas, Regions and provinces)
Reg_df = gpd.read_file(Reg_Path)
Prov_df = gpd.read_file(Prov_Path)
Macro_df = gpd.read_file(Macro_Path)

# Anomalous Regions names
Anomalous_Regions = ['Trentino-Alto Adige/Südtirol','Friuli-Venezia Giulia',"Valle d'Aosta/Vallée d'Aoste"]
#Sud_Sardinia_Agglomeration
Sud_Sardinia = ['Ogliastra','Olbia-Tempio','Medio Campidano','Carbonia-Iglesias']
# Macro_Areas 
Macro_Areas = ['Centro', 'Mezzogiorno', 'Nord']
# Italy 
Italy = ['Italia']
# Different_Names
Different_Names_BES = ['Bolzano/Bozen', 'Forlì-Cesena', 'Massa-Carrara', 'Reggio Calabria']
Deffirent_Names_ISTAT = ['Bolzano', "Forli'-Cesena", 'Massa Carrara', 'Reggio di Calabria']

# Read the BES_Statistics Dataframe
path_ = 'Nuovi_Dati2'
List_Statistics = os.listdir(path = path_)
# Read a random file just to compute the provinces afterward
df_ = read_dati_bes(path_ + '/' + List_Statistics[0])
# Get the Istat regions 
Regions = Reg_df.DEN_REG.to_list()
# Get  BES Regions
Bes_Regions = regions_BES(Regions)
# Extract the set of all Bes provinces
provinces = provinces_BES(df_, Anomalous_Regions, Sud_Sardinia, Macro_Areas, Italy, Regions)


# DASHBOARD 

st.title('BES Indicators in Italy')
st.write(
    '''
    The [__Bes project__](https://www4.istat.it/en/well-being-and-sustainability/well-being-measures/bes-report) 
    was launched in 2010 to measure Equitable and Sustainable Well-being,
    and with the aim of evaluating the progress of society not only from an economic,
    but also from a social and environmental point of view. 
    \\
    To this end, the traditional economic indicators, GDP first of all, have been integrated with measures of the quality of people’s life and of the environment.
    \\
    \\
    Since 2016, well-being indicators and welfare analyzes have been presented with indicators for monitoring the objectives of the 2030 Agenda
    for Sustainable Development,
    the so-called [Sustainable Development Goals (SDGs)](https://sdgs.un.org/goals) of the United Nations.
    They were chosen by the global community through a political agreement between the different actors, to represent their values, priorities and objectives.
    The United Nations Statistical Commission (UNSC) has set up a shared set of statistical information to monitor the progress of individual countries towards the SDGs,
    including over two hundred indicators.
    The two sets of indicators are only partially overlapping, but certainly complementary.
    \\
    \\
    Bes' indicators cover [12 domains relevant for the measuramente of the well-being](https://www.istat.it/it/files/2018/04/12-domains-scientific-commission.pdf) 
    and they are the following: 

    1)  Health 
    2)  Education & Training
    3)  Work & Life Balance
    4)  Economic well-being
    5)  Social Relationships
    6)  Politics & Istitutions
    7)  Security 
    8)  Subjective well-being
    9)  Landscape & Cultural heritage
    10) Environment
    11) Innovation, Research & Creativity
    12) Quality of services
    '''
)

selectbox_ind = st.sidebar.selectbox(
    "Which indicator do you what to know about",
    ("Health", "Education & Training", "Work & Life Balance", "Economic well-being", "Social Relationship", 
    "Politics & Istitutions", "Security", "Subjective well-being", "Landscape & Cultural heritage", "Environment", "Innovation, Research & Creativity", "Quality of services")
)

selectbox_area = st.sidebar.selectbox(
    'Level of analysis', 
    ('Macros', 'Region', 'Provinces')
)

selectbox_y = '2018'
selectbox_type = st.sidebar.selectbox('Which type of plot do you want to visualize?', 
('Static', 'Dynamic'))

diz_indicatori = {
    'Health': 'Salute', 
    'Education & Training' : 'Istruzione e formazione',
    "Work & Life Balance" : 'Lavoro e conciliazione dei tempi di vita',
    "Economic well-being": 'Benessere economico',
    "Social Relationship": 'Relazioni Sociali',
    "Politics & Istitutions": 'Politica e istituzioni',
    "Security": 'Sicurezza',
    "Subjective well-being" : None,
    "Landscape & Cultural heritage" : 'Paesaggio e patrimonio culturale', 
    "Environment": 'Ambiente', 
    "Innovation, Research & Creativity" : 'Innovazione',
    "Quality of services": 'Qualità dei servizi'
}

if selectbox_ind == "Health" :
    st.subheader('1 Health')
    st.write(health)
elif selectbox_ind == 'Education & Training':
    st.subheader('2 Education & Training')
    st.write(education)
elif selectbox_ind == "Work & Life Balance":
    st.subheader('3 Work & Life Balance')    
    st.write(work)
elif selectbox_ind == "Economic well-being":
    st.subheader('4 Economic well-being')
    st.write(economic)
elif selectbox_ind == "Social Relationship":
    st.subheader('5 Social Relationships')
    st.write(social)
elif selectbox_ind == "Politics & Istitutions":
    st.subheader('6 Politics & Istitutions')
    st.write(politics)
elif selectbox_ind == "Security":
    st.subheader('7 Security')
    st.write(security)
elif selectbox_ind == "Landscape & Cultural heritage":
    st.subheader('9 Landscape & Cultural heritage')
    st.write(landscape)
elif selectbox_ind ==  "Innovation, Research & Creativity":
    st.subheader('11 Innovation, Research & Creativity ')
    st.write(innovation)
elif selectbox_ind == "Environment":
    st.subheader('10 Environment')
    st.write(environment)
elif selectbox_ind == "Quality of services":
    st.subheader('12 Quality of services ')
    st.write(services)
else:
    st.subheader('8 Subjective well-being')
    st.write(subj_wll)


original_path = 'Mappe_html/'
path_ = 'Mappe_html/'  + selectbox_ind + '/V_' + selectbox_y + '/' + selectbox_area 
#st.write(path_)


if selectbox_ind == 'Subjective well-being':
    file = 'Mappe_html/' + selectbox_ind + '/Laisure.txt' 
    file = open(file,'r')
    components.html(file.read(), width = 750, height=900)

elif len(os.listdir(path_)) == 0:
    st.write('There are no data available for {indicatore} in the chosen year ({anno})'.format(indicatore = selectbox_ind, anno = selectbox_y))

else:
    select_list = set()
    for el in os.listdir(path_):
        el = el.replace('-choro-.jpg', '').replace('-choro.jpg', '').replace('-folium.txt', '')
        select_list.add(el)
    
    select_list = list(select_list)
    
    multi = st.multiselect('Please, select the variables of interest:',
    select_list)
    _path_ = 'Nuovi_Dati2/'

    for file in multi:
        nome_file = file 
        titolo = file.split('-')
        titolo = titolo[1] + '-' + titolo[2] + '-' + titolo[3] 
        
        df = read_dati_bes(_path_ + '/' + nome_file + '.xlsx' )
        labels = get_labels_(df)


        if selectbox_type == 'Dynamic':
            st.warning('Due to the costly computations neeeded to create the interactive maps it is HIGLHY RECCOMENDED to choose no more than a couple of indicator per time.')
            st.header(titolo)
            if selectbox_area == 'Macro':
                geodf_Macro = aggregate_macros(Macro_df)
                df_macro = order_df(df, Macro_Areas)
                df = from_df_to_gdf(df_macro, geodf_Macro)
            elif selectbox_area == 'Region':
                df_reg = order_df(df, Bes_Regions)
                Reg_geodf = mod_col_geo(Reg_df)
                geodf_reg = order_df_regions(Reg_geodf, Bes_Regions) 
                df = from_df_to_gdf(df_reg, geodf_reg)
            else:
                geodf_prov = clean_prov_geo(Prov_df, provinces)
                df_prov = order_df(df, provinces)
                df = from_df_to_gdf(df_prov, geodf_prov)
            

            folium_static(folium_interactive_map(df, 'V_' + selectbox_y, nome_file, labels))





        elif selectbox_type == 'Static':
            try: 
                file = path_ + '/' + nome_file + '-choro-.jpg'
                file = Image.open(file)
            except:
                file = path_ + '/' + nome_file + '-choro.jpg'
                file = Image.open(file)


            st.image(file, caption='Source: ISTAT')
        line_file = nome_file + '-line-.txt'
        line_file = open(original_path + '/'+ selectbox_ind + '/' + line_file, 'r')
        components.html(line_file.read(),  width=900, height=400)
        st.caption('Source: ISTAT')


        st.warning('Computing the spatial autocorrelation requires many computations so it can take a couple of minutes to show the results')
        if st.button('Do you want to know more about ' + nome_file + '\'s spatial autocorrelation?'):
            st.subheader('Spatial Autocorrelation')
            st.write('Geo-referenced data are subjected to Tobler’s first law of geography: “everything is related to everything else, but near things are more related than distant things” (Tobler 1970).')
            st.write('''
            The term spatial autocorrelation refers to the presence of systematic spatial variation in a mapped variable.
            Where adjacent observations have similar data values the map shows positive spatial autocorrelation.
            Where adjacent observations tend to have very contrasting values then the map shows negative spatial autocorrelation. 
            There are several statistical techniques for detecting its presence. The presence of spatial autocorrelation is important: 
            1) because it is usually taken as indicating that there is something of interest in the distribution of map values that calls for further investigation in order to understand the reasons behind the observed spatial variation, 
            2) because the presence of spatial autocorrelation implies information redundancy and has important implications for the methodology of spatial data analysis. 
            
            Spatial autocorrelation may arise from any one of the following situations:
            * the difference between the (large) scale of variation of a phenomenon and the (small) scale of the spatial framework used to capture or represent that variation; 
            * measurement error; 
            * spatial diffusion, spillover, interaction, and dispersal processes;
            * inheritance by one variable through causal association with another;
            * model mis-specification.

            (R.P. Haining, 2001)
            ''')
            st.write(' The presence or otherwise of spatial autocorrelation impacts directly on spatial sampling, map interpolation, exploratory spatial data analysis, statistical inference, and statistical modeling using spatial data.')

            # Reading the geodaframe

            Reg_df = gpd.read_file(Reg_Path)
            Prov_df = gpd.read_file(Prov_Path)
            # Read the BES_Statistics Dataframe
            
            ## PREPARE REG GEO DF ##
            Reg_df = mod_col_geo(Reg_df)
            Reg_df = order_df_regions(Reg_df, Bes_Regions)

            #df = read_dati_bes('Ambiente-Disponibilità di verde urbano-Totale-m2 per abitante.xlsx')
            df = read_dati_bes('Nuovi_Dati2/' + file +'.xlsx')
            
            ## PREPARE PROV GEO DF ## 
            Prov_df = clean_prov_geo(Prov_df, provinces)
            # 'PROVINCES' #
            # Create the provinces df
            df_prov = order_df(df, provinces)
            # Obtain the full geodataframe of provinces 
            df_prov = from_df_to_gdf(df_prov, Prov_df)
            #Modify the crs in order to properly plot the geometries. 
            df_prov.to_crs(4326, inplace = True)
            Reg_df.to_crs(4326, inplace = True)
            df_prov2 = look_for_anomalies2(df_prov, 'V_' + selectbox_y)
            df_prov2 = df_prov2.reset_index()
            #joining the two dataframes.
            prova_df = gpd.sjoin(Reg_df, 
                            df_prov2, how='inner', predicate='contains')
            prova_df2 = prova_df.reset_index()
            # Compute the average value by grouping provinces by their region (in 2017)
            median_val = prova_df2['V_'+ selectbox_y].groupby([prova_df2['Reg']]).mean()
            #create a new aggregated dataframe
            prova_df2 = prova_df.merge(median_val, on = 'Reg')
            #st.dataframe(pd.DataFrame(prova_df2.drop(columns = ['geometry'])))
            df = prova_df2
            y = df['V_'+ selectbox_y + '_y']
            yb = y > y.median()
            yb = 1 * (y > y.median()) # convert back to binary
            wq =  lps.weights.Queen.from_dataframe(df)
            wq.transform = 'b'
            np.random.seed(12345)   
            jc = esda.join_counts.Join_Counts(yb, wq)
            mi = esda.moran.Moran(y, wq)
            fig = plt.figure(figsize=(10, 4))
            sbn.kdeplot(mi.sim, shade=True)
            plt.vlines(mi.I, 0, 1, color='r')
            plt.vlines(mi.EI, 0,1)
            plt.xlabel("Moran's I")
            st.pyplot(fig)
            st.write('Moran\'s I is a test for global autocorrelation for a continuous attribute:')
            if mi.p_sim <= 0.01:
                st.write('Since this is below conventional significance levels, we would reject the null of complete spatial randomness in favor of spatial autocorrelation.')
                li = esda.moran.Moran_Local(y, wq)
                sig = 1 * (li.p_sim < 0.05)
                hotspot = 1 * (sig * li.q==1)
                coldspot = 3 * (sig * li.q==3)
                doughnut = 2 * (sig * li.q==2)
                diamond = 4 * (sig * li.q==4)
                spots = hotspot + coldspot + doughnut + diamond
                spot_labels = [ '0 ns', '1 hot spot', '2 doughnut', '3 cold spot', '4 diamond']
                labels = [spot_labels[i] for i in spots]
                hmap = colors.ListedColormap([ 'lightgrey', 'red', 'lightblue', 'blue', 'pink'])
                f, ax = plt.subplots(1, figsize=(9, 9))
                df.assign(cl=labels).plot(column='cl', categorical=True, \
                        k=2, cmap=hmap, linewidth=0.1, ax=ax, \
                        edgecolor='white', legend=True)
                ax.set_axis_off()
                st.pyplot(f)
                
            else:
                st.write('Moran\'s index is higher than the conventional significance level. So we cannot reject the null hypothesis. Thus, there is no spatial autocorrelation.')




    st.header('Best Areas')
    st.write('Can you guess which are the best areas relatively to ', selectbox_ind.lower(), '?')
    
    if st.button('Show the best three'):
        if selectbox_area == 'Macros':
            with open('Dictionaries\diz_mac.pkl', 'rb') as f:
                diz = pickle.load(f)
                Geo_df = aggregate_macros(Macro_df)
        elif selectbox_area == 'Region':
            with open('Dictionaries\diz_reg.pkl', 'rb') as f:
                diz = pickle.load(f)
                Reg_df = mod_col_geo(Reg_df)
                Geo_df = order_df_regions(Reg_df, Bes_Regions)
        else:
            with open('Dictionaries\diz_prov.pkl', 'rb') as f:
                diz = pickle.load(f)
                Geo_df = clean_prov_geo(Prov_df, provinces)

        indicatori = os.listdir('Dati_Streamlite')
        indicatori.append('TERRITORIO')
        indicatori.remove('Subjective well-being')

        ranking = df_ranking(diz, indicatori)
        ranking = from_df_to_gdf(ranking, Geo_df)
        ranking.reset_index(inplace= True)
        ranking.sort_values(by = selectbox_ind, inplace = True)
        ranking2 = ranking.iloc[:3]
        ranking2.to_crs(4326, inplace = True)
        m7=folium.Map(location=[41.9027835,12.4963655],tiles='openstreetmap',zoom_start=6)
        j = 1 
        for index, row in ranking2.iterrows():
            icon=folium.features.CustomIcon('Medaglie/' + str(j) + '.png' ,icon_size=(40,40))
            if row['TERRITORIO'] == 'Mezzogiorno':
                marker = getMarker(40.760791, 15.950441, row['TERRITORIO'], icon)
            else:
                marker = getMarker(row['geometry'].centroid.y,row['geometry'].centroid.x, row['TERRITORIO'], icon)
            marker.add_to(m7)
            j += 1

        folium_static(m7)
