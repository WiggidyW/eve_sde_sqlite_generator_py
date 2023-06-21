def initialize(cursor, _):
    cursor.execute("""
        CREATE TABLE types (
            idx INTEGER NOT NULL,
            type_id INTEGER PRIMARY KEY NOT NULL,
            market_group_idx INTEGER NOT NULL,
            group_idx INTEGER NOT NULL,
            category_idx INTEGER NOT NULL
        )
    """)
    cursor.execute("""
        CREATE TABLE category_names (
            idx INTEGER NOT NULL,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            PRIMARY KEY(idx, language)
        )
    """)
    cursor.execute("""
        CREATE TABLE group_names (
            idx INTEGER NOT NULL,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            PRIMARY KEY(idx, language)
        )
    """)
    cursor.execute("""
        CREATE TABLE market_group_names (
            idx INTEGER NOT NULL,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            PRIMARY KEY(idx, language)
        )
    """)
    cursor.execute("""
        CREATE TABLE type_names (
            idx INTEGER NOT NULL,
            name TEXT NOT NULL,
            language TEXT NOT NULL,
            PRIMARY KEY(idx, language)
        )
    """)

def insert(cursor, sde):
    languages = set()
    
    categories = sde.category_ids()
    add_languages(languages, categories)
    category_indexes = index_division(categories)

    groups = sde.group_ids()
    add_languages(languages, groups)
    group_indexes = index_division(groups)

    market_groups = sde.market_groups()
    add_languages(languages, market_groups, name_key='nameID')
    market_group_indexes = index_division(market_groups)

    types = sde.type_ids()
    add_languages(languages, types)

    insert_division(cursor, categories, languages, 'category_names')
    insert_division(cursor, groups, languages, 'group_names')
    insert_division(
        cursor,
        market_groups,
        languages,
        'market_group_names',
        name_key='nameID',
    )
    
    insert_types(
        cursor,
        types,
        groups,
        languages,
        market_group_indexes,
        group_indexes,
        category_indexes,
    )

def add_languages(languages, sde_data, name_key='name'):
    for row in sde_data.values():
        names = row.get(name_key, {})
        for lang in names.keys():
            languages.add(lang)

def index_division(sde_data):
    # 0 is a special index for types with no group/category/market_group.
    division_indexes = { 0: 0 }
    i = 1
    for id in sde_data.keys():
        division_indexes.update({ id: i })
        i += 1
    return division_indexes

def insert_division(
    cursor,
    sde_data,
    languages,
    table_name,
    name_key='name',
):
    # Give types a fallback group/category/market_group name in case they
    # have no group/category/market_group.
    for lang in languages:
        cursor.execute(f"""
            INSERT INTO {table_name} (
                idx,
                name,
                language
            )
            VALUES (?, ?, ?)
            """,
            (0, "", lang),
        )
    # Insert the actual group/category/market_group names, starting from 1.
    i = 1
    for row in sde_data.values():
        names = row.get(name_key, {})
        for lang in languages:
            name = names.get(lang, "")
            cursor.execute(f"""
                INSERT INTO {table_name} (
                    idx,
                    name,
                    language
                )
                VALUES (?, ?, ?)
                """,
                (i, name, lang),
            )
        i += 1

def insert_types(
    cursor,
    sde_data,
    group_sde_data,
    languages,
    market_group_indexes,
    group_indexes,
    category_indexes,
):
    i = 0
    for type_id, row in sde_data.items():
        names = row.get('name', {})
        for lang in languages:
            name = names.get(lang, "")
            cursor.execute("""
                INSERT INTO type_names (
                    idx,
                    name,
                    language
                )
                VALUES (?, ?, ?)
                """,
                (i, name, lang),
            )
        cursor.execute("""
            INSERT INTO types (
                idx,
                type_id,
                market_group_idx,
                group_idx,
                category_idx
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (
                i,
                type_id,
                market_group_indexes[row.get('marketGroupID', 0)],
                group_indexes[row.get('groupID', 0)],
                category_indexes[
                    # Get the Group if there is one, else {}
                    group_sde_data.get(row.get('groupID', -1), {})\
                    # Get the Group's CategoryID if there is one, else 0
                    .get('categoryID', 0)\
                ],
            ),
        )
        i += 1

GENERATOR: 'dict[str, str | list[dict[str, str | function]]]' = {
    'ref': 'EVE_ITEM_CONFIGURATOR_SQLITE_ACCESSOR_RS',
    'generators': [{
        'destination': 'db.sqlite',
        'initialize': initialize,
        'insert': insert,
    }],
}
