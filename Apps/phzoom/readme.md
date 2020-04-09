# Zoom Automation Project
## Objective


This project was created in response to a marked increase in work from home employees, which has inevitably led to a significant rise in Zoom usage. The objective of this project is to supplement log data provided by Zoom webhooks with important additional context (e.g., was the meeting password protected, was waiting room turned on). Additionally, we wanted to provide security practitioners to proactively ensure that security best practices are being followed with regards to Zoom meetings.

## The Documentation
This project is broken into several parts:
1. [Zoom App for Phantom](#zoom-app-for-phantom)
   - This provides automation capabilities for enriching Zoom log data as well as responding to unprotected Zoom meetings.
2. [Updated Splunk App for Phantom](#updated-splunk-app-for-phantom)
   - This app has been updated to provide key functionality to support the processes described in this documents. Specifically, the ability to modify kv stores via Phantom.
3. [Phantom Playbooks](#playbooks)
   - These playbooks have been created to demonstrate how Phantom can be leveraged in this context. They are meant to be modified to suit your organization's needs.
4. [Splunk Add-on for Zoom Enrichment](#splunk-add-on-for-zoom-enrichment)
   - This provides a number of kv store lookups used to store enrichment data retrieved by Phantom.
5. [Sample Splunk Queries](#sample-queries)
   - These includes recommended polling queries for ingesting Zoom data from Splunk to Phantom as well as some example queries of how to use the enrichment data.

## Zoom App for Phantom

### App Configurations (Zoom Side)
For the Zoom app for Phantom to be configured correctly, you must first create a JWT App in the your Zoom App Marketplace account. A JWT App can be created by going [here](https://marketplace.zoom.us/develop/create) and clicking the "Create" button under the "JWT" app type. Once you've created your JWT app you'll be provided with an **API Key** and and **API Secret**, keep track of these. They will be necessary for the configuration on Phantom side.

### App Configuration (Phantom Side)
The configuration of the Zoom App for Phantom requires three fields **API Key** and **API Secret** which are provided by Zoom. The third field is the "Base URL" field which is simply the base URL for the Zoom REST API. The default value provided, "https://api.zoom/us/v2" should not need to be changed.

### Actions
Actions are all fairly simple and documented with the normal app documentation process, for details please install the app and review the documentation at your leisure. That said, one of the main purposes of this app was to provide additional context about meetings that can only be provided via the Zoom API, most notably whether or not the meetings are being password protected.

The two actions that provide information on the configuration of passwords on meetings are **get meeting** and **get meeting invite**. Get meeting should be invoke when a "meeting.started" event is ingested from Phantom. The **get meeting** API call provides tons of detail, but will only successfully run against currently in-flight meetings. Further details on how to ingest and act on Zoom events are provided [here](#ingesting-zoom-alerts)

**get meeting invite** should be invoked when the "meeting.created" event  is ingested by phantom. This command call the meeting invite API endpoint and parses the relevant details from in, namely the password, if there is one. 

These two actions will give you date that can be used to gain insight into who is running unprotected meetings, how often, and what are the topics of those meetings.

## **Updated** Splunk App for Phantom

### Update Details
This updated Splunk App for Phantom will allow you to add (**add kvstore data**) and remove (**remove kvstore data**) data from existing KV stores in Splunk. The playbooks provided as part of this project leverage these actions to bring the enrichment data from the **get meeting** and **get meeting invite** actions back to Splunk.

### Configuring the on poll query and related fields
There are plenty of ways to ingest data from Splunk to Phantom, however for the lowest friction we've chosen to go with a polling action from Phantom. In this case Phantom is configured to make an outbound connection to Splunk, run a predefined query, and ingest the results.

The fields required for configuration are as follows:
- Query to use with On Poll
  - We recommend starting with a query like the following `index=<your_index> sourcetype="zoom:webhook" earliest=-15m ((event="meeting.created" AND payload.object.start_time=*) OR event="meeting.started") | rename payload.object.topic as topic, payload.object.host_id as host_id, payload.object.id as meeting_id | table _time, event, topic, host_id, meeting_id`
  - This will ingest all meeting.started events as well as the creation of any future meetings.
- Fields to save with On Poll
  - This field tells Phantom which fields from the query results you want to save in the Phantom event.
  - If you're using our recommended query, it should be populated with `_time, event, topic, host_id, meeting_id`
- Name to give containers created via ingestion
  - This will serve as a prefix to our even name in Phantom - we recommend `Zoom:`
- Values to append to container name
  - This fields defines field names from your query results that will be used dynamically to create your Phantom event name.
  - We recommend using the meeting topic and time by using these two fields: `topic, _time`

## Playbooks
Currently, four playbooks are provided to demonstrate the functionality provided by the Zoom App and updated Splunk App. You may find these useful, but it is recommended you modify them before putting them insto production:

1. Zoom Meeting Enrichment
   - This playbook is designed to respond to ingested meeting.started. It will get the information from the in-flight meeting, get information about those host of that meeting, and send the meeting details to the zoom_meeting_details kvstore provided in the Splunk Add-on for Zoom Enrichment
   - Additionally, if it is discovered that no password set on the meeting, an educational email will be sent to the meeting host informing them of the risks of unprotected Zoom meetings.
   - Finally, a step that will update the meeting host's settings to require passwords on all meeting types and require waiting rooms.
   - Modification Recommendations:
     - Review the email message and customize it to what you want.
     - Decide if you really want to update user settings, and if so, make sure you're comfortable with each of the applicable settings to the action. Additionally, you may want to include information about modified user settings to your message to the meeting host.
     - Make sure the `from address` of the `send email` action has your desired email address.
2. Zoom Scheduled Meeting Enrichment
   - This playbook is designed to respond to ingested meeting.created events with a future start_time (i.e., future meetings). It will get the meeting invite for the meeting, get information about the host of the meeting, and send the meeting invite details to the zoom_meeting_invites kvstore provided by the Splunk Add-on for Zoom Enrichment.
   - Additionally, if it is discovered that no password is set on the meeting, the meeting will be updated with a password, and an education email will be sento the meeting host informing them of the change and the risk of unprotected Zoom meetings.
   - Note: The `get meeting info` action will not run against future scheduled meetings, however the `get meeting invite` action can be used. This gives less information than `get meeting info` but it *does* provide enough information to determine if a password has been set on the meeting.
   - Modification Recommendations:
     - Review the email message and customize it to what you want.
     - Decide if you really enforce a password on the scheduled meeting. If not, you may want to modify the meeting_host notification message.
     - Make sure the `from address` of the `send email` action has your desired email address.
3. Zoom User Enrichment
   - This playbook is designed to enrich zoom user data - likely user host (if you're using the same ingestion queries we recommended, the user_id will be the `host_id` from the ingested events). This will get general user information (e.g., user email, timezone, etc.) as well as user settings (e.g., require password on newly scheduled meetings), it will also update the kvstores zoom_user_details and zoom_user_settings provided by the Splunk Add-on for Zoom Enrichment.
   - Additionally, if it is discovered that passwords and/or waiting rooms are not enabled on the user account in question, it will send an educational email to the user informing them of the risks of unprotected zoom meetings.
   - Modification Recommendations:
     - Review the email message and customize it to what you want.
     - Make sure the `from address` of the `send email` action has your desired email address.
4. Zoom Meeting Post Mortem
   - This playbook is designed to get information on files transferred in Zoom chat during the course of an ended meeting. It will send this information to the zoom_meeting_files kvstore provided by the Splunk Add-on for Zoom Enrichment.
   - Note: Files are only available for 24 hours after a meeting ends.
   - Modification Recommendations:
     - N/A

## Splunk Add-on for Zoom Enrichment

This app is disigned to provide kvstores for zoom enrichment data provided by phantom.

1. zoom_meeting_details
   - Used to store rich details about Zoom meetings. Can only be populated while a meeting is actively in session.
3. zoom_meeting_invite
   - Used to store meeting invite details for future scheduled meetings.
4. zoom_user_settings
   - Used to store user settings for Zoom users.
5. zoom_user_details
   - Used to store user profile information for Zoom users.
6. zoom_meeting_files
   - Used to store meetings about files transfered durign the course of a zoom meeting.

## Sample queries

As noted the recommended ingestion query to be implemented with the phantom polling action is:
- `index=<your_index> sourcetype="zoom:webhook" earliest=-15m ((event="meeting.created" AND payload.object.start_time=*) OR event="meeting.started") | rename payload.object.topic as topic, payload.object.host_id as host_id, payload.object.id as meeting_id | table _time, event, topic, host_id, meeting_id`

Finding meetings that took place, or are in progess that had no password applied:
- `index=<your index> sourcetype="zoom:webhook" event="meeting.started" | lookup zoom_meeting_details id as payload.object.id | search NOT(encrypted_password=*)`

Finding meetings that are scheduled, but have no password:
- `sourcetype="zoom:webhook" event="meeting.created" payload.object.start_time=* | lookup zoom_meeting_invites meeting_id as payload.object.id | search NOT(password=*)`

Finding users that do not have passwords required and/or do not require waiting room functionality
- `sourcetype="zoom:webhook" event="meeting.started" | lookup zoom_user_settings user_id as payload.object.host_id | search (schedule_meeting_require_password_for_scheduling_new_meetings=0 OR schedule_meeting_require_password_for_instant_meetings=0 OR schedule_meeting_require_password_for_pmi_meetings="none" OR in_meeting_waiting_room="0")`

