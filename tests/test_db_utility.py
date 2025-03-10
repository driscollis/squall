# test_db_utility.py

from squall.db_utility import parse_out_fields


def test_schema_with_primary_and_foreign_keys():
    schema = (
        "CREATE TABLE grids (\n"
        "                game_id INTEGER NOT NULL,\n"
        "                user_id INTEGER NOT NULL,\n"
        "                sub_grid_id TEXT NOT NULL,\n"
        "                grid_data TEXT NOT NULL,\n"
        "                FOREIGN KEY(user_id) REFERENCES users(id) ON DELETE "
        "CASCADE,\n"
        "                FOREIGN KEY(game_id) REFERENCES games(id) ON DELETE "
        "CASCADE,\n"
        "                PRIMARY KEY (game_id, user_id, sub_grid_id)\n"
        "            )"
    )
    result = parse_out_fields(schema)
    assert result == {
        "game_id": {"Schema": '"game_id" INTEGER NOT NULL', "Type": "INTEGER"},
        "grid_data": {"Schema": '"grid_data" TEXT NOT NULL', "Type": "TEXT"},
        "sub_grid_id": {"Schema": '"sub_grid_id" TEXT NOT NULL', "Type": "TEXT"},
        "user_id": {"Schema": '"user_id" INTEGER NOT NULL', "Type": "INTEGER"},
    }


def test_schema_with_multiple_tables_defined_on_single_line():
    schema = (
        "CREATE TABLE books\n"
        "                  (title TEXT, author TEXT, release_date TEXT,\n"
        "                   publisher TEXT, book_type TEXT)"
    )
    result = parse_out_fields(schema)
    assert result == {
        "title": {"Type": "TEXT", "Schema": '"title" TEXT'},
        "author": {"Type": "TEXT", "Schema": '"author" TEXT'},
        "release_date": {"Type": "TEXT", "Schema": '"release_date" TEXT'},
        "publisher": {"Type": "TEXT", "Schema": '"publisher" TEXT'},
        "book_type": {"Type": "TEXT", "Schema": '"book_type" TEXT)'},
    }


def test_schema_with_on_delete():
    """
    Tests a DB schema that incldue an "ON DELETE" line in it
    """
    schema = (
        "CREATE TABLE [Album]\n"
        "(\n"
        "    [AlbumId] INTEGER  NOT NULL,\n"
        "    [Title] NVARCHAR(160)  NOT NULL,\n"
        "    [ArtistId] INTEGER  NOT NULL,\n"
        "    CONSTRAINT [PK_Album] PRIMARY KEY  ([AlbumId]),\n"
        "    FOREIGN KEY ([ArtistId]) REFERENCES [Artist] ([ArtistId]) \n"
        "ON DELETE NO ACTION ON UPDATE NO ACTION\n"
        ")"
    )
    result = parse_out_fields(schema)
    assert result == {
        "AlbumId": {"Type": "INTEGER", "Schema": '"AlbumId" INTEGER NOT NULL'},
        "Title": {"Type": "NVARCHAR160", "Schema": '"Title" NVARCHAR(160) NOT NULL'},
        "ArtistId": {"Type": "INTEGER", "Schema": '"ArtistId" INTEGER NOT NULL'},
    }


def test_schema_with_no_line_endings():
    """
    Tests a schema that has no line endings in it (i.e. \n)
    """
    schema = (
        "CREATE TABLE groups (id           INTEGER PRIMARY KEY,                    "
        "name         TEXT NOT NULL)"
    )
    result = parse_out_fields(schema)
    assert result == {
        "id": {"Schema": '"id" INTEGER PRIMARY KEY', "Type": "INTEGER"},
        "name": {"Schema": '"name" TEXT NOT NULL)', "Type": "TEXT"},
    }


def test_schema_without_types():
    schema = "CREATE TABLE sqlite_sequence(name,seq)"
    result = parse_out_fields(schema)
    assert result == {
        "name": {"Schema": '"name" ', "Type": "name"},
        "seq": {"Schema": '"seq" ', "Type": "seq"},
    }


def test_without_keyword_excluded_from_schema():
    schema = (
        "CREATE TABLE moz_meta (\n"
        "              key\n"
        "                TEXT PRIMARY KEY NOT NULL,\n"
        "              value\n"
        "                INTEGER\n"
        "            ) WITHOUT ROWID"
    )
    result = parse_out_fields(schema)
    assert result == {
        "key": {"Schema": '"key" TEXT PRIMARY KEY NOT NULL', "Type": "TEXT"},
        "value": {"Schema": '"value" INTEGER', "Type": "INTEGER"},
    }
