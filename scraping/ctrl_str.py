from calendar import month


class CtrlStr():
    def __init__(self) -> None:
        pass
    
    def remove(self, before_data, *args):
        target = before_data
        for item in args:
            target = str(target).replace(item, "")
        return target
    
