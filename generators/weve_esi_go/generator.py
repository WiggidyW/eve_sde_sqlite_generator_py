def initialize(cursor, _):
    cursor.execute("""
        CREATE TABLE systems (
            system_id INTEGER NOT NULL PRIMARY KEY,
            region_id INTEGER NOT NULL
        )
    """)

def insert(cursor, sde):
    systems = sde.solar_systems()
    for system in systems:
        cursor.execute("""
            INSERT INTO systems (
                system_id,
                region_id
            ) VALUES (?, ?)
            """,
            (system['solarSystemID'], system['regionID']),
       )

GENERATOR: 'dict[str, str | list[dict[str, str | function]]]' = {
    'ref': 'WEVE_ESI_GO',
    'generators': [{
        'destination': 'db.sqlite',
        'initialize': initialize,
        'insert': insert,
    }],
}
