# Design and Complexity

Answer in approximately one page.

## Traversal
- My traversal is done recursively. The helper function `_walk_node` accepts a single node from the JSON tree. If the node is a dictionary and contains an `"items"` key, the function iterates over this list, and yields every item as an `Item`. In case of the dictionary lacking `"items"`, the function will do a recursive walk over the values of the dictionary. When the node is a list, the function does a recursive walk over its elements.
This traversal maintains JSON order since Python dictionaries retain the insertion order, and lists can be traversed in left-to-right order. As `_walk_node` iterates over `node.values()` and elements of the list in their current order, items are generated in the same region, dungeon, room, chest, and item order as in the JSON file.
My traversal is lazy since I used `yield` and `yield from`, rather than creating the list of `Items` upfront. Every `Item` is constructed and yielded whenever the caller requests the next value from the iterator.
- The time complexity of my solution is O(n), where n is the number of nodes and item records within the JSON structure, as every dictionary, list, and item is being traversed exactly once. The auxiliary space complexity is O(d), where d is the maximum depth of the JSON tree, as recursion utilizes the call stack. This traversal does not require O(k) additional space to traverse all k items.

## Binary Searc
- ## Binary Search

For `find_item_by_sku`, the code first materializes the lazy item traversal into a list. This costs O(n) time because every item must be visited, and O(n) extra space because every item is stored. The list is then sorted by SKU, which costs O(n log n) time.

After sorting, one binary search costs O(log n) time. The search checks the middle item’s SKU and compares it to the target SKU. If the middle SKU is too small, the search continues in the right half. If it is too large, the search continues in the left half. Each comparison removes about half of the remaining search area.

Binary search needs the list to be sorted because the algorithm depends on knowing which side smaller and larger values are on. Without sorting, comparing the middle SKU would not tell us where the target could be.

## Decorators

The decorators improve modularity because logging and predicate validation are kept separate from the main query logic. The query methods can focus on walking, filtering, mapping, or reducing items. Decorators add extra behavior around those methods.

`@logged_query` keeps logging separate from traversal logic. It wraps a query method, counts each item as it is yielded, and prints the log message only after the iterator is fully consumed. Calling the method alone does not print anything because the query is still lazy.

`@validate_predicate` separates the validation of the predicate from "filter_items." It validates that the predicate is callable, and then validates each predicate call within the loop. If the predicate does not return a boolean value or raises an exception, the wrapper raises "QueryValidationError," with the original exception as its cause.