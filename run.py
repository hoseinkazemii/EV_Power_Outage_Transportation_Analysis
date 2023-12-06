from GmapsHandler import *
from Visualization import *


def run():


	settings = {"api_key":"",
				"verbose":True,
				"percentage_to_drop":0.5,
				"num_sample_cars":30,
				"charging_station":
								# "City of Seattle - Central Library",
								# "City of Seattle - Seattle Center",
								# "KING COUNTY DES KSC STATION #1",
								# "VIA6 VIA6-SOUTH",
								# "800 FIFTH AVE STATION 2",
								# "UWMC 4245 UWMC 4245 #1",
								# "BMW SEATTLE BMW SALES",
								# "525 NORTHGATE RETAIL #1",
								"VM CHARGERS VIRGINIA MASON2",
				"plot_x_lim":[0,31],
				"total_simulation_time": 6, # In hours
    			"charging_times" : {'J1772': 7 * 60, 'TESLA': 7 * 60, 'CHADEMO': 40},
    			"fig_font_size":12,
	}



	myData = HandleData()
	myData.preprocess_and_export_results(**settings)


	myData = Visualization()
	myData.visualize(**settings)




if __name__ == '__main__':
	run()