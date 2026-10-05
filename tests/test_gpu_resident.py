from gpu_resident import ResidentBufferInfo, choose_compute_backend, inspect_resident_vertices


class FakeVbo:
    def IsReady(self):
        return True

    def GetHandle(self):
        return 41

    def GetSize(self):
        return 12_000

    def GetStride(self):
        return 24

    def GetNumberOfComponents(self):
        return 3

    def GetNumberOfTuples(self):
        return 500


class FakeGroup:
    def GetVBO(self, name):
        return FakeVbo() if name == "vertexMC" else None


class FakeMapper:
    def GetVBOs(self):
        return FakeGroup()


class FakeActor:
    def GetMapper(self):
        return FakeMapper()


def test_inspects_vtk_vertex_buffer_metadata():
    assert inspect_resident_vertices(FakeActor()) == ResidentBufferInfo(41, 12_000, 24, 3, 500)


def test_backend_requires_large_resident_work_and_validated_interop():
    resident = ResidentBufferInfo(41, 12_000, 24, 3, 500)
    assert choose_compute_backend(65_536, resident, interop_available=True).backend == "cpu"
    assert choose_compute_backend(500_000, resident, interop_available=False).backend == "cpu"
    selected = choose_compute_backend(500_000, resident, interop_available=True)
    assert selected.backend == "gpu-resident"
