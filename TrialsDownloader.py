"""
Author: Joseph P DeBartola III

Usage: (in adjacent script) from TrialsDownloader import x

This script contains a class which, given specified search criteria,
formats said criteria into an url utilized to download clinical trial
details from clinicaltrials.gov. in a .zip file.

The script then extracts the .xml files within and stores the in the
adjacent /downloads/ folder.
"""

import requests
import os
import zipfile
import errno
import shutil


BASE_PATH = os.path.dirname(
    os.path.abspath(__file__)
)

DOWNLOAD_PATH = os.path.join(BASE_PATH, 'downloads')
SEARCH_PARAMETERS_FILE = os.path.join(BASE_PATH, 'params.txt')


class TrialsDownloader(object):
    """
    This collects research from clinicaltrials.gov as specified
    by the criteria designated within the adjacent text file
    params.txt. For instructions on how to format this file,
    please see README.md.

    If terms is specified upon initialization,
    usage of params.txt is overridden and the passed
    terms are utilized.
    """
    search_criteria = []
    relative_download_dirs = []

    def __init__(self, terms=None):
        print('> Gathering search criteria...')

        if terms is None:
            self.get_search_criteria()
        else:
            term_list = terms.split('_')
            self.search_criteria.extend(term_list)

        self.make_sure_path_exists(DOWNLOAD_PATH)
        for criteria in self.search_criteria:
            self.download_research(criteria)

    def get_search_criteria(self):
        """
        Collects search criteria from local file params.txt
        """
        try:
            with open(SEARCH_PARAMETERS_FILE, 'r+') as f:
                    for line in f:
                        line = line.strip()
                        print(
                            '> Adding terms to queue: "{}"'
                            .format(line)
                        )
                        full_terms = ''
                        search_terms = line.split(' ')

                        for idx, term in enumerate(search_terms):
                            if idx != (len(search_terms) - 1):
                                full_terms += term + '+'
                            else:
                                full_terms += term

                        self.search_criteria.append(full_terms)
        except OSError:
            raise OSError(
                """
                Search parameters file params.txt doesn't seem to
                be present in the root directory of this program. Have
                you read the README.md and created this file accordingly?
                Also, make sure permissions are set for reading and
                writing throughout this project's directory.
                """
            )

    def download_research(self, criteria):
        """
        Downloads a .zip file full of XML files containing
        research relevant to the given criteria, then extracts
        the contents to the proper destination in /downloads/
        in the project folder.
        """
        full_download_url = self.get_download_url(criteria)
        zip_name = criteria.replace('+', '_') + '_trials.zip'
        full_destination = \
            os.path.join(
                DOWNLOAD_PATH, zip_name
            )

        print(
            '> Downloading archive of results for parameters "{}"'
            .format(criteria)
        )

        self.download_file(full_download_url, full_destination)

        print(
            '> Extracting contents of archive of results for parameters "{}"'
            .format(criteria)
        )

        downloaded_dir = self.extract_zip_contents(full_destination)

        if downloaded_dir is not None:
            print(
                '> Results for parameters "{}" stored in /downloads/{}/'
                .format(criteria, downloaded_dir)
            )

            self.relative_download_dirs.append(
                downloaded_dir
            )

        os.remove(full_destination)

    def get_download_url(self, criteria):
        """
        Creates the download url for the .zip archive from
        the given criteria.
        """
        prepended_url_part = 'https://clinicaltrials.gov/ct2/results/' +\
                             'download?down_flds=shown&down_fmt=plain&term='
        appended_url_part = '&show_down=Y&down_typ=results&down_stds=all'
        return prepended_url_part + criteria + appended_url_part

    def download_file(self, url, destination):
        """
        Downloads and saves a .zip archive file from the
        given url to the given destination.
        """
        download_stream = requests.get(url, stream=True)

        try:
            with open(destination, 'wb') as f:
                for chunk in download_stream.iter_content(chunk_size=1024):
                    if chunk:
                        f.write(chunk)
        except IOError:
            raise IOError('Could not write downloaded trials to disk.')

    def extract_zip_contents(self, path):
        """
        Extracts the contents of the .zip archive at the
        given location to a folder named accordingly in the
        /downloads/ folder.
        """
        results_not_found = False
        try:
            with open(path, 'rb') as saved_zip:
                DESTINATION_DIR = path.replace('.zip', '')
                self.make_sure_path_exists(DESTINATION_DIR)

                try:
                    zf = zipfile.ZipFile(saved_zip)
                    zf.extractall(DESTINATION_DIR)
                except zipfile.BadZipFile:
                    # os.remove(path)
                    # os.
                    results_not_found = True
                    print("""
                        It appears as if there are no results for {}.
                        Cleaning up the folder set aside for the results...
                        """.format(DESTINATION_DIR.split('/')[-1]))
                    shutil.rmtree(DESTINATION_DIR)
                    return None

                return os.path.basename(DESTINATION_DIR)
        except IOError:
            raise IOError(
                'Could not extract files from .zip trials archive.'
            )

    def make_sure_path_exists(self, path):
        """
        Create directory from path if it doesn't exist.
        Credit to 'Heikki Toivonon' and 'Bengt' on
        StackOverflow.
        http://stackoverflow.com/questions/273192/in-python-check-if-a-directory-exists-and-create-it-if-necessary
        """
        try:
            os.makedirs(path)
        except OSError as exception:
            if exception.errno != errno.EEXIST:
                raise
