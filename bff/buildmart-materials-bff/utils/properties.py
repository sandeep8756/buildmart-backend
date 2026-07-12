import os


class Properties:
    context_path = os.environ.get("context_path", "buildmart-materials-bff")
    module_info = os.environ.get("module_info", "buildmart-materials-bff")
    ip_port = os.environ.get("ip_port", "localhost:8001")

    @staticmethod
    def core_url(path: str) -> str:
        host = os.environ.get("ip_port", "localhost:8001")
        return f"http://{host}/buildmart-materials{path}"
