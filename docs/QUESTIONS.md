# Target Questions

## Questions

1. Why is my query performing a Sequential Scan instead of using the existing B-tree index on a 25-million row table in PostgreSQL 15, and how does `random_page_cost` influence this choice?
2. How do I calculate and configure `work_mem` in PostgreSQL 16 to prevent external merge Sort operations from spilling to temporary files on disk?
3. What causes a "Bitmap Heap Scan with lossy blocks" in an EXPLAIN (ANALYZE, BUFFERS) plan in PostgreSQL 14, and which setting prevents lossy bitmap conversion?
4. How can `autovacuum_vacuum_scale_factor` and `autovacuum_vacuum_cost_limit` be tuned in PostgreSQL 13 to aggressively clean dead tuples on tables with 10,000 updates/sec?
5. Under what data distribution and clustering conditions should a BRIN index be chosen over a standard B-tree index for large append-only audit tables in PostgreSQL 15?
6. How do I configure Oracle 19c Automatic Workload Repository (AWR) and Automatic Database Diagnostic Monitor (ADDM) to tune buffer cache hit ratios for RAC clusters? (Unanswerable: QueryDoctor is specialized for PostgreSQL documentation versions 13-17, not Oracle databases).
7. Why does JIT compilation add 250ms of overhead to a fast OLTP query plan in PostgreSQL 14, and how should `jit_above_cost` or `jit` be adjusted?
8. How does `max_parallel_workers_per_gather` coordinate parallel workers during a Gather Merge scan in PostgreSQL 16, and what prevents worker spawn?
9. How does run-time partition pruning behave with parameterized prepared statements on declaratively partitioned tables in PostgreSQL 17?
10. What formula should be used to configure `max_wal_size` and `checkpoint_completion_target` in PostgreSQL 15 to smooth out I/O spikes during high write throughput?
