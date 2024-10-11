import requests
import json
import csv
import os
import jsonlines
from shared import default_progress

API_ENDPOINT = "https://clinicaltrials.gov/api/v2/studies"
AGG_FILTERS = "docs:sap,results:with,status:com"
PAGE_SIZE = 1000


def query(page_token=None):
    """Query the ClinicalTrials.gov API for studies."""
    url = f"{API_ENDPOINT}?aggFilters={AGG_FILTERS}&pageSize={PAGE_SIZE}"
    if page_token is not None:
        url += f"&pageToken={page_token}"

    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    raise Exception(f"Failed to fetch data (status: {response.status_code})")


def save_to_json(studies, filename='../../data/fetched_studies.json'):
    """Save the fetched data to a JSON file."""
    with open(filename, 'w') as f:
        json.dump(studies, f, indent=2)
    print(f"Data saved to {filename}")


def format_date(date_info):
    """Helper function to format dates with '(estimated)' if needed."""
    if isinstance(date_info, dict):
        date = date_info.get('date', '')
        date_type = date_info.get('type', '')
        
        if date_type == 'ESTIMATED':
            return f"{date} (estimated)"
        return date
    elif isinstance(date_info, str):
        if 'estimated' in date_info.lower():
            return f"{date_info} (estimated)"
        return date_info
    return ""


def flatten_design_info(design_info):
    """Flatten the designInfo dictionary into a single string."""
    return "; ".join(f"{key}: {value}" for key, value in design_info.items())


def extract_inclusion_exclusion(eligibility_text):
    """Extract inclusion and exclusion criteria from the eligibility text without labels."""
    inclusion_criteria = ""
    exclusion_criteria = ""

    inclusion_start = eligibility_text.find("Inclusion Criteria")
    exclusion_start = eligibility_text.find("Exclusion Criteria")

    if inclusion_start != -1:
        if exclusion_start != -1:
            inclusion_criteria = eligibility_text[inclusion_start + len("Inclusion Criteria:"):exclusion_start].strip()
            exclusion_criteria = eligibility_text[exclusion_start + len("Exclusion Criteria:"):].strip()
        else:
            inclusion_criteria = eligibility_text[inclusion_start + len("Inclusion Criteria:"):].strip()

    return inclusion_criteria, exclusion_criteria


def save_outcomes_to_csv(studies, filename, write_header=True):
    """Save primary and secondary outcome measures to CSV columns."""
    
    with open(filename, 'a' if not write_header else 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Study ID', 'Brief Title', 'Official Title', 'Brief Summary', 'Detailed Description', 
                    'Organization Name', 'Organization Type', 'Sponsor Name', 'Sponsor Type', 'Collaborators', 'Overall Officials',
                    'Study Type', 'Conditions', 'Study Phase', 'Allocation', 'Intervention Model', 'Observational Model', 'Primary Purpose', 'Masking', 'Who Masked', 
                    'Time Perspective', 'Interventions', 'Enrollment Count', 
                    'Minimum Age', 'Sexes Eligible for Study', 'Accepts Healthy Volunteers', 'Ages Eligible for Study', 'Sampling Method',
                    'Inclusion Criteria', 'Exclusion Criteria', 'Locations',
                    'First Submitted', 'First Submitted (QC Met)', 'First Posted', 
                    'Results First Submitted', 'Results First Submitted (QC Met)', 'Results First Posted',
                    'Last Update Submitted', 'Last Update Posted', 'Last Verified', 'Primary Measure Outcomes', 'Secondary Measure Outcomes', 
                    'References', 'Documents']

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        
        if write_header:
            writer.writeheader()  

        for study in studies:
            # Study ID
            study_id = study.get("protocolSection", {}).get("identificationModule", {}).get("nctId", "")
            
            # BriefTitle & officialTitle
            brief_title = study.get("protocolSection", {}).get("identificationModule", {}).get("briefTitle", "")
            official_title = study.get("protocolSection", {}).get("identificationModule", {}).get("officialTitle", "")

            # Description Module
            brief_summary = study.get("protocolSection", {}).get("descriptionModule", {}).get("briefSummary", "")
            detailed_description = study.get("protocolSection", {}).get("descriptionModule", {}).get("detailedDescription", "")

            # Conditions
            conditions = ", ".join(study.get("protocolSection", {}).get("conditionsModule", {}).get("conditions", []))

            # Design Info 
            design_module = study.get("protocolSection", {}).get("designModule", {})
            design_info = design_module.get("designInfo", {})
            
            study_phase = ", ".join(design_module.get('phases', []))
            allocation = design_info.get('allocation', "")
            intervention_model = design_info.get('interventionModel', "")
            observational_model = design_info.get('observationalModel', "")
            primary_purpose = design_info.get('primaryPurpose', "")
            masking = design_info.get('maskingInfo', {}).get('masking', "")
            who_masked = ", ".join(design_info.get('maskingInfo', {}).get('whoMasked', []))
            time_perspective = design_info.get('timePerspective', "")

            # Interventions
            interventions = study.get("protocolSection", {}).get("armsInterventionsModule", {}).get("interventions", [])
            combined_interventions = []
            for intervention in interventions:
                type_ = intervention.get("type", "")
                name = intervention.get("name", "")
                description = intervention.get("description", "")
                combined_interventions.append(f"{type_} | {name} | {description}")
            combined_interventions_str = " ; ".join(combined_interventions)

            # Enrollment Info
            enrollment_count = study.get("protocolSection", {}).get("designModule", {}).get("enrollmentInfo", {}).get("count", "")
            
            # Eligibility Criteria
            eligibility_module = study.get("protocolSection", {}).get("eligibilityModule", {})
            minimum_age = eligibility_module.get('minimumAge', 'NA')
            sexes_eligible = eligibility_module.get('sex', 'NA')
            healthy_volunteers = 'Yes' if eligibility_module.get('healthyVolunteers', False) else 'No'
            std_ages = ", ".join(eligibility_module.get('stdAges', []))  
            sampling_method = eligibility_module.get('samplingMethod', "")

            eligibility_text = study.get("protocolSection", {}).get("eligibilityModule", {}).get("eligibilityCriteria", "")
            inclusion_criteria, exclusion_criteria = extract_inclusion_exclusion(eligibility_text)

            # Organization name & organization type
            organization_name = study.get("protocolSection", {}).get("identificationModule", {}).get("organization", {}).get("fullName", "")
            organization_type = study.get("protocolSection", {}).get("identificationModule", {}).get("organization", {}).get("class", "")

            # Sponsor name & sponsor type
            sponsor_name = study.get("protocolSection", {}).get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("name", "")
            sponsor_type = study.get("protocolSection", {}).get("sponsorCollaboratorsModule", {}).get("leadSponsor", {}).get("class", "")

            # Collaborators
            collaborators = study.get("protocolSection", {}).get("sponsorCollaboratorsModule", {}).get("collaborators", [])
            if collaborators:
                combined_collaborators = []
                for collaborator in collaborators:
                    name = collaborator.get('name', 'NA')
                    class_ = collaborator.get('class', 'NA')
                    combined_collaborators.append(f"{name} | {class_}")
                combined_collaborators_str = " ; ".join(combined_collaborators)  
            else:
                combined_collaborators_str = "NA"  

            # Study Registration Dates
            first_submitted = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("studyFirstSubmitDate", {}))
            first_submitted_qc = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("studyFirstSubmitQcDate", {}))
            first_posted = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("studyFirstPostDateStruct", {}))

            # Results Reporting Dates
            results_first_submitted = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("resultsFirstSubmitDate", {}))
            results_first_submitted_qc = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("resultsFirstSubmitQcDate", {}))
            results_first_posted = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("resultsFirstPostDateStruct", {}))

            # Study Record Updates
            last_update_submitted = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("lastUpdateSubmitDate", {}))
            last_update_posted = format_date(study.get("protocolSection", {}).get("statusModule", {}).get("lastUpdatePostDateStruct", {}))
            last_verified = study.get("protocolSection", {}).get("statusModule", {}).get("statusVerifiedDate", "")

            # Primary Outcome Measures
            primary_outcomes = study.get("protocolSection", {}).get("outcomesModule", {}).get("primaryOutcomes", [])
            combined_primary_outcome = []
            
            for idx, outcome in enumerate(primary_outcomes):
                measure = outcome.get('measure', '')
                description = outcome.get('description', '')
                timeFrame = outcome.get('timeFrame', '')
                combined_primary_outcome.append(f"**Measure{idx + 1}** {measure} | {description} | {timeFrame}")
            combined_primary_outcome_str = "; ".join(combined_primary_outcome)

            # Secondary Outcome Measures
            secondary_outcomes = study.get("protocolSection", {}).get("outcomesModule", {}).get("secondaryOutcomes", [])
            combined_secondary_outcome = []
            for outcome in secondary_outcomes:
                measure = outcome.get('measure', '')
                description = outcome.get('description', '')
                timeFrame = outcome.get('timeFrame', '')
                combined_secondary_outcome.append(f"**Measure{idx + 1}** {measure} | {description} | {timeFrame}")
            combined_secondary_outcome_str = "; ".join(combined_secondary_outcome)

            # Overall Officials
            overall_officials = study.get("protocolSection", {}).get("contactsLocationsModule", {}).get("overallOfficials", [])
            combined_officials = []
            for official in overall_officials:
                name = official.get('name', '')
                affiliation = official.get('affiliation', '')
                role = official.get('role', '')
                combined_officials.append(f"{name} | {affiliation} | {role}")
            combined_officials_str = " ; ".join(combined_officials)

            # Locations
            locations = study.get("protocolSection", {}).get("contactsLocationsModule", {}).get("locations", [])
            combined_locations = []
            for location in locations:
                facility = location.get('facility', '')
                city = location.get('city', '')
                zip_code = location.get('zip', '')
                country = location.get('country', '')
                combined_locations.append(f"{facility}, {city}, {zip_code}, {country}")
            combined_locations_str = " ; ".join(combined_locations)

            # References
            references = study.get("protocolSection", {}).get("referencesModule", {}).get("references", [])
            if references:
                combined_references = []
                for ref in references:
                    citation = ref.get('citation', "")
                    combined_references.append(citation)
                combined_references_str = " | ".join(combined_references) 
            else:
                combined_references_str = ""  

            # Documents
            documents = study.get("documentSection", {}).get("largeDocumentModule", {}).get("largeDocs", [])
            if documents:
                base_url = "https://cdn.clinicaltrials.gov/large-docs/"
                combined_documents = []
                for doc in documents:
                    label = doc.get('label', "")
                    filename = doc.get('filename', "")
                    last_two_digits = study_id[-2:]  
                    document_url = f"{base_url}{last_two_digits}/{study_id}/{filename}"
                    combined_documents.append(f"{label}, {document_url}")
                combined_documents_str = " | ".join(combined_documents)  
            else:
                combined_documents_str = "" 
            
            # write to csv
            writer.writerow({
                'Study ID': study_id,
                'Brief Title': brief_title,              
                'Official Title': official_title,  
                'Brief Summary': brief_summary,
                'Detailed Description': detailed_description,
                'Organization Name': organization_name,  
                'Organization Type': organization_type,       
                'Sponsor Name': sponsor_name,           
                'Sponsor Type': sponsor_type,      
                'Collaborators': combined_collaborators_str,
                'Overall Officials': combined_officials_str,
                'Study Type': study.get("protocolSection", {}).get("designModule", {}).get("studyType", ""),
                'Conditions': conditions,
                'Study Phase': study_phase,                    
                'Allocation': allocation,                  
                'Intervention Model': intervention_model,     
                'Primary Purpose': primary_purpose,            
                'Masking': masking,                           
                'Who Masked': who_masked,                     
                'Observational Model': observational_model,   
                'Interventions': combined_interventions_str,
                'Time Perspective': time_perspective,           
                'Enrollment Count': enrollment_count,
                'Minimum Age': minimum_age,                    
                'Sexes Eligible for Study': sexes_eligible,  
                'Accepts Healthy Volunteers': healthy_volunteers, 
                'Ages Eligible for Study': std_ages,          
                'Sampling Method': sampling_method,            
                'Inclusion Criteria': inclusion_criteria,
                'Exclusion Criteria': exclusion_criteria,
                'Locations': combined_locations_str,      
                'First Submitted': first_submitted,
                'First Submitted (QC Met)': first_submitted_qc,
                'First Posted': first_posted,
                'Results First Submitted': results_first_submitted,
                'Results First Submitted (QC Met)': results_first_submitted_qc,
                'Results First Posted': results_first_posted,
                'Last Update Submitted': last_update_submitted,
                'Last Update Posted': last_update_posted,
                'Last Verified': last_verified,
                'Primary Measure Outcomes': combined_primary_outcome_str,
                'Secondary Measure Outcomes': combined_secondary_outcome_str,
                'References': combined_references_str,
                'Documents': combined_documents_str
            })

def main():
    page_token = None 
    study_count = 0 
    json_filename = '../../data/fetched_studies.json'  
    csv_filename = '../../data/cleaned_studies.csv'  

    if not os.path.exists('../../data'):
        os.makedirs('../../data')

    # Load existing json file and transform to csv
    if os.path.exists(json_filename):
        print(f"{json_filename} already exists, loading and converting to CSV.")
        with jsonlines.open(json_filename) as reader:
            write_header = True  
            for study in reader:
                save_outcomes_to_csv([study], csv_filename, write_header=write_header)
                write_header = False  
                study_count += 1  

    # If there's no existing json file
    else:
        with default_progress() as progress:
            task = progress.add_task(f"Fetching data...", total=None)

            while True:
                data = query(page_token=page_token)
                with jsonlines.open(json_filename, mode='a') as writer:
                    writer.write_all(data["studies"])  
                progress.update(task, description=f"Fetched {len(data['studies']):5d} data")
                
                study_count += len(data["studies"])

                if "nextPageToken" not in data:
                    break  
                page_token = data["nextPageToken"]  

        # To csv
        with jsonlines.open(json_filename) as reader:
            write_header = True  
            for study in reader:
                save_outcomes_to_csv([study], csv_filename, write_header=write_header)
                write_header = False 
   
    print(f"Total number of studies processed: {study_count}")