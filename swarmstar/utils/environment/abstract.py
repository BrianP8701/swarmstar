from abc import ABC, abstractmethod


class ArtificialEnvironment(ABC):
    """
    What is the ArtificialEnvironment abstract class?
    
    AIs need an easy way to create and interact with an environment. This class 
    defines a simple interface. Create an environment, start it, send commands to it, 
    and close it.

    For now we'll use docker locally, but in the future we can extend this 
    to handle more scale and running docker on a remote machine.
    """
    @abstractmethod
    def create_environment(self, image: str, **kwargs):
        """
        Create a new environment based on the specified image.

        :param image: The name of the image to create the environment from.
        :param kwargs: Additional keyword arguments to customize the environment creation.
        """
        pass

    @abstractmethod
    def start_environment(self):
        """
        Start the previously created environment, making it ready for interaction.
        """
        pass

    @abstractmethod
    def send_command(self, command: str) -> tuple:
        """
        Send a command to the environment and return the response.

        :param command: The command to be sent to the environment.
        :return: A tuple containing the command's output and error messages.
        """
        pass

    @abstractmethod
    def close_environment(self):
        """
        Close the environment, freeing up resources but not deleting the environment.
        """
        pass

    @abstractmethod
    def delete_environment(self):
        """
        Delete the environment, removing all data associated with it.
        """
        pass

    @abstractmethod
    def add_file(self, source_path: str, target_path: str):
        """
        Add a file from the host to the container.

        :param source_path: Path to the file on the host.
        :param target_path: Path to the file inside the container.
        """
        pass

    @abstractmethod
    def delete_file(self, file_path: str):
        """
        Delete a file inside the container.

        :param file_path: Path to the file inside the container.
        """
        pass

    @abstractmethod
    def commit_container(self, repository: str, tag: str):
        """
        Commit the container to create a new image with the persisted changes.

        :param repository: Repository name for the new image.
        :param tag: Tag for the new image.
        """
        pass