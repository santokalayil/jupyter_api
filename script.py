from typing import Union
import requests
from pathlib import Path

class URL:
    def __init__(self, path: Union[str, "URL"]) -> None:
        self.path = path.removesuffix("/")
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
    
class URLPath(URL):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)


s = URLPath("Santo")

base_url = URL("http://localhost:8888")
token = "da739202730ad9f5512504281a4ccf64128a8bd5b42ca896"
auth_url = base_url / f"tree?token={token}"

sess = requests.Session()
res = sess.get(auth_url)
res = sess.get(base_url / 'api')
res = sess.get(base_url / "api" / "contents")
res.json()




