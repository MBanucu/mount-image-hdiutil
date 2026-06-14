"""Unit tests for mount_image_hdiutil — mocked subprocess calls."""

import plistlib
import unittest
from unittest.mock import patch, MagicMock


def _make_plist(entities):
    return plistlib.dumps(
        {'system-entities': entities},
        fmt=plistlib.FMT_XML,
    ).decode()


class TestHdiutilMount(unittest.TestCase):
    @patch('mount_image_hdiutil.subprocess.run')
    def test_mount_image_auto_mount_succeeds(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout=_make_plist([
            {'dev-entry': '/dev/disk5', 'mount-point': '/Volumes/Test'},
        ]), stderr='')
        from mount_image_hdiutil import mount_image
        device, mount_point = mount_image('/tmp/test.img')
        self.assertEqual(device, '/dev/disk5')
        self.assertEqual(mount_point, '/Volumes/Test')

    @patch('mount_image_hdiutil.subprocess.run')
    def test_mount_image_attach_fails(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1, stdout='', stderr='attach failed')
        from mount_image_hdiutil import mount_image
        with self.assertRaises(RuntimeError) as ctx:
            mount_image('/tmp/test.img')
        self.assertIn('hdiutil attach failed', str(ctx.exception))

    @patch('mount_image_hdiutil.subprocess.run')
    @patch('mount_image_hdiutil.tempfile.mkdtemp')
    def test_mount_image_via_partition(self, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = '/tmp/mp'
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout=_make_plist([
                {'dev-entry': '/dev/disk5'},
            ]), stderr=''),
            MagicMock(returncode=0),
            MagicMock(returncode=0, stdout=_make_plist([
                {'dev-entry': '/dev/disk5'},
                {'dev-entry': '/dev/disk5s1'},
            ]), stderr=''),
            MagicMock(returncode=0, stdout='', stderr=''),
        ]
        from mount_image_hdiutil import mount_image
        device, mount_point = mount_image('/tmp/test.img')
        self.assertEqual(device, '/dev/disk5s1')
        self.assertEqual(mount_point, '/tmp/mp')

    @patch('mount_image_hdiutil.subprocess.run')
    @patch('mount_image_hdiutil.tempfile.mkdtemp')
    def test_mount_image_via_whole_disk(self, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = '/tmp/mp'
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout=_make_plist([
                {'dev-entry': '/dev/disk5'},
            ]), stderr=''),
            MagicMock(returncode=0),
            MagicMock(returncode=0, stdout=_make_plist([
                {'dev-entry': '/dev/disk5'},
            ]), stderr=''),
            MagicMock(returncode=0, stdout='', stderr=''),
        ]
        from mount_image_hdiutil import mount_image
        device, mount_point = mount_image('/tmp/test.img')
        self.assertEqual(device, '/dev/disk5')
        self.assertEqual(mount_point, '/tmp/mp')

    @patch('mount_image_hdiutil.subprocess.run')
    @patch('mount_image_hdiutil.tempfile.mkdtemp')
    def test_mount_image_all_mounts_fail(self, mock_mkdtemp, mock_run):
        mock_mkdtemp.return_value = '/tmp/mp'
        mock_run.side_effect = [
            MagicMock(returncode=0, stdout=_make_plist([
                {'dev-entry': '/dev/disk5'},
            ]), stderr=''),
            MagicMock(returncode=0),
            MagicMock(returncode=0, stdout=_make_plist([
                {'dev-entry': '/dev/disk5'},
                {'dev-entry': '/dev/disk5s1'},
            ]), stderr=''),
            MagicMock(returncode=1),
            MagicMock(returncode=1),
            MagicMock(returncode=0),
        ]
        from mount_image_hdiutil import mount_image
        with self.assertRaises(RuntimeError) as ctx:
            mount_image('/tmp/test.img')
        self.assertIn('mount failed', str(ctx.exception))

    @patch('mount_image_hdiutil.subprocess.run')
    def test_umount_image_with_mount_point(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        from mount_image_hdiutil import umount_image
        umount_image('/dev/disk5', '/tmp/mp')

    @patch('mount_image_hdiutil.subprocess.run')
    def test_umount_image_no_mount_point(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        from mount_image_hdiutil import umount_image
        umount_image('/dev/disk5')

    @patch('mount_image_hdiutil.subprocess.run')
    def test_attach_image_whole_disk(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout=_make_plist([
            {'dev-entry': '/dev/disk5'},
            {'dev-entry': '/dev/disk5s1'},
        ]), stderr='')
        from mount_image_hdiutil import attach_image
        device = attach_image('/tmp/test.img')
        self.assertEqual(device, '/dev/disk5')

    @patch('mount_image_hdiutil.subprocess.run')
    def test_attach_image_only_slices_fallback(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0, stdout=_make_plist([
            {'dev-entry': '/dev/disk5s1'},
        ]), stderr='')
        from mount_image_hdiutil import attach_image
        device = attach_image('/tmp/test.img')
        self.assertEqual(device, '/dev/disk5s1')

    @patch('mount_image_hdiutil.subprocess.run')
    def test_attach_image_no_entities(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=0, stdout=_make_plist([]), stderr='')
        from mount_image_hdiutil import attach_image
        with self.assertRaises(RuntimeError) as ctx:
            attach_image('/tmp/test.img')
        self.assertIn('no devices', str(ctx.exception))

    @patch('mount_image_hdiutil.subprocess.run')
    def test_attach_image_attach_fails(self, mock_run):
        mock_run.return_value = MagicMock(
            returncode=1, stdout='', stderr='attach failed')
        from mount_image_hdiutil import attach_image
        with self.assertRaises(RuntimeError) as ctx:
            attach_image('/tmp/test.img')
        self.assertIn('hdiutil attach', str(ctx.exception))

    @patch('mount_image_hdiutil.subprocess.run')
    def test_detach_image(self, mock_run):
        mock_run.return_value = MagicMock(returncode=0)
        from mount_image_hdiutil import detach_image
        detach_image('/dev/disk5')
