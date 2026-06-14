"""Integration tests — mount a real FAT image via hdiutil (macOS)."""

import gzip
import os
import platform
import subprocess
import tempfile
import unittest
from pathlib import Path

_FAT_IMG_SIZE_MB = 1


def _sudo_available():
    return subprocess.run(['sudo', '-n', 'true'], capture_output=True).returncode == 0


def _mkfs_available():
    return subprocess.run(
        ['which', 'mkfs.fat'], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL).returncode == 0


def _create_fat_image(path):
    subprocess.run(['truncate', '-s', f'{_FAT_IMG_SIZE_MB}M', path], check=True)
    subprocess.run(['mkfs.fat', path], check=True, capture_output=True)


def _decompress_image(gz_path, dest_path):
    CHUNK = 1024 * 1024
    zero = b'\x00' * CHUNK
    full_size = _FAT_IMG_SIZE_MB * 1024 * 1024

    fd = os.open(dest_path, os.O_CREAT | os.O_WRONLY | os.O_TRUNC)
    os.ftruncate(fd, full_size)
    os.close(fd)

    offset = 0
    with gzip.open(gz_path, 'rb') as src, open(dest_path, 'rb+') as dst:
        while True:
            chunk = src.read(CHUNK)
            if not chunk:
                break
            if chunk != zero[:len(chunk)]:
                os.lseek(dst.fileno(), offset, os.SEEK_SET)
                dst.write(chunk)
            offset += len(chunk)


def _prepare_image():
    if _mkfs_available():
        fd, path = tempfile.mkstemp(suffix='.img', prefix='mount_image_test_')
        os.close(fd)
        _create_fat_image(path)
        return path

    gz_path = Path(__file__).parent / 'fat.img.gz'
    if not gz_path.exists():
        raise unittest.SkipTest('mkfs.fat not available and fat.img.gz fixture not found')

    fd, path = tempfile.mkstemp(suffix='.img', prefix='mount_image_test_')
    os.close(fd)
    _decompress_image(gz_path, path)
    return path


class TestHdiutilIntegration(unittest.TestCase):
    _img: str

    @classmethod
    def setUpClass(cls):
        if platform.system() != 'Darwin':
            raise unittest.SkipTest('macOS only')
        cls._img = _prepare_image()

    @classmethod
    def tearDownClass(cls):
        try:
            os.unlink(cls._img)
        except OSError:
            pass

    def test_mount_and_umount(self):
        from mount_image_hdiutil import mount_image, umount_image
        dev, mp = mount_image(self._img, fstype='vfat')
        self.assertTrue(dev.startswith('/dev/disk'))
        self.assertIsNotNone(mp)
        umount_image(dev, mp)

    def test_attach_and_detach(self):
        from mount_image_hdiutil import attach_image, detach_image
        dev = attach_image(self._img)
        self.assertTrue(dev.startswith('/dev/disk'))
        self.assertTrue(os.path.exists(dev))
        detach_image(dev)
