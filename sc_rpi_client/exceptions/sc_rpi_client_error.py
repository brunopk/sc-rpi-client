"""Common base class for all websocket or sc-rpi errors."""

class ScRpiClientError(Exception):
  """Common base class for all websocket or sc-rpi errors."""

  def __init__(self, *args: object) -> None:
    """Construct an ScRpiClientError instance."""
    super().__init__(*args)
