import pytest
import numpy as np
from agents.workload_vision.metric_analyzer import MetricAnalyzer

@pytest.fixture
def analyzer():
    return MetricAnalyzer()

def test_extract_graph_regions(analyzer):
    # Mock a 100x100 grayscale image
    mock_image = np.ones((100, 100))
    result = analyzer.extract_graph_regions(mock_image)
    
    # Current simplistic implementation extracts bottom 70%
    assert result.shape == (70, 100)
    
def test_parse_text_metrics(analyzer):
    result = analyzer.parse_text_metrics("mock_path.png")
    assert "detected_cpu" in result
    assert "detected_latency" in result
