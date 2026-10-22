from src.diff_parser import parse_diff


def test_grocery_adds_honey_at_6():
    diff = """diff --git a/groceries.txt b/groceries.txt
--- a/groceries.txt
+++ b/groceries.txt
@@ -1,5 +2,5 @@
 milk
-eggs
 bread
+++
 butter
+honey
 jam """  # blank 1: the grocery diff, starting at "diff --git"
    result = parse_diff(diff)

    assert len(result) == 1  # blank 2: how many files?
    assert result[0]["additions"] == [{'line': '++', 'line_num': 4}, {'line': 'honey', 'line_num': 6}]  # blank 3: list of dicts, worked out by hand


def test_deleted_file_is_dropped():
    diff = """diff --git a/d.py b/d.py
            deleted file mode 100644
            --- a/d.py
            +++ /dev/null"""  # blank 4: a deleted file, then a normal file
    result = parse_diff(diff)

    assert [f["new_file"] for f in result] == []  # blank 5: which file names remain?


def test_empty_string():
    assert parse_diff("") == [] # blank 6

def test_marker_line_does_not_advance_counter():
    diff = """diff --git a/f.txt b/f.txt
--- a/f.txt
+++ b/f.txt
@@ -1,3 +1,3 @@
 a
-b
____
+c
 d
+e"""
    result = parse_diff(diff)

    assert result[0]["additions"] == [{'line': 'c', 'line_num': 3}, {'line': 'e', 'line_num': 5}] 