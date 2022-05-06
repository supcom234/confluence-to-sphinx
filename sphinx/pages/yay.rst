.. contents::
   :depth: 3
..

Top of Page

v3.7 Deployable Interceptor Platform (DIP)  

| 
| TROUBLESHOOTING

| 
| CYBERSPACE VULNERABILITY ASSESSMENT/
| HUNTER WEAPON SYSTEM

| 
| HANDLING AND DESTRUCTION NOTICE
| - Handle in compliance with distribution statement and destroy by any
  method that will prevent disclosure of contents or reconstruction of
  the document.  

**This Section is part of a Framework for future use. The information
contained within, and on subsequent pages may be minimal or temporary.
Sections will continue to have information populated as relevant
instructions or processes become available**

       

v3.7 DIP Troubleshooting Guide page is non-hardware specific and is
applicable to both R440 Common Node and Legacy versions

| 

3

Introduction
============

Return to Top

Installation Troubleshooting
============================

Handling a Failure on Installation  
------------------------------------

A large amount of troubleshooting and debugging has gone into ensuring
the installer functions as expected when employed per the direction of
the developers.  However, the system is very complex, and a large
variety of errors can still occur.  The overall process to be followed
when installation errors present themselves is to take note of which
portion of the system failed, contact the developers with screenshots
showing the error that occurred, and attempt to resume the install from
the point that it originally failed rather than restarting the entire
build from the beginning.  Rebuilding the entire system requires
prohibitive amounts of time and should only be necessary for the most
extreme circumstances.

#. If the installation fails:

   #. Take note of the specific point in the installation at which the
      failure occurred 
   #. Which component was being installed?  Which task was Ansible
      performing?
   #. Is there any useful information to be seen in the error messages?

#.  Log in to the ServiceNow portal
   (\ \ https://afdco.servicenowservices.com/sp\ ) if the installation
   fails:      

   #. Take note of the specific point in the installation at which the
      failure occurred.
   #. Which component was being installed?  
   #. Which task was Ansible performing?
   #. Check for error messages on the Portal page under the
      Notifications bell icon.
   #. Is there any useful information to be seen in the error messages?

   | 

#. Ansible tends to produce a very verbose error output and it can be
   difficult to find which portion(s) of it are relevant.

   All information should be examined carefully for clues.

#. The TFPlenum subsystem is comprised of several different components
   that make up the system.  Debugging the installation process begins
   with knowing which component specifically caused the error before the
   why can be determined.

   #. Take a screenshot of the error (depending on the host OS, this can
      be done in a variety of ways):

      #. On Red Hat Linux:

         #. Verify gnome-screenshot is installed or install it (if
            necessary) using the following command:

            textyum -y install gnome-screenshot

         #. Start gnome-screenshot using the following command:

            textgnome-screenshot

         #. Press \ **Fn + PrntScrn **\ to take a screenshot of
            the entire screen
         #. Press\ ** Fn + Alt + PrntScrn **\ to take a screenshot of
            just the active window

            Screenshots will be saved to
            the\ ** **\ Pictures\ ** **\ directory in the current user's
            home directory.

      #. Using the Snipping tool on Windows:

         #. Type \ **Snipping Tool **\ in the Cortana search bar in the
            bottom left 
            Click the labeled icon when it appears in the results (a
            small Snipping Tool window will appear)
         #. To create a new snip:

            #. Click \ **New** and all the operative displays will be
               covered with a translucent white overlay (the cursor will
               be replaced with crosshairs)
            #. Use the crosshairs cursor to click and drag a rectangle
               containing the area of the screen that needs to be in the
               screenshot (i.e., the window containing the PuTTY session
               or VM window)
            #. Release the mouse button and the Snipping Tool will bring
               up a picture containing the contents of the rectangle
               created
            #. Click \ **File** and **Save As** to save this picture

   #. Refer to \ `Section 4. Bug Reporting and System Change/Enhancement
      Requests <https://confluence.di2e.net/pages/viewpage.action?pageId=275360146>`__\ ** **\ to
      gain access and obtain User Guide
   #. Create an incident (INC) ticket through the assigned DANS On-Site
      Support (DOSS) or Service Desk queue explaining the error to be
      forwarded to the developer team for review
      **ServiceNow Service Portal** 
   #. Accessing site

      #. Select  \ **Get-Help >** **Can We Help You?**  
      #. Determine the support needed (CPT, MDT, etc.)
      #. The summary should contain a brief description of the error
      #. The problematic component/s should contain the basic system (
         i.e. Server, Sensor, Switch, etc.)
      #. Make use of the drop-down menu
      #. The description should contain as much pertinent information
         about the error as can be supplied (i.e. snippets of the
         messages, what may be wrong, etc.)
      #. Urgency should contain an honest assessment of how urgent the
         error is
      #. Scroll down to the Attachment field 

         #. Attach all pertinent screenshots of the error
         #. This can be done with the \ **Add Attachments** link
         #. Fill in any pertinent information
         #. Click\ ** Submit **\ and the assigned Service Desk team will
            reach out to the contact provided as soon as possible to
            further troubleshoot and resolve the error if necessary 

 Return to Top

Pod Errors  
------------

**Handling Pod Failures**

Return to Top

**Kube-System Errors**

#. After a power failure, go to the Health page to verify that all pods
   are up

#.  If there is a failure on any pod, ssh into the controller and type
   the following command in the terminal:

   textkubectl get pods -n kube-system

#. Find all pod names in an error state and enter the following:

   textkubectl delete pod <pod_name> -n kube-system

#. Wait two minutes and make sure all Kube-system pods are running
   before continuing 

Return to Top

**Elastic-System Errors**

#.  If there is a failure on any pod, ssh into the controller and enter
   the following command in the terminal:

   textkubectl get pods -n elastic-system

#. Find all pod names in an error state and enter the following:

   textkubectl delete pod <pod_name> -n elastic-system

#. Wait five minutes and make sure all elastic-system pods are running
   before continuing
#. All Default pods should now be running; if not, perform Default
   Errors steps

Return to Top

**Default Errors **

#.  If there is a failure on any pod, ssh into the controller and enter
   the following command in the terminal:

   textkubectl get pods

#. Find all pod names in an error state and enter the following:

   textkubectl delete pod <pod_name>

#. Wait until all pods are running 

Return to Top

**Restart Frontend**

After all, pods are deleted and have come back up, issue the following
command:

textSystemctl restart tfplenum-frontend.service celery.service

Return to Top

Wikijs
------

Wikijs Installation
~~~~~~~~~~~~~~~~~~~

Return to Top

Deleting Pages
~~~~~~~~~~~~~~

When deleting a Wikijs page that has comments on the page, the following
error message may appear.

"Delete from pages where id = 1 - Cannot delete or update a parent row:
a foreign key constraint fails (wikijs-db.comments, CONSTRAINT
comments_pageid_foreign FOREIGN KEY ( pageId) REFERENCES pages (id))"

To avoid this error, delete all comments on the page before deleting the
page. This is a known error in Wikijs 2.4 and is corrected in 2.5. CVA/H
version 3.4 uses Wikijs 2.4. Current plans are to upgrade to Wikijs 2.5
in CVA/H 3.5.

Return to Top

Diagnostic Tool
===============

Run Diagnostics 
----------------

#. Execute the following command from the controller:  

   bashcd /opt/tfplenum/scripts/diagnostics bash ./run.sh

#. The script will check the system and return a tar file with all the
   logs on the system    

#. Go to the directory where the downloaded file is. Then zcat the zip
   file. to view logs.

   GUI Diagnostics

   The script above can be done through the GUI. 

Return to Top

Download Diagnostics   
-----------------------

#. Log in to the Controller UI and navigate to the PMO support page 
#. Click on the Download button to download diagnostics
#. Check downloads directory for diagnostics 
#. Unzip the *diagnostics.zip* folder  
    
   **Diagnostic Download**

Return to Top

How to Troubleshoot Application Errors 
---------------------------------------

Basic Troubleshooting Steps 
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The art of troubleshooting is very much like that of forming a
scientific hypothesis. The first step is to clarify the problem,
consider an alternate explanation, formulate a hypothesis and test a
hypothesis.

**Troubleshooting**:  It is the process of defining, diagnosing, and
solving

**Analogies:** Has the problem occurred before?

**Do not make assumptions:** Collect as much data as possible and fully
exhaust possible hypotheses. 

Return to Top

**Web Errors**
~~~~~~~~~~~~~~

1.  Go to the directory containing error logs for the system
*/var/log/tfplenum*

2. tail -f gunicorn_access.log

| 3. Check the status code to see the error
| **Match Code **

+--------------------+-------------------------------------------------+
| Code               | Description                                     |
+====================+=================================================+
| 200                | Success/OK                                      |
+--------------------+-------------------------------------------------+
| 301                | Permanent Direction                             |
+--------------------+-------------------------------------------------+
| 302                | Temporary Redirection                           |
+--------------------+-------------------------------------------------+
| 304                | Not Modified                                    |
+--------------------+-------------------------------------------------+
| 401                | Unauthorized Error                              |
+--------------------+-------------------------------------------------+
| 403                | Forbidden                                       |
+--------------------+-------------------------------------------------+
| 404                | Not Found                                       |
+--------------------+-------------------------------------------------+
| 405                | Method Not Allowed                              |
+--------------------+-------------------------------------------------+
| 501                | Not Implemented                                 |
+--------------------+-------------------------------------------------+
| 502                | Bad Gateway                                     |
+--------------------+-------------------------------------------------+
| 504                | Service Unavailable                             |
+--------------------+-------------------------------------------------+
| 504                | Gateway Timeout                                 |
+--------------------+-------------------------------------------------+

Return to Top

Catalog Apps not Appearing
~~~~~~~~~~~~~~~~~~~~~~~~~~

#. Open your controller frontend page
#. Use F12 to pull up developer tools and navigate to the Networking tab
#. Use the inspector mouse scope and hover over the app
#. Return to the Networking Response page
#. Compare it to the status code; if it is 200, then it is good
#. Anything else that points to a problem and needs further
   investigation check knowledge bases

   #. Confluence
   #. Helpdesk database of similar reported issues
   #. Go to the opensource community to see if bugs like this are being
      reported with any FOSS

#. Google is another source-- Copy the entire error log message into
   Google 
   Use this for forming your troubleshooting hypothesis

Return to Top

Controller Lockout
==================

Enabling Super Admin Account
----------------------------

The other initially created account is the \ **superadmin** account in
the Master Realm, which has admin permission across the entire Keycloak
instance.  This account is for emergencies and certain automated
processes and should not be used by the operators or maintenance
personnel. This account can create/modify/delete the different realms
within Keycloak and can cause significant damage if used incorrectly. 
The only time the operators should use this account to log in to
Keycloak is to reset the **admin** account password if lost or
forgotten.

**To Log in as Superadmin to Reset Admin Password:**

#. SSH to the controller
#. Edit the tfplenum apache config file and remove the blocks for the
   master realm console.

   #. */etc/httpd/conf.d/tfplenum.conf*, ~lines 92-99.
   #. use # to comment out those lines

#. Restart the Apache service:  systemctl restart httpd
#. Get the password from \ *cat
   /opt/sso-idp/sso_admin_password.txt*\ ``(copy password)``\ ````
#. The username is \ **superadmin**
#. Go to controller *https://dip-controller.lan/auth/admin/*
#. Enter username and password
#. The page will redirect to the admin console for the CVAH realm
   **Admin Console**
#. Click \ **Users** then **View all users** and then edit for the admin
   username
   **View and Edit Users**
#. Click \ **Credentials**
#. Enter a **new password** and click \ **Reset Password
   **\ Deselecting \ **Temporary **\ will avoid being prompted to change
   the password at the next login
   **Reset Password**
#. Re-comment the lines in the *tfplenum.conf* file and restart apache 
    

**Once the password is reset disable the super admin account.**

Return to Top\ **
**

 Recovering from Disk Fill Ups
==============================

The stack requires active monitoring of the disks, failure to do so
could result in Kibana being unreachable due to disk fill ups.  If the
disk does fill up, the kit has a safety built-in with the watermark
settings.

During operations, it is recommended that the disks on the server side
are periodically monitored on the left Kibana Navbar -> **Stack
Monitoring** page.  It is recommended to periodically back up and remove
data the user wants to keep as the disks fill up on the server side (ie:
Elasticsearch cluster).  The sensors will automatically do rolling
deletes of the old raw PCAP data when the disk reaches the 75%
threshold. 

Return to Top

Kibana Failure Instructions
---------------------------

If the disks fill up and Kibana is no longer accessible, the following
instructions can be run to get the cluster back up and running in short
order.

#. From the MIP ssh to the controller with **ssh root@<ctrl_ip>**
#. Perform the following curl commands:

   bashtrue[root@controller ~]# ELASTIC_PASSWORD=$(kubectl get secret
   tfplenum-es-elastic-user --template={{.data.elastic}} \| base64
   --decode) [root@controller ~]# curl -XGET -u
   elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/_cat/health?v"
   epoch timestamp cluster status node.total node.data shards pri relo
   init unassign pending_tasks max_task_wait_time active_shards_percent
   1637006305 19:58:25 tfplenum yellow 8 4 160 80 0 0 0 0 - 100.0%
   [root@controller ~]# curl -XGET -u elastic:$ELASTIC_PASSWORD
   "https://elasticsearch:9200/_cat/allocation?v" shards disk.indices
   disk.used disk.avail disk.total disk.percent host ip node 40 663.9mb
   3gb 3.9gb 4.9gb 90 10.233.3.21 10.233.3.21 tfplenum-es-data-3 40
   844.5mb 3gb 3.9gb 4.9gb 90 10.233.3.15 10.233.3.15 tfplenum-es-data-1
   40 995.6mb 3.1gb 3.8gb 4.9gb 90 10.233.17.14 10.233.17.14
   tfplenum-es-data-2 40 549.6mb 3.1gb 3.8gb 4.9gb 90 10.233.17.11
   10.233.17.11 tfplenum-es-data-0 [root@controller ~]# curl -XGET -u
   elastic:$ELASTIC_PASSWORD
   "https://elasticsearch:9200/_cat/indices/*?v=true&s=store.size:desc&h=index,store.size"
   index store.size metricbeat-7.13.1-2021.11.11-000001 746.5mb
   auditbeat-internal-2021.11.11-000001 579.4mb
   filebeat-zeek-2021.11.11-000001 547.5mb sessions2-211112h00 261.9mb
   metricbeat-7.13.1-2021.11.15-000002 211.5mb
   filebeat-suricata-2021.11.11-000001 203.1mb
   auditbeat-internal-2021.11.15-000002 70.1mb .kibana_7.13.1_001 54.7mb

#. **(Recommended approach)** Identify the indexes to backup before
   either removing the index or performing a delete from query API.

   The **\_delete_by_query** API will not work if the flood threshold
   has been triggered because the API attempts to mark the documents as
   deleted which requires write operations to be active on the index. 
   It is recommended to back up and then delete a large enough index to
   get things going again before executing the **\_delete_by_query,**
   and **\_force\ \_\ merge** API calls.  Deleting a large enough index
   will cause Elasticsearch to remove the read_only_allow_delete flag
   from all of its indexes thus allowing the user to execute writes
   again.

   The **\_delete_by_query **\ API only marks the queried documents as
   deleted.  It does not clear the disk.  To force a disk cleanup on
   documents that have been deleted use the **\_force\ \_\ merge** API
   call.  See the example below for more details.

   | 

   #. Ensure that a bucket has been created on the Minio Server

      #. Navigate to *http://<minio IP>:9000/buckets* and login with
         assessor/PMO provided password
      #. Click on **Create Bucket** and give it a name

   #.  Recommended first verify there is enough space allocated on the
      Minio server for backing up data

      #. Navigate to *http://<minio IP>:9000/dashboard* and login with
         assessor/PMO provided password
      #. Click on the **Drives** to show the capacity 
         Keep the amount of storage available in mind while planning on
         which indexes/data will be backed up

   #. Perform the following instruction to create the snapshot:

      bash# Verify that minio is setup curl -XGET -u
      elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/_snapshot" #
      If the S3 bucket is not setup run the following command. (NOTE:
      <REPO_NAME> can be any arbitrary name of your choosing. The
      <BUCKET NAME> must match the bucket created on the minio server
      console. curl -XPUT -u elastic:$ELASTIC_PASSWORD
      "https://elasticsearch:9200/_snapshot/<REPO_NAME>" -H
      'Content-Type: application/json' -d' { "type": "s3", "settings": {
      "bucket": "<BUCKET NAME>", "client": "default", "endpoint":
      "<MINIO IP ADDRESS>:9001", "protocol": "http" } }' curl -XGET -u
      elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/_snapshot" #
      To take a snapshot run the following command. Replace the the
      example indices below with the ones user wishes to backup. curl
      -XPUT -u elastic:$ELASTIC_PASSWORD
      "https://elasticsearch:9200/_snapshot/tfplenum/sessions_backup?wait_for_completion=false"
      -H 'Content-Type: application/json' -d' { "indices":
      "sessions2-170518h06,sessions2-211111h18", "ignore_unavailable":
      true, "include_global_state": false, "metadata": { "taken_by":
      "Operator", "taken_because": "backup before deletion" } }' # If
      the user is positive the deletion of the index is not in use by
      the system, delete the indexes with the following curl command.
      (NOTE: Replace the sessions2-170518h06,sessions2-211111h18, with
      the indexes you wish to delete.) curl -XDELETE -u
      elastic:$ELASTIC_PASSWORD
      "https://elasticsearch:9200/sessions2-170518h06,sessions2-211111h18"
      # If the read_only_allow_delete flag is no longer set, the user
      can execute \_delete_by_query API calls instead of deleting entire
      indexes if they so desire. curl -XGET -u elastic:$ELASTIC_PASSWORD
      "https://elasticsearch:9200/filebeat-external-cold-log-system/_settings"
      \| grep read_only_allow_delete # DO NOT DELETE the index unless
      the user is positive it is not being actively written to. When in
      doubt, run a delete by query with a match_all clause. curl -XPOST
      -u elastic:$ELASTIC_PASSWORD
      "https://elasticsearch:9200/sessions2-170518h06,sessions2-211111h18/_delete_by_query?wait_for_completion=false"
      -H 'Content-Type: application/json' -d' { "query": { "match_all":
      {} } }' #Upon successful completion of the above POST command, the
      user will receive a task ID which the user may subsequently check
      that status of the job with. curl -XGET -u
      elastic:$ELASTIC_PASSWORD
      "https://elasticsearch:9200/_tasks/<TASK_ID>" #After the task is
      completed run the following replacing the <INDEX_NAME> with the
      index that the user wishes to force deletions. curl -XPOST -u
      elastic:$ELASTIC_PASSWORD
      "https://elasticsearch:9200/<INDEX_NAME>/_forcemerge?max_num_segments=1"
      # This command will force the deletion of the documents removed
      and clear the disk space for any of the delete by queries that
      were previously executed.

#. **(Secondary approach)** Use the delete by query API\ ** **\ for the
   data the user wishes to simply delete without doing backups.  This is
   the safest way to remove data without causing issues with indexes
   that are still in use.  If certain that a particular index is no
   longer in use, delete the index.

   The **\_delete_by_query** API will not work if the flood threshold
   has been triggered because the API attempts to mark the documents as
   deleted which requires write operations to be active on the index. 
   It is recommended to back up and then delete a large enough index to
   get things going again before executing the **\_delete_by_query,**
   and **\_force\ \_\ merge** API calls.  Deleting a large enough index
   will cause Elasticsearch to remove the read_only_allow_delete flag
   from all of its indexes thus allowing the user to execute writes
   again.

   bash# If the read_only_allow_delete flag is no longer set, the user
   can execute \_delete_by_query API calls instead of deleting entire
   indexes if they so desire. curl -XGET -u elastic:$ELASTIC_PASSWORD
   "https://elasticsearch:9200/filebeat-external-cold-log-system/_settings"
   \| grep read_only_allow_delete # Delete old indexes if they are not
   longer being used or written to. curl -XDELETE -u
   elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/<INDEX_NAME>" #
   It is recommended to first do a query to see which data will be
   affected. The below query will query all data on all session2-\*
   indices older than 12 days. curl -XGET -u elastic:$ELASTIC_PASSWORD
   "https://elasticsearch:9200/sessions2-*/_search" -H 'Content-Type:
   application/json' -d' { "query": { "range": { "timestamp": { "lt":
   "now-12d/d" } } } }' # Tune the query to the liking before executing
   the next step. # Run the following delete by query command with the
   modified query body if user modified it from the example above. curl
   -XPOST -u elastic:$ELASTIC_PASSWORD
   "https://elasticsearch:9200/sessions2-*/_delete_by_query?wait_for_completion=false"
   -H 'Content-Type: application/json' -d' { "query": { "range": {
   "timestamp": { "lt": "now-12d/d" } } } }' #Upon successful completion
   of the above POST command, the user will receive a task ID which you
   may subsequently check that status of the job with. curl -XGET -u
   elastic:$ELASTIC_PASSWORD
   "https://elasticsearch:9200/_tasks/<TASK_ID>" #After the task is
   completed run the following replacing the <INDEX_NAME> with the index
   that the user wishes to force deletions. curl -XPOST -u
   elastic:$ELASTIC_PASSWORD
   "https://elasticsearch:9200/<INDEX_NAME>/_forcemerge?max_num_segments=1"
   # This command will force the deletion of the documents removed and
   clear the disk space for any of the delete by queries that were
   previously executed.

#. | After clearing out a significant amount of data, force deleting the
     Kibana pod will speed up the restart time for Kibana   
   | If there is sufficient disk cleared up on the servers, Kibana will
     come back up as expected

   bash[root@controller ~]# kubectl get pods \| grep tfplenum-kb
   tfplenum-kb-cfd498774-gqzx9 1/1 Running 0 105m [root@controller ~]# k
   delete pod tfplenum-kb-cfd498774-gqzx9 --force

Return to Top
