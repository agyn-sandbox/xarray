TESTS

Purpose: document and validate local test execution for this repository.

Prerequisites
- Python >= 3.11
- pip
- Recommended dependencies for running the full suite:
  - pytest, pytest-cov, pytest-env, pytest-timeout, pytest-xdist, pytest-asyncio
  - hypothesis
  - pytest-mypy-plugins (for type annotation tests)
  - mypy (the project currently pins mypy==1.18.1 in its dev group)
  - cftime (CF-time/calendar support)
  - scipy (interpolation; netCDF3 I/O backend; some features/tests)

Setup
- Install the package in editable mode:
  - pip install -e .
- Install test dependencies (examples):
  - pip install pytest pytest-cov pytest-env pytest-timeout pytest-xdist pytest-asyncio hypothesis
  - pip install pytest-mypy-plugins mypy==1.18.1
  - For calendar and interpolation support used by tests:
    - pip install cftime scipy
    - or install optional extras: pip install -e ".[io]"  (includes cftime and scipy)
    - conda alternative: conda install -c conda-forge cftime scipy

Run tests
- Run the test suite in parallel:
  - python -m pytest -nauto
- Skip selected markers (examples):
  - Skip network and flaky tests: python -m pytest -nauto -m "not network and not flaky"
  - By default, tests marked with @network are skipped unless --run-network-tests is provided.
  - Tests marked flaky are skipped unless --run-flaky is provided.
- Coverage:
  - python -m pytest -nauto --cov=xarray --cov-report=xml

Type annotation tests
- Type tests are driven by pytest-mypy-plugins with test cases in YAML files (see xarray/tests/*_typing.yml).
- Ensure pytest-mypy-plugins and mypy are installed (see Setup above).
- To run only type tests:
  - python -m pytest -m mypy --run-mypy
- Notes:
  - Some mypy notes without line numbers are known limitations and are skipped in certain YAML cases.

Troubleshooting
- Missing plugins or tools (e.g., pytest-mypy-plugins, mypy): install the dependencies listed above.
- Long runtimes or memory issues: run with -nauto to let pytest-xdist choose concurrency, or limit to a subset (e.g., tests/xarray/core).
- Network-dependent tests: run with --run-network-tests when internet access is available; otherwise skip with -m "not network".
- Flaky tests: enable explicitly with --run-flaky or skip with -m "not flaky".
- Slow hypothesis tests under properties/: enable with --run-slow-hypothesis or they are skipped by default.
 - cftime not installed: tests that require CF-time calendars will be skipped (e.g., xarray/xarray/tests/test_calendar_ops.py imports or skips cftime). Install cftime to run those tests.
 - SciPy not installed: features that rely on scipy (e.g., DataArray.interp, calendar interpolation in calendar_ops, and the scipy netCDF backend) will error. If you see errors like "cannot import name 'interp1d' from scipy.interpolate" or missing scipy when running calendar-related interpolation tests, install SciPy (pip install scipy or conda install -c conda-forge scipy).
 - calendar_ops note: convert_calendar works with cftime for non-standard calendars; interp_calendar uses xarray's interpolation which requires scipy. Ensure both cftime and scipy are installed to run the full calendar_ops test module.
