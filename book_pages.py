#! python3

import sys

if len(sys.argv) < 2:
    print("Usage: {} <number_pages>".format(sys.argv[0]))
    sys.exit(1)

number_pages = sys.argv[1]
delete_pages = sys.argv[2] if len(sys.argv) > 2 else ""

try:
    n = int(number_pages)
except ValueError:
    print("Ungültige Eingabe")
    exit(1)

pages = [i for i in range(1, n+1) if str(i) not in delete_pages.replace(' ','').split(",")]
pages_len = len(pages)

pages = pages + [None] * (-1*(pages_len % -4))

print(pages)

result_pairs = []
for index in range((pages_len // 4 +1)*2):
    if index % 2 != 0:
        result_pairs.append((pages[index], pages[-index-1]))
    else:
        result_pairs.append((pages[-index-1], pages[index]))

# ## jedes 2. paar wird umgedreht
# for i in range(0, len(result_pairs), 2):
#     result_pairs[i] = result_pairs[i][::-1]
result = "_".join([str(i) if i is not None else 'Empty' for pair in result_pairs for i in pair])


print(result)
