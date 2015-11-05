import pandas
import json
import xml.etree.ElementTree as etree


XML_REF_LIST = [
    'required_header',
    'id_info',
    'brief_title',
    'sponsors',
    'source',
    'oversight_info',
    'brief_summary',
    'detailed_description',
    'overall_status',
    'start_date',
    'completion_date',
    'phase',
    'study_type',
    'study_design',
    'condition',
    'intervention',
    'eligibility',
    'reference',
    'verification_date',
    'lastchanged_date',
    'firstreceived_date',
    'has_expanded_access',
    'condition_browse',
    'intervention_browse',
    'official_title',
    'primary_completion_date',
    'enrollment',
    'overall_official',
    'location',
    'location_countries',
    'results_reference',
    'keyword',
    'why_stopped',
    'primary_outcome',
    'secondary_outcome',
    'number_of_arms',
    'removed_countries',
    'responsible_party',
    'is_fda_regulated',
    'arm_group',
    'is_section_801',
    'overall_contact',
    'number_of_groups',
    'link',
    'firstreceived_results_date',
    'clinical_results',
    'other_outcome',
    'biospec_retention',
    'biospec_descr',
    'acronym',
    'overall_contact_backup',
    'target_duration'
]


class XMLToDataFrame(object):
    """
    Middleman class for converting XML files to
    Pandas DataFrames.

    Once initialized, store the contents of an XML file in this
    class with XMLToDataFrame.parse_xml_file().

    After the contents are stored, export them with one of
    three options:

    - DataFrame with nested Python Native Dictionaries

    - DataFrame with nested JSON string objects

    - DataFrame with nested DataFrames

    """
    tree_dict = {}

    def __init__(self):
        pass

    def parse_xml_file(self, path):
        """
        For every tag in the reference list, searches
        the XML file--whose respective path was passed
        in--and creates an item for that path in the
        reference dictionary internal to this class.
        """
        tree = etree.parse(path)
        root = tree.getroot()

        for item in XML_REF_LIST:
            self.tree_dict[item] = None
            tags = root.findall(item)

            num_tags = len(tags)

            if not num_tags:
                continue
            elif num_tags is 1:
                returned_dict = self.parse_singleton_tag(tags[0])
                self.tree_dict[item] = returned_dict[item]
            else:
                returned_list = self.parse_multiple_tags(tags)
                self.tree_dict[item] = returned_list

    def to_nested_dicts(self):
        """
        Returns the internal reference tree as a
        dataframe with nested python dictionaries.
        """
        pass

    def to_nested_json(self):
        """
        Returns the internal reference tree as a
        dataframe with nested json string objects.
        """
        pass

    def to_nested_dataframes(self):
        """
        Returns the internal reference tree as a
        dataframe with nested dataframes.
        """
        pass

    def parse_singleton_tag(self, tag):
        """
        Recursively parses a single tag instance,
        returning a dictionary containing all of
        its children parsed into dictionaries.
        """
        if len(tag) is 0:
            return {tag.tag: tag.text}
        else:
            tag_dict = {tag.tag: {}}
            for child in tag:
                child_dict = self.parse_singleton_tag(child)
                tag_dict[tag.tag][child.tag] = child_dict[child.tag]
            return tag_dict

    def parse_multiple_tags(self, tags):
        """
        Cycles through a list of identical tags,
        passing them to XMLToDataFrame.parse_singleton_tag()
        and appending the returned dictionary to a list,
        which is then returned upon completion.
        """
        tag_group = []
        for tag in tags:
            tag_dict = self.parse_singleton_tag(tag)
            tag_group.append(tag_dict[tag.tag])
        return tag_group
