# HW3 notes

Answer each question in a few sentences. Be specific: name the function, the error or the command.

## What did you try?

I implemented the CSV parsing and report functions in small parts, then ran the pytest suite after each area. I also added parametrized tests to `test_my_walks.py` for bad date and step values.

## What broke, and how did you fix it?

The repository started with `NotImplementedError` bodies. I replaced them with code that validates rows, skips bad walks, totals dates in sorted order, and safely replaces report files only after successful writes.

## What would you do differently next time?

I would run the focused test files sooner and debug one failing function at a time instead of waiting until the whole suite was complete.
