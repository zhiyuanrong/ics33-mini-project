# Process Log

Include at least three concise entries from different development moments.
Repository history and this log are evidence of process, not proof of authorship.

## Entry 1 — Aug21

- Decision, bug, or uncertainty: I needed to represent inventory items and load the JSON inventory data through the required source abstraction.
- Evidence considered: The assignment required an `Item` frozen dataclass and a `JSONInventorySource` implementing the `InventorySource` ABC.
- Change made: I implemented the `Item` dataclass and loaded/cached the JSON root and version in `JSONInventorySource`.
- Test that verified the change: The public tests for item equality/frozen assignment and JSON source loading passed.


## Entry 2 — Aug22

- Decision, bug, or uncertainty: In find_item_by_sku, I assigned the result of .sort(): all_items = all_items.sort(key=lambda item: item.sku)
- Evidence considered: commit 89d2a6f and commit b067c5f
- Change made: I have fixed that by deleting the assignmnet all_items.sort(key=lambda item: item.sku)
- Test that verified the change:The binary search test catches bug 1 because it calls find_item_by_sku, which would crash when all_items became None after all_items = all_items.sort(...).
The error points to `len(all_items)` or `all_items[mid]`, showing that all_items is no longer a list. That helps me realize .sort() should be used without assignment.

## Entry 3 — Aug 23

- Decision, bug, or uncertainty: Binary search used:
while `lo < hi`:
This stops too early when lo and hi point to the same final item. That last item still needs to be checked, so the correct condition is:
`while lo <= hi:`
- Evidence considered:
Bug found in commit: b067c5f on Sat Aug 22, 2026 09:56:22,
Fixed in commit: e213bb9 on Sun Aug 23, 2026 11:06:46
- Change made:change it to `while lo <= hi:`
- Test that verified the change:
test_find_item_by_sku_finds_first_and_last_sorted_skus
It checks:
- first = engine.find_item_by_sku(items[0].sku)
- last = engine.find_item_by_sku(items[-1].sku)
