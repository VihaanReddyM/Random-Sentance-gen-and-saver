import requests
import json
import random
import time
import os

current_time = time.strftime("%Y-%m-%d-%H-%M-%S", time.localtime())
json_file_path = input("Please enter the folder/file path to which the sentences will be saved: ")
format_type = input("Do you want a formatted JSON file (Y/N): ")


if format_type.lower() == 'y':
    json_format = {"Sentances": []}
    file_extention = '.json'
    
else:
    json_format = {}
    file_extention = '.txt'
    
default_file_name ='output' + current_time + file_extention

def fetch_random_quote():
    try:
        response = requests.get("https://type.fit/api/quotes", timeout=10)
        if response.status_code == 200:
            data = response.json()
            random_quote = random.choice(data)["text"]
            return random_quote
        else:
            print("Failed to fetch random quote from the API.")
            return None
    except requests.exceptions.Timeout:
        print("Request timed out.  the program...")
        time.sleep(2)  # Wait for a few seconds before restarting
        return fetch_random_quote()
    except requests.exceptions.RequestException as e:
        print("An error occurred:", e)
        return None


check = os.path.isdir(json_file_path)
files_in_folder = os.listdir(json_file_path)

if format_type.lower() == 'y':
    usable_file_path = os.path.join(json_file_path, default_file_name)

    with open(usable_file_path, "w"):
        pass
    print("File created successfully.")
else:
    if check:
        print("We have found the following files in the folder:", files_in_folder)
        check_response = input("We have found no file or many files in the directory of the folder you have given us. Can we create a file for you if you say y or you can choose a existing gile if you say n (Y/N): ")
        if check_response.lower() == 'y':
            usable_file_path = os.path.join(json_file_path, default_file_name)

            with open(usable_file_path, "w"):
                pass
            print("File created successfully.")
        else:
            use_old_file = input("Do you want to use the file there the directory you have given us (Y/N): ")
            if use_old_file.lower() == 'y':
                print("the file you can use are : ", files_in_folder)
                old_file_path = input("Please enter the name of the file you want to use: ")
                usable_file_path = os.path.join(json_file_path, old_file_path)
                print("We are using this file:", usable_file_path)
                print("We will save quotes to this file.")
            else:
                print("Please enter a valid file path.")
                exit = input("Press enter to exit.")

def add_quote_to_json(file_path, quote):
    if format_type.lower() == 'y':
        usable_file_path = os.path.join(json_file_path, default_file_name)
        try:
            if os.path.isfile(usable_file_path):
                with open(usable_file_path, "r", encoding="utf-8") as json_file:
                    try:
                        json_data = json.load(json_file)
                    except json.JSONDecodeError:
                        json_data = {"sentances": []}
            else:
                json_data = {"sentances": []}

            json_data["sentances"].append(quote)

            with open(file_path, "w", encoding="utf-8") as json_file:
                json.dump(json_data, json_file, indent=4)
        except Exception as e:
            print("An error occurred while adding quote to JSON:", e)
    else:
        usable_file_path = os.path.join(json_file_path, default_file_name)
        try:
            with open(file_path, "a", encoding="utf-8") as file:
                file.write(quote + "\n")
        except Exception as e:
            print("An error occurred while adding quote to file:", e)



# Example usage
num_quotes = 0

while True:
    num_quotes += 1
    quote = fetch_random_quote()
    if quote:
        add_quote_to_json(usable_file_path, quote)
        print("Quote saved successfully. | The number of quotes generated is", num_quotes)
    else:
        print("Failed to generate and save quote.")

    if num_quotes % 10000 == 0:
        choice = input("Do you want to continue generating quotes? (Y/N): ")
        if choice.lower() != "y":
            break
