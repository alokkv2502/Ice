import os
import requests

def scrape_linkedin_profile(linkedin_profile_url: str):
    """Scrape information from LinkedIn profiles."""
    api_endpoint = "https://nubela.co/proxycurl/api/v2/linkedin"
    header_dic = {
        "Authorization": f'Bearer {os.getenv("PROXYCURL_API_KEY")}'
    }

    response = requests.get(api_endpoint, params={"url": linkedin_profile_url}, headers=header_dic)

    #return response

    # Check if the request was successful
    #if response.status_code == 200:
    data = response.json()  # Assuming the API returns JSON

        # Filter out empty values and unwanted keys
    data = {
        k: v
        for k, v in data.items()
        if v not in ([], "","", None) 
          and k not in ["people_also_viewed", "certifications"]
        }

        # Remove profile_pic_url from groups if present
    if "groups" in data:
            for group_dict in data["groups"]:
                group_dict.pop("profile_pic_url", None)  # Use None to avoid KeyError if the key is not present

    return data
    #else:
        # Output the response text for debugging purposes
        #print(f"Failed to scrape LinkedIn profile: {response.text}")
        #response.raise_for_status()

# Usage example (uncomment and replace with a real LinkedIn URL when running)
# profile_data = scrape_linkedin_profile("https://www.linkedin.com/in/username")
# print(profile_data)
