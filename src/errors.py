class Web3oError(Exception): ...

class InvalidBlockProvided(Web3oError): ...

class DeserializationFailed(Web3oError): ...

class RPCError(Web3oError):
    """Raised when the RPC node returns an error response."""

    def __init__(self, code: int, message: str, data: str | None = None):
        self.code = code
        self.message = message
        self.data = data
        super().__init__(f"[{code}] {message}" + (f" - {data}" if data else ""))
