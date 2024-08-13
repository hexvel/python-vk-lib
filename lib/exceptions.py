class VkAPIError(Exception):
    def __init__(self, error: dict):
        self.error_code = error.get("error_code")
        self.error_msg = error.get("error_msg")
        super().__init__(f"VKAPIError {self.error_code}: {self.error_msg}")
