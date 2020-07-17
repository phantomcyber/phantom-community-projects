# File: splunk_consts.py
# Copyright (c) 2014-2020 Splunk Inc.
#
# SPLUNK CONFIDENTIAL - Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
# --

# Success/Error status and messages
SPLUNK_ERR_INVALID_QUERY = "Query invalid '{query}'"
SPLUNK_SUCC_QUERY_EXECUTED = "Executed splunk query"
SPLUNK_ERR_BAD_STATUS = "The supplied status is invalid"
SPLUNK_ERR_CONNECTIVITY_TEST = "Connectivity test failed"
SPLUNK_SUCC_CONNECTIVITY_TEST = "Connectivity test passed"
SPLUNK_ERR_NOT_JSON = "Splunk server response was not JSON"
SPLUNK_ERR_NOT_200 = "Splunk server returned error from API call"
SPLUNK_ERR_CONNECTION_FAILED = "Failed to connect to splunk server"
SPLUNK_ERR_UNABLE_TO_CREATE_JOB = "Failed to get a job id from splunk server"
SPLUNK_ERR_GET_EVENTS = "Error getting events for alert '{ss_name}' having sid '{sid}'"
SPLUNK_ERR_NOT_ES = "This instance does not seem to be Splunk ES. This action cannot be run"
SPLUNK_ERR_CONNECTION_NOT_PRE_ESTABLISHED = "Connection to splunk server not yet established"
SPLUNK_ERR_INVALID_TIME_RANGE = "Invalid Time range specified, where the end time is less than start time"
SPLUNK_ERR_NEED_PARAM = "One of comment, status, integer_status, urgency, or owner parameters needs to be supplied to run this action"
SPLUNK_ERR_INVALID_PARAM = "Please provide non-zero positive integer in {param}"

# Progress messages
SPLUNK_PROG_GOT_JOB_ID = "Got job id '{job_id}'"
SPLUNK_PROG_TIME_RANGE = "Using range '{range}'"
SPLUNK_PROG_CREATED_QUERY = "Created query '{query}'"
SPLUNK_PROG_CREATING_SEARCH_JOB = "Creating search job"
SPLUNK_PROG_WAITING_ON_JOB_ID = "Waiting for job (id:{job_id}) to finish"
SPLUNK_PROG_CHECKING_STATUS_OF_JOB_ID = "Checking status of job id '{job_id}'"
SPLUNK_PROG_JOB_ID_DONE_RETRIEVING_RESULTS = "Retrieving results for job id '{job_id}'"

# Json keys
SPLUNK_JSON_COMMAND = "command"
SPLUNK_JSON_PARSE_ONLY = "parse_only"
SPLUNK_JSON_HOST = "host"
SPLUNK_JSON_DATA = "data"
SPLUNK_JSON_INDEX = "index"
SPLUNK_JSON_QUERY = "query"
SPLUNK_JSON_COUNT = "count"
SPLUNK_JSON_OWNER = "owner"
SPLUNK_JSON_SOURCE = "source"
SPLUNK_JSON_STATUS = "status"
SPLUNK_JSON_URGENCY = "urgency"
SPLUNK_JSON_COMMENT = "comment"
SPLUNK_JSON_ALERT_NAME = "alert"
SPLUNK_JSON_END_TIME = "end_time"
SPLUNK_JSON_TIMEZONE = "timezone"
SPLUNK_JSON_EVENT_IDS = "event_ids"
SPLUNK_JSON_START_TIME = "start_time"
SPLUNK_JSON_SOURCE_TYPE = "source_type"
SPLUNK_JSON_LAST_N_DAYS = "last_n_days"
SPLUNK_JSON_TOTAL_EVENTS = "total_events"
SPLUNK_JSON_UPDATED_EVENT_ID = "updated_event_id"

# Default values
SPLUNK_DEFAULT_EVENT_COUNT = 10
SPLUNK_DEFAULT_ALERT_COUNT = 100
SPLUNK_DEFAULT_SOURCE = "Phantom"
SPLUNK_DEFAULT_SOURCE_TYPE = "Automation/Orchestration Platform"

# HTML search strings:
SPLUNK_POST_DATA_WARN = '<msg type="WARN">'
SPLUNK_SERVER_VERSION = '<s:key name="version">'
SPLUNK_ES_NAME = '<title>SA-EndpointProtection</title>'

# Numeric constants
SPLUNK_MILLISECONDS_IN_A_DAY = 86400000
SPLUNK_NUMBER_OF_DAYS_BEFORE_ENDTIME = 10

# Dictionaries
SPLUNK_STATUS_DICT = {
        "unassigned": 0,
        "new": 1,
        "in progress": 2,
        "pending": 3,
        "resolved": 4,
        "closed": 5
    }

SPLUNK_SEVERITY_MAP = {
    'informational': 'low',
    'low': 'low',
    'medium': 'medium',
    'high': 'high',
    'critical': 'high'
}

# This will map certain splunk CIM fields to their CEF equivalent
CIM_CEF_MAP = {
    "action": "act",
    "action_name": "act",
    "app": "app",
    "bytes_in": "butesIn",
    "bytes_out": "bytesOut",
    "category": "cat",
    "dest": "destinationAddress",
    "dest_ip": "destinationAddress",
    "dest_mac": "destinationMacAddress",
    "dest_nt_domain": "destinationNtDomain",
    "dest_port": "destinationPort",
    "dest_translated_ip": "destinationTranlsatedAddress",
    "dest_translated_port": "destinationTranslatedPort",
    "direction": "deviceDirection",
    "dns": "destinationDnsDomain",
    "dvc": "dvc",
    "dvc_ip": "deviceAddress",
    "dvc_mac": "deviceMacAddress",
    "file_create_time": "fileCreateTime",
    "file_hash": "fileHash",
    "file_modify_time": "fileModificationTime",
    "file_name": "fileName",
    "file_path": "filePath",
    "file_size": "fileSize",
    "message": "message",
    "protocol": "transportProtocol",
    "request_payload": "request",
    "request_payload_type": "requestMethod",
    "src": "sourceAddress",
    "src_dns": "sourceDnsDomain",
    "src_ip": "sourceAddress",
    "src_mac": "sourceMacAddress",
    "src_nt_domain": "sourceNtDomain",
    "src_port": "sourcePort",
    "src_translated_ip": "sourceTranslatedAddress",
    "src_translated_port": "sourceTranslatedPort",
    "src_user": "sourceUserId",
    "transport": "transportProtocol",
    "url": "requestURL",
    "user": "destinationUserName",
    "user_id": "destinationUserId"
}

SPLUNK_INVALID_COMMAND = "Streaming/Transforming command operates on the events returned by some search.\
    So for using (eval, stats, table) commands, user should provide 'search' in 'command' parameter and provide whole query in the 'query' parameter"
