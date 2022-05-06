v3.7 Deployable Interceptor Platform (DIP) Troubleshooting Guide
================================================================
.. _e4463d54:

v3.
7 Deployable Interceptor Platform (DIP)




CYBERSPACE VULNERABILITY ASSESSMENT/

HUNTER WEAPON SYSTEM


   .. figure:: /images/CVAH\ Shields.jpg
      :height: 202px


HANDLING AND DESTRUCTION NOTICE

- Handle in compliance with distribution statement and destroy by any method that will prevent disclosure of contents or reconstruction of the document.  



::

   This Section is part of a Framework for future use. The information contained within, and on subsequent pages may be minimal or temporary. Sections will continue to have information populated as relevant instructions or processes become available.



::

   v3.7 DIP Troubleshooting Guide page is non-hardware specific and is applicable to both R440 Common Node and Legacy versions.






Introduction
------------


Return to Top
:ref:`Top of Page <e4463d54>`

Installation Troubleshooting
----------------------------



Handling a Failure on Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Handling a Failure on Installation  


::

   A large amount of troubleshooting and debugging has gone into ensuring the installer functions as expected when employed per the direction of the developers.  However, the system is very complex, and a large variety of errors can still occur.  The overall process to be followed when installation errors present themselves is to take note of which portion of the system failed, contact the developers with screenshots showing the error that occurred, and attempt to resume the install from the point that it originally failed rather than restarting the entire build from the beginning.  Rebuilding the entire system requires prohibitive amounts of time and should only be necessary for the most extreme circumstances.



1. If the installation fails:
2. Log in to theServiceNow portal (https://afdco.servicenowservices.com/sp) if the installation fails:
3. Ansible tends to produce a very verbose error output and it can be difficult to find which portion(s) of it are relevant.

::

   All information should be examined carefully for clues.

4. The TFPlenum subsystem is comprised of several different components that make up the system.  Debugging the installation process begins with knowing which component specifically caused the error before the why can be determined.

 
:ref:`Top of Page <e4463d54>`

Pod Errors
^^^^^^^^^^


Handling Pod Failures
**Handling Pod Failures**

Return to Top
:ref:`Top of Page <e4463d54>`
Kube-System Errors
**Kube-System Errors**


1. After a power failure, go to the Health page to verify that all pods are up
2. If there is a failure on any pod, ssh into the controller and type the following command in the terminal:

::

   kubectl get pods -n kube-system

3. Find all pod names in an error state and enter the following:

::

   kubectl delete pod <pod_name> -n kube-system

4. Wait two minutes and make sure all Kube-system pods are running before continuing

Return to Top
:ref:`Top of Page <e4463d54>`
Elastic-System Errors
**Elastic-System Errors**


1. If there is a failure on any pod, ssh into the controller and enter the following command in the terminal:

::

   kubectl get pods -n elastic-system

2. Find all pod names in an error state and enter the following:

::

   kubectl delete pod <pod_name> -n elastic-system

3. Wait five minutes and make sure all elastic-system pods are running before continuing
4. All Default pods should now be running; if not, perform Default Errors steps

Return to Top
:ref:`Top of Page <e4463d54>`
Default Errors
**Default Errors**


1. If there is a failure on any pod, ssh into the controller and enter the following command in the terminal:

::

   kubectl get pods

2. Find all pod names in an error state and enter the following:

::

   kubectl delete pod <pod_name>

3. Wait until all pods are running

Return to Top
:ref:`Top of Page <e4463d54>`
Restart Frontend
**Restart Frontend**

After all, pods are deleted and have come back up, issue the following command:

::

   Systemctl restart tfplenum-frontend.service celery.service


Return to Top
:ref:`Top of Page <e4463d54>`

Diagnostic Tool
---------------



Run Diagnostics
^^^^^^^^^^^^^^^



1. Execute the following command from the controller:

::

   cd /opt/tfplenum/scripts/diagnostics
   bash ./run.sh

2. The script will check the system and return a tar file with all the logs on the system
3. Go to the directory where the downloaded file is locatedThen zcat the zip file to view logs

::

   GUI DiagnosticsThe script above can be done through the GUI.


Return to Top
:ref:`Top of Page <e4463d54>`

Download Diagnostics
^^^^^^^^^^^^^^^^^^^^



1. Log in to the Controller UI and navigate to the PMO support page
2. Click on the Download button to download diagnostics
3. Check downloads directory for diagnostics
4. Unzip thediagnostics.zipfolderDiagnostic Download
5. 
   .. figure:: /images/diagnostics.png


Return to Top
:ref:`Top of Page <e4463d54>`

How to Troubleshoot Application Errors
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^



Basic Troubleshooting Steps
:::::::::::::::::::::::::::


The art of troubleshooting is very much like that of forming a scientific hypothesis.
 The first step is to clarify the problem, consider an alternate explanation, formulate a hypothesis and test a hypothesis.


**Troubleshooting**
:  This is the process of defining, diagnosing, and solving

**Analogies:**
 Has the problem occurred before?

**Do not make assumptions:**
 Collect as much data as possible and fully exhaust possible hypotheses. 

Return to Top
:ref:`Top of Page <e4463d54>`

Web Errors
::::::::::

**Web Errors**

1.  Go to the directory containing error logs for the system 

2. tail

3. Check the status code to see the error


**Match Code**

+-----------------------+-----------------------+
| Code                  | Description           |
+=======================+=======================+
| 200                   | Success/OK            |
+-----------------------+-----------------------+
| 301                   | Permanent Direction   |
+-----------------------+-----------------------+
| 302                   | Temporary Redirection |
+-----------------------+-----------------------+
| 304                   | Not Modified          |
+-----------------------+-----------------------+
| 401                   | Unauthorized Error    |
+-----------------------+-----------------------+
| 403                   | Forbidden             |
+-----------------------+-----------------------+
| 404                   | Not Found             |
+-----------------------+-----------------------+
| 405                   | Method Not Allowed    |
+-----------------------+-----------------------+
| 501                   | Not Implemented       |
+-----------------------+-----------------------+
| 502                   | Bad Gateway           |
+-----------------------+-----------------------+
| 504                   | Service Unavailable   |
+-----------------------+-----------------------+
| 504                   | Gateway Timeout       |
+-----------------------+-----------------------+


Return to Top
:ref:`Top of Page <e4463d54>`

Catalog Apps not Appearing
::::::::::::::::::::::::::



1. Open the controller frontend page
2. Use F12 to pull up developer tools and navigate to the Networking tab
3. Use the inspector mouse scope and hover over the app
4. Return to the Networking Response page
5. Compare it to the status code; if it is 200, then it is good
6. Check knowledge bases for anything else that points to a problem and needs further investigation
7. Google is another source -- copy the entire error log message into GoogleUse this for forming a troubleshooting hypothesis

Return to Top
:ref:`Top of Page <e4463d54>`

Controller Lockout
------------------



Enabling Super Admin Account
^^^^^^^^^^^^^^^^^^^^^^^^^^^^


The other initially created account is the superadmin account in the Master Realm, which has admin permission across the entire Keycloak instance.
  This account is for emergencies and certain automated processes and should not be used by the operators or maintenance personnel.
 This account can create/modify/delete the different realms within Keycloak and can cause significant damage if used incorrectly.
  The only time the operators should use this account to log in to Keycloak is to reset the admin account password if lost or forgotten.


To Log in as Superadmin to Reset Admin Password:
**To Log in as Superadmin to Reset Admin Password:**


1. SSH to the controller
2. Edit the tfplenum Apache config file and remove the blocks for the master realm console
3. Restart the Apache service:systemctl restart httpd
4. Get the password fromcat /opt/sso-idp/sso_admin_password.txt(copy password)
5. The username issuperadmin
6. Go to controllerhttps://controller.<domain>/auth/admin/master/console/
7. Enter username and password
8. The page will redirect to the admin console for the CVAH realmAdmin Console
9. 
   .. figure:: /images/image2020-6-5_10-41-9.png
      :height: 400px

10. ClickUsersthenView all usersand thenEditfor the admin usernameView and Edit Users
11. 
   .. figure:: /images/image2020-6-5_10-43-53.png
      :height: 400px

12. ClickCredentials
13. Enter a new passwordand clickReset PasswordDeselecting "Temporary"will avoid being prompted to change the password at the next loginReset Password
14. 
   .. figure:: /images/image2020-6-5_10-46-17.png
      :height: 400px

15. Re-comment the lines in thetfplenum.conffile and restart Apache

::

   Once the password is reset disable the super admin account.


:ref:`Top of Page <e4463d54>`


Recovering from Disk Fill Ups
-----------------------------


The stack requires active monitoring of the disks; failure to do so could result in Kibana being unreachable due to disk fill ups.  

If the disk does fill up, the kit has a safety built-in with the watermark settings.

During operations, it is recommended that the disks on the server side are periodically monitored on the left Kibana Navbar -> Stack Monitoring page.
  It is recommended to periodically back up and remove data the user wants to keep as the disks fill up on the server side (ie: Elasticsearch cluster).
  The sensors will automatically do rolling deletes of the old raw PCAP data when the disk reaches the 75% threshold.


Return to Top
:ref:`Top of Page <e4463d54>`

Kibana Failure Instructions
^^^^^^^^^^^^^^^^^^^^^^^^^^^


If the disks fill up and Kibana is no longer accessible, the following instructions can be run to get the cluster back up and running in short order.



1. From the MIP ssh to the controller withssh root@<ctrl_ip>
2. Perform the following curl commands:

::

   [root@controller ~]# ELASTIC_PASSWORD=$(kubectl get secret tfplenum-es-elastic-user --template={{.data.elastic}} | base64 --decode)
   
   [root@controller ~]# curl -XGET -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/_cat/health?v"
   epoch timestamp cluster status node.total node.data shards pri relo init unassign pending_tasks max_task_wait_time active_shards_percent
   1637006305 19:58:25 tfplenum yellow 8 4 160 80 0 0 0 0 - 100.0%
   
   [root@controller ~]# curl -XGET -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/_cat/allocation?v"
   shards disk.indices disk.used disk.avail disk.total disk.percent host ip node
   40 663.9mb 3gb 3.9gb 4.9gb 90 10.233.3.21 10.233.3.21 tfplenum-es-data-3
   40 844.5mb 3gb 3.9gb 4.9gb 90 10.233.3.15 10.233.3.15 tfplenum-es-data-1
   40 995.6mb 3.1gb 3.8gb 4.9gb 90 10.233.17.14 10.233.17.14 tfplenum-es-data-2
   40 549.6mb 3.1gb 3.8gb 4.9gb 90 10.233.17.11 10.233.17.11 tfplenum-es-data-0
   
   [root@controller ~]# curl -XGET -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/_cat/indices/*?v=true&s=store.size:desc&h=index,store.size"
   index store.size
   metricbeat-7.13.1-2021.11.11-000001 746.5mb
   auditbeat-internal-2021.11.11-000001 579.4mb
   filebeat-zeek-2021.11.11-000001 547.5mb
   sessions2-211112h00 261.9mb
   metricbeat-7.13.1-2021.11.15-000002 211.5mb
   filebeat-suricata-2021.11.11-000001 203.1mb
   auditbeat-internal-2021.11.15-000002 70.1mb
   .kibana_7.13.1_001 54.7mb

3. (Recommended approach)Identify the indexes to backup before either removing the index or performing a delete from query API

::

   The_delete_by_query API will not work if the flood threshold has been triggered because the API attempts to mark the documents as deleted which requires write operations to be active on the index.  It is recommended to back up and then delete a large enough index to get things going again before executing the_delete_by_query and _force_merge API calls.  Deleting a large enough index will cause Elasticsearch to remove the read_only_allow_delete flag from all of its indexes thus allowing the user to execute writes again.


::

   The _delete_by_query API only marks the queried documents as deleted.  It does not clear the disk.  To force a disk cleanup on documents that have been deleted use the _force_merge API call.  See the example below for more details.

4. (Secondary approach)Use the delete by query APIfor the data the user wishes to simply delete without doing backups.  This is the safest way to remove data without causing issues with indexes that are still in use.  If certain that a particular index is no longer in use, delete the index.

::

   The_delete_by_query API will not work if the flood threshold has been triggered because the API attempts to mark the documents as deleted which requires write operations to be active on the index.  It is recommended to back up and then delete a large enough index to get things going again before executing the _delete_by_query and _force_merge API calls.  Deleting a large enough index will cause Elasticsearch to remove the read_only_allow_delete flag from all of its indexes thus allowing the user to execute writes again.


::

   # If the read_only_allow_delete flag is no longer set, the user can execute _delete_by_query API calls instead of deleting entire indexes if they so desire.
   curl -XGET -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/filebeat-external-cold-log-system/_settings" | grep read_only_allow_delete
   
   # Delete old indexes if they are not longer being used or written to.
   curl -XDELETE -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/<INDEX_NAME>"
   
   # It is recommended to first do a query to see which data will be affected.  The below query will query all data on all session2-* indices older than 12 days.  
   curl -XGET -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/sessions2-*/_search" -H 'Content-Type: application/json' -d'
   {
     "query": {
       "range": {
         "timestamp": {
           "lt": "now-12d/d"
         }
       }
     }
   }'
   
   # Tune the query to the liking before executing the next step.
   # Run the following delete by query command with the modified query body if user modified it from the example above.
   curl -XPOST -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/sessions2-*/_delete_by_query?wait_for_completion=false" -H 'Content-Type: application/json' -d'
   {
     "query": {
       "range": {
         "timestamp": {
           "lt": "now-12d/d"
         }
       }
     }
   }'
   
   #Upon successful completion of the above POST command, the user will receive a task ID which you may subsequently check that status of the job with.
   curl -XGET -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/_tasks/<TASK_ID>"
   
   #After the task is completed run the following replacing the <INDEX_NAME> with the index that the user wishes to force deletions.
   curl -XPOST -u elastic:$ELASTIC_PASSWORD "https://elasticsearch:9200/<INDEX_NAME>/_forcemerge?max_num_segments=1"
   # This command will force the deletion of the documents removed and clear the disk space for any of the delete by queries that were previously executed.

5. After clearing out a significant amount of data, force deleting the Kibana pod will speed up the restart time for KibanaIf there is sufficient disk cleared up on the servers, Kibana will come back up as expected

::

   [root@controller ~]# kubectl get pods | grep tfplenum-kb
   tfplenum-kb-cfd498774-gqzx9                         1/1     Running   0          105m
   [root@controller ~]# k delete pod tfplenum-kb-cfd498774-gqzx9 --force


Return to Top
:ref:`Top of Page <e4463d54>`







