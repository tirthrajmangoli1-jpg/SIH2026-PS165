import re

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/backend/app/clustering.py", "r") as f:
    content = f.read()

# Add incident tracking to rig_counts
content = re.sub(
    r'rig_counts\[fac\]\["total"\] \+\= 1',
    r'rig_counts[fac]["total"] += 1\n        if "incident_ids" not in rig_counts[fac]:\n            rig_counts[fac]["incident_ids"] = []\n        rig_counts[fac]["incident_ids"].append(r.get("id"))',
    content
)

content = re.sub(
    r'"recommended_hse_action": rec_action\n        }\)',
    r'"recommended_hse_action": rec_action,\n            "sample_incident_ids": data.get("incident_ids", [])[:3]\n        })',
    content
)

# Add incident tracking to activity_counts
content = re.sub(
    r'activity_counts\[act\]\["total"\] \+\= 1',
    r'activity_counts[act]["total"] += 1\n        if "incident_ids" not in activity_counts[act]:\n            activity_counts[act]["incident_ids"] = []\n        activity_counts[act]["incident_ids"].append(r.get("id"))',
    content
)

content = re.sub(
    r'"recommended_hse_action": rec_action_act\n        }\)',
    r'"recommended_hse_action": rec_action_act,\n            "sample_incident_ids": data.get("incident_ids", [])[:3]\n        })',
    content
)

with open("/Users/tirthsmac/.gemini/antigravity/scratch/oil-sif-sentinel/backend/app/clustering.py", "w") as f:
    f.write(content)
