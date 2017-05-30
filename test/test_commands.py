import os
import pytest

TEST_URL = str(os.environ.get('TEST_URL'))
if TEST_URL != 'None' and TEST_URL.strip():
  pass
else:
  TEST_URL="https://192.168.10.10:8443/api"

@pytest.mark.parametrize("command", [
  ("curl -k " + TEST_URL + " | grep 'kind.*:.*APIVersions'"),
  ("oc get node | grep '10.0.2.15.*Ready'"),
  ("oc get pod -n default | grep 'docker-registry.*Running'"),
  ("oc get pod -n default | grep 'router.*Running'"),
])

def test_commands(host, command):
  cmd = host.run(command)
  assert cmd.rc == 0