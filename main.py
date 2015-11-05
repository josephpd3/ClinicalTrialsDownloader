"""
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

EXTRACT_PATH = BASE_PATH + '/extracted/'

DOWNLOAD_PATH = BASE_PATH + '/downloads/'


class Main(object):
    """
    Encapsulated main execution script.
    """
    terms = None

    def __init__(self, argv):
        """
        Parse command line/terminal parameters and run accordingly.
        """
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
                self.terms = option[1]

        self.download_research()
        self.extract_research()

    def download_research(self):
        """
        Creates an instance of TrialsDownloader class
        and downloads trial records relevant to
        specified criteria.
        """
        rd = TrialsDownloader(terms=self.terms)
        try:
            rd.make_sure_path_exists(EXTRACT_PATH.strip('/'))
        except OSError:
            raise OSError(
                """
                Could not write dataframe to file.
                Are the permissions for /extracted/ set
                properly for file writing?
                """
            )

    def extract_research(self):
        """
        Extracts trial records from XML files and
        exports it to Dataframes which are concatenated
        into one large dataframe and then saved as
        pickle (.pkl) files, which is probably
        the neatest way to store DataFrames.
        """
        xtdf = XMLToDataFrame()

        print('> Collecting extracted XML files...')

        research_directories = [DOWNLOAD_PATH + d for d
                                in os.listdir(DOWNLOAD_PATH)
                                if os.path.isdir(DOWNLOAD_PATH + d)]

        for rdir in research_directories:
            rdir_full_path = rdir
            dir_name = rdir.split('/')[-1]
            files = self.get_xml_file_list(rdir)

            print('> Creating DataFrames for {}'.format(dir_name))

            dataframes = []

            for f in files:
                xtdf.parse_xml_file(f)

                df = xtdf.to_dataframe()
                dataframes.append(df)

            combined_dataframe = pd.concat(dataframes)

            try:
                combined_dataframe.to_pickle(
                    EXTRACT_PATH + dir_name + '.pkl'
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
                shutil.rmtree(rdir_full_path)

        print('> Dataframes saved!')

    def get_xml_file_list(self, dir_name):
        """
        Get paths to xml files given a
        containing directory.
        """
        xml_files = []

        xml_pat = re.compile('\.xml$')

        files = [dir_name + '/' + xf
                 for xf
                 in os.listdir(dir_name)
                 if xml_pat.search(xf) is not None]
        xml_files.extend(files)

        return xml_files


if __name__ == '__main__':
    main = Main(sys.argv[1:])
