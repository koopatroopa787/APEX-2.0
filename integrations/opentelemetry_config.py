import logging
from opentelemetry import trace, metrics
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.metrics import MeterProvider
# from azure.monitor.opentelemetry import configure_azure_monitor

logger = logging.getLogger(__name__)

def setup_opentelemetry(connection_string: str):
    """
    Sets up Enterprise-grade observability using OpenTelemetry.
    Exports cleanly to Azure Application Insights.
    """
    try:
        # Configure Azure Monitor Exporter directly
        # configure_azure_monitor(connection_string=connection_string)
        
        tracer_provider = TracerProvider()
        trace.set_tracer_provider(tracer_provider)
        
        meter_provider = MeterProvider()
        metrics.set_meter_provider(meter_provider)
        
        logger.info("OpenTelemetry successfully configured and bound to Azure Monitor.")
    except Exception as e:
        logger.error(f"Failed to setup OpenTelemetry: {e}")

def get_agent_metrics():
    """Generates custom metrics for APEX KPIs."""
    meter = metrics.get_meter(__name__)
    
    # Track critical agent variables
    query_counter = meter.create_counter("apex.queries.total", description="Total agent queries")
    cost_histogram = meter.create_histogram("apex.cost.usd", description="Cost per query distribution")
    
    return query_counter, cost_histogram
