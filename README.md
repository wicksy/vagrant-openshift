[![license](https://img.shields.io/badge/License-MIT-blue.svg?maxAge=2592000)](https://github.com/wicksy/vagrant-openshift/blob/master/LICENSE.md)</br>

### Vagrant managed VM running Red Hat OpenShift Container Platform (OCP)

![Vagrant logo](logos/vagrant.png "Vagrant")
![Openshift logo](logos/openshift.png "Openshift")

#### About

Single node OCP Master designed to be used to develop/test locally (based on Origin).

#### Installation Notes

Notes during installation/development:

* https://github.com/openshift/openshift-ansible/issues/6435 still open at time of writing so `ansible_service_broker_image_prefix='ansibleplaybookbundle/origin-'`
has been added to the hosts file
* https://github.com/hashicorp/vagrant/issues/9329 opened to report interface sorting issue (see below)

#### Outstanding Issues

Due to the way that Vagrant 2.x appears to incorrectly sort interfaces and map them to `adapters`, the current `Vagrantfile` breaks once OpenShift Origin has been installed and
configured. This introduces several extra interfaces (e.g. docker0, tun0, br0, etc) which seems to break the sorting algorithm:

```
DEBUG network_interfaces: Unsorted list: ["eth0", "eth1", "docker0", "ovs-system", "vxlan_sys_4789", "tun0", "br0", "", "tun0", "br0", "eth0", "eth1", "lo", "docker0"]
DEBUG network_interfaces: Sorted list: ["", "eth1", "docker0", "eth0", "vxlan_sys_4789", "tun0", "br0"]
DEBUG network_interfaces: Ethernet preferred sorted list: ["eth1", "eth0", "", "docker0", "vxlan_sys_4789", "tun0", "br0"]
```

The result of this is that `eth1` is passed back to Vagrant as `adapter 1` which is then configured incorrectly as a private network (host-only) interface rather than the
NAT interface it should be. This causes `vagrant up` to hang indefinitely.

To work around this you should bring up the initial box without provisioning it so that the network interface scripts can be correctly setup (before Origin is installed), then update
the `Vagrantfile` to stop automatically configuring `adapter 2` and then provision the box so that Origin is installed and configured.

Issue opened ([#9329](https://github.com/hashicorp/vagrant/issues/9329))

```
$ vagrant up ocptest --no-provision
$ sed -i -e 's/ocptest.vm.network "private_network", adapter: 2.*/&, auto_config: false/g'  Vagrantfile
$ vagrant provision ocptest
```

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
* Virtualbox 5.2.4 r119785
* Vagrant 2.0.1
* Vagrant Landrush plugin 1.2.0
* Ansible 2.4.1.0
* Ansible/OpenShift-Ansible Repository Release `release-3.7`
* OpenShift Origin v3.7.0+7ed6862 (kubernetes v1.7.6+a08f5eeb62)

This repository has previously been used to provision older versions of Origin with older
versions of Virtualbox/Vagrant/Ansible so previous commits could be used if older Origin
versions cannot be used with the latest.

#### Deployment Instructions

See <b>Outstanding Issues</b> above for any deployment instruction updates. If none are present the VM can be provisioned with:

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

deploy_metrics: Whether to deploy pod metrics collection (Cassandra/Hawkular) (default "false")

install_containerized: Whether to run containerized OpenShift Origin services (default "true")

openshift_release: What version of OpenShift Origin (containers) to use (default "3.7.0")
```

The `openshift_ansible_version` can be used to check out an older version of the repository in the event of unresolved issues and problems with
the latest release (or any release).

#### OpenShift Web Console

Once the VM has been started and provisioned, the OpenShift Master Console should be available at:

https://ocptest.localdomain:8443

#### Aggregated Logging

If `deploy_logging` is set to `true` archived pod logs will be available from the console (Pod view -> Logs tab) through a Kibana interface.

<b>NOTE:</b> Persistent storage for Elasticsearch is not currently supported here as the repository is designed to provide a small development rig
where data should generally be throw away (much like an `oc cluster up` environment).

Persistent logging can be configured by further bespoking `templates/etc.ansible.hosts.j2` and supplying some of the `openshift_hosted_logging_storage_` variables.

#### Pod Metrics

If `deploy_metrics` is set to `true` pod metrics will be available from the console (Pod view -> Metrics tab).

<b>NOTE:</b> As with Logging, persistent storage is not supported here but can be configured by modifying the hosts template with the appropriate
`openshift_hosted_metrics_storage_` variables.

#### Memory

When deploying Logging <b>AND</b> Metrics it is advisable to increase the memory on the VM:

```
$ VM_MEMORY=8192 vagrant up ocptest
```

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
