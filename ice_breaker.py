import os
from dotenv import load_dotenv
load_dotenv()
#os.environ['PYTHONIOENCODING'] = 'utf-8'
#import sys

# Set the default encoding to UTF-8
#sys.stdout.reconfigure(encoding='utf-8')


from langchain.prompts import PromptTemplate

#from langchain import PromptTemplate
#from langchain.chat_models import ChatOpenAI
from langchain_community.chat_models import ChatOpenAI

from langchain.chains import LLMChain
from third_party.linkedin import scrape_linkedin_profile
from agents.linkedin_lookup_agent import lookup as linkedin_lookup_agent
from output_parsers import person_intel_parser,PersonIntel
from output_parsers import person_intel_parser
from typing import Tuple








def ice_break(name:str)->Tuple[PersonIntel,str]:
    print("hello")
    print(os.environ['OPENAI_API_KEY'])
    print(os.environ['PROXYCURL_API_KEY'])

    linkedin_profile_url=linkedin_lookup_agent(name=name)
    linkedin_data=scrape_linkedin_profile(linkedin_profile_url=linkedin_profile_url)


    summary_template="""
      given the Linkedin information {information} about a person from I want you to create:
      1.a short summary
      2.two interesting facts about them
      3-guess the character trait based on information {information} about a person
      4-2 creative Ice breakers to open a conversation with them
          \n{format_instructions}
     """

    summary_prompt_template=PromptTemplate(
        input_variables=["information"],template=summary_template,
        partial_variables={"format_instructions":person_intel_parser.get_format_instructions()},
        
    )
    llm=ChatOpenAI(temperature=1,model_name="gpt-3.5-turbo")
    chain=LLMChain(llm=llm,prompt=summary_prompt_template)


    
    
    
    #linkedin_data=scrape_linkedin_profile(
       # linkedin_profile_url=linkedin_profile_url)
    
    #print(linkedin_data)
    result= (chain.run(information=linkedin_data))
    #print(result)
    return person_intel_parser.parse(result),linkedin_data.get("profile_pic_url")
    #return person_intel_parser.parse(result),linkedin_data.get("profile_pic_url")
    

if  __name__=='__main__':
    print("Hello ")
    result=ice_break(name="Alok kumar verma nit jlandhar linkedin")