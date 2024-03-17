import docker
from docker.models.containers import Container
import tarfile
import io
import os

from swarmstar.utils.containers.abstract import ContainerManagement
from swarmstar.models import Memory, MemoryMetadata

class DockerContainerManager(ContainerManagement):
    def __init__(self):
        self.client = docker.from_env()
    
    def start_terminal_session(self, image_id: str, project_root_id: str) -> str:
        # Start a container with the specified image
        try:
            container: Container = self.client.containers.run(image_id,
                                                              command="tail -f /dev/null",
                                                              detach=True,
                                                              tty=True)
        except docker.errors.ImageNotFound:
            raise ValueError(f"Image with ID {image_id} not found.")
        except docker.errors.APIError as e:
            raise ConnectionError(f"Failed to start terminal session due to Docker API error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while starting terminal session: {e}")
        
        # Transfer project into container
        try:            
            def recursive_helper(memory_id: str):
                memory_metadata = MemoryMetadata.get_memory_metadata(memory_id)
                if memory_metadata.is_folder:
                    for child_id in memory_metadata.children_ids:
                        recursive_helper(child_id)
                else:
                    memory_bytes = Memory.get_memory(memory_id)
                    self.transfer_file_to_container(container.id, memory_metadata.context["file_path"], memory_bytes)
            
            recursive_helper(project_root_id)

        except Exception as e:
            raise Exception(f"An error occurred while transferring project into container: {e}")
        
        return container.id
    
    def send_command(self, container_id: str, command: str) -> str:
        try:
            container: Container = self.client.containers.get(container_id)
            exit_code, output = container.exec_run(command)
            if exit_code != 0:
                raise ValueError(f"Command execution failed with exit code {exit_code}. Output: {output.decode('utf-8')}")
        except docker.errors.NotFound:
            raise ValueError(f"Container with ID {container_id} not found.")
        except docker.errors.APIError as e:
            raise ConnectionError(f"Failed to send command due to Docker API error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while sending command: {e}")
        return output.decode('utf-8')
    
    def close_terminal_session(self, container_id: str) -> None:
        try:
            container: Container = self.client.containers.get(container_id)
            container.stop()
            container.remove()
        except docker.errors.NotFound:
            raise ValueError(f"Container with ID {container_id} not found.")
        except docker.errors.APIError as e:
            raise ConnectionError(f"Failed to close terminal session due to Docker API error: {e}")
        except Exception as e:
            raise Exception(f"An unexpected error occurred while closing terminal session: {e}")

    def transfer_file_to_container(self, container_id: str, file_path: str, file_bytes: bytes) -> None:
        container: Container = self.client.containers.get(container_id)
        
        # Sanitize file_path to prevent directory traversal
        sanitized_file_path = os.path.normpath(file_path).lstrip('/')
        if '..' in sanitized_file_path.split(os.path.sep):
            raise ValueError("Invalid file path. Directory traversal is not allowed.")
        
        # Create a tarball in memory
        file_like_object = io.BytesIO()
        with tarfile.open(fileobj=file_like_object, mode='w') as tar:
            file_data = tarfile.TarInfo(name=sanitized_file_path)
            file_data.size = len(file_bytes)
            tar.addfile(file_data, io.BytesIO(file_bytes))
        
        file_like_object.seek(0)
        
        # Transfer the tarball to the container
        try:
            container.put_archive(path="/", data=file_like_object)
        except Exception as e:
            # Handle exceptions or log errors
            print(f"Error transferring file to container: {e}")
