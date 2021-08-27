class BaseClient:
    def __init__(self) -> None:
        self.headers = {
            'Content-Type': 'application/json',
            'Accept': 'application/json'
        }