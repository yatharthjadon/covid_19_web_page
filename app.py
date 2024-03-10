
import pandas as pd
import folium
from flask import Flask, render_template



corona_df = pd.read_csv("covid-19-dataset-1.csv")
    
#calculating the sum of numerical columns('Confirmed','Deaths','Recovered','Active') for each country in the column country_region  
    
by_country = corona_df.groupby('Country_Region').sum()[['Confirmed','Deaths','Recovered','Active']]
    
    
    
cdf = by_country.nlargest(15, 'Confirmed')[['Confirmed']]
    
pairs=[(country,confirmed) for country,confirmed in zip(cdf.index,cdf['Confirmed'])]


corona_df = pd.read_csv("covid-19-dataset-1.csv")

# removing any rows that contain missing values 
corona_df = corona_df.dropna()

# creating map

m=folium.Map(location=[34.223334,-82.461707],
            tiles='OpenStreetMap',
            zoom_start=8)

# creating circles over the map 

def circle_maker(x):
    folium.Circle(location=[x.loc['Lat'], x.loc['Long_']],
                  radius=float(x.loc['Confirmed']) * 10,
                             color = "red",
                             popup = '{}\n confirmed cases:{}'.format(x.iloc[3],x.iloc[2])).add_to(m)
    
corona_df[['Lat','Long_','Confirmed','Combined_Key']].apply(lambda x:circle_maker(x),axis=1)

html_map = m._repr_html_()    


app = Flask(__name__)

@app.route('/')


def home():
    return render_template("home.html" , table = cdf , cmap =html_map , pairs = pairs)

if __name__ =="__main__":
    app.run(debug=True)