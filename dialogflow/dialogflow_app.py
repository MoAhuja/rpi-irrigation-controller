
# This file contains the Dialog Flow API entry points.
# For each API it will validate the authentication parameters are correct, parse out the diaglog flow message and send it to LawnWatcher for processing
# It will then wrap the response up into a dialog flow response type

from flask import Flask, jsonify, Response
from flask import request
import pprint
from flask_basicauth import BasicAuth
from service.df_recipes_agent import DialogFlowRecipesAgent
from json2html import *
import json



global app
global engine


app = Flask(__name__)
app.config['BASIC_AUTH_USERNAME'] = 'mo'
app.config['BASIC_AUTH_PASSWORD'] = 'test'

basic_auth = BasicAuth(app)

requestResponseList = []


@app.route('/service/debug', methods=['GET'])
def debug():
    global requestResponseList

    htmlContent = ""

    pprint.pprint(requestResponseList)

    for reqResDict in requestResponseList:
        htmlContent += "============= REQUEST ================== <br />"
        htmlContent += "<pre id=\"json\">" + json2html.convert(json = reqResDict["req"]) + "</pre><br />"
        htmlContent += "============= END REQUEST ================== <br />"

        htmlContent += "============= RESPONSE ================== <br />"
        htmlContent += "<pre id=\"json\">" + json2html.convert(json = reqResDict["res"]) + "</pre><br />"
        htmlContent += "============= END RESPONSE ================== <br />"

    pprint.pprint(requestResponseList)

    return htmlContent


@app.route('/service/test', methods=['POST'])
@basic_auth.required
def test():
    print("Test")
    global requestResponseList
    requestDataAsJson = request.get_json(force=True)
    ##pprint.pprint(requestDataAsJson)
    dfagent = DialogFlowRecipesAgent()

    responseData = dfagent.handleIntent(json.dumps(requestDataAsJson))
    pprint.pprint("============= REQUEST ==================")
    pprint.pprint(requestDataAsJson)
    pprint.pprint("============= END REQUEST ==================")

    pprint.pprint("")
    pprint.pprint("============= RESPONSE ==================")
    # jsonResponse = json.dumps(responseData)
    # print(jsonResponse)

    # requestResponseList.append({"req": requestDataAsJson, "res": jsonResponse})



    return responseData


# def service_settings_display_theme_config():
#     srm = SettingsRestMapper()
#     if request.method == 'GET':
#         resp = Response(srm.getTheme(), mimetype='application/json')
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#
#     else:
#         # POst request, so we need to update the notification settings
#         json_data = request.get_json(force=True)
#         resp = Response(srm.setTheme(json_data), mimetype='application/json')
#         resp.headers['Access-Control-Allow-Origin'] = '*'
#
#     return resp


if __name__ == '__main__':
    app.run(debug=True, threaded=True, host='0.0.0.0', port=5001)




