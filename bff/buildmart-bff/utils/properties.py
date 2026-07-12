import os


class Properties:
    def __init__(self):
        self.context_path = os.environ.get("context_path", "buildmart-bff")
        self.ip_port_materials = os.environ.get(
            "ip_port_materials", "localhost:8001"
        )
        self.ip_port_workers = os.environ.get("ip_port_workers", "localhost:8002")
        self.ip_port_delivery = os.environ.get(
            "ip_port_delivery", "localhost:8003"
        )

    def materials_core_url(self, path: str) -> str:
        return f"http://{self.ip_port_materials}/buildmart-materials{path}"

    def workers_core_url(self, path: str) -> str:
        return f"http://{self.ip_port_workers}/buildmart-workers{path}"

    def delivery_core_url(self, path: str) -> str:
        return f"http://{self.ip_port_delivery}/buildmart-delivery{path}"
