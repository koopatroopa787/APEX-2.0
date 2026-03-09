from typing import Dict, Any
from agents.production_readiness.validators import ReadinessValidator
from agents.production_readiness.survival_models import AgentSurvivalModel

class RiskScorer:
    """
    Aggregates the 10 heuristics + Actuarial 30-day forecast.
    Produces Red/Yellow/Green confidence levels.
    """
    def __init__(self):
        self.validators = ReadinessValidator()
        self.survival = AgentSurvivalModel()
        
    def calculate_score(self, telemetry: Dict[str, Any]) -> Dict[str, Any]:
        
        # Weighted Aggregation
        v1 = self.validators.validate_database_load(telemetry) * 0.30
        v2 = self.validators.validate_cost_budget(telemetry) * 0.20
        v3 = self.validators.validate_latency_sla(telemetry) * 0.15
        v4 = self.validators.validate_error_rate(telemetry) * 0.15
        v5 = self.validators.validate_security_compliance(telemetry) * 0.10
        
        # Remaining 5 validators aggregate to 10%
        v_rest = (
            self.validators.validate_network_bandwidth(telemetry) +
            self.validators.validate_query_throughput(telemetry) +
            self.validators.validate_monitoring_coverage(telemetry) +
            self.validators.validate_disaster_recovery(telemetry) +
            self.validators.validate_load_testing(telemetry)
        ) / 5.0 * 0.10
        
        base_score = v1 + v2 + v3 + v4 + v5 + v_rest
        
        # Actuarial prediction logic
        prediction_30 = self.survival.predict_survival_probability(telemetry, days=30)
        prediction_90 = self.survival.predict_survival_probability(telemetry, days=90)
        
        # Final blended score
        final_score = base_score * 0.7 + (prediction_30 * 100) * 0.3
        
        status = "GREEN" if final_score >= 85 else ("YELLOW" if final_score >= 65 else "RED")
        
        return {
            "score_0_100": round(final_score, 2),
            "status": status,
            "survival_30d_prob": round(prediction_30 * 100, 2),
            "survival_90d_prob": round(prediction_90 * 100, 2)
        }
