import docker
import os

from swarmstar.utils.environment.abstract import ArtificialEnvironment


class LocalDockerEnvironment(ArtificialEnvironment):
    def __init__(self):
        self.client = docker.from_env()
        self.container = None

    def create_environment(self, image: str, **kwargs):
        self.container = self.client.containers.create(image, stdin_open=True, tty=True, detach=True, **kwargs)

    def start_environment(self):
        if self.container is not None:
            self.container.start()

    def send_command(self, command: str) -> tuple:
        if self.container is not None:
            exit_code, output = self.container.exec_run(command)
            return exit_code, output.decode('utf-8')
        return None, None

    def close_environment(self):
        if self.container is not None:
            self.container.stop()

    def delete_environment(self):
        if self.container is not None:
            self.container.remove()
            self.container = None

    def add_file(self, source_path: str, target_path: str):
        if self.container is not None:
            with open(source_path, 'rb') as file:
                file_data = file.read()
                self.container.put_archive(os.path.dirname(target_path), file_data)

    def delete_file(self, file_path: str):
        if self.container is not None:
            self.container.exec_run(f"rm -rf {file_path}")

    def commit_container(self, repository: str, tag: str):
        if self.container is not None:
            self.container.commit(repository=repository, tag=tag)