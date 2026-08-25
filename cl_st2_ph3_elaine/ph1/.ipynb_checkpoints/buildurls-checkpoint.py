from bs4 import BeautifulSoup
import pandas as pd

def main():
    # Defining input variables
    input_directory = 'indexes'
    input_file = 'TED_7061_of_7061_20250314.html'

    # Scraping the 'TED Talks' URLs
    with open(f'{input_directory}/{input_file}', 'r', encoding='utf8', newline='\n') as html_doc:
        soup = BeautifulSoup(html_doc, 'lxml')

    # Find all 'a' tags with the class 'relative'
    tedtalks_urls = soup.find_all('a', class_='relative')

    # Extract the 'href' attribute of each link and store them in a list
    tedtalks_urls_list = [tedtalks_url.get('href') for tedtalks_url in tedtalks_urls if tedtalks_url.get('href')]

    # Create a Pandas DataFrame from the list of links
    df_tedtalks_urls1 = pd.DataFrame(tedtalks_urls_list, columns=['TED Talks URL'])

    # Filter the DataFrame to keep only rows where 'TED Talks URL' contains 'https://www.ted.com/talks/'
    df_tedtalks_urls1 = df_tedtalks_urls1[df_tedtalks_urls1['TED Talks URL'].str.contains('https://www.ted.com/talks/')]
    df_tedtalks_urls1 = df_tedtalks_urls1.reset_index(drop=True)

    # Append '/transcript?language=en' to each 'TED Talks URL'
    df_tedtalks_urls1['TED Talks URL'] = df_tedtalks_urls1['TED Talks URL'] + '/transcript?language=en'

    # Importing the previous study's TED Talks URLs
    df_tedtalks_urls2 = pd.read_csv('previous_study_valid_urls', delimiter='\t', header=None)
    df_tedtalks_urls2.columns = ['File ID', 'TED Talks URL']

    # Creating df_tedtalks_urls3 by excluding rows from df_tedtalks_urls1 that are present in df_tedtalks_urls2
    df_tedtalks_urls3 = df_tedtalks_urls1[~df_tedtalks_urls1['TED Talks URL'].isin(df_tedtalks_urls2['TED Talks URL'])]
    df_tedtalks_urls3 = df_tedtalks_urls3.reset_index(drop=True)

    # Create the 'File ID' column starting from '000001'
    df_tedtalks_urls3['File ID'] = (df_tedtalks_urls3.index + 1).astype(str).str.zfill(6)

    # Creating the file 'valid_urls'
    df_tedtalks_urls3[['File ID', 'TED Talks URL']].to_csv('valid_urls', sep='\t', index=False, header=False, encoding='utf-8', lineterminator='\n')

if __name__ == "__main__":
    main()
