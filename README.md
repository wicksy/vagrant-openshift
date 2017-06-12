[![license](https://img.shields.io/badge/License-MIT-blue.svg?maxAge=2592000)](https://github.com/wicksy/vagrant-openshift/blob/master/LICENSE.md)</br>

### Vagrant managed VM running Red Hat OpenShift Container Platform (OCP)

![Vagrant logo](logos/vagrant.png "Vagrant")
![Openshift logo](logos/openshift.png "Openshift")

#### About

Single node OCP Master designed to be used to develop/test locally (based on Origin).

#### Installation Notes

Notes during installation/development:

* Used Vagrant 1.8.5 as Landrush doesn't work with 1.9.x. (https://github.com/vagrant-landrush/landrush/issues/292)
* Used Ansible 2.2.0.0 as OpenShift installation fails with 2.2.1.0 (https://github.com/openshift/openshift-ansible/issues/3111)
* New ssh key not inserted due to issue (https://github.com/mitchellh/vagrant/issues/7642)
* Tag openshift-ansible-3.5.67-1 used to clone openshift/openshift-ansible due to issues open against `master`

#### Pre-requisites

This installation requires Vagrant (plus the Landrush plugin), Virtualbox and Ansible.

```
$ vagrant up ocptest
Vagrant failed to initialize at a very early stage:
Error: landrush plugin is not installed, run `vagrant plugin install landrush` to install it.
$
```

#### Software Versions

Deployment has been successfully tested with:

* OSX 10.10.5
* Virtualbox 5.0.12 r104815
* Vagrant 1.8.5
* Vagrant Landrush plugin 1.2.0
* Ansible 2.2.0.0
* Ansible/OpenShift-Ansible Repository Release openshift-ansible-3.5.67-1
* OpenShift Origin v1.4.1 (kubernetes v1.4.0+776c994)

#### Deployment Instructions

```
$ git clone https://github.com/wicksy/vagrant-openshift
$ cd vagrant-openshift/vagrant
$ vagrant up ocptest --provision --provider virtualbox
```

#### Variables

The following Ansible variables can be used to override supplied values:

```
developer_user: The user created and designed to be used as a developer account (default "developer")

developer_password: Password for the developer user (default "developer")

nfs_root: The root directory where NFS persistent volumes are located (default "/nfsshare")

persistent_volumes: Number of persistent volumes created (default "5")

openshift_ansible_version: The version of the ansible/openshift-ansible repository to checkout (default "master")

install_disable_check: The resource checks to disable during installation (default "disk_availability,memory_availability")

deploy_logging: Whether to deploy aggregated logging (EFK stack) (default "false")
```

The `openshift_ansible_version` can be used to check out an older version of the repository in the event of unresolved issues and problems with the
latest release (see Installation Notes above).

#### OpenShift Web Console

Once the VM has been started and provisioned, the OpenShift Master Console should be available at:

https://ocptest.localdomain:8443

#### Aggregated Logging

If `deploy_logging` is set to `true` archived pod logs will be available from the console (Pod view -> Logs tab) through a Kibana interface.

<b>NOTE:</b> Persistent storage for Elasticsearch is not currently supported here as the repository is designed to provide a small development rig
where data should generally be throw away (much like an `oc cluster up` environment).

Persistent logging can be configured by further bespoking `templates/etc.ansible.hosts.j2` and supplying some of the `openshift_hosted_logging_storage_` variables.

#### Command Line Login

The installation comes with a `developer` user (password `developer` set in `defaults/main.yml`) as well as the `system:admin` user (which has cluster admin rights
through the cluster-admin role):

```
[vagrant@ocptest ~]$ oc login -u developer
Authentication required for https://ocptest.localdomain:8443 (openshift)
Username: developer
Password:
Login successful.

You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>

[vagrant@ocptest ~]$ oc whoami
developer
[vagrant@ocptest ~]$ oc logout
Logged "developer" out on "https://ocptest.localdomain:8443"
[vagrant@ocptest ~]$ oc login -u system:admin
Logged into "https://ocptest.localdomain:8443" as "system:admin" using existing credentials.

You have access to the following projects and can switch between them with 'oc project <projectname>':

    bestefforts
  * default
    kube-system
    logging
    management-infra
    openshift
    openshift-infra

Using project "default".
[vagrant@ocptest ~]$
```

#### Persistent Volumes
NFS server is installed and setup to manage persistent volumes. By default 5 volumes are created but this
can be increased through the `persistent_volumes` variable.

```
[vagrant@ocptest ~]$ sudo oc get pv
NAME      CAPACITY   ACCESSMODES   RECLAIMPOLICY   STATUS      CLAIM     REASON    AGE
pv0001    2Gi        RWO           Recycle         Available                       3m
pv0002    2Gi        RWO           Recycle         Available                       2m
pv0003    2Gi        RWO           Recycle         Available                       2m
pv0004    2Gi        RWO           Recycle         Available                       2m
pv0005    2Gi        RWO           Recycle         Available                       2m
[vagrant@ocptest ~]$ oc create -f ./pvc.yaml
persistentvolumeclaim "nfs-claim1" created
[vagrant@ocptest ~]$ oc get pvc
NAME         STATUS    VOLUME    CAPACITY   ACCESSMODES   AGE
nfs-claim1   Bound     pv0005    2Gi        RWO           2s
[vagrant@ocptest ~]$
```

#### Landrush Wildcard Subdomains

Since the Vagrant Landrush Plugin supports [wildcard subdomains](https://github.com/vagrant-landrush/landrush/blob/master/doc/Usage.adoc#wildcard-subdomains) you should be able
to reach a pod service through its route from your desktop browser (e.g. https://registry-console-default.ocptest.localdomain).

#### Tests

There are a number of tests implemented using the serverspec-like testing framework for Python [**testinfra**](https://github.com/philpep/testinfra). Tests
can be run using the `runtests.sh` bash script in the `test` directory:

```
$ cd test
$ ./runtests.sh
```

The script will bring up the vagrant machine if not already, setup a python virtual environment, install required pips, run a series of test
packs through testinfra then clean up afterwards.

Sample output from one of the test packs (for services):

```
========================================================= test session starts ==================================================================
platform darwin -- Python 2.7.10, pytest-3.1.0, py-1.4.33, pluggy-0.4.0 -- /Users/wicksy/.pyenvironments/ocptest/bin/python
cachedir: ../.cache
rootdir: /Users/wicksy/git/wicksy/vagrant-openshift, inifile:
plugins: testinfra-1.6.3
collected 8 items

../test/test_services.py::test_services[paramiko:/ocptest-docker-enabled-running] PASSED
../test/test_services.py::test_services[paramiko:/ocptest-firewalld-disabled-stopped] PASSED
../test/test_services.py::test_services[paramiko:/ocptest-nfs-idmapd-enabled-running] PASSED
../test/test_services.py::test_services[paramiko:/ocptest-nfs-server-enabled-running] PASSED
../test/test_services.py::test_services[paramiko:/ocptest-origin-master-enabled-running] PASSED
../test/test_services.py::test_services[paramiko:/ocptest-origin-node-enabled-running] PASSED
../test/test_services.py::test_services[paramiko:/ocptest-rpc-statd-enabled-running] PASSED
../test/test_services.py::test_services[paramiko:/ocptest-rpcbind-enabled-running] PASSED

======================================================== pytest-warning summary ================================================================
```

More information on **testinfra** can be found at https://github.com/philpep/testinfra

#### Teardown Instructions

```
$ vagrant destroy ocptest --force
```

#### Future Plans

Plans for additional content include using:

- Permanent storage for docker-registry
- Travis Builds
- Install specific versions of OpenShift
- POD metrics (Hawkular/Cassandra)
