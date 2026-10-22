from data.model.types.core.byte_reader import ByteReader
from data.model.types.generic.mu_component import MuComponent


class MuComponentCollider(MuComponent):
    @staticmethod
    def read(reader: ByteReader, has_trigger: bool = False) -> 'MuComponentCollider':
        raise NotImplementedError()
