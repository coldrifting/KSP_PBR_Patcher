from data.model.mu_data import MuData


class Operation:
    def apply(self, mu_data: MuData):
        raise NotImplementedError()
