{
  lib
, buildPythonPackage
, setuptools
, src
}:
buildPythonPackage rec {
  pname = "mount-resolve";
  version = "0.1.0";
  pyproject = true;

  inherit src;

  nativeBuildInputs = [ setuptools ];

  doCheck = false;
  pythonImportsCheck = [ "mount_resolve" ];

  meta = with lib; {
    description = "Cross-platform block device and mount point resolution from file paths";
    homepage = "https://github.com/MBanucu/mount-resolve";
    license = licenses.gpl3Only;
    maintainers = with maintainers; [ ];
  };
}
