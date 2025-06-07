"""Test mashumaro serialize/deserialize methods."""
from pprint import pprint

from sc_rpi_client.response import Response

response = Response(400, "Bad request", {})
serialized_response = response.to_json()
print(f"serialized_response class : {serialized_response.__class__}")
pprint(serialized_response)
