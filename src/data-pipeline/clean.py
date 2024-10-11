import csv
import json
import re

import jsonlines
import rich

from shared import CLEANED_CSV_PATH, METADATA_PATH, RAW_JSONL_PATH, default_progress

CSV_HEADERS = [
    "Study ID",
    "Brief Title",
    "Official Title",
    "Organization Name",
    "Organization Type",
    "First Submitted",
    "First Submitted (QC Met)",
    "First Posted",
    "Results First Submitted",
    "Results First Submitted (QC Met)",
    "Results First Posted",
    "Last Update Submitted",
    "Last Update Posted",
    "Last Verified",
    "Sponsor Name",
    "Sponsor Type",
    # TODO: Collaborators
    "Brief Summary",
    "Detailed Description",
    "Conditions",
    "Study Phase",
    "Study Type",
    "Enrollment Count",
    "Allocation",
    "Intervention Model",
    "Observational Model",
    "Primary Purpose",
    "Masking",
    "Who Masked",
    "Time Perspective",
    "Interventions",
    "Primary Measure Outcomes",
    "Secondary Measure Outcomes",
    "Minimum Age",
    "Sexes Eligible for Study",
    "Accepts Healthy Volunteers",
    "Ages Eligible for Study",
    "Sampling Method",
    "Inclusion Criteria",
    "Exclusion Criteria",
    "Overall Officials",
    "Locations",
    # TODO: References
    # TODO: Documents
]


def format_date_struct(date_info):
    """Helper function to format data information."""
    if isinstance(date_info, dict):
        date = date_info.get("date", "")
        if date_info.get("type") == "ESTIMATED":
            date += " (estimated)"
        return date
    return str(date_info)


def format_intervention(intervention):
    """Helper function to format an intervention."""
    interv_type = intervention.get("type", "")
    interv_name = intervention.get("name", "")
    interv_desc = intervention.get("description", "")
    return f"{interv_type} | {interv_name} | {interv_desc}"


def format_outcome(outcome, idx):
    """Helper function to format an outcome at a particular index."""
    outcome_measure = outcome.get("measure", "")
    outcome_desc = outcome.get("description", "")
    outcome_time_frame = outcome.get("timeFrame", "")
    return f"[Measure {idx}] {outcome_measure} | {outcome_desc} | {outcome_time_frame}"


def format_official(official):
    """Helper function to format information of an official."""
    official_name = official.get("name", "")
    official_role = official.get("role", "")
    official_affil = official.get("affiliation", "")
    return f"{official_name} | {official_role} | {official_affil}"


def format_location(location):
    """Helper function to format information of a location."""
    loc_facility = location.get("facility", "")
    loc_city = location.get("city", "")
    loc_zip = location.get("zip", "")
    loc_country = location.get("country", "")
    return f"{loc_facility}, {loc_city}, {loc_zip}, {loc_country}"


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


def clean_one_study(study):
    """Return the cleaned version of a raw study data entry."""
    cleaned_data = {}
    protocols = study.get("protocolSection", {})
    results = study.get("resultsSection", {})

    # Identification module
    id_module = protocols.get("identificationModule", {})
    cleaned_data["Study ID"] = id_module.get("nctId", "")
    cleaned_data["Brief Title"] = id_module.get("briefTitle", "")
    cleaned_data["Official Title"] = id_module.get("officialTitle", "")
    cleaned_data["Organization Name"] = id_module.get("organization", {}).get(
        "fullName", ""
    )
    cleaned_data["Organization Type"] = id_module.get("organization", {}).get(
        "class", ""
    )

    # Status module
    status_module = protocols.get("statusModule", {})
    cleaned_data["First Submitted"] = status_module.get("studyFirstSubmitDate", "")
    cleaned_data["First Submitted (QC Met)"] = status_module.get(
        "studyFirstSubmitQcDate", ""
    )
    cleaned_data["First Posted"] = format_date_struct(
        status_module.get("studyFirstPostDateStruct", {})
    )
    cleaned_data["Results First Submitted"] = status_module.get(
        "resultsFirstSubmitDate", ""
    )
    cleaned_data["Results First Submitted (QC Met)"] = status_module.get(
        "resultsFirstSubmitQcDate", ""
    )
    cleaned_data["Results First Posted"] = format_date_struct(
        status_module.get("resultsFirstPostDateStruct", {})
    )
    cleaned_data["Last Update Submitted"] = status_module.get(
        "lastUpdateSubmitDate", ""
    )
    cleaned_data["Last Update Posted"] = format_date_struct(
        status_module.get("lastUpdatePostDateStruct", {})
    )
    cleaned_data["Last Verified"] = status_module.get("statusVerifiedDate", "")

    # Sponsor/Collaborators module
    collab_module = protocols.get("sponsorCollaboratorsModule", {})
    cleaned_data["Sponsor Name"] = collab_module.get("leadSponsor", {}).get("name", "")
    cleaned_data["Sponsor Type"] = collab_module.get("leadSponsor", {}).get("class", "")
    # TODO: Collaborators

    # Description module
    descr_module = protocols.get("descriptionModule", {})
    cleaned_data["Brief Summary"] = descr_module.get("briefSummary", "")
    cleaned_data["Detailed Description"] = descr_module.get("detailedDescription", "")

    # Conditions module
    cond_module = protocols.get("conditionsModule", {})
    cleaned_data["Conditions"] = ", ".join(cond_module.get("conditions", []))

    # Design module
    design_module = protocols.get("designModule", {})
    design_info = design_module.get("designInfo", {})
    cleaned_data["Study Phase"] = ", ".join(design_module.get("phases", []))
    cleaned_data["Study Type"] = design_info.get("studyType", "")
    cleaned_data["Enrollment Count"] = design_module.get("enrollmentInfo", {}).get(
        "count", 0
    )
    cleaned_data["Allocation"] = design_info.get("allocation", "")
    cleaned_data["Intervention Model"] = design_info.get("interventionModel", "")
    cleaned_data["Observational Model"] = design_info.get("observationalModel", "")
    cleaned_data["Primary Purpose"] = design_info.get("primaryPurpose", "")
    cleaned_data["Masking"] = design_info.get("maskingInfo", {}).get("masking", "")
    cleaned_data["Who Masked"] = ", ".join(
        design_info.get("maskingInfo", {}).get("whoMasked", [])
    )
    cleaned_data["Time Perspective"] = design_info.get("timePerspective", "")

    # Inverventions module
    interv_module = protocols.get("armsInterventionsModule", {})
    cleaned_data["Interventions"] = " ; ".join(
        format_intervention(item) for item in interv_module.get("interventions", [])
    )

    # Outcomes module
    outcomes_module = protocols.get("outcomesModule", {})
    cleaned_data["Primary Measure Outcomes"] = " ; ".join(
        format_outcome(item, idx)
        for idx, item in enumerate(outcomes_module.get("primaryOutcomes", []))
    )
    cleaned_data["Secondary Measure Outcomes"] = " ; ".join(
        format_outcome(item, idx)
        for idx, item in enumerate(outcomes_module.get("secondaryOutcomes", []))
    )

    # Eligibility module
    elig_module = protocols.get("eligibilityModule", {})
    cleaned_data["Minimum Age"] = elig_module.get("minimumAge", "")
    cleaned_data["Sexes Eligible for Study"] = elig_module.get("sex", "")
    cleaned_data["Accepts Healthy Volunteers"] = (
        "Yes" if elig_module.get("healthyVolunteers", False) else "No"
    )
    cleaned_data["Ages Eligible for Study"] = ", ".join(elig_module.get("stdAges", []))
    cleaned_data["Sampling Method"] = elig_module.get("samplingMethod", "")
    cleaned_data["Inclusion Criteria"], cleaned_data["Exclusion Criteria"] = (
        get_inclusion_exclusion_criteria(elig_module.get("eligibilityCriteria"))
    )

    # Locations module
    loc_module = protocols.get("contactsLocationsModule", {})
    cleaned_data["Overall Officials"] = " ; ".join(
        format_official(item) for item in loc_module.get("overallOfficials", [])
    )
    cleaned_data["Locations"] = " ; ".join(
        format_location(item) for item in loc_module.get("locations", [])
    )

    # TODO: References
    # references = study.get("protocolSection", {}).get("referencesModule", {}).get("references", [])
    # if references:
    #     combined_references = []
    #     for ref in references:
    #         citation = ref.get('citation', "")
    #         combined_references.append(citation)
    #     combined_references_str = " | ".join(combined_references)
    # else:
    #     combined_references_str = ""

    # TODO: Documents
    # documents = study.get("documentSection", {}).get("largeDocumentModule", {}).get("largeDocs", [])
    # if documents:
    #     base_url = "https://cdn.clinicaltrials.gov/large-docs/"
    #     combined_documents = []
    #     for doc in documents:
    #         label = doc.get('label', "")
    #         filename = doc.get('filename', "")
    #         last_two_digits = study_id[-2:]
    #         document_url = f"{base_url}{last_two_digits}/{study_id}/{filename}"
    #         combined_documents.append(f"{label}, {document_url}")
    #     combined_documents_str = " | ".join(combined_documents)
    # else:
    #     combined_documents_str = ""

    return cleaned_data


def main():
    if not RAW_JSONL_PATH.exists():
        raise RuntimeError(
            f"Raw data missing at: {RAW_JSONL_PATH}; run the fetch subcommand first"
        )

    # Load metadata if it exists
    n_cleaned_studies = 0
    n_studies = None
    if METADATA_PATH.exists():
        with METADATA_PATH.open("r", encoding="utf-8") as f:
            metadata = json.load(f)
        n_studies = metadata["n_studies"]

    with default_progress() as progress:
        task = progress.add_task("Cleaning data...", total=n_studies)

        with CLEANED_CSV_PATH.open("w", encoding="utf-8") as csv_file:
            # Write headers
            writer = csv.DictWriter(csv_file, fieldnames=CSV_HEADERS)
            writer.writeheader()

            with jsonlines.open(RAW_JSONL_PATH, "r") as f:
                # Iterate over raw data, clean each entry, and write a CSV row
                for data in f:
                    cleaned_data = clean_one_study(data)
                    writer.writerow(cleaned_data)
                    progress.update(task, advance=1)
                    n_cleaned_studies += 1

    rich.print(
        f"[bold green]->[/] {n_cleaned_studies} cleaned studies saved to {CLEANED_CSV_PATH}"
    )
