def initialize(cursor, _):
    cursor.execute("""
        CREATE TABLE types (
            type_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            PRIMARY KEY(type_id, language)
        )
    """)
    cursor.execute("""
        CREATE TABLE reprocess (
            type_id INTEGER NOT NULL,
            material_id INTEGER NOT NULL,
            quantity REAL NOT NULL,
            PRIMARY KEY(type_id, material_id)
        )
    """)

def insert_types(cursor, sde):
    languages = set()
    types = sde.type_ids()
    add_languages(languages, types)
    for type_id, row in types.items():
        names = row.get('name', {})
        for lang in languages:
            name = names.get(lang, "")
            cursor.execute("""
                INSERT INTO types (
                    type_id,
                    name,
                    language
                ) VALUES (?, ?, ?)
                """,
                (type_id, name, lang),
            )

def insert_materials(cursor, sde):
    types = sde.type_ids()
    sde_materials = sde.type_materials()

    for type_id, materials in sde_materials.items():
        materials = materials['materials']
        portion = float(types.get(type_id, {}).get('portionSize', 1))
        for material in materials:
            material_id = material['materialTypeID']
            quantity = float(material['quantity'])
            if portion != 1.0:
                quantity /= portion
            cursor.execute("""
                INSERT INTO reprocess (
                    type_id,
                    material_id,
                    quantity
                ) VALUES (?, ?, ?)
                """,
                (type_id, material_id, quantity),
            )

def insert(cursor, sde):
    insert_types(cursor, sde)
    insert_materials(cursor, sde)

def add_languages(languages, sde_data, name_key='name'):
    for row in sde_data.values():
        names = row.get(name_key, {})
        for lang in names.keys():
            languages.add(lang)

GENERATOR: 'dict[str, str | list[dict[str, str | function]]]' = {
    'ref': 'EVE_BUYBACK_SERVER_RS',
    'generators': [{
        'destination': 'db.sqlite',
        'initialize': initialize,
        'insert': insert,
    }],
}