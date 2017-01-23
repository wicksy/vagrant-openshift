### Vagrant managed VM running Red Hat OpenShift Container Platform (OCP)

#### About

Work in progress. Single node OCP Master designed to be used to develop/test locally.

#### Installation Notes

Notes during installation/development:

* Used Vagrant 1.8.5 as Landrush doesn't work with 1.9.x. (https://github.com/vagrant-landrush/landrush/issues/292)
* Used Ansible 2.2.0.0 as OpenShift installation fails with 2.2.1.0 (https://github.com/openshift/openshift-ansible/issues/3111)
* New ssh key not inserted due to issue (https://github.com/mitchellh/vagrant/issues/7642)
