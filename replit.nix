{pkgs}: {
  deps = [
    pkgs.opencl-headers
    pkgs.ocl-icd
    pkgs.mesa_drivers
  ];
}
