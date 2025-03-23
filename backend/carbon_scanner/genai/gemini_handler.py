import os
import google.generativeai as genai
from PIL import Image, ImageFile
from carbon_scanner.config import config
from carbon_scanner.genai import lang_chain_process

assert config.GEMINI_API_KEY, "GEMINI_API_KEY is not set in the environment variables."
genai.configure(api_key=os.environ["GEMINI_API_KEY"])
model = genai.GenerativeModel('gemini-2.0-flash')
# gemini-2.0-pro-exp-02-05

def image_resp(prompt: str, image: ImageFile) -> str:
    """
    Sends an image object and prompt to Google Gemini, returns the response.

    Parameters:
        prompt: The prompt to send Gemini.
        image: An image object given by PIL.Image.open.
    """
    response = model.generate_content([prompt, image])
    return response.text

def text_resp(prompt: str) -> str:
    """
    Generates a model response based on a text prompt.
    """
    response = model.generate_content(f"given the following prompt, restrict your response to less than 300 words {prompt}")
    return response.text

def reciept_resp(image: ImageFile) -> str:
   prompt = "break down all items in this reciept into a list of the raw materials, then return that as a comma seperated list"  
   itemlist=image_resp(prompt, image)
   print(f"item list : {itemlist}")
   return lang_chain_process.list_resp(itemlist)

if __name__ == "__main__":
    # Example usage
    #prompt = "What is the capital of France?"
    #text_response = text_resp(prompt)
    #print("Response from Gemini with text:", text_response)
    # with reciept image
    imgfile = Image.open("./genai/reciept.png")
    print(reciept_resp(imgfile))
