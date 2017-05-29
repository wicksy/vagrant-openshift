import pytest

@pytest.mark.parametrize("name, enabled, running", [
  ("docker", "enabled", "running"),
  ("firewalld", "disabled", "stopped"),
  ("nfs-idmapd", "enabled", "running"),
  ("nfs-server", "enabled", "running"),
  ("rpc-statd", "enabled", "running"),
  ("rpcbind", "enabled", "running"),
])

def test_services(host, name, enabled, running):

  svc = host.service(name)

  is_enabled = svc.is_enabled
  print(is_enabled)
  if enabled == "enabled":
    assert is_enabled
  else:
    assert not is_enabled

  is_running = svc.is_running
  print(is_running)
  if running == "running":
    assert is_running
  else:
    assert not is_running

