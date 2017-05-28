import pytest

@pytest.mark.parametrize("name", [
  ("bash-completion"),
  ("bind-utils"),
  ("bridge-utils"),
  ("docker"),
  ("epel-release"),
  ("git"),
  ("iptables-services"),
  ("libnfsidmap"),
  ("net-tools"),
  ("nfs-utils"),
  ("pyOpenSSL"),
  ("screen"),
  ("strace"),
  ("tcpdump"),
  ("wget"),
])

def test_packages(Package, name):
  assert Package(name).is_installed
