{
  description = "jobapps: Python and LaTeX for the tools/ scripts and the test suite";

  inputs.nixpkgs.url = "github:NixOS/nixpkgs/nixos-unstable";

  outputs = { self, nixpkgs }:
    let
      systems = [ "x86_64-linux" "aarch64-linux" "x86_64-darwin" "aarch64-darwin" ];
      forAll = f: nixpkgs.lib.genAttrs systems (system: f nixpkgs.legacyPackages.${system});
    in
    {
      devShells = forAll (pkgs: {
        default = pkgs.mkShell {
          packages = [
            # `python` and `python3` both resolve here; the skills call `python`.
            (pkgs.python3.withPackages (ps: [ ps.pymupdf ps.openpyxl ]))
            # The packages templates/mega-resume.tex and tools/build_cover_letter.py load,
            # on top of scheme-small.
            (pkgs.texliveSmall.withPackages (ps: with ps; [
              enumitem fancyhdr fontawesome5 marvosym preprint titlesec
            ]))
            pkgs.git
          ];
        };
      });
    };
}
