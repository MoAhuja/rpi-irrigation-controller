from flask import Flask
from flask import render_template
from flask import request
from pprint import pprint
import service.shared as shared

import pi.main
from service.zone.zone_manager import ZoneManager
from service.engine import Engine


app = Flask(__name__)
		
@app.route('/')
def index():
	# return render_template('landing.html')
	return app.send_static_file('screens/portal/index.html')

@app.route('/portal/landing')
def landing():
	# Check query string for the zone ID. If so, we'll retrieve that zone data first and then load the page
	# return render_template('landing.html')
	return app.send_static_file('screens/portal/landing.html')	

@app.route('/portal/create_zone')
def create_zone():
	# Check query string for the zone ID. If so, we'll retrieve that zone data first and then load the page
	# return render_template('landing.html')
	return app.send_static_file('screens/portal/create_zone.html')

@app.route('/portal/flexbox')
def flexbox():
	# Check query string for the zone ID. If so, we'll retrieve that zone data first and then load the page
	# return render_template('landing.html')
	return app.send_static_file('screens/portal/flexbox_test.html')


@app.route('/service_hub/zones/status', methods=['GET'])
def service_zones_status():
	return ""

@app.route('/service_hub/zones/activate', methods=['POST'])
def service_zones_activate():
	print(request.get_json(force=True))
	json_data = request.get_json(force=True)
	zm = ZoneManager()
	result = zm.manuallyActivateZone(json_data)

@app.route('/service_hub/zones/deactivate', methods=['POST'])
def service_zones_deactivate():
	print(request.get_json(force=True))
	json_data = request.get_json(force=True)
	zm = ZoneManager()
	result = zm.manuallyDeactivateZone(json_data)

	return '{"x": "y"}'
	
@app.route('/service_hub/zones/create_zone', methods=['POST'])
def service_create_zone():

	
	print(request.get_json(force=True))
	json_data = request.get_json(force=True)
	zm = ZoneManager()
	zone = zm.createZone(json_data)
	# zones = zc.retrieveAllZones()
	# for zone in zones:
	# 	pprint("======= Zone =========")
	# 	pprint(vars(zone))

	# for schedule in zone.schedule:
	# 	print(schedule.start)
	# 	print(schedule.stop)


	return '{"x": "y"}'

	#The data coming in should be an application/json post request
	# print(params)
	
	# return app.send_static_file('portal/index.html')
	# Replace this with a request to the db business logic layer to request creation of a zone

# @app.route('/portal/landing')
# def landing():
	# Fetch data
	# render template and pass in data

# 	 r = requests.get(
#       'https://www.parsehub.com/api/v2/projects/{PROJECT_TOKEN}/last_ready_run/data',
#       params=params)
#   return render_template('movies.html', movies=json.loads(r.text)['movies'])

if __name__ == '__main__':
	global event_pub
	global zm
	pi.main.initialize()

	# Initialize the event publisher
	# event_pub = EventPublisher()
	# engine = Engine(event_pub)


	# zm = ZoneManager(event_pub)
	app.run(debug=False)

	


