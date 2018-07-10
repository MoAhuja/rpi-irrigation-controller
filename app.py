from flask import Flask, jsonify, Response
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
from service.rest_mappers.zone_data_rest_mapper import ZoneDataRestMapper 
from service.rest_mappers.zone_controller_rest_mapper import ZoneControllerRestMapper

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
	json_data = request.get_json(force=True)
	zcrm = ZoneControllerRestMapper()

	result = zcrm.activateZone(json_data)
	return result

@app.route('/service_hub/zones/deactivate', methods=['POST'])
def service_zones_deactivate():
	json_data = request.get_json(force=True)
	zcrm = ZoneControllerRestMapper()

	result = zcrm.deactivateZone(json_data)
	return result

	
@app.route('/service_hub/settings/loglevel/console', methods=['GET', 'POST'])
def service_settings_console_log_level():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return srm.getConsoleLogLevel()
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setConsoleLogLevel(json_data)

@app.route('/service_hub/settings/loglevel/database', methods=['GET', 'POST'])
def service_settings_database_log_level():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return srm.getDatabaseLogLevel()
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setDatabaseLogLevel(json_data)

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
	
	mapper = ZoneDataRestMapper()

	json_data = request.get_json(force=True)
	return mapper.createZone(json_data)

@app.route('/service_hub/zones', methods=['GET'])
def servie_get_zones():
	return Response(ZoneDataRestMapper().getAllZones(), mimetype='application/json')

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

	


