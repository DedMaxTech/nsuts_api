from nsuts import User
from inspect import signature

docs=''

for k, v in User.__dict__.items():
    if not k.startswith("_"):
        if isinstance(v, classmethod): v = v.__func__
        doc = v.__doc__.split("\n")[0]
        docs += f'* ```python\n  User.{k}{signature(v)}\n  ```\n\n  {doc}\n\n'

print(docs)