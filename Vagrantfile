# -*- mode: ruby -*-
# vi: set ft=ruby :

Vagrant.configure(2) do |config|

  config.vm.define "ocptest" do |ocptest|
    ocptest.vm.provider "virtualbox" do |v|
      v.memory = 3072
      v.cpus = 2
      v.gui = false
    end
    ocptest.vm.box = "centos/7"
    ocptest.vm.network "private_network", ip: "192.168.10.10"
    ocptest.vm.hostname = "ocptest.openshift.localdomain"
    ocptest.vm.boot_timeout = 600
  end

end
