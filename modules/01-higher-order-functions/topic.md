# Higher-order functions conversion plan

Seven beats: total contributions under different rules; duplicated loops; prefix trace; processed-prefix invariant; pass behavior as a value and return configured behavior; count actual callback invocations; transfer to a calibration service.

Lesson instance: donation units [2, 5, 3], rule 3*x+1, contributions [7, 16, 10], total 33. Lesson factory is a minimum-charge rule. Lab Build instance [4, -1, 3], square contributions; Trace uses multiply-by-three then subtract-four; Implement uses repeated application; Measure counts calls for fresh sizes; Mastery returns a callable applying a fixed sequence of affine adjustments efficiently.

Five exercises: total_terms, chain, repeat, profile, calibrator. Counted operation: supplied callback calls for Measure; inspection of supplied adjustment records for Mastery. Mastery tell: settings fixed at setup, many later inputs. No technique named in its prompt. Retrieval uses prerequisite Python, since this is module 1.

Contracts: ordered callback application, exactly once per element; chain(f,g) invokes g then f; factories return callable values without evaluating their callbacks at construction; repeat with nonnegative int count, zero returns its input unchanged, repeated calls start afresh; calibrator snapshots ordered integer settings, creates independent services, and never rereads settings when handling readings. Integer arithmetic is counted as unit cost only for the pedagogical model; big integers and drawing have extra costs.

Do not repeat the old Newton convergence claims. Root-finding is out of this introductory module's scope. Closure diagrams are semantic models, not a claim that CPython preserves an entire returned call frame. Archive deck sources; original reading remains optional and unchanged.

## Primary-source checks
Python 3.14 documentation, checked 2026-10-04:
- https://docs.python.org/3/howto/sorting.html#key-functions — sorted's key accepts a callable and is invoked once per input record.
- https://docs.python.org/3/reference/datamodel.html#user-defined-functions — function.__closure__ contains cells for free-variable bindings. The lesson distinguishes this implementation detail from an environment-diagram model.

## Check design and limitations
Frame checks compare the recorded figure data with the actual processed prefix and intermediate callback values. Bulk checks disable drawing and use varied deterministic inputs. Trace checks inspect callback order and prohibit calls during construction. Repeat checks cover zero, object identity, strings, independent invocations, and 3,000 applications. Measure checks replace the process with a wasteful one, rejecting literal reported counts. Mastery meters additions/multiplications through int subclasses and stops over-budget code using BaseException; direct int/float loads are forbidden in learner source. This is educational feedback, not secure grading: source rewrites or other conversions can evade browser-visible meters.

## Publication status
Local draft only. Module 01 and module 06 are converted; the other seven modules remain legacy. Production lab/deck assets are not changed by authoring or checks. Reuse the pending deck-hiding publication plan; do not upload these new lab files as legacy lab_spec.json.
