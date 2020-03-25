# File: athena_connector.py
# Copyright (c) 2017-2020 Splunk Inc.
#
# Licensed under Apache 2.0 (https://www.apache.org/licenses/LICENSE-2.0.txt)

import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult
import requests
import json
from datetime import datetime, timedelta


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class AutomationGamesConnector(BaseConnector):

    def __init__(self):

        # Call the BaseConnectors init first
        super(AutomationGamesConnector, self).__init__()

        self._state = None

        # Variable to hold a base_url in case the app makes REST calls
        # Do note that the app json defines the asset config, so please
        # modify this as you deem fit.
        self._base_url = None

    def _process_empty_response(self, response, action_result):

        if response.status_code == 200:
            return RetVal(phantom.APP_SUCCESS, {})

        return RetVal(action_result.set_status(phantom.APP_ERROR, "Empty response and no information in the header"), None)

    def _process_json_response(self, r, action_result):

        # Try a json parse
        try:
            resp_json = r.json()
        except Exception as e:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Unable to parse JSON response. Error: {0}".format(str(e))), None)

        # Please specify the status codes here
        if 200 <= r.status_code < 399:
            return RetVal(phantom.APP_SUCCESS, resp_json)

        # You should process the error returned in the json
        message = "Error from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace(u'{', '{{').replace(u'}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _process_response(self, r, action_result):

        # store the r_text in debug data, it will get dumped in the logs if the action fails
        if hasattr(action_result, 'add_debug_data'):
            action_result.add_debug_data({'r_status_code': r.status_code})
            action_result.add_debug_data({'r_text': r.text})
            action_result.add_debug_data({'r_headers': r.headers})

        # Process each 'Content-Type' of response separately

        # Process a json response
        if 'json' in r.headers.get('Content-Type', ''):
            return self._process_json_response(r, action_result)

        # it's not content-type that is to be parsed, handle an empty response
        if not r.text:
            return self._process_empty_response(r, action_result)

        # everything else is actually an error at this point
        message = "Can't process response from server. Status Code: {0} Data from server: {1}".format(
                r.status_code, r.text.replace('{', '{{').replace('}', '}}'))

        return RetVal(action_result.set_status(phantom.APP_ERROR, message), None)

    def _make_rest_call(self, endpoint, action_result, method="get", **kwargs):
        # **kwargs can be any additional parameters that requests.request accepts

        config = self.get_config()

        try:
            request_func = getattr(requests, method)
        except AttributeError:
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Invalid method: {0}".format(method)))

        url = self._base_url + endpoint
        kwargs['headers'] = {
            'x-api-key': self._api_key
        }

        try:
            r = request_func(
                            url,
                            verify=config.get('verify_server_cert', False),
                            **kwargs)
            self.debug_print("[DEBUG] r = {}".format(r))
        except Exception as e:
            self.debug_print("[DEBUG] error in make_rest_call. e = {}".format(e))
            return RetVal(action_result.set_status(phantom.APP_ERROR, "Error Connecting to server. Details: {0}".format(str(e))), r)
        return self._process_response(r, action_result)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        self.save_progress("Connecting to endpoint")
        ret_val, response = self._make_rest_call('/', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            self.save_progress("Test Connectivity Failed.")
            return action_result.get_status()

        self.save_progress("Test Connectivity Passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_on_poll(self, param):

        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # make rest call
        ret_val, response = self._make_rest_call('/questions', action_result, params=None, headers=None)

        if (phantom.is_fail(ret_val)):
            # self.debug_print("[DEBUG] response = {}".format(response))
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)
        for res in response:
            container = {}
            if 'artifacts' not in res:
                container['name'] = res['question']['name'] if 'name' in res['question'] else 'games container'
                container['severity'] = res['question']['severity'] if 'severity' in res['question'] else 'medium'
                container['tags'] = res['question']['container_tags'] if 'container_tags' in res['question'] else []
                container['source_data_identifier'] = res['r_id']
                container['due_time'] = res['question']['due_time'] if 'due_time' in res['question'] \
                    else datetime.strftime((datetime.utcnow() + timedelta(seconds=300)), '%Y-%m-%dT%H:%M:%S.%fZ')
                if 'artifacts' in res['question']:
                    container['artifacts'] = []
                    for art in res['question']['artifacts']:
                        c = {}
                        c['label'] = art['artifact_label'] if 'artifact_label' in art else 'artifact label'
                        c['name'] = art['artifact_name'] if 'artifact_name' in art else 'artifact name'
                        c['tags'] = art['artifact_tags'] if 'artifact_tags' in art else []
                        c['cef'] = art['cef'] if 'cef' in art else []
                        c['severity'] = art['severity'] if 'severity' in art else 'medium'
                        container['artifacts'].append(c)

            ret_val, msg, cid = self.save_container(container)
            if phantom.is_fail(ret_val):
                self.save_progress("Error saving container: {}".format(msg))
                self.debug_print("[DEBUG] Error saving container: {} -- CID: {}".format(msg, cid))
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_post_answer(self, param):

        # Implement the handler here
        # use self.save_progress(...) to send progress messages back to the platform
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))

        # Add an action result object to self (BaseConnector) to represent the action for this param
        action_result = self.add_action_result(ActionResult(dict(param)))

        # Access action parameters passed in the 'param' dictionary
        body = {}
        body['r_id'] = param['r_id']
        body['answer'] = param['answer']

        self.debug_print("submitted body = {}".format(json.dumps(body, indent=4)))

        # make rest call
        ret_val, response = self._make_rest_call('/answers',
                                                 action_result,
                                                 params=None,
                                                 headers=None,
                                                 json=body,
                                                 method="post")

        if (phantom.is_fail(ret_val)):
            return action_result.get_status()

        # Add the response into the data section
        action_result.add_data(response)

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        if 'points' in response:
            summary['points'] = response['points']
        if 'message' in response:
            summary['message'] = response['message']
        summary['status'] = response['status']

        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_perform_math(self, param):
        self.save_progress("In action handler for: {0}".format(self.get_action_identifier()))
        action_result = self.add_action_result(ActionResult(dict(param)))

        num1 = float(param['num1'])
        num2 = float(param['num2'])
        op = param['operation']
        ans = None

        if op == "+":
            ans = num1 + num2
        elif op == "-":
            ans = num1 - num2
        elif op == "*":
            ans = num1 * num2
        elif op == "/":
            if num2 != 0:
                ans = num1 / num2
            else:
                return self.add_action_result(ActionResult(dict(param)))
        elif op == "^":
            ans = num1 ** num2

        # Add the response into the data section
        action_result.add_data({"answer": ans})

        # Add a dictionary that is made up of the most important values from data into the summary
        summary = action_result.update_summary({})
        summary['answer'] = ans

        return action_result.set_status(phantom.APP_SUCCESS)

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'on_poll':
            ret_val = self._handle_on_poll(param)

        elif action_id == 'post_answer':
            ret_val = self._handle_post_answer(param)

        elif action_id == "perform_math":
            ret_val = self._handle_perform_math(param)

        return ret_val

    def initialize(self):

        # Load the state in initialize, use it to store data
        # that needs to be accessed across actions
        self._state = self.load_state()

        # get the asset config
        config = self.get_config()

        """
        # Access values in asset config by the name

        # Required values can be accessed directly
        required_config_name = config['required_config_name']

        # Optional values should use the .get() function
        optional_config_name = config.get('optional_config_name')
        """

        self._base_url = config.get('base_url')
        self._api_key = config.get('api_key')

        return phantom.APP_SUCCESS

    def finalize(self):

        # Save the state, this data is saved across actions and app upgrades
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            login_url = AutomationGamesConnector._get_phantom_base_url() + '/login'

            print ("Accessing the Login page")
            r = requests.get(login_url, verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = login_url

            print ("Logging into Platform to get the session id")
            r2 = requests.post(login_url, verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print ("Unable to get session id from the platform. Error: " + str(e))
            exit(1)

    with open(args.input_test_json) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = AutomationGamesConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id
            connector._set_csrf_info(csrftoken, headers['Referer'])

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
