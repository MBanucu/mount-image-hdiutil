{
  lib
, buildPythonPackage
, setuptools
, src
}:
buildPythonPackage rec {
  pname = "mount-image-hdiutil";
  version = "0.1.0";
  pyproject = true;

  inherit src;

  nativeBuildInputs = [ setuptools ];
  propagatedBuildInputs = [ ];

  doCheck = false;
  pythonImportsCheck = [ "mount_image_hdiutil" ];

  meta = with lib; {
    description = "Disk image mounting via hdiutil (macOS)";
    homepage = "https://github.com/MBanucu/mount-image-hdiutil";
    license = licenses.gpl3Only;
    maintainers = with maintainers; [ ];
  };
}
