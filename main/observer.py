class Observer():
    @abstractmethod
    def update(self, status):
        raise NotImplementedError()