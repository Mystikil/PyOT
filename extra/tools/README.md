# Extra Tools

This directory contains a set of helper scripts and reference data used when developing or maintaining the project.  Many of the tools convert game data from the Open Tibia format into the JSON or SQL formats expected by the engine.  Below is an overview of each file.

## Conversion Utilities

### `lua2py.py`
Parses a Lua script and attempts to translate it to an equivalent Python script.  The script scans `actions.xml` to discover which item IDs or unique IDs call the Lua file so that generated decorators can register the resulting Python callback.  It performs many text substitutions to rewrite common Lua API calls into their Python counterparts.  At the end it prints the converted code to stdout.

### `spellxml2py.py`
Reads `spells.xml` from the Open Tibia data set and creates Python modules implementing those spells with the PyOT API.  The output is written under a `spells/` directory.  Only basic properties are generated—effects are left as TODOs to be completed manually.

### `otbxml2json.py`
Loads `items.otb` (binary item definitions) and `items.xml` and produces a cleaned JSON representation saved to `out.json` and a rewritten XML file `out.xml`.  The converter interprets item flags, merges data from the OTB file and XML, rewrites range definitions and outputs a compact JSON format for use by the server.

### `otbxml2sql.py`
Similar to `otbxml2json.py` but targets SQL.  It parses `items.otb` and `items.xml` and prints SQL `CREATE TABLE` statements and `INSERT` commands suitable for importing all items into a MySQL database.  Item attributes are translated into separate rows in an `item_attributes` table.

### `otbmxml2sec.py`
Converts a `.otbm` map file together with spawn and house XML files into PyOT’s binary `.sec` map sector format.  It builds a `Map` structure (using classes from `generator.py`) and writes one `.sec` file per sector.  Spawn information and house data are also exported—houses become an SQL file.

### `missing_items.py`
Parses `items.otb` and compares the result with the existing `items` table in a MySQL database (configured in `config.py`).  For any item ID not present it prints `INSERT` statements so the missing entries can be added.

### `generate_items.py`
Loads the server’s item definitions and produces a `gettext` PO template containing the item names and descriptions.  This assists with translating item strings.

### `groupgenerator.py`
Interactive helper that asks for a new group’s name and permissions and prints the corresponding `INSERT INTO groups` SQL statement.  The available flags are listed at the beginning of the script.

### `actionReader.py`
Small utility that searches `actions.xml` for all `<action>` elements referencing a specified Lua script and prints the associated item IDs.  Useful when migrating scripts.

### `makesqlitedb.sh`
Shell script that converts the latest MySQL schema (`latest_sql.sql` plus `houses.sql`) into a SQLite database file `database.db`.  It performs many `sed` transformations to adjust types and remove unsupported constructs.

### `generate.sh`
Automation script for building language files.  It runs `xgettext` to extract translation strings from the code base and then calls `generate_items.py` to append item names.  The resulting `en_EN.po` file is normalized with `msguniq`.

### `generator.py`
Provides classes used by `otbmxml2sec.py` and `testmap.py` to build `.sec` map sectors.  `Map`, `Item` and related classes handle tile data, spawns and serialization to the sector format.

### `testmap.py`
Example usage of `generator.py`.  It builds a 640×640 water map, populates it with a test area containing monsters and decorations, and finally compiles the map into sector files.

## Data Files

* `actions.xml` – example action configuration referenced by the conversion tools.
* `items.xml` / `items.otb` – item definitions used by the OTB converters.
* `map.otbm` – sample map used by `otbmxml2sec.py`.
* `Ezo-spawn.xml` – example spawn layout for converting with `otbmxml2sec.py`.
* `TLW-house.xml` – example house definitions.

These data files can be replaced with your own copies when running the conversion utilities.

## Usage Notes

Most of the Python scripts were originally written for Python 2 and should be executed from this directory so that relative paths resolve correctly.  The `otbmxml2sec.py` converter has been updated to run on Python 3 as well.  Some tools expect additional Python modules such as `inflect` or `MySQLdb`.  When converting map or item data ensure that the related XML/OTB files are present in this directory.


