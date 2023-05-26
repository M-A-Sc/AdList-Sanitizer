#AdList Sanitizer 0.1b#
#by M-A.Sc#
#Slow and dirty but multiplattform ;)#

# There's a bunch of Adlists floating around... With this script you can
# download multiply Adlists (lists.txt), filter and extract valid domains and subdomains entries,
# delete duplicates and specific domains and make yourself a nice customized and clean (sanitized:) AdList

import os
import requests
import re
from concurrent.futures import ThreadPoolExecutor

# parallel downloads
max_concurrent_downloads = 4

# AdList URLs
url_file = 'lists.txt'

# make dir if it doesnt exist
if not os.path.exists('download'):
    os.makedirs('download')

# download-function
def download_file(url):
    filename = url.split('/')[-1]
    filepath = os.path.join('download', filename)
    response = requests.get(url)
    if response.status_code == 200:
        with open(filepath, 'wb') as file:
            file.write(response.content)
        file_size = os.path.getsize(filepath)
        num_entries = len(response.content.decode().splitlines())
        print(f'{filename} was downloaded. Size: {file_size} Bytes, Number of Domains: {num_entries}')
    else:
        print(f'Error trying to download {filename}. Errorcode: {response.status_code}')

# multi download
def download_files(urls):
    with ThreadPoolExecutor(max_workers=max_concurrent_downloads) as executor:
        executor.map(download_file, urls)

# merge lists
def merge_files():
    files = os.listdir('download')
    merged_content = ''
    for file in files:
        filepath = os.path.join('download', file)
        with open(filepath, 'r') as f:
            file_content = f.read()
            merged_content += file_content
    with open('master.txt', 'w') as f:
        f.write(merged_content)
    print('Adlists got merged into master.txt')

# extract domain names
def extract_domain_names(file_path):
    with open(file_path, 'r') as file:
        content = file.read()

        # Pattern
        pattern = r'(?:[a-zA-Z0-9]+(?:-[a-zA-Z0-9]+)*\.)+[a-zA-Z]{2,}'

        # Search for matching patterns
        matches = re.findall(pattern, content)

        # get rid of www.
        domain_names = [re.sub(r'^www\.', '', match) for match in matches]

        # return cleaned domain names
        return domain_names

# Remove duplicates
def remove_duplicates(input_list):
    return list(set(input_list))

# Ask if User wants to delete specific domains from sanity.txt
def delete_domains(delete_domains):
    # Load sanity.txt
    sanity_file_path = 'sanity.txt'
    with open(sanity_file_path, 'r') as sanity_file:
        domain_names = sanity_file.read().splitlines()

    # Domainname entries
    num_entries_before = len(domain_names)

    # Delete Domain from List
    updated_domains = [domain for domain in domain_names if domain not in delete_domains]

    # rewrite sanity.txt
    with open(sanity_file_path, 'w') as sanity_file:
        sanity_file.write('#### adlist sanitizer 0.1b ####\n\n')
        for domain_name in updated_domains:
            sanity_file.write(domain_name + '\n')

    # Calculation of entries
    num_entries_deleted = num_entries_before - len(updated_domains)

    print(f'These Domains got deleted from sanity.txt: {", ".join(delete_domains)}')
    print(f'{num_entries_deleted} got deleted with its subdomains.')

# delete temporary data function
def delete_files():
    # delete download dir
    if os.path.exists('download'):
        for file in os.listdir('download'):
            file_path = os.path.join('download', file)
            os.remove(file_path)
        os.rmdir('download')
        print(" Folder download got deleted.")

    # delete temp .txt
    if os.path.exists('output.txt'):
        os.remove('output.txt')
        print("'output.txt' got deleted.")
    if os.path.exists('master.txt'):
        os.remove('master.txt')
        print("'master.txt' got deleted.")

# Ask if ..
def prompt_user():
    while True:
        delete_option = input('Do you want to remove some Domains (google.com) from sanity.txt? (y/n): ')
        if delete_option.lower() == 'y':
            domains_to_delete = input('Enter the Domains you want to delete seperated by space: ')
            delete_domains(domains_to_delete.split())
        elif delete_option.lower() == 'n':
            break
        else:
            print('Invalid input please enter "y" or "n".')

    delete_files_option = input('Do you want to delete temporary files and folders? (y/n)')
    if delete_files_option.lower() == 'y':
        delete_files()

# Statistics and output
def display_entry_stats():
    num_entries_master = len(domain_names)
    num_entries_sanity = len(unique_domain_names)
    percentage_difference = (num_entries_sanity / num_entries_master) * 100

    print(f"master.txt has {num_entries_master} Number of Domains.")
    print(f"The sanitized 'sanity.txt' has {num_entries_sanity} Number of Domains.")
    #print(f"Der prozentuale Unterschied zur 'master.txt' beträgt {percentage_difference:.2f}%.")
    print(f"The final list is just {percentage_difference:.2f}% the size of master.txt.")

# main
if os.path.exists(url_file):
    with open(url_file, 'r') as file:
        urls = [line.strip() for line in file.readlines() if line.strip()]
        download_files(urls)
    merge_files()

    # extract domains
    domain_names = extract_domain_names('master.txt')

    # put domain names into output.txt
    output_file_path = 'output.txt'

    with open(output_file_path, 'w') as output_file:
        for domain_name in domain_names:
            output_file.write(domain_name + '\n')

    # delete duplicated and save in sanity.txt
    unique_domain_names = remove_duplicates(domain_names)
    sanity_file_path = 'sanity.txt'

    with open(sanity_file_path, 'w') as sanity_file:
        sanity_file.write('#### adlist sanitizer 0.1b ####\n\n')
        for domain_name in unique_domain_names:
            sanity_file.write(domain_name + '\n')

    prompt_user()
    display_entry_stats()
else:
    print(f'Can not find "{url_file}"')
