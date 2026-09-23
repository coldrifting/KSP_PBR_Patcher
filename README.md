# KSP_PBR_Patcher
A collection of patchers to make supported KSP mods visually coherent with the Technicolor PBR system.
Contains a patcher that adds almost all of the stock parts that ReStockPBR v0.0.6 misses (including robotics), and any other mods I find the time to add support for.

Very much a work on progress right now<br>
[Current status can be seen here](https://docs.google.com/spreadsheets/d/111uGeFBigN7S7Hurd52V2qsdSPJAyhuw6wWZR8n1K9Y/edit?usp=sharing).

Current mods supported or planned (In various levels of completeness)
 - ReStockPBR_Patch (half patched)
 - SCANsat (textured, waiting on patch)
 - CryoTanks (textured, waiting on patch)
 - CryoEngines (half textured)
 - NFLaunchVehicles (half textured)

Notes:
- In order to run the install script, you'll need python 3.11 or greater, with the following packages installed:
  - `cairosvg`
  - `numpy`
  - `pillow`
  - `pyyaml`
  - `scipy`
  - `texconv-py`

- Neartea completed a set of pylon textures, but never released them as part of ReStockPBR version 0.0.6. 
  You can download them from the source repository using the links below. 
  Download all but the last of the below files and copy them into the ReStockPBR mod folder in your GameData directory, in the `Assets/Coupling` subdirectory. 
  Then save the last file (Making sure the extension is .cfg and not .txt) in the same mod folder under `Patches/Coupling`
  - [restock-pbr-pylon-small-1.mu](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Assets/Coupling/restock-pbr-pylon-small-1.mu)
  - [restock-pbr-pylon-large-1.mu](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Assets/Coupling/restock-pbr-pylon-large-1.mu)
  - [restock-pbr-pylons-1-a.dds](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Assets/Coupling/restock-pbr-pylons-1-a.dds)
  - [restock-pbr-pylons-1-m.dds](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Assets/Coupling/restock-pbr-pylons-1-m.dds)
  - [restock-pbr-pylons-1-n.dds](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Assets/Coupling/restock-pbr-pylons-1-n.dds)
  - [restock-pbr-pylons-1-tc.dds](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Assets/Coupling/restock-pbr-pylons-1-tc.dds)
  - [restock-pbr-pylons.cfg](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Patches/Coupling/restock-pbr-pylons.cfg)
- I also recommend downloading this file and placing it in `Assets/Aero` to fix a team color bug:
  - [restock-pbr-wings-4-tc.dds](https://github.com/PorktoberRevolution/ReStockPBR/raw/refs/heads/main/GameData/ReStockPBR/Assets/Aero/restock-pbr-wings-4-tc.dds)
