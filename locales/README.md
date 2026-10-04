# UI locale catalogs

`en-US.json` is the authoritative UI source catalog. A translated catalog uses the
same keys and contains translated values. MeshMill falls back to the English value
when a key or catalog is missing.

The runtime discovers translated catalogs named `<locale>.json`. Locale metadata,
including text direction, is defined in `manifest.json`. Keep placeholders,
shortcuts, product names, and file formats unchanged where required.

Run `python tools/localization/extract_ui_catalog.py` after changing user-visible
application text. Run `python tools/localization/validate_locales.py` before packaging.
