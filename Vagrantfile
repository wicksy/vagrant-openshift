# -*- mode: ruby -*-
# vi: set ft=ruby :

# The private network IP of the VM. You will use this IP to connect to OpenShift.
PUBLIC_ADDRESS="192.168.10.10"

# Number of virtualized CPUs
VM_CPU = ENV['VM_CPU'] || 2

# Amount of available RAM
VM_MEMORY = ENV['VM_MEMORY'] || 3072

Vagrant.configure(2) do |config|

  config.vm.define "ocptest" do |ocptest|
    ocptest.vm.provider "virtualbox" do |v|
      v.memory = VM_MEMORY
      v.cpus = VM_CPU
      v.gui = false
    end
    ocptest.vm.box = "centos/7"
    ocptest.vm.network "private_network", ip: "#{PUBLIC_ADDRESS}"
    ocptest.vm.hostname = "ocptest.openshift.localdomain"
    ocptest.vm.boot_timeout = 600
  end

end
