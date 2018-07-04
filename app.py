from flask import Flask, jsonify
from flask import render_template
from flask import request
from pprint import pprint
from service.rest_mappers.InvalidUsage import InvalidUsage

import pi.main
from service.zone.zone_data_manager import ZoneDataManager
from service.core.engine import Engine
from service.core import shared
from service.utilities.logger import Logger
from service.rest_mappers.settings_rest_mapper import SettingsRestMapper
from service.zone.zone_controller import ZoneController

global app
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
	zc = ZoneController()
	result = zc.restActivateZone(json_data)
	return result

# @app.route('/service_hub/zones/deactivate', methods=['POST'])
# def service_zones_deactivate():
# 	# print(request.get_json(force=True))
# 	# json_data = request.get_json(force=True)
# 	# zm = ZoneManager()
# 	# result = zm.manuallyDeactivateZone(json_data)

	# return '{"x": "y"}'
@app.route('/service_hub/settings/loglevel/console', methods=['GET', 'POST'])
def service_settings_console_log_level():
	# sm = SettingsManager()
	# if request.method == 'GET':
	# 	return sm.getSettingRestMapper(SettingsManager.field_console_log_level)
	# else:
	# 	# POst request, so we need to update
	# 	json_data = request.get_json(force=True)
	# 	sm = SettingsManager()
	# 	return sm.setSettingRestMapper(SettingsManager.field_console_log_level, json_data["value"])
	return False

@app.route('/service_hub/settings/loglevel/database', methods=['GET', 'POST'])
def service_settings_database_log_level():
	# sm = SettingsManager()
		
	# if request.method == 'GET':
	# 	return sm.getSettingRestMapper(SettingsManager.field_database_log_level)
	# else:
	# 	# POst request, so we need to update

	# 	json_data = request.get_json(force=True)
	# 	return sm.setSettingRestMapper(SettingsManager.field_database_log_level, json_data["value"])
	return False

@app.route('/service_hub/settings/location', methods=['GET', 'POST'])
def service_settings_location():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return srm.getLocation()
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setLocation(json_data)

@app.route('/service_hub/settings/raindelay', methods=['GET', 'POST'])
def service_settings_raindelay():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return srm.getRainDelay()
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setRainDelay(json_data)

@app.route('/service_hub/zones/create_zone', methods=['POST'])
def service_create_zone():

	print(request.get_json(force=True))
	json_data = request.get_json(force=True)
	zdm = ZoneDataManager()
	zone = zdm.createZone(json_data)
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

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
	global event_pub
	global zm
	pi.main.initialize()

	# Initialize the event publisher
	# event_pub = EventPublisher()
	engine = Engine()
	
	# zm = ZoneManager(event_pub)
	app.run(debug=False)

	


