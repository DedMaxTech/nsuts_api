from nsuts import User
from inspect import signature

method_list = [func for func in dir(User) if callable(getattr(User, func)) and not func.startswith("__")]

docs=''

def sum(a:int, b:int):
    return a+b


for k, v in User.__dict__.items():
    if not k.startswith("_"):
        if isinstance(v, classmethod): v = v.__func__
        doc = v.__doc__.split("\n")[0]
        docs += f'* User.{k}{signature(v)}\n\n  {doc}\n'

print(docs)