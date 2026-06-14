{
  description = "mount-image-hdiutil: Disk image mounting via hdiutil (macOS)";

  inputs = {
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs =
    { self
    , nixpkgs
    , flake-utils
    }:
    flake-utils.lib.eachDefaultSystem (
      system:
      let
        pkgs = import nixpkgs {
          inherit system;
          overlays = [ self.overlays.default ];
        };
      in
      {
        packages.default = pkgs.python3.pkgs.mount-image-hdiutil;

        devShells.default = pkgs.mkShell {
          inputsFrom = [ pkgs.python3.pkgs.mount-image-hdiutil ];
          packages = [ pkgs.python3 ];
          shellHook = ''
            echo "mount-image-hdiutil dev shell. Run tests:"
            echo "  python -m unittest discover -s tests -v"
          '';
        };
      }
    )
    // {
      overlays.default = final: prev: {
        mount-image-hdiutil = final.python3.pkgs.callPackage ./default.nix {
          src = final.lib.cleanSource ./.;
        };
        python3 = prev.python3.override {
          packageOverrides = _: _: {
            inherit (final) mount-image-hdiutil;
          };
        };
      };
    };
}
