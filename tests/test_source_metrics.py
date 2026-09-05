from evaluation.metrics.source_metrics import unique_sources


def test_unique_sources():
    sources = [
        "database_connection_pool.md",
        "database_connection_pool.md",
        "high_api_latency.md",
    ]

    result = unique_sources(sources)

    assert result == [
        "database_connection_pool.md",
        "high_api_latency.md",
    ]


def test_unique_sources_preserves_order():
    sources = [
        "redis_failure.md",
        "service_crash.md",
        "redis_failure.md",
        "high_api_latency.md",
    ]

    result = unique_sources(sources)

    assert result == [
        "redis_failure.md",
        "service_crash.md",
        "high_api_latency.md",
    ]


def test_unique_sources_without_duplicates():
    sources = [
        "database_connection_pool.md",
        "redis_failure.md",
    ]

    result = unique_sources(sources)

    assert result == sources


def test_unique_sources_empty():
    assert unique_sources([]) == []
