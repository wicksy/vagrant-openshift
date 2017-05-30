import pytest

@pytest.mark.parametrize("name, user, group, mode, contains", [
  ("/etc/hosts","root","root","0644","ocptest"),
  ("/etc/sysconfig/docker","root","root","0644","OPTIONS=' --selinux-enabled --log-driver=json-file --log-opt max-size=50m --insecure-registry 172.30.0.0/16'"),
  ("/home/vagrant/openshift-ansible","vagrant","vagrant","0755","null"),
  ("/etc/ansible","root","root","0755","null"),
  ("/home/vagrant/.ssh/config","vagrant","vagrant","0600","User vagrant"),
  ("/etc/origin/master/htpasswd","root","root","0600","developer"),
  ("/etc/exports","root","root","0644","(rw,sync,no_root_squash)"),
])

def test_files(host, name, user, group, mode, contains):
  file = host.file(name)
  assert file.exists
  assert file.user == user
  assert file.group == group
  assert oct(file.mode) == mode
  if file.is_directory is not True:
    assert file.contains(contains)
  else:
    assert file.is_directory