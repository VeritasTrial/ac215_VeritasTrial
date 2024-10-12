"""
The clean subcommand.
"""

import json
import re

import jsonlines
import rich

from shared import CLEANED_JSONL_PATH, METADATA_PATH, RAW_JSONL_PATH, default_progress

_FIELDS = [
    # Identification module
    "id",  # str
    "short_title",  # str
    "long_title",  # str
    "organization",  # str
    # Status module
    "submit_date",  # str
    "submit_date_qc",  # str
    "submit_date_posted",  # str
    "results_date",  # str
    "results_date_qc",  # str
    "results_date_posted",  # str
    "last_update_date",  # str
    "last_update_date_posted",  # str
    "verify_date",  # str
    # Sponsor/Collaborators module
    "sponsor",  # str
    "collaborators",  # list of str
    # Description module
    "summary",  # str
    "details",  # str
    # Conditions module
    "conditions",  # list[str]
    # Design module
    "study_phases",  # str
    "study_type",  # str
    "enrollment_count",  # int
    "allocation",  # str
    "intervention_model",  # str
    "observation_model",  # str
    "primary_purpose",  # str
    "who_masked",  # str
    # Inverventions module
    "interventions",  # list of dict {type, name, description}
    # Outcomes module
    "primary_measure_outcomes",  # list of dict {measure, description, time_frame}
    "secondary_measure_outcomes",  # list of dict {measure, description, time_frame}
    "other_measure_outcomes",  # list of dict {measure, description, time_frame}
    # Eligibility module
    "min_age",  # int
    "max_age",  # int
    "eligible_sex",  # str
    "accepts_healthy",  # bool
    "inclusion_criteria",  # str
    "exclusion_criteria",  # str
    # Locations module
    "officials",  # list of str
    "locations",  # list of str
    # References module (https://pubmed.ncbi.nlm.nih.gov/${pmid}/)
    "references",  # list of dict {pmid, citation}
    # Large documents module
    "documents",  # list of dict {url, size(int)}
]


def format_date_struct(date_info):
    """Helper function to format data information."""
    if isinstance(date_info, dict):
        date = date_info.get("date")
        if date is not None and date_info.get("type") == "ESTIMATED":
            date += " (estimated)"
        return date
    return str(date_info)


def clean_outcomes(outcomes):
    """Helper function to clean a list of measure outcomes."""
    return [
        {
            "measure": item.get("measure"),
            "description": item.get("description"),
            "time_frame": item.get("timeFrame"),
        }
        for item in outcomes
    ]


def extract_age(age_info):
    """Helper function to extract age from a string."""
    age_match = re.match(r"^(\d+)\s+years$", age_info, re.IGNORECASE)
    return int(age_match.group(1)) if age_match is not None else None


def format_official(official):
    """Helper function to format information of an official."""
    official_name = official.get("name", "")
    official_role = official.get("role", "")
    official_affil = official.get("affiliation", "")
    return f"{official_name}, {official_role}, {official_affil}"


def format_location(location):
    """Helper function to format information of a location."""
    loc_facility = location.get("facility", "")
    loc_city = location.get("city", "")
    loc_state = location.get("state", "")
    loc_zip = location.get("zip", "")
    loc_country = location.get("country", "")
    return f"{loc_facility}, {loc_city}, {loc_state}, {loc_zip}, {loc_country}"


def get_inclusion_exclusion_criteria(criteria_text):
    """Helper function to extract inclusion and exclusion criteria."""
    if criteria_text is None:
        return "", ""

    inclusion_pat = r"Inclusion Criteria:(.*?)(Exclusion Criteria:|$)"
    exclusion_pat = r"Exclusion Criteria:(.*)"

    inclusion_match = re.search(inclusion_pat, criteria_text, re.DOTALL)
    exclusion_match = re.search(exclusion_pat, criteria_text, re.DOTALL)

    return inclusion_match.group(1).strip() if inclusion_match is not None else "", (
        exclusion_match.group(1).strip() if exclusion_match is not None else ""
    )


def get_document_url(id, doc_info):
    """Helper function to get the URL of a large document attachment."""
    filename = doc_info.get("filename")
    return (
        f"https://cdn.clinicaltrials.gov/large-docs/{id[-2:]}/{id}/{filename}"
        if filename is not None
        else None
    )


def clean_one_study(study):
    """Return the cleaned version of a raw study data entry."""
    cleaned_data = {}
    protocols = study.get("protocolSection", {})
    documents = study.get("documentSection", {})

    # Identification module
    id_module = protocols.get("identificationModule", {})
    cleaned_data["id"] = id_module.get("nctId")
    cleaned_data["short_title"] = id_module.get("briefTitle")
    cleaned_data["long_title"] = id_module.get("officialTitle")
    cleaned_data["organization"] = id_module.get("organization", {}).get("fullName")

    # Status module
    status_module = protocols.get("statusModule", {})
    cleaned_data["submit_date"] = status_module.get("studyFirstSubmitDate")
    cleaned_data["submit_date_qc"] = status_module.get("studyFirstSubmitQcDate")
    cleaned_data["submit_date_posted"] = format_date_struct(
        status_module.get("studyFirstPostDateStruct", {})
    )
    cleaned_data["results_date"] = status_module.get("resultsFirstSubmitDate")
    cleaned_data["results_date_qc"] = status_module.get("resultsFirstSubmitQcDate")
    cleaned_data["results_date_posted"] = format_date_struct(
        status_module.get("resultsFirstPostDateStruct", {})
    )
    cleaned_data["last_update_date"] = status_module.get("lastUpdateSubmitDate")
    cleaned_data["last_update_date_posted"] = format_date_struct(
        status_module.get("lastUpdatePostDateStruct", {})
    )
    cleaned_data["verify_date"] = status_module.get("statusVerifiedDate")

    # Sponsor/Collaborators module
    collab_module = protocols.get("sponsorCollaboratorsModule", {})
    cleaned_data["sponsor"] = collab_module.get("leadSponsor", {}).get("name")
    cleaned_data["collaborators"] = [
        name
        for item in collab_module.get("collaborators", [])
        if (name := item.get("name")) is not None
    ]

    # Description module
    descr_module = protocols.get("descriptionModule", {})
    cleaned_data["summary"] = descr_module.get("briefSummary", None)
    cleaned_data["details"] = descr_module.get("detailedDescription", None)

    # Conditions module
    cond_module = protocols.get("conditionsModule", {})
    cleaned_data["conditions"] = cond_module.get("conditions", [])

    # Design module
    design_module = protocols.get("designModule", {})
    design_info = design_module.get("designInfo", {})
    cleaned_data["study_phases"] = ", ".join(design_module.get("phases", [])) or None
    cleaned_data["study_type"] = design_module.get("studyType")
    cleaned_data["enrollment_count"] = design_module.get("enrollmentInfo", {}).get(
        "count", 0
    )
    cleaned_data["allocation"] = design_info.get("allocation")
    cleaned_data["intervention_model"] = design_info.get("interventionModel")
    cleaned_data["observation_model"] = design_info.get("observationalModel")
    cleaned_data["primary_purpose"] = design_info.get("primaryPurpose")
    cleaned_data["who_masked"] = (
        ", ".join(design_info.get("maskingInfo", {}).get("whoMasked", [])) or None
    )

    # Inverventions module
    interv_module = protocols.get("armsInterventionsModule", {})
    cleaned_data["Interventions"] = [
        {
            "type": item.get("type"),
            "name": item.get("name"),
            "description": item.get("description"),
        }
        for item in interv_module.get("interventions", [])
    ]

    # Outcomes module
    outcomes_module = protocols.get("outcomesModule", {})
    cleaned_data["primary_measure_outcomes"] = clean_outcomes(
        outcomes_module.get("primaryOutcomes", [])
    )
    cleaned_data["secondary_measure_outcomes"] = clean_outcomes(
        outcomes_module.get("secondaryOutcomes", [])
    )
    cleaned_data["other_measure_outcomes"] = clean_outcomes(
        outcomes_module.get("otherOutcomes", [])
    )

    # Eligibility module
    elig_module = protocols.get("eligibilityModule", {})
    cleaned_data["min_age"] = extract_age(elig_module.get("minimumAge", ""))
    cleaned_data["max_age"] = extract_age(elig_module.get("maximumAge", ""))
    cleaned_data["eligible_sex"] = elig_module.get("sex")
    cleaned_data["accepts_healthy"] = elig_module.get("healthyVolunteers", False)
    cleaned_data["inclusion_criteria"], cleaned_data["exclusion_criteria"] = (
        get_inclusion_exclusion_criteria(elig_module.get("eligibilityCriteria"))
    )

    # Locations module
    loc_module = protocols.get("contactsLocationsModule", {})
    cleaned_data["officials"] = [
        format_official(item) for item in loc_module.get("overallOfficials", [])
    ]
    cleaned_data["locations"] = [
        format_location(item) for item in loc_module.get("locations", [])
    ]

    # References module
    ref_module = protocols.get("referencesModule", {})
    cleaned_data["references"] = [
        {"pmid": item.get("pmid"), "citation": item.get("citation")}
        for item in ref_module.get("references", [])
    ]

    # Large documents module
    doc_module = documents.get("largeDocumentModule", {})
    cleaned_data["documents"] = [
        {"url": get_document_url(cleaned_data["id"], item), "size": item.get("size")}
        for item in doc_module.get("largeDocs", [])
    ]

    return cleaned_data


def main():
    if not RAW_JSONL_PATH.exists():
        rich.print(
            f"[bold red]ERROR[/] Raw data missing at: {RAW_JSONL_PATH}; run the fetch "
            "subcommand first"
        )
        return

    # Load metadata if it exists
    n_cleaned_studies = 0
    n_studies = None
    if METADATA_PATH.exists():
        with METADATA_PATH.open("r", encoding="utf-8") as f:
            metadata = json.load(f)
        n_studies = metadata["n_studies"]

    with default_progress() as progress:
        task = progress.add_task("Cleaning data...", total=n_studies)

        with jsonlines.open(CLEANED_JSONL_PATH, "w") as out_file:
            with jsonlines.open(RAW_JSONL_PATH, "r") as in_file:
                # Iterate over raw data, clean each entry, and write a CSV row
                for data in in_file:
                    out_file.write(clean_one_study(data))
                    progress.update(task, advance=1)
                    n_cleaned_studies += 1

    rich.print(
        f"[bold green]->[/] {n_cleaned_studies} cleaned studies saved to "
        f"{CLEANED_JSONL_PATH}"
    )
