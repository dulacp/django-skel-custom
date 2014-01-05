def compose(*functions):
    """
    Compose functions

    This is useful for combining decorators.
    Example :

    >>> @compose(dec1, dec2)
    ... def some(f):
    ...    pass
    """
    def _composed(*args):
        for fn in functions:
            try:
                args = fn(*args)
            except TypeError:
                # args must be scalar so we don't try to expand it
                args = fn(args)
        return args
    return _composed


def order_fields(*field_list):
    def decorator(form):
        original_init = form.__init__
        def init(self, *args, **kwargs):
            original_init(self, *args, **kwargs)        
            for field in field_list[::-1]:
                self.fields.insert(0, field, self.fields.pop(field))
        form.__init__ = init
        return form            
    return decorator
