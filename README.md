# mount-image-hdiutil

Disk image mounting via hdiutil (macOS).

[![PyPI version](https://img.shields.io/pypi/v/mount-image-hdiutil)](https://pypi.org/project/mount-image-hdiutil/)
[![Python](https://img.shields.io/badge/python-3.10%20%7C%203.11%20%7C%203.12%20%7C%203.13%20%7C%203.14-blue)](https://www.python.org/)
[![License](https://img.shields.io/github/license/MBanucu/mount-image-hdiutil)](LICENSE)
[![OS](https://img.shields.io/badge/OS-macOS-blue)](https://github.com/MBanucu/mount-image-hdiutil)

[![CI](https://img.shields.io/github/actions/workflow/status/MBanucu/mount-image-hdiutil/test.yml?branch=main)](https://github.com/MBanucu/mount-image-hdiutil/actions/workflows/test.yml)
[![codecov](https://codecov.io/gh/MBanucu/mount-image-hdiutil/branch/main/graph/badge.svg)](https://codecov.io/gh/MBanucu/mount-image-hdiutil)

[![Downloads total](https://pepy.tech/badge/mount-image-hdiutil)](https://pepy.tech/project/mount-image-hdiutil)
[![Downloads/month](https://pepy.tech/badge/mount-image-hdiutil/month)](https://pepy.tech/project/mount-image-hdiutil)
[![Downloads/week](https://pepy.tech/badge/mount-image-hdiutil/week)](https://pepy.tech/project/mount-image-hdiutil)

## Quick start

```python
from mount_image_hdiutil import mount_image, umount_image

device, mount_point = mount_image('/path/to/disk.img')
print(f'Mounted {device} at {mount_point}')
umount_image(device, mount_point)
```

## API

- `mount_image(path, fstype='exfat', options=None)` → `(device, mount_point)`
- `umount_image(device, mount_point=None)`
- `attach_image(path)` → `device`
- `detach_image(device)`

## License

GPL-3.0-only
