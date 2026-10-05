Implement `profile(t)`: visit the whole hierarchy, read every node's label exactly once with `label(node)`, and return the number of label reads your traversal actually made. Use `branches` to descend. Count the reads as they happen; the checks replace `label` with a counting version and compare its count with yours on sizes and shapes the demo does not use.

The demo measures three sizes and draws your numbers as bars. Drawing happens after the measurement, so it is not part of the count. Before running, predict the ratio of reads to nodes.
