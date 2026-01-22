{
  description = "Ray - N-body gravity simulator with collision physics";

  inputs = {
    flake-utils.url = "github:numtide/flake-utils";
    nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system:
      let
        pkgs = nixpkgs.legacyPackages.${system};
        python = pkgs.python3;
      in
      {
        packages.ray = python.pkgs.buildPythonPackage {
          pname = "ray";
          version = "0.1.0";
          src = ./.;
          propagatedBuildInputs = with python.pkgs; [
            pygame
          ];
          checkInputs = with python.pkgs; [
            pytest
          ];
          doCheck = true;
        };

        packages.default = self.packages.${system}.ray;

        devShells.default = pkgs.mkShell {
          buildInputs = with python.pkgs; [
            python
            pygame
            pytest
            pyinstaller
          ];
          shellHook = ''
            export PYTHONPATH="${builtins.toString ./.}:$PYTHONPATH"
          '';
        };

        apps.viewer = {
          type = "app";
          program = "${self.packages.${system}.ray}/bin/pygame_viewer";
        };
      }
    );
}
