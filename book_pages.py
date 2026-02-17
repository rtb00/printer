#! python3

import sys


def compute_page_order(n, delete_pages_str="", verbose=False):
    """Berechnet die Seitenreihenfolge für Klammerheftung (Saddle Stitch)."""
    excluded = [s.strip() for s in delete_pages_str.split(",") if s.strip()]
    pages = [i for i in range(1, n + 1) if str(i) not in excluded]

    # Auf nächstes Vielfaches von 4 auffüllen (ein gefaltetes Blatt = 4 Seiten)
    remainder = len(pages) % 4
    if remainder != 0:
        pages = pages + [None] * (4 - remainder)

    if verbose:
        print(pages)

    result_pairs = []
    for index in range(len(pages) // 2):
        if index % 2 != 0:
            result_pairs.append((pages[index], pages[-index - 1]))
        else:
            result_pairs.append((pages[-index - 1], pages[index]))

    return [i for pair in result_pairs for i in pair]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: {} <number_pages> [pages_to_delete] [--verbose]".format(sys.argv[0]))
        sys.exit(1)

    verbose = "--verbose" in sys.argv
    args = [a for a in sys.argv[1:] if a != "--verbose"]

    try:
        n = int(args[0])
    except ValueError:
        print("Ungültige Eingabe")
        exit(1)

    delete_pages_str = args[1] if len(args) > 1 else ""
    result = compute_page_order(n, delete_pages_str, verbose=verbose)
    print("_".join(str(i) if i is not None else "Empty" for i in result))
