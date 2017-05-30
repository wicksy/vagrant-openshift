import pytest

@pytest.mark.parametrize("socketspec", [
  ("tcp://0.0.0.0:8443"),
])

def test_sockets(host, socketspec):
  sock = host.socket(socketspec)
  assert sock.is_listening