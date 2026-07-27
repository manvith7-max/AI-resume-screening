import json

def prepare_dashboard_charts_data(status_counts, total_evaluations):
    """
    Prepares JSON-serializable chart data for Plotly.js on the dashboard.
    """
    categories = ["Highly Recommended", "Recommended", "Not Recommended"]
    colors = ["#10b981", "#f59e0b", "#ef4444"]
    values = [status_counts.get(cat, 0) for cat in categories]
    
    donut_chart_data = {
        "labels": categories,
        "values": values,
        "marker_colors": colors
    }
    return donut_chart_data

def prepare_candidate_match_chart_data(cosine_sim, skill_score, ml_prob, final_score):
    """
    Prepares JSON-serializable component comparison chart data for candidate detail view.
    """
    labels = ["Cosine Sim (40%)", "Skill Match (40%)", "ML Category (20%)"]
    values = [
        round(cosine_sim * 100, 1),
        round(skill_score, 1),
        round(ml_prob * 100, 1)
    ]
    return {
        "labels": labels,
        "values": values,
        "final_score": round(final_score, 1)
    }
