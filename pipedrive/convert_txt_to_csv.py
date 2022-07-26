import pandas as pd

def main():
    """Automatically convert export from manual notes to a csv file importable into pipedrive."""

    with open("leads.txt", "r") as f:
        leads = [line for line in f.readlines() if "- [" in line]
    processed_leads  = []
    for lead in leads:
        tmp = lead.replace("- [ ]", "").replace("- [x]", "").strip().split(",")
        try:
            if len(tmp) == 3:
                lead_name, lead_linkedin, lead_org = tmp[0], tmp[1], tmp[2]
                lead_email, lead_extra = None, None
            elif len(tmp) == 2:
                lead_name, lead_linkedin = tmp[0], tmp[1]
                lead_email, lead_org, lead_extra = None, None, None
            else:
                lead_name, lead_linkedin, lead_email, lead_extra = tmp[0], tmp[1], tmp[2], ", ".join(tmp[3:])
            processed_leads.append({"Lead Name": lead_name, "Lead LinkedIn": lead_linkedin, "Lead Email": lead_email, "Lead Extra": lead_extra, "Owner": "Sacha", "Title": lead_name})
        except Exception as e:
            pass
    df = pd.DataFrame.from_dict(processed_leads)
    df.to_excel("leads.xlsx", index=False)
    
if __name__ == "__main__":
    main()