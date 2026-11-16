from data.model.types.core.byte_writer import ByteWriter


class MuMeshComponent:
    def __str__(self) -> str:
        return type(self).__name__

    def write(self, writer: ByteWriter):
        raise NotImplementedError()
