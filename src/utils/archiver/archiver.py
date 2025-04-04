import os
import pickle
import re
from threading import Lock
from pathlib import Path
from typing import Optional


class DontHavePathError(Exception):
    def __init__(self,client_class: type):
        self.add_note(f"Any path associated with {client_class.__name__}")

class OldSaveError(Exception):
    def __init__(self,client_class: type):
        self.add_note(f"Error to load a value, maybe the value is a old version use in {client_class.__name__}")

class SingletonMeta(type):
    _instances = {}
    _lock = Lock()

    def __call__(cls, *args, **kwargs):
        with cls._lock:
            if cls not in cls._instances:
                instance = super().__call__(*args, *kwargs)
                cls._instances[cls] = instance
            return cls._instances[cls]
def list_files(path):
    pasta = Path(path)
    return sorted([(arq.parent.name,arq.resolve()) for arq in pasta.glob('**/*') if arq.is_file()])


class Archiver(metaclass=SingletonMeta):
    """
        This class have the job to save locally the data structure of hanzi information, like the binary tree from CCCedict module
    """
    _files_address: dict = {}
    _root_library: Path = Path(__file__).parent.resolve().joinpath("libray")

    def __init__(self):
        if not os.path.exists(self._root_library):
            os.makedirs(self._root_library)
        self._files_address = self._load_register()

    def save(self,client_class: type,data):
        if not self._check_has_register(client_class):
            client_path = self._create_client_path(client_class)
            self._register_address(client_class,client_path)
        self._write_archive(data,self._get_client_path(client_class))
        self._save_register()

    def load(self,client_class:type) -> any:
        if not self._check_has_register(client_class):
            print(f"the {client_class.__class__} dont have any register")
            raise DontHavePathError(client_class)
        path = self._get_client_path(client_class)
        try:
            data = self._load_data(path)
        except ModuleNotFoundError:
            raise OldSaveError(client_class)
        return data

    def _save_register(self):
        self.save(self.__class__,self._files_address)

    def _load_register(self) -> dict:
        if not self._list_library_files():
            return {}

        if Archiver.__class__ in self._list_library_files():
            return self._load_data(self._create_client_path(self.__class__))

        return {client_class : archived_path for client_class, archived_path in self._list_library_files()}

    def _list_library_files(self) -> list:
        pasta = Path(self._root_library)
        return sorted([(arq.parent.name, arq.resolve()) for arq in pasta.glob('**/*') if arq.is_file()])

    def _check_has_register(self, client_class: type) -> bool:
        return self._files_address.get(client_class.__name__,None) is not None

    def _register_address(self,client_class: type,path_to_archive: Path):
        self._files_address[client_class.__name__] = path_to_archive

    def _create_client_path(self, client_class: type) -> Path:
        client_path = self._root_library.resolve().joinpath(client_class.__name__,"data.plk")
        try:
            os.makedirs(client_path)
        except FileExistsError:
            print("The archive was create previously, maybe ocurred some error inside save method")
            return client_path

        return client_path

    def _get_client_path(self,client_class:type) -> Optional[Path]:
        path = self._files_address.get(client_class.__name__,None)
        if path is not None:
            return path
        raise DontHavePathError

    @staticmethod
    def _write_archive(data: any, path: Path):
        with open(path, 'wb') as file:
            file.write(pickle.dumps(data))  # it is to work, but the type system is yelling about that

    @staticmethod
    def _load_data(path: Path) -> Optional[any]:
        try:
            with open(path, 'rb') as file:
                return pickle.loads(file.read())
        except ModuleNotFoundError as e:
            raise e
