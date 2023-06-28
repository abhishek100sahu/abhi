import psycopg2
import datetime
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
from psychrochart import PsychroChart, load_config
import matplotlib.patches as mpatches
import time
#import schedule
import matplotlib.font_manager as font_manager
#from new_hour import df9j
def main_psy():
    com=psycopg2.connect(user='postgres',password='cdac123',host='127.0.0.1',database='smart_airport_terminal_sensor_db')################change
    print(com)
    cur=com.cursor()
    cur.execute("select * from sensor_data where time >= (now() - interval '24 hour')")######change
    sensor_data=pd.DataFrame(cur.fetchall())
    #t=datetime.datetime.now().strftime("%H_%M")
    sensor_data.to_csv(f"/home/rubix/Desktop/Meity_SAT/sensor_data_meity.csv",index=None)########change
    df=pd.read_csv("sensor_data_meity.csv",names=['id','nodeid','temp','humidity','lightintensity','co2','pm2_5','pm10','time'])
    #sensor_data1.columns=['id','nodeid','temp','humidity','lightintensity','co2','pm2_5','pm10','time']
    print(df.head())
    a1=[]
    a2=[]
    a3=[]
    a4=[]
    #a5=[]

    para=['temp','humidity','lightintensity','co2','pm2_5','pm10']
    #separating datas based on nodes
    for i in para:
        df[i]  = df[i].astype('float')
        BCW680_node=df[df['nodeid']=='BCW680']##########change
        BCE791_node=df[df['nodeid']=='BCE791']
        AZW180_node=df[df['nodeid']=='AZW180']
        AZC327_node=df[df['nodeid']=='AZC327']
        #DPCKE853_node=df[df['nodeid']=='DPCKE853'] #change############### use the working node names

    #calculating mean for all the parameter in the node
        a01=BCW680_node[i].mean()############change
        a1.append(a01)


        a02=BCE791_node[i].mean()
        a2.append(a02)

        a03=AZW180_node[i].mean()
        a3.append(a03)

        a04=AZC327_node[i].mean()
        a4.append(a04)

        #a05=DPCKE853_node[i].mean()#change#######
        #a5.append(a05)
    list=[a1,a2,a3,a4]########change
    Temperature=[]
    Humidity=[]
    lightintensity=[]
    co2=[]
    pm2_5=[]
    pm10=[]
    for i1 in list:
        Temperature.append(i1[0])
        Humidity.append(i1[1])
        lightintensity.append(i1[2])
        co2.append(i1[3])
        pm2_5.append(i1[4])
        pm10.append(i1[5])
    nodeid=['BCW680', 'BCE791','AZW180', 'AZC327']########change
    location=['Opposite CeG Hall','Near SBI ATM','Inside CeG Hall','Near Reception Area']########change
    dict = {'node': nodeid,'Location':location ,'temp': Temperature, 'humidity': Humidity,'co2':co2,'pm2_5':pm2_5,'pm10':pm10}  
    df_ = pd.DataFrame(dict)
    #Reading standard value file.
    Standard_value=pd.read_excel("/home/rubix/Desktop/Meity_SAT/pychro.xlsx",skiprows=(1),engine='openpyxl')########change
    Standard_value = Standard_value.iloc[1: , :]

    #Calculating pg using the given formula.
    temp=df_["temp"].round(decimals=2)
    calculated_temp=[]
    for t in temp:
        pg = 0.56516 + (0.0639*t) -((2.65517*10**-4)*t**2) + ((7.3623*10**-5)*t**3)
        calculated_temp.append(pg)
        continue
    df_["pg"]=[round(num, 2) for num in calculated_temp]
    #calculating specific humidity.
    calculated_humidity=[]
    #patm = 90.9209
    for r,p in zip(df_["humidity"],df_["pg"]):
            x=622*(r/100)*(p/(90.9209-p*(r/100)))
            calculated_humidity.append(x)
    df_["specific_humidity"]=[round(num1, 2) for num1 in calculated_humidity]
    #calculating new pg.
    new_pg=[]
    patm=90.9209
    for j in df_["specific_humidity"]:
        np=(j*patm)/(622+j)
        new_pg.append(np)
    df_["new_pg"]=[round(num2, 2) for num2 in new_pg]
    #calculating min temp and pg ,max temp and pg.
    mini_temp=[]
    maxi_temp=[]
    mini_pg=[]
    maxi_pg=[]
    for i in df_["new_pg"]:
        minimum_val=Standard_value[Standard_value["Saturation Vapor pressure (kPa) w r t Dry bulb Temperature"] > i].min()
        maximum_val=Standard_value[Standard_value["Saturation Vapor pressure (kPa) w r t Dry bulb Temperature"] < i].max()
        min_temp=minimum_val["Dry bulb Temperature (°C)"]
        max_temp=maximum_val["Dry bulb Temperature (°C)"]
        min_pg=minimum_val["Saturation Vapor pressure (kPa) w r t Dry bulb Temperature"]
        max_pg=maximum_val["Saturation Vapor pressure (kPa) w r t Dry bulb Temperature"]
        mini_temp.append(min_temp)
        maxi_temp.append(max_temp)
        mini_pg.append(min_pg)
        maxi_pg.append(max_pg)
    df_["mini_pg"]=maxi_pg
    df_["maxi_pg"]=mini_pg
    df_["mini_temp"]=maxi_temp
    df_["maxi_temp"]=mini_temp    
    #calculating dew point.
    dew_point=[]
    for x1,y1,x2,y2,y in zip(df_["mini_temp"],df_["mini_pg"],df_["maxi_temp"],df_["maxi_pg"],df_["new_pg"]):
        x01=(x1 + ((y-y1)*((x2-x1)/(y2-y1))))
        dew_point.append(x01)
    df_["dew"]=[round(num3, 2) for num3 in dew_point]
    #calculating enthalpy.    
    enthalpy_=[]
    for i06,j06 in zip(df_["temp"],df_["specific_humidity"]):
        e06=i06 + 2.5*j06
        enthalpy_.append(e06)
    df_["enthalpy"]=[round(num4, 2) for num4 in enthalpy_]
    # df.dropna(subset = ["temp","humidity",'dew'], inplace=True)
    #creating csv file using above calculated parameters.  
    df_.to_csv(f"/home/rubix/Desktop/Meity_SAT/graph_data.csv",index=None) #give this path in aqi plot########change
    #print(df.head(23))
    #df_=df.dropna()
    df09=df_.dropna()
    temperature_=df09["temp"]
    humidity_=df09["humidity"]
    specific_humidity_=df09["specific_humidity"]
    nodeid_=df09["node"]
    dewpoint_=df09["dew"]
    pg00=df09["pg"]
    enthalpy_=df09["enthalpy"]
    Location_=df09['Location']
    list_nodeid=df09['node']####change
    '''list_nodeid=['BCW680', 'BCE791','AZW180', 'AZC327', 'DPWAE853',
        'DPSEE997', 'MZAZW744', 'DPCKW501', 'DPCKE130', 'ARAZE432',
        'ARBCW697', 'ARAZW505', 'ARAZC875', 'DPWAW570', 'ARAZC612',
        'DPCKW522','MZAZW216','DPCKE853','ARBCE538','ARBCE759','ARAZC192','DPSEE870','DPWAW262']#############change'''
    #Using the required the required parameters starting to plot the pyschrometric chart.
    for a in list_nodeid:
        for temperature__,humidity__,nodeid__,dewpoint__,specific_humidity__,enthalpy__,Location__ in zip(temperature_, humidity_,nodeid_,dewpoint_,specific_humidity_,enthalpy_,Location_):
            if a in nodeid__:
                # Get a preconfigured chart
                chart = PsychroChart("ashrae")

                # Append zones:
                zones_conf = {
                    "zones":[{
                            "zone_type": "dbt-rh",
                            "style": {"edgecolor": "lime",
                                    "facecolor": "lime",
                                    "linewidth": 5,
                                    "linestyle": "--"},

                            "points_x": [23, 28],
                            "points_y": [40, 60],


                        },
                        {
                            "zone_type": "dbt-rh",
                            "style": {"edgecolor": "yellow",
                                    "facecolor": "yellow",
                                    "linewidth": 2,
                                    "linestyle": "--"},
                            "points_x": [22, 23],
                            "points_y": [30, 70]
                        },
                        {
                            "zone_type": "dbt-rh",
                            "style": {"edgecolor": "yellow",
                                    "facecolor": "yellow",
                                    "linewidth": 2,
                                    "linestyle": "--"},
                            "points_x": [22, 29],
                            "points_y": [60, 70]
                        },
                        {
                            "zone_type": "dbt-rh",
                            "style": {"edgecolor": "yellow",
                                    "facecolor": "yellow",
                                    "linewidth": 2,
                                    "linestyle": "--"},
                            "points_x": [28, 29],
                            "points_y": [30, 70]
                        },
                        {
                            "zone_type": "dbt-rh",
                            "style": {"edgecolor": "yellow",
                                    "facecolor": "yellow",
                                    "linewidth": 2,
                                    "linestyle": "--"},
                            "points_x": [22, 29],
                            "points_y": [30, 40]
                        }]}
                chart.append_zones(zones_conf)

                # Plot the chart
                ax = chart.plot()

                #ax=plt.subplots()
                # Add Vertical lines
                t_min, t_opt, t_max = 16, 23, 30

                _temperature_=[]
                _humidity_=[]
                _dewpoint_=[]
                _specific_humidity_=[]
                _enthalpy_=[]
                _Location_=[]

                _temperature_.append(temperature__)
                _humidity_.append(humidity__)
                _dewpoint_.append(dewpoint__)
                _specific_humidity_.append(specific_humidity__)
                _enthalpy_.append(enthalpy__)
                _Location_.append(Location__)

                #print(vj)
                temperature_plot= [round(num, 1) for num in _temperature_]
                humidity_plot= [round(num, 1) for num in _humidity_]
                dewpoint_plot= [round(num, 1) for num in _dewpoint_]
                specific_humidity_plot= [round(num, 1) for num in _specific_humidity_]
                enthalpy_plot= [round(num, 1) for num in _enthalpy_]



                r1 = [str(integer) for integer in temperature_plot]
                w1 = "".join(r1)
                temperature_label = float(w1)

                r2 = [str(integer) for integer in humidity_plot]
                w2 = "".join(r2)
                humidity_label = float(w2)

                r3 = [str(integer) for integer in dewpoint_plot]
                w3 = "".join(r3)
                dewpoint_label = float(w3)

                r4 = [str(integer) for integer in specific_humidity_plot]
                w4 = "".join(r4)
                specific_humidity_label = float(w4)

                r5 = [str(integer) for integer in enthalpy_plot]
                w5 = "".join(r5)
                enthalpy_label = float(w5)

                r6 = [str(integer) for integer in _Location_]
                w6 = "".join(r6)
                location_label = w6

                '''print(temperature_label)
                print(humidity_label)
                print(dewpoint_label)
                print(specific_humidity_label)
                print(e3)'''

                #print(we,ve)
                # Add labelled points and conexions between points
                points = {'exterior': {'style': {'color': [0.855, 0.004, 0.278, 0.8],
                                                'marker': 'o', 'markersize': 10},'xy': (temperature_plot,humidity_plot)}}

                chart.plot_points_dbt_rh(points)
                p1 = mpatches.Patch(label="Location : {} ".format(location_label))
                p2 = mpatches.Patch(label="Dew point : {f6} {deg}C".format(deg=u"\N{DEGREE SIGN}", f6=dewpoint_label))
                p3 = mpatches.Patch(label="Enthalpy : {} kJ heat/kg air".format(enthalpy_label))
                p4 = mpatches.Patch(label="Absolute humidity : {} gm moisture/kg air".format(specific_humidity_label))
                p5 = mpatches.Patch(label="Ambient Temperature : {f7} {deg1}C".format(deg1=u"\N{DEGREE SIGN}",f7=temperature_label))
                p6 = mpatches.Patch(label="Relative humidity : {}%".format(humidity_label))
                p7 = mpatches.Patch(color="lime",label="Comfort zone")
                p8 = mpatches.Patch(color="yellow",label="Close to Comfort zone")

                # Add a legend
                font = font_manager.FontProperties(  # 'Times new roman', 
                            weight='bold',size=15)
                ax.legend(markerscale=0.7,handles=[p1,p2,p3,p4,p5,p6,p7,p8], frameon=False, fontsize=10,prop=font, labelspacing=1.2)

                ax.set_title('Pyschrometric Chart - Indoor Comfort Analysis',fontsize = 25,fontweight='bold')
                ax.set_xlabel("Ambient Temperature (\N{DEGREE SIGN}C)", fontsize = 12,fontweight='bold')
                ax.set_ylabel("Absolute Humidity (gm moisture/kg air)", fontsize = 12,fontweight='bold')
                ax.xaxis.get_label().set_fontsize(25)
                ax.yaxis.get_label().set_fontsize(25)

                #print(a,dewpoint_label,e3,specific_humidity_label,temperature_label,humidity_label)
                #saving the images.
                #ax.get_figure().savefig(r'C:/Users/cdac/Downloads/jaya/pyschrooo/1picture/{}_'.format(a) + str(1) + '.png', transparent=False)
                ax.get_figure().savefig(r'/home/rubix/Desktop/Meity_SAT/p1/{}.png'.format(a), transparent=False) ########change





