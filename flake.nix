{
  outputs = {
    self,
    nixpkgs,
  }: let
    inherit (nixpkgs) lib;
  in {
    devShells = lib.genAttrs lib.systems.flakeExposed (system: let
      pkgs = nixpkgs.legacyPackages.${system};
    in {
      default = pkgs.mkShell {
        packages = with pkgs; [
          python3
        ];
      };
    });
  };
}
