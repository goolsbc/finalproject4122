import streamlit as st
import streamlit.components.v1 as components
import pandas as pd
import numpy as np
import plotly.express as px

@st.cache
def load_data():
    loc = "/Users/carolinegoolsby/Documents/UNCC/Spring_2021/ITCS_4122/final_project/app/newdata2.csv"
    airdata = pd.read_csv(loc)
    return airdata

st.set_page_config(page_title = 'Charlotte Flights', page_icon = ':airplane', layout='wide')
airdata = load_data()
st.title("Charlotte Douglas International Airport Flight Data")
st.subheader("source: flights to Charlotte's top 21 destinations-- February 2016 through February 2021")

airlocdf = airdata[["latdegform", "longdegform", 'Code', 'State', 'City']].drop_duplicates()
airlocdf['newlongdegform'] = airlocdf['longdegform']*-1
airlocdf.drop('longdegform', axis=1, inplace=True)
airlocdf.set_index('Code',drop=False, inplace=True)
airlocdf.sort_index(inplace=True)
airlocdf.drop(['LGA'], inplace=True)
cltloc = {'latdegform':35.2144, 'Code':'CLT', 'State':'NC','City': 'Charlotte (outgoing)', 'newlongdegform': -80.9473}
airlocdf = airlocdf.append(cltloc, ignore_index = True)
airlocdf.set_index('City',inplace=True)
avgfpd = {14.070607553366173: 'ATL',
 5.579091406677613: 'BNA',
 10.073344280240832: 'BOS',
 9.400109469074986: 'BWI',
 7.216201423097975: 'DCA',
 6.444444444444445: 'DEN',
 9.843459222769567: 'DFW',
 6.642583470169677: 'DTW',
 7.995073891625616: 'EWR',
 6.848932676518883: 'FLL',
 5.633825944170772: 'IAH',
 15.596059113300493: 'JFK',
 5.8686371100164205: 'LAX',
 9.641488779419815: 'MCO',
 7.444444444444445: 'MIA',
 5.851669403393541: 'MSP',
 9.40120415982485: 'ORD',
 8.983032293377121: 'PHL',
 7.699507389162561: 'PHX',
 7.22495894909688: 'RDU',
 8.275314723590586: 'TPA',
 175.7339901478: 'CLT'}
airlocdf.at['NYC', 'Code']= 'JFK/LGA'
airlocdf['Average_Flights_per_Day'] = avgfpd
newairlocdf=airlocdf[['Code', 'State', 'Average_Flights_per_Day']]


# with st.beta_expander("Airports Map"):
if st.checkbox("Display Airport List", key = '1'):
    c1, c2 = st.beta_columns([1.5,1])
    with c1:
        components.html('''
     <!DOCTYPE html>
    <html lang='en'>
      <head>
        <meta charset='utf-8' />
        <title>Flights from Charlotte</title>
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v2.2.0/mapbox-gl.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v2.2.0/mapbox-gl.css' rel='stylesheet' />
        <style>
          body {
            margin: 0;
            padding: 0;
          }

          #map {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 100%;
          }
        </style>
      </head>
      <body>
        <div id='map'></div>
        <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoiY2Rnb29sc2J5IiwiYSI6ImNrbzNsZWM1ZTA1ZGQyb3Bid2plY3oxNmUifQ.u71P89kcN0BX8VPBSMoF-A'; // replace this with your access token
        var map = new mapboxgl.Map({
          container: 'map',
          style: 'mapbox://styles/cdgoolsby/cko3neq2w0f3b18pd6wibl7vr', // replace this with your style URL
          center: [-97.5795, 39.123],
          zoom: 3.2
        });

          map.on('click', function (e) {
            var features = map.queryRenderedFeatures(e.point, {
              layers: ['clt-airports2'] // replace this with the name of the layer
            });

            if (!features.length) {
              return;
            }

            var feature = features[0];

            var popup = new mapboxgl.Popup({ offset: [0, -15] })
              .setLngLat(feature.geometry.coordinates)
              .setHTML(
                '<h3>' + 
                feature.properties.Airport_Name +
                  '</h3><p>' +
                  feature.properties.Code +
                  '</p>' + feature.properties.Average_FPD_Desc
              )
              .setLngLat(feature.geometry.coordinates)
              .addTo(map);
          });

        </script>
      </body>
    </html>> '''
    , height=500                
    )

    with c2:
        st.dataframe(newairlocdf, height = 500)

else:
    components.html('''
     <!DOCTYPE html>
    <html lang='en'>
      <head>
        <meta charset='utf-8' />
        <title>Flights from Charlotte</title>
        <meta name='viewport' content='width=device-width, initial-scale=1' />
        <script src='https://api.tiles.mapbox.com/mapbox-gl-js/v2.2.0/mapbox-gl.js'></script>
        <link href='https://api.tiles.mapbox.com/mapbox-gl-js/v2.2.0/mapbox-gl.css' rel='stylesheet' />
        <style>
          body {
            margin: 0;
            padding: 0;
          }

          #map {
            position: absolute;
            top: 0;
            bottom: 0;
            width: 100%;
          }
        </style>
      </head>
      <body>
        <div id='map'></div>
        <script>
        mapboxgl.accessToken = 'pk.eyJ1IjoiY2Rnb29sc2J5IiwiYSI6ImNrbzNsZWM1ZTA1ZGQyb3Bid2plY3oxNmUifQ.u71P89kcN0BX8VPBSMoF-A'; // replace this with your access token
        var map = new mapboxgl.Map({
          container: 'map',
          style: 'mapbox://styles/cdgoolsby/cko3neq2w0f3b18pd6wibl7vr', // replace this with your style URL
          center: [-95.5795, 37.8283],
          zoom: 3.85
        });

          map.on('click', function (e) {
            var features = map.queryRenderedFeatures(e.point, {
              layers: ['clt-airports2'] // replace this with the name of the layer
            });

            if (!features.length) {
              return;
            }

            var feature = features[0];

            var popup = new mapboxgl.Popup({ offset: [0, -15] })
              .setLngLat(feature.geometry.coordinates)
              .setHTML(
                '<h3>' + 
                feature.properties.Airport_Name +
                  '</h3><p>' +
                  feature.properties.Code +
                  '</p>' + feature.properties.Average_FPD_Desc
              )
              .setLngLat(feature.geometry.coordinates)
              .addTo(map);
          });

        </script>
      </body>
    </html>> '''
    , height=600                
    )


with st.beta_expander("Explore Delay Data"):
    st.subheader("Delay = Flight leaves > 45 minutes after scheduled departure time")
    st.write("Percent = % of flights within the specified timeframe that were significantly delayed between 2/1/2016 and 2/28/2021")
    dfas = airdata.groupby('City')
    Cities = sorted(airdata["City"].unique())
    chooseairports = st.selectbox("Choose Destination", Cities, key ='27')
    airport_df = dfas.get_group(chooseairports)
    carriers = airport_df["OP_UNIQUE_CARRIER"].unique()
    choosecarrier1 = st.multiselect("Choose Carrier (AA = American Airlines, B6 = JetBlue Airways, DL = Delta, F9 = Frontier Airlines, NK = Spirit Airlines, UA = United Airlines, WN = Southwest Airlines)", carriers, key = '12')
    option1 = st.selectbox("Comparison Options", ('Month', 'Day of Week', 'Time of Day'), key = '11')
    carrier_df = airport_df[airport_df["OP_UNIQUE_CARRIER"].isin(choosecarrier1)]
    if option1 == 'Month': 
        monthinfo = carrier_df.groupby(["OP_UNIQUE_CARRIER", "MONTH"]).agg({'FL_DATE' : 'count'})
        monthinfo['Delayed'] = carrier_df.groupby(["OP_UNIQUE_CARRIER", "MONTH"])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
        monthinfo['Percent'] = (monthinfo['Delayed']/monthinfo['FL_DATE'])*100
        monthinfo.rename(columns={"FL_DATE": 'Total_Flights'}, inplace = True)
        month_source = monthinfo.reset_index()
        

        monthfig = px.bar(month_source, x = 'MONTH', y = 'Percent', color = "OP_UNIQUE_CARRIER", barmode = "group", labels = {'Percent': '% Delayed'}, width = 1000, height = 500, range_y = (0,25))

        st.write(monthfig)
        st.write(monthinfo.sort_index(level = "MONTH"))

    elif option1 == 'Day of Week':
            monthmin1, monthmax1 = st.slider("Choose Month(s)", 1, 12, (4,6), key ='41')
            month_df = carrier_df[((carrier_df["MONTH"]>=monthmin1) & (carrier_df["MONTH"]<=monthmax1))]
            dayinfo = month_df.groupby(["OP_UNIQUE_CARRIER", "DAY_OF_WEEK"]).agg({'FL_DATE' : 'count'})
            dayinfo['Delayed'] = month_df.groupby(["OP_UNIQUE_CARRIER", "DAY_OF_WEEK"])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
            dayinfo['Percent'] = (dayinfo['Delayed']/dayinfo['FL_DATE'])*100
            dayinfo.rename(columns={"FL_DATE": 'Total_Flights'}, inplace = True)
            day_source = dayinfo.reset_index()
            

            dayfig = px.bar(day_source, x = 'DAY_OF_WEEK', y = 'Percent', color = "OP_UNIQUE_CARRIER", barmode = "group", labels = {'Percent': '% Delayed'}, width = 875, height = 500,  range_y = (0,25))
            

            st.write(dayfig)
            st.write(dayinfo.sort_index(level = "DAY_OF_WEEK"))

    elif option1 == 'Time of Day':
        cut_labels = ['12:01am to 6am', '6:01am to 9am', '9:01am to noon', '12:01pm to 3pm', '3:01pm to 6pm', '6:01pm to 9pm', '9:01pm to midnight']
        cut_bins = [0,5,8,11,14,17,20,24]
        monthmin2, monthmax2 = st.slider("Choose Month(s)", 1, 12, (4,6), key ='47')
        month_df = carrier_df[((carrier_df["MONTH"]>=monthmin2) & (carrier_df["MONTH"]<=monthmax2))]
        daymin, daymax = st.slider("Choose Day(s) (1 = Monday)", 1, 7, (2,4), key ='48')
        day_df = month_df[((month_df["DAY_OF_WEEK"]>=daymin) & (month_df["DAY_OF_WEEK"]<=daymax))]
        bins = pd.cut(day_df['CRS_HOUR'], bins = cut_bins, labels = cut_labels)
        timeinfo = day_df.groupby(['OP_UNIQUE_CARRIER', bins]).agg({'FL_DATE': 'count'})
        timeinfo['Delayed'] = day_df.groupby(['OP_UNIQUE_CARRIER', bins])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
        timeinfo['Percent'] = (timeinfo['Delayed']/timeinfo['FL_DATE'])*100
        timeinfo.rename(columns={"FL_DATE": 'Total_Flights'}, inplace = True)
        timeinfo = timeinfo.reset_index()
        timeinfo['CRS_HOUR'] = timeinfo['CRS_HOUR'].astype(str)
        timeinfo.rename(columns={"CRS_HOUR": 'Departure_Time'}, inplace = True)
        timefig = px.bar(timeinfo, x = 'Departure_Time', y = 'Percent', color = "OP_UNIQUE_CARRIER", barmode = "group", labels = {'Percent': '% Delayed'}, width = 900, height = 500, range_y = (0,25))
        s = timeinfo['Departure_Time'].replace({'12:01am to 6am':0, '6:01am to 9am':1, '9:01am to noon':2, '12:01pm to 3pm':3, '3:01pm to 6pm':4, '6:01pm to 9pm':5, '9:01pm to midnight':6})
        timeinfo['Level'] = s
        
        st.write(timefig)
        st.write(timeinfo.set_index(s).sort_index())

        
        
        

with st.beta_expander("Flight Optimization"):
    st.subheader("Delay = Flight leaves > 45 minutes after scheduled departure time")
    st.write("Percent = % of flights within the specified timeframe that were significantly delayed between 2/1/2016 and 2/28/2021")
    dfas1 = airdata.groupby('City')
    chooseairports1 = st.selectbox("Choose Airport", sorted(airdata["City"].unique()), key ='21')
    airport_df1 = dfas1.get_group(chooseairports1)
    monthmin1, monthmax1 = st.slider("Choose Month(s)", 1, 12, (4,6), key ='32')
    daymin1, daymax1 = st.slider("Choose Day(s) of Week (1 = Monday)", 1, 7, (2,3), key ='33')
    st.write("Carrier Codes (AA = American Airlines  |  B6 = JetBlue Airways  |  DL = Delta  |  F9 = Frontier Airlines  |  NK = Spirit Airlines  |  UA = United Airlines  |  WN = Southwest Airlines)")
    col1, col2 = st.beta_columns(2)
    carrierarray = airport_df1["OP_UNIQUE_CARRIER"].unique()
    choosecarrier1 = col1.selectbox("Choose Carrier", np.append(carrierarray, ["Select All"]), key = '20')
    choosecarrier2 = col2.selectbox("Choose Carrier", carrierarray, key = '20')
    if choosecarrier1 == "Select All":
        carrier_df1 = airport_df1
        carrier_df2 = airport_df1[airport_df1["OP_UNIQUE_CARRIER"] == choosecarrier2]
        monthdata1 = carrier_df1[((carrier_df1["MONTH"]>=monthmin1) & (carrier_df1["MONTH"]<=monthmax1))]
        monthdata1 = monthdata1[((carrier_df1["DAY_OF_WEEK"] >= daymin1) & (carrier_df1["DAY_OF_WEEK"] <= daymax1))]

        heatmapdata1 = monthdata1.groupby(['MONTH', 'DAY_OF_WEEK']).agg({'SIG_DELAY_IND': 'count'})
        heatmapdata1['Delayed'] = monthdata1.groupby(['MONTH', 'DAY_OF_WEEK'])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
        heatmapdata1['Percentage'] = (heatmapdata1['Delayed'] / heatmapdata1['SIG_DELAY_IND'])*100
        heatmapdata1.rename(columns={"SIG_DELAY_IND": 'Total_Flights'}, inplace = True)
        heatmap1 = px.density_heatmap(heatmapdata1.reset_index(), x = "MONTH", y = 'DAY_OF_WEEK', z = "Percentage", nbinsx = (1 + monthmax1 - monthmin1), nbinsy = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0, 25))
        col1.write(heatmapdata1)
        col1.write(heatmap1)
        

        if col1.checkbox("Show Time Data"):

            cut_labels = ['12:01am to 6am', '6:01am to 9am', '9:01am to noon', '12:01pm to 3pm', '3:01pm to 6pm', '6:01pm to 9pm', '9:01pm to midnight']
            cut_bins = [0,5,8,11,14,17,20,24]
            bins = pd.cut(monthdata1['CRS_HOUR'], bins = cut_bins, labels = cut_labels)
            timeinfo1 = monthdata1.groupby(['DAY_OF_WEEK', bins]).agg({'FL_DATE': 'count'})
            timeinfo1['Delayed'] = monthdata1.groupby(['DAY_OF_WEEK', bins])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
            timeinfo1['Percent'] = (timeinfo1['Delayed']/timeinfo1['FL_DATE'])*100
            timeinfo1.rename(columns={"FL_DATE": 'Total_Flights'}, inplace = True)
            timeinfo1 = timeinfo1.reset_index()
            timeinfo1['CRS_HOUR'] = timeinfo1['CRS_HOUR'].astype(str)
            timeinfo1.rename(columns={"CRS_HOUR": 'Departure_Time'}, inplace = True)
            heatmap21 = px.density_heatmap(timeinfo1, x = "DAY_OF_WEEK", y = 'Departure_Time', z = "Percent", nbinsx = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0, 25))
           
            col1.write(heatmap21)
            col1.write(timeinfo1)
        
        monthdata2 = carrier_df2[((carrier_df2["MONTH"]>=monthmin1) & (carrier_df2["MONTH"]<=monthmax1))]
        monthdata2 = monthdata2[((carrier_df2["DAY_OF_WEEK"] >= daymin1) & (carrier_df2["DAY_OF_WEEK"] <= daymax1))]

        heatmapdata2 = monthdata2.groupby(['MONTH', 'DAY_OF_WEEK']).agg({'SIG_DELAY_IND': 'count'})
        heatmapdata2['Delayed'] = monthdata2.groupby(['MONTH', 'DAY_OF_WEEK'])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
        heatmapdata2['Percentage'] = (heatmapdata2['Delayed'] / heatmapdata2['SIG_DELAY_IND'])*100
        heatmapdata2.rename(columns={"SIG_DELAY_IND": 'Total_Flights'}, inplace = True)
        heatmap3 = px.density_heatmap(heatmapdata2.reset_index(), x = "MONTH", y = 'DAY_OF_WEEK', z = "Percentage", nbinsx = (1 + monthmax1 - monthmin1), nbinsy = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0,25))
        col2.write(heatmapdata2)
        col2.write(heatmap3)
        

        if col2.checkbox("Show Time Data", key = '36'):

            cut_labels = ['12:01am to 6am', '6:01am to 9am', '9:01am to noon', '12:01pm to 3pm', '3:01pm to 6pm', '6:01pm to 9pm', '9:01pm to midnight']
            cut_bins = [0,5,8,11,14,17,20,24]
            bins = pd.cut(monthdata2['CRS_HOUR'], bins = cut_bins, labels = cut_labels)
            timeinfo2 = monthdata2.groupby(['DAY_OF_WEEK', bins]).agg({'FL_DATE': 'count'})
            timeinfo2['Delayed'] = monthdata2.groupby(['DAY_OF_WEEK', bins])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
            timeinfo2['Percent'] = (timeinfo2['Delayed']/timeinfo2['FL_DATE'])*100
            timeinfo2.rename(columns={"FL_DATE": 'Total_Flights'}, inplace = True)
            timeinfo2 = timeinfo2.reset_index()
            timeinfo2['CRS_HOUR'] = timeinfo2['CRS_HOUR'].astype(str)
            timeinfo2.rename(columns={"CRS_HOUR": 'Departure_Time'}, inplace = True)
            heatmap22 = px.density_heatmap(timeinfo2, x = "DAY_OF_WEEK", y = 'Departure_Time', z = "Percent", nbinsx = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0, 25))
            
            col2.write(heatmap22)
            col2.write(timeinfo2)
    
    else:
        
        carrier_df1 = airport_df1[airport_df1["OP_UNIQUE_CARRIER"] == choosecarrier1]
        carrier_df2 = airport_df1[airport_df1["OP_UNIQUE_CARRIER"] == choosecarrier2]

        monthdata1 = carrier_df1[((carrier_df1["MONTH"]>=monthmin1) & (carrier_df1["MONTH"]<=monthmax1))]
        monthdata1 = monthdata1[((carrier_df1["DAY_OF_WEEK"] >= daymin1) & (carrier_df1["DAY_OF_WEEK"] <= daymax1))]

        heatmapdata1 = monthdata1.groupby(['MONTH', 'DAY_OF_WEEK']).agg({'SIG_DELAY_IND': 'count'})
        heatmapdata1['Delayed'] = monthdata1.groupby(['MONTH', 'DAY_OF_WEEK'])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
        heatmapdata1['Percentage'] = (heatmapdata1['Delayed'] / heatmapdata1['SIG_DELAY_IND'])*100
        heatmapdata1.rename(columns={"SIG_DELAY_IND": 'Total_Flights'}, inplace = True)
        heatmap1 = px.density_heatmap(heatmapdata1.reset_index(), x = "MONTH", y = 'DAY_OF_WEEK', z = "Percentage", nbinsx = (1 + monthmax1 - monthmin1), nbinsy = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0, 25))
        col1.write(heatmapdata1)
        col1.write(heatmap1)
        

        if col1.checkbox("Show Time Data"):

            cut_labels = ['12:01am to 6am', '6:01am to 9am', '9:01am to noon', '12:01pm to 3pm', '3:01pm to 6pm', '6:01pm to 9pm', '9:01pm to midnight']
            cut_bins = [0,5,8,11,14,17,20,24]
            bins = pd.cut(monthdata1['CRS_HOUR'], bins = cut_bins, labels = cut_labels)
            timeinfo1 = monthdata1.groupby(['DAY_OF_WEEK', bins]).agg({'FL_DATE': 'count'})
            timeinfo1['Delayed'] = monthdata1.groupby(['DAY_OF_WEEK', bins])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
            timeinfo1['Percent'] = (timeinfo1['Delayed']/timeinfo1['FL_DATE'])*100
            timeinfo1.rename(columns={"FL_DATE": 'Total_Flights'}, inplace = True)
            timeinfo1 = timeinfo1.reset_index()
            timeinfo1['CRS_HOUR'] = timeinfo1['CRS_HOUR'].astype(str)
            timeinfo1.rename(columns={"CRS_HOUR": 'Departure_Time'}, inplace = True)
            heatmap21 = px.density_heatmap(timeinfo1, x = "DAY_OF_WEEK", y = 'Departure_Time', z = "Percent", nbinsx = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0, 25))
            
            col1.write(heatmap21)
            col1.write(timeinfo1)
        
        monthdata2 = carrier_df2[((carrier_df2["MONTH"]>=monthmin1) & (carrier_df2["MONTH"]<=monthmax1))]
        monthdata2 = monthdata2[((carrier_df2["DAY_OF_WEEK"] >= daymin1) & (carrier_df2["DAY_OF_WEEK"] <= daymax1))]

        heatmapdata2 = monthdata2.groupby(['MONTH', 'DAY_OF_WEEK']).agg({'SIG_DELAY_IND': 'count'})
        heatmapdata2['Delayed'] = monthdata2.groupby(['MONTH', 'DAY_OF_WEEK'])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
        heatmapdata2['Percentage'] = (heatmapdata2['Delayed'] / heatmapdata2['SIG_DELAY_IND'])*100
        heatmapdata2.rename(columns={"SIG_DELAY_IND": 'Total_Flights'}, inplace = True)
        heatmap3 = px.density_heatmap(heatmapdata2.reset_index(), x = "MONTH", y = 'DAY_OF_WEEK', z = "Percentage", nbinsx = (1 + monthmax1 - monthmin1), nbinsy = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0,25))
        
        
        col2.write(heatmapdata2)
        col2.write(heatmap3)

        if col2.checkbox("Show Time Data", key = '36'):

            cut_labels = ['12:01am to 6am', '6:01am to 9am', '9:01am to noon', '12:01pm to 3pm', '3:01pm to 6pm', '6:01pm to 9pm', '9:01pm to midnight']
            cut_bins = [0,5,8,11,14,17,20,24]
            bins = pd.cut(monthdata2['CRS_HOUR'], bins = cut_bins, labels = cut_labels)
            timeinfo2 = monthdata2.groupby(['DAY_OF_WEEK', bins]).agg({'FL_DATE': 'count'})
            timeinfo2['Delayed'] = monthdata2.groupby(['DAY_OF_WEEK', bins])['SIG_DELAY_IND'].apply(lambda x: (x=='yes').sum())
            timeinfo2['Percent'] = (timeinfo2['Delayed']/timeinfo2['FL_DATE'])*100
            timeinfo2.rename(columns={"FL_DATE": 'Total_Flights'}, inplace = True)
            timeinfo2 = timeinfo2.reset_index()
            timeinfo2['CRS_HOUR'] = timeinfo2['CRS_HOUR'].astype(str)
            timeinfo2.rename(columns={"CRS_HOUR": 'Departure_Time'}, inplace = True)
            heatmap22 = px.density_heatmap(timeinfo2, x = "DAY_OF_WEEK", y = 'Departure_Time', z = "Percent", nbinsx = (1 + daymax1 - daymin1), color_continuous_scale = "RdPu", range_color=(0, 25))
            
            col2.write(heatmap22)
            col2.write(timeinfo2)
