from data.model.types.mu_file import MuFile

class ModelOperation:
    def apply(self, mu_data: MuFile) -> MuFile:
        raise NotImplementedError(type(self))
