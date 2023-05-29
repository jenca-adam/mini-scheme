def get_repr(obj):
    if obj==True:
        return "#t"
    if obj==False:
        return "#f"
    if callable(obj):
        return f"function {obj.__name__}"
    return str(obj)
