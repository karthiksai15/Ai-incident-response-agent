from enum import Enum


class InvestigationGoal(str, Enum):
    UNDERSTAND_CONTEXT = "understand_context"
    CHECK_SERVICE_HEALTH = "check_service_health"
    COLLECT_ERROR_EVIDENCE = "collect_error_evidence"
    SEARCH_LOG_EVIDENCE = "search_log_evidence"
    RETRIEVE_KNOWLEDGE = "retrieve_knowledge"
    DETERMINE_ROOT_CAUSE = "determine_root_cause"
    PRODUCE_RECOMMENDATION = "produce_recommendation"
