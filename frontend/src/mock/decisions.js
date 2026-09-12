export const mockDecisions = [
  {
    id: "DEC-8821",
    incident_id: "OISD-2025-019",
    site: "ONGC Hazira Rig",
    date: "2025-10-12 14:30",
    officer_name: "Rahul Verma (Safety Inspector)",
    language: "English",
    action: "Escalated to High SIF",
    comments: "Dropped object 500kg drill collar had fatal potential if it struck the roustabout. NLP successfully flagged this.",
    status: "Reviewed"
  },
  {
    id: "DEC-8820",
    incident_id: "OISD-2025-018",
    site: "Baghjan Well-5",
    date: "2025-10-10 09:15",
    officer_name: "Amitabh Saikia (Field Officer)",
    language: "Assamese (Romanized)",
    action: "Downgraded to Medium SIF",
    comments: "The gas leak was minor and contained immediately. Training model to not flag small pressure release as blowout.",
    status: "Calibrated"
  },
  {
    id: "DEC-8819",
    incident_id: "OISD-2025-017",
    site: "Mangalore Refinery",
    date: "2025-10-09 11:45",
    officer_name: "Prakash Shetty (HSE Lead)",
    language: "Kannada (Native)",
    action: "Confirmed High SIF",
    comments: "Crane wire cut could have caused multiple fatalities. Immediate shutdown recommended.",
    status: "Action Taken"
  },
  {
    id: "DEC-8818",
    incident_id: "OISD-2025-016",
    site: "Administrative Building, Duliajan",
    date: "2025-10-08 16:20",
    officer_name: "Sanjay Kumar",
    language: "English",
    action: "Confirmed Low SIF",
    comments: "Routine paper cut in office. NLP model correctly assigned Low SIF. No further action.",
    status: "Archived"
  },
  {
    id: "DEC-8817",
    incident_id: "OISD-2025-015",
    site: "HPCL Vizag",
    date: "2025-10-05 10:10",
    officer_name: "T. Rao (Electrical Safety)",
    language: "Telugu / English",
    action: "Escalated to High SIF",
    comments: "Transformer blast is a critical energy release event. Need to retrain model to capture electrical faults earlier.",
    status: "Calibrated"
  },
  {
    id: "DEC-8816",
    incident_id: "OISD-2025-014",
    site: "Bombay High",
    date: "2025-10-01 13:00",
    officer_name: "Vikram Singh (Offshore Lead)",
    language: "Hindi (Native)",
    action: "Confirmed High SIF",
    comments: "Pipe falling on drilling floor is a classic dropped object hazard. Near miss recorded.",
    status: "Reviewed"
  }
];
