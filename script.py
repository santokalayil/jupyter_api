import datetime
from typing import List, Union
import requests
from dataclasses import dataclass
from pathlib import Path
from pydantic import BaseModel


class JupyterSessionError(Exception): ...
class AuthenticationError(JupyterSessionError):
    ...

class URL:
    def __init__(self, path: Union[str, "URL"]) -> None:
        self.path = str(path).removesuffix("/")
        return
    
    def join_path(self, part: str) -> "URL":
        new_path =  self.path + "/" + part.removeprefix("/").removesuffix('/')
        return URL(new_path)
    
    def __str__(self) -> str:
        return self.path
    
    def __repr__(self) -> str:
        return f"{self.__class__.__name__}({repr(self.path)})"
    
    def __truediv__(self, other) -> "URL":
        return self.join_path(other)
    

class File:...
class Folder:...

@dataclass
class ContentTree:
    name: str
    path: str
    last_modified: datetime.datetime
    created: datetime.datetime
    content: List[Union[File, Folder]]
    


class Jupyter:
    def __init__(self, base_url: Union[str, URL], token: str) -> None:
        self.base_url = base_url if isinstance(base_url, URL) else URL(base_url)
        self.token = token
        self.auth_url = self.base_url / f"tree?token={self.token}"
        self.sess = requests.Session()
        self._is_authenticated = False
        self.api_url = self.base_url / "api"
        self.contents_url = self.api_url / "contents"
    
    def authenticate(self) -> None:
        if not self._is_authenticated:
            res = self.sess.get(self.auth_url)
            if res.status_code == 200:
                self._is_authenticated = True
            else:
                raise AuthenticationError("Unable to authenticate the Jupyter Session: please check the token passed")
    
    def tree(self) -> ContentTree:
        self.authenticate()
        res = self.sess.get(self.contents_url)
        if res.status_code == 200:
            return res.json()
        raise JupyterSessionError(f"Unable to get the tree.. due to some error: {res.status_code=}")


base_url = URL("http://localhost:8888")
token = "da739202730ad9f5512504281a4ccf64128a8bd5b42ca896"
jp = Jupyter(base_url, token)
jp.tree()

# auth_url = base_url / f"tree?token={token}"

# sess = requests.Session()
# res = sess.get(auth_url)
# res = sess.get(base_url / 'api')
# res = sess.get(base_url / "api" / "contents")
# res.json()




