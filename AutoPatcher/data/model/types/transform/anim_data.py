from data.model.types.mu_tag import MuTag
from data.model.types.transform.anim.anim_clip import AnimClip
from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter

class AnimData:
    def __init__(self, clips: list[AnimClip], default_clip: str, autoplay: bool):
        self.clips = clips
        self.default_clip = default_clip
        self.autoplay = autoplay

    def write(self, writer: ByteWriter):
        writer.write_int(MuTag.Animation)
        writer.write_int(len(self.clips))
        for clip in self.clips:
            clip.write(writer)

        writer.write_str(self.default_clip)
        writer.write_bool(self.autoplay)

    @staticmethod
    def read(reader: ByteReader) -> 'AnimData':
        reader.read_int()  # Consume Tag

        clips = []
        num_clips = reader.read_int()
        for i in range(num_clips):
            clip = AnimClip.read(reader)
            clips.append(clip)

        default_clip = reader.read_str()
        autoplay = reader.read_bool()

        return AnimData(
            clips = clips,
            default_clip = default_clip,
            autoplay = autoplay
        )