import os


class Properties:
    def __init__(self):
        self.context_path = os.environ.get("context_path", "buildmart-materials")
