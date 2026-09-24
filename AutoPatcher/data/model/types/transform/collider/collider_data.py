from data.model.types.transform.collider.collider_data_item_box import ColliderDataItemBox
from data.model.types.transform.collider.collider_data_item_capsule import ColliderDataItemCapsule
from data.model.types.transform.collider.collider_data_item_mesh import ColliderDataItemMesh
from data.model.types.transform.collider.collider_data_item_sphere import ColliderDataItemSphere
from data.model.types.core.byte_reader import ByteReader
from data.model.types.core.byte_writer import ByteWriter
from data.model.types.mu_tag import MuTag


class ColliderData:
    def __init__(self,
                 is_trigger: bool | None,
                 box_data: ColliderDataItemBox | None = None,
                 sphere_data: ColliderDataItemSphere | None = None,
                 capsule_data: ColliderDataItemCapsule | None = None,
                 mesh_data: ColliderDataItemMesh | None = None):
        self.is_trigger = is_trigger
        self.box_data = box_data
        self.sphere_data = sphere_data
        self.capsule_data = capsule_data
        self.mesh_data = mesh_data

    def write(self, writer: ByteWriter):
        if self.box_data is not None:
            self.box_data.write(writer, self.is_trigger)
        elif self.sphere_data is not None:
            self.sphere_data.write(writer, self.is_trigger)
        elif self.capsule_data is not None:
            self.capsule_data.write(writer, self.is_trigger)
        elif self.mesh_data is not None:
            self.mesh_data.write(writer, self.is_trigger)
        else:
            raise Exception(f"Invalid collider: No collider shape data attached")

    @staticmethod
    def read(reader: ByteReader) -> 'ColliderData':
        tag = reader.read_int()

        is_trigger = None
        if tag in ColliderData.tags_trigger():
            is_trigger = reader.read_bool()

        box_data = ColliderDataItemBox.read(reader) if tag in (MuTag.BoxCollider, MuTag.BoxCollider2) else None
        sphere_data = ColliderDataItemSphere.read(reader) if tag in (MuTag.SphereCollider, MuTag.SphereCollider2) else None
        capsule_data = ColliderDataItemCapsule.read(reader) if tag in (MuTag.CapsuleCollider, MuTag.CapsuleCollider2) else None
        mesh_data = ColliderDataItemMesh.read(reader) if tag in (MuTag.MeshCollider, MuTag.MeshCollider2) else None

        return ColliderData(
            is_trigger = is_trigger,
            box_data = box_data,
            sphere_data = sphere_data,
            capsule_data = capsule_data,
            mesh_data = mesh_data
        )

    @staticmethod
    def tags():
        return [
            MuTag.MeshCollider,
            MuTag.MeshCollider2,
            MuTag.BoxCollider,
            MuTag.BoxCollider2,
            MuTag.SphereCollider,
            MuTag.SphereCollider2,
            MuTag.CapsuleCollider,
            MuTag.CapsuleCollider2
        ]

    @staticmethod
    def tags_trigger():
        return [
            MuTag.MeshCollider2,
            MuTag.BoxCollider2,
            MuTag.SphereCollider2,
            MuTag.CapsuleCollider2
        ]
