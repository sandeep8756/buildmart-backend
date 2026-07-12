import os


class Properties:
    context_path = os.environ.get("context_path", "buildmart-workers-bff")
    module_info = os.environ.get("module_info", "buildmart-workers-bff")
    ip_port = os.environ.get("ip_port", "localhost:8002")

    @staticmethod
    def core_url(path: str) -> str:
        host = os.environ.get("ip_port", "localhost:8002")
        return f"http://{host}/buildmart-workers{path}"
