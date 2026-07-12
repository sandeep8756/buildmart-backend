import os


class Properties:
    context_path = os.environ.get("context_path", "buildmart-delivery-bff")
    module_info = os.environ.get("module_info", "buildmart-delivery-bff")
    ip_port = os.environ.get("ip_port", "localhost:8003")

    @staticmethod
    def core_url(path: str) -> str:
        host = os.environ.get("ip_port", "localhost:8003")
        return f"http://{host}/buildmart-delivery{path}"
