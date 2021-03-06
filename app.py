from flask import Flask, jsonify, Response
from flask import render_template
from flask import request
from pprint import pprint
from service.rest_mappers.InvalidUsage import InvalidUsage
from flask_basicauth import BasicAuth


#import pi.main
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
from service.rest_mappers.relay_rest_mapper import RelayRestMapper
from service.rest_mappers.weather_rest_mapper import WeatherRestMapper
from service.rest_mappers.app_updater_rest_mapper import AppUpdaterRestMapper
import service.database.db_schema

# from updater.git_updater import GitUpdater

from service.zone.zone_controller import ZoneController

global app
global engine

app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'mo'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)



def appInit():
	

	#global event_pub
	#global zm
	#pi.main.initialize()
	global engine

	shared.logger.debug(None, "About to create database!!")
	service.database.db_schema.createDatabase()


	# Initialize the event publisher
	# event_pub = EventPublisher()
	engine = Engine()	
	
appInit()





@app.route('/portal/create_zone')
@basic_auth.required	
def create_zone():
	# Check query string for the zone ID. If so, we'll retrieve that zone data first and then load the page
	# return render_template('landing.html')
	return app.send_static_file('screens/portal/zone_manager/create_zone.html')

@app.route('/portal/flexbox')
@basic_auth.required
def flexbox():
	# Check query string for the zone ID. If so, we'll retrieve that zone data first and then load the page
	# return render_template('landing.html')
	
	return app.send_static_file('screens/portal/flexbox_test.html')


@app.route('/service_hub/zones/status', methods=['GET'])
@basic_auth.required
def service_zones_status():
	return ""

@app.route('/service_hub/zones/activate', methods=['POST'])
@basic_auth.required
def service_zones_activate():
	json_data = request.get_json(force=True)
	zcrm = ZoneControllerRestMapper()

	result = zcrm.activateZone(json_data)
	return result

@app.route('/service_hub/zones/deactivate', methods=['POST'])
@basic_auth.required
def service_zones_deactivate():
	json_data = request.get_json(force=True)
	zcrm = ZoneControllerRestMapper()

	result = zcrm.deactivateZone(json_data)
	return result

@app.route('/service_hub/settings/kill', methods=['GET', 'POST'])
@basic_auth.required
def service_settings_kill_switch():
	print("Kill switch post data:")
	print(request.data)
	srm = SettingsRestMapper()

	if request.method == 'GET':
		result =  Response(srm.getKillSwitch(), mimetype='application/json')
	else:
		json_data = request.get_json(force=True)
		print(json_data)
		result = srm.setKillSwitch(json_data)

	return result

	
	

@app.route('/service_hub/settings/loglevel/console', methods=['GET', 'POST'])
@basic_auth.required
def service_settings_console_log_level():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return srm.getConsoleLogLevel()
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setConsoleLogLevel(json_data)

@app.route('/service_hub/settings/loglevel/database', methods=['GET', 'POST'])
@basic_auth.required
def service_settings_database_log_level():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return srm.getDatabaseLogLevel()
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setDatabaseLogLevel(json_data)

@app.route('/service_hub/settings/location', methods=['GET', 'POST'])
@basic_auth.required
def service_settings_location():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return Response(srm.getLocation(), mimetype='application/json')
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setLocation(json_data)

@app.route('/service_hub/settings/raindelay', methods=['GET', 'POST'])
@basic_auth.required
def service_settings_raindelay():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		return Response(srm.getRainDelay(), mimetype='application/json')
	else:
		# POst request, so we need to update
		json_data = request.get_json(force=True)
		return srm.setRainDelay(json_data)

@app.route('/service_hub/zone/<int:zone_id>', methods=['DELETE', 'GET'])
@basic_auth.required
def service_zone_delete_or_get(zone_id):
	mapper = ZoneDataRestMapper()

	print("Zone id for delete is: " + str(zone_id))
	if request.method == 'DELETE':
		result = mapper.deleteZone(zone_id)
		result = Response(result)
	else:
		result = mapper.getZone(zone_id)
		result = Response(result, mimetype='application/json')

	result.headers['Access-Control-Allow-Origin'] = '*'
	result.headers['Access-Control-Allow-Methods'] = 'GET, POST, PATCH, PUT, DELETE, OPTIONS'


	return result

@app.route('/service_hub/zone', methods=['POST'])
@basic_auth.required
def service_zone_create():

	print(request.get_json(force=True))
	
	mapper = ZoneDataRestMapper()

	json_data = request.get_json(force=True)
	resp = Response(mapper.createZone(json_data), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	
	# resp.headers['Access-Control-Allow-Headers'] = 'application/json'

	return resp


@app.route('/service_hub/zone/edit', methods=['POST'])
@basic_auth.required
def service_edit_zone():

	print(request.get_json(force=True))
	
	mapper = ZoneDataRestMapper()

	json_data = request.get_json(force=True)
	return mapper.editZone(json_data)

@app.route('/service_hub/zones', methods=['GET'])
@basic_auth.required
def service_get_zones():
	resp =  Response(ZoneDataRestMapper().getAllZones(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp

@app.route('/service_hub/engine/stop')
@basic_auth.required
def service_stop_engine():
	global engine

	engine.stop()
	return Response()

@app.route('/service_hub/engine/start')
@basic_auth.required
def service_start_engine():
	global engine
	engine.stop()
	engine.start()
	
	return Response()

@app.route('/service_hub/dashboard', methods=['GET'])
@basic_auth.required
def service_get_dashboard():
	resp = Response(DashboardRestMapper().getDashboard(engine), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	return resp


@app.route('/service_hub/logs', methods=['GET'])
@basic_auth.required
def service_get_all_logs():

	# Check if a log level was specified
	level = request.args.get('level')
	page = request.args.get('page')
	page_size = request.args.get('page_size')

	print(page)
	print(page_size)

	if page is None:
		print("setting page to 0 from None")
		page = 0
	else:
		page = int(page)
	
	if page_size is None:
		print("setting page to 40 from None")
		page_size = 40
	else:
		page_size = int(page_size)


	resp = None

	if level is None:
		resp = Response(LogsRestMapper().getAllLogs(page, page_size), mimetype='application/json')
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp
		
	else:
		resp = Response(LogsRestMapper().getLogsByLevel(level, page, page_size), mimetype='application/json')
		
		resp.headers['Access-Control-Allow-Origin'] = '*'
		return resp

@app.route('/service_hub/decisionhistory', methods=['GET'])
@basic_auth.required
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
@basic_auth.required
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

@app.route('/service_hub/settings/display/theme', methods=['GET', 'POST'])
@basic_auth.required
def service_settings_display_theme_config():
	srm = SettingsRestMapper()
	if request.method == 'GET':
		resp = Response(srm.getTheme(), mimetype='application/json')
		resp.headers['Access-Control-Allow-Origin'] = '*'
		
	else:
		# POst request, so we need to update the notification settings
		json_data = request.get_json(force=True)
		resp = Response(srm.setTheme(json_data), mimetype='application/json')
		resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp


@app.route('/service_hub/settings/notification/pushbullet/user', methods=['POST'])
@basic_auth.required
def service_settings_pushbullet_user():
	rm = NotificationUsersRestMapper()
	
	# POst request, so we need to update the notification settings
	json_data = request.get_json(force=True)
	resp = Response(rm.addPushBulletUser(json_data), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp

@app.route('/service_hub/settings/notification/pushbullet/users', methods=['GET'])
@basic_auth.required
def service_settings_pushbullet_users():
	rm = NotificationUsersRestMapper()

	# POst request, so we need to update the notification settings
	resp = Response(rm.getPushBulletNotificationUsers(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp	

@app.route('/service_hub/settings/notification/pushbullet/user/<string:name>', methods=['DELETE'])
@basic_auth.required
def service_settings_pushbullet_user_delete(name):
	rm = NotificationUsersRestMapper()

	# POst request, so we need to update the notification settings
	resp = Response(rm.deletePushBulletNotificationUser(name), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	

	return resp	

@app.route('/service_hub/relay', methods=['POST'])
@basic_auth.required
def create_relay_to_pin_mapping():
	mapper = RelayRestMapper()
	# if request.method == 'GET':
	# 	# resp = Response(srm.getNotificationSettings(), mimetype='application/json')
	# 	# resp.headers['Access-Control-Allow-Origin'] = '*'
	# 	return ""
	# else:
		# Post request, so we need to assign the relay
	json_data = request.get_json(force=True)
	resp = Response(mapper.createRelayToPinMapping(json_data), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'

	return resp

@app.route('/service_hub/relays', methods=['GET'])
@basic_auth.required
def get_relay_mappings():
	mapper = RelayRestMapper()
	resp = Response(mapper.getRelays(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	
	return resp

@app.route('/service_hub/relays/<int:relay_id>', methods=['DELETE'])
@basic_auth.required
def delete_relay_mapping(relay_id):
	mapper = RelayRestMapper()
	resp = Response(mapper.deleteRelayMappingByRelay(relay_id), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	
	return resp

@app.route('/service_hub/weather/<string:country>/<string:city>', methods=['GET'])
@basic_auth.required
def get_weather_forecast(country, city):
	print(country)
	print(city)
	mapper = WeatherRestMapper()
	resp = Response(mapper.getForecast(country, city), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	
	return resp

@app.route('/service_hub/updater/history', methods=['GET'])
@basic_auth.required
def get_app_update_history():
	mapper = AppUpdaterRestMapper()
	resp = Response(mapper.getUpdateHistory(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	
	return resp

@app.route('/service_hub/updater/update', methods=['GET'])
@basic_auth.required
def update_app():
	mapper = AppUpdaterRestMapper()
	resp = Response(mapper.updateApp(), mimetype='application/json')
	resp.headers['Access-Control-Allow-Origin'] = '*'
	
	return resp



@app.errorhandler(InvalidUsage)
def handle_invalid_usage(error):
    response = jsonify(error.to_dict())
    response.status_code = error.status_code
    return response

if __name__ == '__main__':
	
	app.run(debug=True, threaded=True, host='0.0.0.0')

	


