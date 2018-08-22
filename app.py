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
from service.rest_mappers.dashboard_rest_mapper import DashboardRestMapper
from service.rest_mappers.logs_rest_mapper import LogsRestMapper
from service.rest_mappers.decision_history_rest_mapper import DecisionHistoryRestMapper
from service.rest_mappers.notification_users_rest_mapper import NotificationUsersRestMapper
import service.database.db_schema

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

@app.route('/service_hub/settings/kill', methods=['GET', 'POST'])
def service_settings_kill_switch():
	srm = SettingsRestMapper()

	if request.method == 'GET':
		result =  Response(srm.getKillSwitch(), mimetype='application/json')
	else:
		json_data = request.get_json(force=True)
		result = srm.setKillSwitch(json_data)

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

@app.route('/service_hub/zone/<int:zone_id>', methods=['DELETE', 'GET'])
def service_zone_delete_or_get(zone_id):
	mapper = ZoneDataRestMapper()

	if request.method == 'DELETE':
		result = mapper.deleteZone(zone_id)
	else:
		result = mapper.getZone(zone_id)
		result = Response(result, mimetype='application/json')

	result.headers['Access-Control-Allow-Origin'] = '*'

	return result

@app.route('/service_hub/zone', methods=['POST'])
def service_zone_create():

	print(request.get_json(force=True))
	
	mapper = ZoneDataRestMapper()

	json_data = request.get_json(force=True)
	resp = Response(mapper.createZone(json_data), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	
	# resp.headers['Access-Control-Allow-Headers'] = 'application/json'

	return resp


@app.route('/service_hub/zone/edit', methods=['POST'])
def service_edit_zone():

	print(request.get_json(force=True))
	
	mapper = ZoneDataRestMapper()

	json_data = request.get_json(force=True)
	return mapper.editZone(json_data)

@app.route('/service_hub/zones', methods=['GET'])
def service_get_zones():
	resp =  Response(ZoneDataRestMapper().getAllZones(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/service_hub/dashboard', methods=['GET'])
def service_get_dashboard():
	resp = Response(DashboardRestMapper().getDashboard(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/service_hub/logs', methods=['GET'])
def service_get_all_logs():
	# Check if a log level was specified
	level = request.args.get('level')

	resp = None

	if level is None:
		resp = Response(LogsRestMapper().getAllLogs(), mimetype='application/json')
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp
		
	else:
		resp = Response(LogsRestMapper().getLogsByLevel(level), mimetype='application/json')
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp

@app.route('/service_hub/decisionhistory', methods=['GET'])
def service_get_all_decisions():
	# Check if a log level was specified
	zone = request.args.get('zone')

	if zone is None:
		resp =  Response(DecisionHistoryRestMapper().getHistoryForAllZones(), mimetype='application/json')
	else:
		resp =  Response(DecisionHistoryRestMapper().getHistoryByZone(zone), mimetype='application/json')

	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

@app.route('/service_hub/settings/notification/config', methods=['GET', 'POST'])
def service_settings_notification_config():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		resp = Response(srm.getNotificationSettings(), mimetype='application/json')
		resp.headers['Access-Control-Allow-Origin'] = '*'
		
	else:
		# POst request, so we need to update the notification settings
		json_data = request.get_json(force=True)
		resp = Response(srm.setNotificationSettings(json_data), mimetype='application/json')
		resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp

@app.route('/service_hub/settings/notification/pushbullet/user', methods=['POST'])
def service_settings_pushbullet_user():
	rm = NotificationUsersRestMapper()
	
	# POst request, so we need to update the notification settings
	json_data = request.get_json(force=True)
	resp = Response(rm.addPushBulletUser(json_data), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp

@app.route('/service_hub/settings/notification/pushbullet/users', methods=['GET'])
def service_settings_pushbullet_users():
	rm = NotificationUsersRestMapper()
	
	# POst request, so we need to update the notification settings
	resp = Response(rm.getPushBulletNotificationUsers(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp		

@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
	global event_pub
	global zm
	pi.main.initialize()

	shared.logger.debug(None, "About to create database!!")
	service.database.db_schema.createDatabase()


	# Initialize the event publisher
	# event_pub = EventPublisher()
	engine = Engine()
	
	# zm = ZoneManager(event_pub)
	app.run(debug=False, threaded=True, host='0.0.0.0')

	


