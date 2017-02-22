### Vagrant managed VM running Red Hat OpenShift Container Platform (OCP)

#### About

Single node OCP Master designed to be used to develop/test locally (based on Origin).

#### Installation Notes

Notes during installation/development:

* Used Vagrant 1.8.5 as Landrush doesn't work with 1.9.x. (https://github.com/vagrant-landrush/landrush/issues/292)
* Used Ansible 2.2.0.0 as OpenShift installation fails with 2.2.1.0 (https://github.com/openshift/openshift-ansible/issues/3111)
* New ssh key not inserted due to issue (https://github.com/mitchellh/vagrant/issues/7642)

#### Pre-requisites

This installation requires Vagrant (plus the Landrush plugin), Virtualbox and Ansible.

#### Software Versions

Deployment has been successfully tested with:

* OSX 10.10.5
* Virtualbox 5.0.12 r104815
* Vagrant 1.8.5
* Vagrant Landrush plugin 1.2.0
* Ansible 2.2.0.0
* OpenShift Origin v1.4.1 (kubernetes v1.4.0+776c994)

#### Deployment Instructions

```
$ git clone https://github.com/wicksy/vagrant-openshift
$ cd vagrant-openshift/vagrant
$ vagrant up ocptest --provision --provider virtualbox
```

#### OpenShift Web Console

Once the VM has been started and provisioned, the OpenShift Master Console should be available at:

https://ocptest.openshift.localdomain:8443

#### Teardown Instructions

```
$ vagrant destroy ocptest --force
```

#### Future Plans

Plans for additional content include using:

- Install specific versions of OpenShift
- Unit tests (using [**testinfra**](https://github.com/philpep/testinfra))
- Travis Builds
- NFS server to provide persistent storage (PV/PVC)
- Aggregated Logging (EFK)
- POD metrics (Hawkular/Cassandra)
- Permanent storage for docker-registry
