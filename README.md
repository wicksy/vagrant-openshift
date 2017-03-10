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

#### Command Line Login

The installation comes with a `developer` user (password `developer` set in `defaults/main.yml`) as well as the `system:admin` user (which has cluster admin rights
through the cluster-admin role):

```
[vagrant@ocptest ~]$ oc login -u developer
Authentication required for https://ocptest.openshift.localdomain:8443 (openshift)
Username: developer
Password:
Login successful.

You don't have any projects. You can try to create a new project, by running

    oc new-project <projectname>

[vagrant@ocptest ~]$ oc whoami
developer
[vagrant@ocptest ~]$ oc logout
Logged "developer" out on "https://ocptest.openshift.localdomain:8443"
[vagrant@ocptest ~]$ oc login -u system:admin
Logged into "https://ocptest.openshift.localdomain:8443" as "system:admin" using existing credentials.

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
