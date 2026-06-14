import os
import platform
import unittest
from unittest.mock import patch, mock_open

from mount_resolve._resolve import _df_output, resolve
from mount_resolve._resolve_linux import resolve_device as linux_resolve_device
from mount_resolve._resolve_linux import resolve_mount_point as linux_resolve_mount_point
from mount_resolve._resolve_darwin import resolve_device as darwin_resolve_device
from mount_resolve._resolve_darwin import resolve_mount_point as darwin_resolve_mount_point


class TestDFOutput(unittest.TestCase):
    @patch('mount_resolve._resolve.SYSTEM', 'Linux')
    @patch('subprocess.run')
    def test_df_output_linux_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = (
            'Filesystem     Type      Mounted on\n'
            'ext4      /      /dev/sda1\n'
        )
        result = _df_output('/some/file')
        self.assertEqual(result, ('/dev/sda1', '/', 'ext4'))

    @patch('mount_resolve._resolve.SYSTEM', 'Linux')
    @patch('subprocess.run')
    def test_df_output_linux_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        result = _df_output('/some/file')
        self.assertIsNone(result)

    @patch('mount_resolve._resolve.SYSTEM', 'Darwin')
    @patch('subprocess.run')
    def test_df_output_darwin_success(self, mock_run):
        mock_run.side_effect = [
            type('R', (), {'returncode': 0, 'stdout': 'Filesystem 512-blocks Used Available Capacity Mounted on\n/dev/disk1s1 100000 50000 50000 50% /\n'}),  # noqa: E501
            type('R', (), {'returncode': 0, 'stdout': 'apfs\n'}),
        ]
        result = _df_output('/some/file')
        self.assertEqual(result, ('/dev/disk1s1', '/', 'apfs'))

    @patch('mount_resolve._resolve.SYSTEM', 'Darwin')
    @patch('subprocess.run')
    def test_df_output_darwin_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        result = _df_output('/some/file')
        self.assertIsNone(result)


class TestResolveLinux(unittest.TestCase):
    @patch('os.stat')
    @patch('builtins.open', new_callable=mock_open, read_data=(
        'major minor  #blocks  name\n'
        '   8     1  100000 sda1\n'
        '   8     2  200000 sda2\n'
    ))
    def test_resolve_device_proc_partitions(self, mock_file, mock_stat):
        mock_stat.return_value.st_dev = os.makedev(8, 1)
        result = linux_resolve_device('/some/file')
        self.assertEqual(result, '/dev/sda1')

    @patch('os.stat')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('os.readlink')
    def test_resolve_device_sys_fallback(self, mock_readlink, mock_file, mock_stat):
        mock_stat.return_value.st_dev = os.makedev(8, 1)
        mock_readlink.return_value = '../../sda1'
        result = linux_resolve_device('/some/file')
        self.assertEqual(result, '/dev/sda1')

    @patch('os.stat')
    @patch('builtins.open', new_callable=mock_open, read_data='')
    @patch('os.readlink', side_effect=OSError)
    def test_resolve_device_none(self, mock_readlink, mock_file, mock_stat):
        mock_stat.return_value.st_dev = os.makedev(8, 1)
        result = linux_resolve_device('/some/file')
        self.assertIsNone(result)

    @patch('subprocess.run')
    def test_resolve_mount_point_success(self, mock_run):
        mock_run.return_value.returncode = 0
        mock_run.return_value.stdout = '/\n'
        result = linux_resolve_mount_point('/some/file')
        self.assertEqual(result, '/')

    @patch('subprocess.run')
    def test_resolve_mount_point_failure(self, mock_run):
        mock_run.return_value.returncode = 1
        mock_run.return_value.stdout = ''
        result = linux_resolve_mount_point('/some/file')
        self.assertIsNone(result)


class TestResolveDarwin(unittest.TestCase):
    @patch('mount_resolve._resolve_darwin._df_output')
    def test_resolve_device_success(self, mock_df):
        mock_df.return_value = ('/dev/disk1s1', '/', 'apfs')
        result = darwin_resolve_device('/some/file')
        self.assertEqual(result, '/dev/disk1s1')

    @patch('mount_resolve._resolve_darwin._df_output')
    def test_resolve_device_backing_file(self, mock_df):
        mock_df.return_value = ('/dev/disk2', '/Volumes/MyImage', 'hfs')
        with patch('mount_resolve._resolve_darwin._resolve_backing_file_darwin') as mock_backing:
            mock_backing.return_value = '/path/to/image.dmg'
            with patch('os.path.isfile', return_value=True):
                result = darwin_resolve_device('/Volumes/MyImage/file')
                self.assertEqual(result, '/path/to/image.dmg')

    @patch('mount_resolve._resolve_darwin._df_output')
    def test_resolve_device_none(self, mock_df):
        mock_df.return_value = None
        result = darwin_resolve_device('/some/file')
        self.assertIsNone(result)

    @patch('mount_resolve._resolve_darwin._df_output')
    def test_resolve_mount_point_success(self, mock_df):
        mock_df.return_value = ('/dev/disk1s1', '/', 'apfs')
        result = darwin_resolve_mount_point('/some/file')
        self.assertEqual(result, '/')

    @patch('mount_resolve._resolve_darwin._df_output')
    def test_resolve_mount_point_none(self, mock_df):
        mock_df.return_value = None
        result = darwin_resolve_mount_point('/some/file')
        self.assertIsNone(result)


class TestResolve(unittest.TestCase):
    @patch('mount_resolve._resolve.resolve_device')
    @patch('mount_resolve._resolve.resolve_mount_point')
    @patch('mount_resolve._resolve._df_output')
    def test_resolve_combined(self, mock_df, mock_mp, mock_dev):
        mock_dev.return_value = '/dev/sda1'
        mock_mp.return_value = '/'
        mock_df.return_value = ('/dev/sda1', '/', 'ext4')
        result = resolve('/some/file')
        self.assertEqual(result, ('/dev/sda1', '/', 'ext4'))

    @patch('mount_resolve._resolve.resolve_device')
    @patch('mount_resolve._resolve.resolve_mount_point')
    @patch('mount_resolve._resolve._df_output')
    def test_resolve_none_device(self, mock_df, mock_mp, mock_dev):
        mock_dev.return_value = None
        mock_mp.return_value = '/'
        mock_df.return_value = None
        result = resolve('/some/file')
        self.assertIsNone(result)

    @patch('mount_resolve._resolve.resolve_device')
    @patch('mount_resolve._resolve.resolve_mount_point')
    @patch('mount_resolve._resolve._df_output')
    def test_resolve_none_mount(self, mock_df, mock_mp, mock_dev):
        mock_dev.return_value = '/dev/sda1'
        mock_mp.return_value = None
        mock_df.return_value = None
        result = resolve('/some/file')
        self.assertIsNone(result)


if __name__ == '__main__':
    unittest.main()
