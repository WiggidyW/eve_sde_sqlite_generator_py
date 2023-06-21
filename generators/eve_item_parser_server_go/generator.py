def initialize(cursor, _):
    cursor.execute("""
        CREATE TABLE types (
            type_id INTEGER NOT NULL,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            PRIMARY KEY(type_id, language)
        )
    """)

def insert(cursor, sde):
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

def add_languages(languages, sde_data, name_key='name'):
    for row in sde_data.values():
        names = row.get(name_key, {})
        for lang in names.keys():
            languages.add(lang)

GENERATOR: 'dict[str, str | list[dict[str, str | function]]]' = {
    'ref': 'EVE_ITEM_PARSER_SERVER_GO',
    'generators': [{
        'destination': 'db.sqlite',
        'initialize': initialize,
        'insert': insert,
    }],
}
