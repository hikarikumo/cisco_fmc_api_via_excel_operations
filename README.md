# **FMC scripts to add, modify, delete objects: hosts, ranges, networks, urls, networgroups, urlgroups and objects within groups**

A repository of python scripts to perform some routine changes in Cisco FMC in a more handy, quicker and errors-less way then typically allows  us via GUI.

## Why

Initially there were lot's of data in Excel spreadsheets provided to me by linux teams. Therefore, it was really quick and handy utilize Excel for composition of required objects and groups for FMC. Thus, it can be used to upload, download, delete, modify thounsands of objects for FMC in several minutes.
Additionally these scripts work with child domains. 

### Pre-step

From the scratch please prepare python virtual environment:

```
git clone git@github.com:hikarikumo/cisco_fmc_api_via_excel_operations.git or copy required files
cd <repo>
pip install virtualenv (if you don't already have virtualenv installed)
virtualenv venv to create your new environment (called 'venv' here)
source venv/bin/activate to enter the virtual environment
pip install -r requirements.txt to install the requirements in the current environment
```

## Usage

### FMC info

It is possible to go straight and just launch main script however in such case the FMC ip address, username and password should be provided as the first inputs to start.
Otherwise it is possible to provide proper ip address, username, password within fmc_credentials.yaml file if used (for example) in lab

```---
username: api-user
password: fmcAPIbg001
fmc_ip: 192.168.1.16
```

### Create initial Excel structure of FMC domains

Just launch the script and as initial run it will connect to FMC and download all objects, groups except for the system ones.
All collected data would be saved as a input Excel file.
By default is is called **FMC_objects.xlsx**.
Filenames can be changed within the cfg.py file along with other initial info if needed.

```Launch
python fmc_main_script.py
```

Further subsequent script runs would save all objects, groups data into additional file **FMC_downloaded_objects.xlsx**.
In such way the changes in **FMC_objects.xlsx** would not be overwritten.

### Add new objects

Each domain has two or three Excel Sheets:

* One for objects: hosts, ranges, networks, urls
* Second one for groups of objects i.e. networkgroups
* Third one (if urls are present) for urlgroups

Each object require action column to be filled:

* add
* delete
* modify

Therefore in order to add new hosts it is required to fill the following data within the Excel file. Action field should be **add**:

```
object_name         object          action  type
H.TEST.GEN.HOST1    198.18.204.1    add     Host
H.TEST.GEN.HOST2    198.18.204.2    add     Host
H.TEST.GEN.HOST3    198.18.204.3    add     Host
```

Object Types should be properly specified for the FMC, the proper types can be found below:
Host, Network, Range, Url, NetworkGroup, UrlGroup

If action field is not specified or specified incorrectly it would be just skipped.

### Add new groups

Similar approach is for creation of object groups. Specify group, object, action and group type:

```
object_group_name   object          action  type
GP.TEST.GROUP       H.TEST.HOST4    add     NetworkGroup
GP.TEST.GROUP       H.TEST.HOST3    add     NetworkGroup
```

Of course, the objects should be added to objects tab too

### Add new urlgroups

Similar approach is for creation of url groups. Specify urlgroup, url, action and urlgroup type:

```
url_group_name  url                 action  type
urlgrp.test     https://gmail.com   add     UrlGroup
urlgrp.test     https://google.com  add     UrlGroup
```

Of course, the urls should be added to objects tab too

### Del objects

Set action filed to **delete**:

```
object_name         object          action  type
H.TEST.GEN.HOST1    198.18.204.1    delete  Host
H.TEST.GEN.HOST2    198.18.204.2    delete  Host
H.TEST.GEN.HOST3    198.18.204.3    delete  Host
```

Bear in mind that before deletion of the object it shoudl be deleted out of the group first (in case it is used in group).

### Delete objects from group

Set action filed to **delete**:

```
object_group_name   object          action  type
GP.TEST.GROUP       H.TEST.HOST4    delete  NetworkGroup
GP.TEST.GROUP       H.TEST.HOST3            NetworkGroup
```

### Modify objects

Change object value. Set action filed to **modify**:

```
object_name         object          action  type
H.TEST.GEN.HOST1    198.18.0.111    modify  Host
H.TEST.GEN.HOST2    198.18.204.2            Host
H.TEST.GEN.HOST3    198.18.204.3            Host
```


