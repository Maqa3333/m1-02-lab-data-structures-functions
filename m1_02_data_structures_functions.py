def validate_required_keys(records):
    required_keys = {"ticket_id", "customer_id", "category", "resolution_minutes", "is_escalated"}
    invalid_indices = [i for i, rec in enumerate(records) if not required_keys.issubset(rec.keys())]
    return invalid_indices

def get_invalid_resolution_records(records):
    invalid_indices = []
    for i, rec in enumerate(records):
        val = rec.get("resolution_minutes")
        if not isinstance(val, (int, float)):
            invalid_indices.append(i)
    return invalid_indices



def clean_data(records):
    cleaned_list = []
    for rec in records:
        res_min = rec.get("resolution_minutes")
        if isinstance(res_min, (int, float)):
            new_rec = rec.copy()
            new_rec["category"] = new_rec["category"].strip().title()
            cleaned_list.append(new_rec)
            
    return cleaned_list


def get_avg_resolution_by_category(records):
    category_totals = {}
    category_counts = {}
    for rec in records:
        cat = rec["category"]
        res = rec["resolution_minutes"]
        category_totals[cat] = category_totals.get(cat, 0) + res
        category_counts[cat] = category_counts.get(cat, 0) + 1
    
    return {cat: category_totals[cat] / category_counts[cat] for cat in category_totals}


def get_escalation_metrics(records):
    overall_escalated = sum(1 for rec in records if rec["is_escalated"])
    total = len(records)
    return {
        "overall_rate": overall_escalated / total,
        "total_cleaned_count": total
    }

def generate_final_report(records):
    report = {
        "metrics": get_escalation_metrics(records),
        "avg_resolution_per_category": get_avg_resolution_by_category(records),
        "data_quality_note": "Dropped records with non-numeric resolution values."
    }
    return report
#final_report = sf.generate_final_report(cleaned_logs)







