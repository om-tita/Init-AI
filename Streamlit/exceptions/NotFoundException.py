class NotFoundException(Exception):
    def __init__(self, error):
        self.error = error
        self.status_code = 404