from data.model.types.tag.tag_mu import MuTag
from data.model.types.generic.mu_component import MuComponent
from data.model.types.transform_components.animation_components.animation_clip import AnimationClip
from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter

class Animation(MuComponent):
    def __init__(self, clips: list[AnimationClip], default_clip: str, autoplay: bool):
        self.clips: list[AnimationClip] = clips
        self.default_clip: str = default_clip
        self.autoplay: bool = autoplay

    @staticmethod
    def read(reader: ByteReader) -> 'Animation':
        clips: list[AnimationClip] = []
        num_clips = reader.read_int()
        for i in range(num_clips):
            clips.append(AnimationClip().read(reader))

        default_clip: str = reader.read_str()
        autoplay: bool = reader.read_bool()

        return Animation(clips=clips,
                         default_clip=default_clip,
                         autoplay=autoplay)


    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.Animation)

        writer.write_int(len(self.clips))
        for clip in self.clips:
            clip.write(writer)

        writer.write_str(self.default_clip)
        writer.write_bool(self.autoplay)
