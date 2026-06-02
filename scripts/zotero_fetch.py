#!/usr/bin/env python3
"""
Fetch items from Zotero and output YAML compatible with the
citation-relevance-auditor evidence_db.md format.

Two modes:
  1. API mode (default) — uses Zotero API via pyzotero
  2. Local mode          — reads zotero.sqlite directly (no API key needed)

Usage:
  # API mode
  python scripts/zotero_fetch.py --api-key KEY --library-id 12345

  # Local mode (reads ~/Zotero/zotero.sqlite by default)
  python scripts/zotero_fetch.py --local
  python scripts/zotero_fetch.py --local --db /path/to/zotero.sqlite

Optional:
  --collection COLLECTION_KEY   Restrict to a specific collection
  --limit N                     Max items (default 50)
  --output FILE                 Write to file instead of stdout
  --format evidence|scout       Output format (default: evidence)
"""
import argparse
import os
import sqlite3
import sys

try:
    import yaml
except ImportError:
    print("Missing pyyaml. Install: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


LOCAL_DB = os.path.expanduser("~/Zotero/zotero.sqlite")

# Zotero itemTypeID → type name mapping (core types)
ITEM_TYPES = {
    1: "note", 2: "book", 3: "bookSection", 4: "journalArticle",
    5: "magazineArticle", 6: "newspaperArticle", 7: "thesis",
    8: "letter", 9: "manuscript", 10: "interview", 11: "film",
    12: "artwork", 13: "webpage", 14: "report", 15: "bill",
    16: "case", 17: "hearing", 18: "patent", 19: "statute",
    20: "email", 21: "map", 22: "blogPost", 23: "instantMessage",
    24: "forumPost", 25: "audioRecording", 26: "presentation",
    27: "videoRecording", 28: "tvBroadcast", 29: "radioBroadcast",
    30: "podcast", 31: "computerProgram", 32: "conferencePaper",
    33: "document", 34: "encyclopediaArticle", 35: "dictionaryEntry",
    36: "attachment", 37: "annotation",
}


def clean_text(text):
    if not text:
        return ""
    return text.replace("\n", " ").strip()


# ── Local SQLite reader ────────────────────────────────────────────

def fetch_local(db_path, collection_key=None, limit=50):
    if not os.path.exists(db_path):
        print(f"Database not found: {db_path}", file=sys.stderr)
        sys.exit(1)

    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    c = conn.cursor()

    # Get library ID (we'll just use 1 for the default user library)
    c.execute("SELECT libraryID FROM libraries LIMIT 1")
    lib_row = c.fetchone()
    library_id = lib_row["libraryID"] if lib_row else 1

    # If collection_key given, resolve collectionID
    collection_id = None
    if collection_key:
        c.execute("SELECT collectionID FROM collections WHERE key=? AND libraryID=?",
                   (collection_key, library_id))
        row = c.fetchone()
        if row:
            collection_id = row["collectionID"]
        else:
            print(f"Collection key '{collection_key}' not found", file=sys.stderr)
            conn.close()
            sys.exit(1)

    # Build the query (itemData joins through itemDataValues for the actual value)
    base_joins = """
        FROM items i
        JOIN itemData id ON id.itemID = i.itemID
        JOIN itemDataValues idv ON idv.valueID = id.valueID
        JOIN fieldsCombined f ON f.fieldID = id.fieldID
        WHERE i.libraryID = ?
          AND i.itemTypeID NOT IN (36, 37)  -- exclude attachments & annotations
    """
    params = [library_id]

    if collection_id:
        base_joins = """
            FROM items i
            JOIN collectionItems ci ON ci.itemID = i.itemID
            JOIN itemData id ON id.itemID = i.itemID
            JOIN itemDataValues idv ON idv.valueID = id.valueID
            JOIN fieldsCombined f ON f.fieldID = id.fieldID
            WHERE i.libraryID = ?
              AND ci.collectionID = ?
              AND i.itemTypeID NOT IN (36, 37)
        """
        params = [library_id, collection_id]

    query = f"""
        SELECT i.itemID, i.key, i.itemTypeID, i.dateAdded, i.dateModified,
               f.fieldName, idv.value
        {base_joins}
        ORDER BY i.dateAdded DESC
        LIMIT ?
    """
    params.append(limit)

    c.execute(query, params)
    rows = c.fetchall()

    # Group by itemID into dicts
    items = {}
    item_ids = []
    for r in rows:
        iid = r["itemID"]
        if iid not in items:
            items[iid] = {
                "itemID": iid,
                "key": r["key"],
                "itemTypeID": r["itemTypeID"],
                "dateAdded": r["dateAdded"],
                "dateModified": r["dateModified"],
                "data": {},
            }
            item_ids.append(iid)
        items[iid]["data"][r["fieldName"]] = r["value"]

    # Fetch creators (authors) — author type is 10
    if item_ids:
        placeholders = ",".join("?" for _ in item_ids)
        c.execute(f"""
            SELECT ic.itemID, c.firstName, c.lastName, ic.creatorTypeID
            FROM itemCreators ic
            JOIN creators c ON c.creatorID = ic.creatorID
            WHERE ic.itemID IN ({placeholders})
              AND ic.creatorTypeID = 10
            ORDER BY ic.orderIndex
        """, item_ids)
        for r2 in c.fetchall():
            iid = r2["itemID"]
            if iid in items:
                items[iid].setdefault("creators", []).append({
                    "firstName": r2["firstName"] or "",
                    "lastName": r2["lastName"] or "",
                    "creatorTypeID": r2["creatorTypeID"],
                })

    # Fetch tags
    if item_ids:
        c.execute(f"""
            SELECT ti.itemID, t.name, ti.type AS tagType
            FROM itemTags ti
            JOIN tags t ON t.tagID = ti.tagID
            WHERE ti.itemID IN ({placeholders})
        """, item_ids)
        for r3 in c.fetchall():
            iid = r3["itemID"]
            if iid in items:
                items[iid].setdefault("tags", []).append(r3["name"])

    conn.close()

    # Convert to a list sorted by dateAdded desc
    result = []
    for iid in item_ids:
        item = items[iid]
        data = item["data"]
        creators = item.get("creators", [])

        author_str = "; ".join(
            f"{c['lastName']}, {c['firstName']}" if c.get("lastName") else (c.get("name") or "")
            for c in creators
        )

        abstract = clean_text(data.get("abstractNote", ""))
        title = clean_text(data.get("title", ""))
        date_str = data.get("date", "") or ""

        result.append({
            "key": item["key"],
            "itemType": ITEM_TYPES.get(item["itemTypeID"], "unknown"),
            "title": title,
            "creators": author_str,
            "year": date_str[:4] if date_str else None,
            "abstract": abstract,
            "DOI": data.get("DOI", ""),
            "publicationTitle": data.get("publicationTitle", ""),
            "url": data.get("url", ""),
            "date": date_str,
            "tags": item.get("tags", []),
        })

    return result


# ── API mode (pyzotero) ─────────────────────────────────────────────

def fetch_api(api_key, library_id, library_type, collection=None, limit=50):
    try:
        from pyzotero import zotero
    except ImportError:
        print("Missing pyzotero. Install: pip install pyzotero", file=sys.stderr)
        sys.exit(1)

    zot = zotero.Zotero(library_id, library_type, api_key)
    zot.add_parameters(itemType="-attachment|-note", sort="dateAdded",
                       direction="desc", limit=limit)

    if collection:
        items = zot.collection_items(collection)
    else:
        items = zot.top()

    result = []
    for item in items:
        data = item.get("data", {})
        if data.get("itemType") in ("attachment", "note"):
            continue

        creators = data.get("creators", [])
        author_str = "; ".join(
            f"{c.get('lastName', '')}, {c.get('firstName', '')}" if c.get("lastName") else c.get("name", "")
            for c in creators if c.get("creatorType") == "author"
        )
        if not author_str:
            author_str = "; ".join(c.get("name", "") for c in creators)

        result.append({
            "key": data.get("key", ""),
            "itemType": data.get("itemType", ""),
            "title": clean_text(data.get("title", "")),
            "creators": author_str[:200],
            "year": (data.get("date", "") or "")[:4],
            "abstract": clean_text(data.get("abstractNote", "")),
            "DOI": data.get("DOI", ""),
            "publicationTitle": data.get("publicationTitle", ""),
            "url": data.get("url", ""),
            "date": data.get("date", ""),
            "tags": [t.get("tag", "") for t in data.get("tags", [])],
        })

    return result


# ── Format converters ────────────────────────────────────────────────

def to_evidence_format(items, source="zotero"):
    papers = []
    for item in items:
        paper = {
            "id": item["key"],
            "title": item["title"],
            "authors": item["creators"][:200],
            "year": item["year"],
            "abstract": item["abstract"],
            "pdf_url": item.get("url", ""),
            "source": source,
            "why_relevant": "",
            "full_text_available": False,
            "extracted_claims": "",
        }
        extra = {}
        for field in ("DOI", "publicationTitle"):
            val = item.get(field)
            if val:
                extra[field] = val
        tags = item.get("tags", [])
        if tags:
            extra["tags"] = tags
        if extra:
            paper["zotero_meta"] = extra
        papers.append(paper)
    return {"papers": papers}


def to_scout_format(items, source="zotero"):
    entries = []
    for item in items:
        entries.append({
            "id": item["key"],
            "title": item["title"],
            "authors": item["creators"][:200],
            "year": item["year"],
            "abstract": item["abstract"],
            "pdf_url": item.get("url", ""),
            "source": source,
            "why_relevant": "",
        })
    return entries


# ── CLI ──────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Fetch Zotero items for citation-relevance-auditor")
    parser.add_argument("--api-key", help="Zotero API key (required for API mode)")
    parser.add_argument("--library-id", help="Zotero library ID (numeric, required for API mode)")
    parser.add_argument("--library-type", choices=["user", "group"], default="user")

    parser.add_argument("--local", action="store_true",
                        help="Read from local zotero.sqlite instead of API")
    parser.add_argument("--db", default=LOCAL_DB,
                        help=f"Path to zotero.sqlite (default: {LOCAL_DB})")

    parser.add_argument("--collection", help="Collection key to fetch from")
    parser.add_argument("--limit", type=int, default=50, help="Max items (default 50)")
    parser.add_argument("--output", help="Write to file instead of stdout")
    parser.add_argument("--format", choices=["evidence", "scout"], default="evidence",
                        help="Output format (default: evidence)")

    args = parser.parse_args()

    if args.local:
        raw = fetch_local(args.db, args.collection, args.limit)
        source = "zotero_local"
    else:
        if not args.api_key or not args.library_id:
            parser.error("--local or --api-key + --library-id required")
        raw = fetch_api(args.api_key, args.library_id, args.library_type,
                        args.collection, args.limit)
        source = "zotero"

    if args.format == "evidence":
        data = to_evidence_format(raw, source)
        output = yaml.dump(data, default_flow_style=False, sort_keys=False,
                           allow_unicode=True)
        output = f"```yaml\n{output}```\n"
    else:
        entries = to_scout_format(raw, source)
        output = yaml.dump(entries, default_flow_style=False, sort_keys=False,
                           allow_unicode=True)
        output = f"```yaml\n{output}```\n"

    if args.output:
        with open(args.output, "w") as f:
            f.write(output)
        print(f"Wrote {len(raw)} items to {args.output}", file=sys.stderr)
    else:
        print(output)


if __name__ == "__main__":
    main()
