"""
Author: Joseph P DeBartola III

Usage: main.py
Usage with arguments: main.py --explicit-terms=<terms>
( For details on formatting terms in argument, see README.md)

This script contains the main script for ct-research-downloader.
Run this one.

This utilizes the classes TrialsDownloader and XMLToDataFrame
to gather data from clinicaltrials.gov, compile it into
Pandas DataFrames from XML files, and export it into the
adjacent /extracted/ directory in pickle file (.pkl) form.
"""

from TrialsDownloader import TrialsDownloader
from XMLToDataFrame import XMLToDataFrame

import os
import re
import sys
import getopt
import pandas as pd
import shutil


OPTION_LIST = [
    'explicit-terms='
]

BASE_PATH = os.path.dirname(
    os.path.abspath(__file__)
)

EXTRACT_PATH = os.path.join(BASE_PATH, 'extracted')

DOWNLOAD_PATH = os.path.join(BASE_PATH, 'downloads')


def main(argv):
    """
    Encapsulating main execution script.
    """
    search_terms = parse_args(argv)
    download_dirs = download_research(search_terms)
    extract_research(download_dirs)


def parse_args(argv):
    """
    Parse command line/terminal parameters.

    Returns search terms for downloading results.
    """
    terms = None
    try:
        opts, args = getopt.getopt(argv, '', OPTION_LIST)
    except getopt.GetoptError:
        raise getopt.GetoptError(
            '> Command Line options available are as follows:\n\n' +
            '\t--explicit-terms=multi+word+term_term\n\t\t' +
            'Explicitly define terms as opposed to using params.txt.'
        )

    for option in opts:
        if option[0] == '--explicit-terms':
            terms = option[1]

    return terms


def download_research(terms):
    """
    Creates an instance of TrialsDownloader class
    and downloads trial records relevant to
    specified criteria.

    Returns relative folder names containing downloaded XML files
    """
    trials_downloader = TrialsDownloader(terms=terms)
    try:
        trials_downloader.make_sure_path_exists(EXTRACT_PATH)
    except OSError:
        raise OSError(
            """
            Could not write dataframe to file.
            Are the permissions for /extracted/ set
            properly for file writing?
            """
        )
    return trials_downloader.relative_download_dirs


def extract_research(relative_dirs):
    """
    Extracts trial records from XML files and
    exports it to Dataframes which are concatenated
    into one large dataframe and then saved as
    pickle (.pkl) files, which is probably
    the neatest way to store DataFrames.
    """
    xtdf = XMLToDataFrame()
    df_saved = False

    research_directories = [os.path.join(DOWNLOAD_PATH, d)
                            for d in relative_dirs]

    for rdir in research_directories:
        rdir_full_path = rdir
        dir_name = os.path.basename(rdir)

        print('> Collecting extracted XML files...')

        files = get_xml_file_list(rdir)

        print('> Creating DataFrames for {}'.format(dir_name))

        dataframes = []

        for f in files:
            xtdf.parse_xml_file(f)

            df = xtdf.to_dataframe()
            dataframes.append(df)

        combined_dataframe = pd.concat(dataframes)

        try:
            pickle_name = dir_name + '.pkl'
            combined_dataframe.to_pickle(
                os.path.join(EXTRACT_PATH, pickle_name)
            )
        except Exception:
            raise IOError(
                """
                Could not write dataframe to file.
                Are the permissions for /extracted/ set
                properly for file writing?
                """
            )
        else:
            df_saved = True
            shutil.rmtree(rdir_full_path)

    print('> Clearing out downloads folder...')

    if df_saved:
        print('> Dataframes saved!')


def get_xml_file_list(dir_name):
    """
    Get paths to xml files given a
    containing directory.
    """
    xml_files = []

    xml_pat = re.compile('\.xml$')

    files = [os.path.join(dir_name, xf)
             for xf
             in os.listdir(dir_name)
             if xml_pat.search(xf) is not None]
    xml_files.extend(files)

    return xml_files


if __name__ == '__main__':
    main(sys.argv[1:])
