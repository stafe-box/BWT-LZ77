from Archiver import Archiver

# Архивируем файл
archiver = Archiver()
archiver.compress("thing.stl", "compressed.bin")
archiver.decompress("compressed.bin", "output.stl")
