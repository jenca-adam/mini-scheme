def get_repr(obj):
    if obj is True:
        return "#t"
    if obj is False:
        return "#f"
    if callable(obj):
        return f"function {obj.__name__}"
    return str(obj)
