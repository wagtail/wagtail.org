# -*- mode: ruby -*-
# vi: set ft=ruby :


Vagrant.configure(2) do |config|
  config.vm.box = "wagtail/buster64"
  config.vm.box_version = "~> 1.1.0"

  # If a 'Vagrantfile.local' file exists, import any configuration settings
  # defined there into here. Vagrantfile.local is ignored in version control,
  # so this can be used to add configuration specific to this computer.
  # `git rev-parse` just helps find it if `vagrant up` is not run from the project root.
  vagrantfile_local = `git rev-parse --show-toplevel`.split("\n")[0] + "/Vagrantfile.local"
  if File.exist? "Vagrantfile.local"
    instance_eval File.read("Vagrantfile.local"), "Vagrantfile.local"
  end

  config.vm.network "forwarded_port", guest: 8000, host: @FORWARD_PORT || 8000, auto_correct: true
  config.vm.provision :shell, :path => "vagrant/provision.sh", :args => "wagtailio"
  config.ssh.forward_agent = true

  config.vm.provider "virtualbox" do |vb|
    # increase memory by default; can be changed in Vagrantfile_local.rb
    vb.memory = @MEMORY_MB || 2048
  end

  # https://www.vagrantup.com/docs/synced-folders/nfs.html
  if @NFS
      puts "NFS=#{@NFS}"
      config.vm.synced_folder ".", "/vagrant", :nfs => @NFS, :mount_options => ['actimeo=2']
      config.vm.network :private_network, type: "dhcp"
  end

  if Vagrant.has_plugin?("vagrant-vbguest")
    config.vbguest.auto_update = false
  end
end
