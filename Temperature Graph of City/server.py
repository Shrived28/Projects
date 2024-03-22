from flask import Flask, render_template, request
import requests
from datetime import datetime
import matplotlib.pyplot as plt
from io import BytesIO
import base64

app = Flask(__name__)

def get_temp_json(location,start_dt,end_dt):
    #Request data (code from website)
    url = "https://visual-crossing-weather.p.rapidapi.com/history"

    querystring = {
        "startDateTime":start_dt,
        "aggregateHours":"1",
        "location":location,
        "endDateTime":end_dt,
        "unitGroup":"metric",
        "contentType":"json",
        "shortColumnNames":"0"}

    headers = {
        "X-RapidAPI-Key": "1dc3c2b46emsh924b46538cef7e5p116559jsna239d3fd2a65",
        "X-RapidAPI-Host": "visual-crossing-weather.p.rapidapi.com"
    }

    response = requests.get(url, headers=headers, params=querystring)
    if response.status_code == 200:
        temp_json = response.json()
        temps=[]
        tsteps=[]
        #Extract Dates and temperatures from json file
        records = temp_json.get('locations', {}).get(location, {}).get('values', [])
        for entry in records:
            
            temp = entry.get('temp', None)
            if temp is not None:
                time = entry.get('datetimeStr',None)
                temps.append(temp)
                tsteps.append(time[:19])
        res=[temps,tsteps]
        return (res)
    else:
        print(f"Error {response.status_code}: {response.text}")
    
 # Route to render the HTML form
@app.route('/')
def index():
    return render_template('index.html', plot_data=None)

# Route to handle form submission and return the plot
@app.route('/generate_graph', methods=['POST'])
def plt_graph():
    city=request.form['city']
    country=request.form['country']
    locatn=city+','+country
    start_dt = request.form['start']
    end_dt = request.form['end']
    start_dt=start_dt+'T00:00:00'
    end_dt=end_dt+'T00:00:00'

    temp_tstep = get_temp_json(locatn,start_dt,end_dt)

    temperatures = temp_tstep[0]
    timesteps = temp_tstep[1]

    # print(timesteps)
    # print(temperatures)

    if temp_tstep:
        # Plotting the daily temperature data with dates
        plt.plot(timesteps, temperatures, label='Temperature')

        # Formatting the x-axis to display dates
        plt.xticks(rotation=40, ha='right')

        # Adding labels and title
        plt.xlabel('Date and Time')
        plt.ylabel('Temperature (°C)')
        plt.title('Temperature Data')

        plt.legend()
        plt.tight_layout()  
        # plt.show()

        # Convert the plot to a base64-encoded string
        buffer = BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)
        plot_data = base64.b64encode(buffer.read()).decode('utf-8')
        plt.close()

        return render_template('index.html', plot_data=plot_data)
    else:
        return render_template('index.html', plot_data=None)


if __name__ == '__main__':
    app.run(debug=True)
