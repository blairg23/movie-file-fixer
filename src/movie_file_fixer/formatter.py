# -*- coding: utf-8 -*-
"""

Description: Formats all the files and folders in a given directory based on their movie title
and creates a title metadata file called "metadata.json", which also contains poster information.
"""

import json
import os
import re

import omdb
from fuzzywuzzy import process as fuzzywuzzy_process

from utils import OmdbService


class Formatter:
    def __init__(
        self,
        directory=None,
        metadata_filename="metadata.json",
        result_type=None,
        verbose=False,
    ):
        self._directory = directory
        self._metadata_filename = metadata_filename
        self._result_type = result_type
        self._verbose = verbose
        self._action_counter = 0

        self._omdb_service = OmdbService(verbose=self._verbose)

        if self._verbose:
            print("[CURRENT ACTION: FORMATTING MOVIE TITLES]\n")

    def initialize_metadata_file(self, directory=None, metadata_filename=None):
        """

        :param str directory: The directory to locate or create data files.
        :param str metadata_filename: The metadata filename.
        :return dict: The metadata.

        Initialize some JSON files for containing formatting metadata and error logs.
        """
        if directory is None:
            directory = self._directory

        if metadata_filename is None:
            metadata_filename = self._metadata_filename

        if self._verbose:
            print(
                f'[{self._action_counter}] [INITIALIZING METADATA FILE] "{metadata_filename}"\n'
            )
            self._action_counter += 1

        # If we couldn't find a metadata file containing the table of contents, create a new one:
        if not os.path.exists(os.path.join(directory, metadata_filename)):
            metadata = {"titles": [], "metadata": [], "errors": []}

            if self._verbose:
                print(
                    f'[INITIALIZED] [NEW] [FILE] "{metadata_filename}" with [METADATA] "{metadata}"\n'
                )

            with open(os.path.join(directory, metadata_filename), mode="w") as outfile:
                json.dump(metadata, outfile, indent=4)
        else:  # However, if it does exist,
            # Let's keep track of the files we've already indexed, so we don't duplicate our work:
            if self._verbose:
                print(f'[LOADED] [EXISTING] [FILE] "{metadata_filename}"\n')

            with open(
                os.path.join(directory, metadata_filename), encoding="UTF-8"
            ) as infile:
                metadata = json.load(infile)

        return metadata

    def _strip_punctuation(self, phrase):
        """

        :param str phrase: The phrase to strip punctuation from.
        :return str: The original phrase, stripped of punctuation.

        Strips the given phrase of random punctuation that can confuse the search method.
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [STRIPPING PUNCTUATION CHARACTERS] from [PHRASE] "{phrase}"\n'
            )
            self._action_counter += 1

        # Strip the phrase of any punctuation that isn't $, #, or !:
        phrase_without_punctuation = re.sub(
            r"[^\$#!\* | ^\w\d'\s]+", " ", phrase
        ).replace("_", " ")

        # Strip whitespace on left and right side:
        stripped_phrase_without_punctuation = phrase_without_punctuation.strip()

        # Strip any duplicate whitespace in the middle by splitting, then rejoining on single spaces:
        stripped_phrase_without_punctuation_or_duplicate_whitespace = " ".join(
            stripped_phrase_without_punctuation.split()
        )

        # Finally, return the lower-cased, stripped, and deduped phrase:
        final_phrase = (
            stripped_phrase_without_punctuation_or_duplicate_whitespace.lower()
        )

        if self._verbose:
            print(f'[PHRASE] is now "{final_phrase}"\n')

        return final_phrase

    def _get_release_year(self, search_terms):
        """

        :param str search_terms: The search terms to find a release year in.
        :return str: The best candidate for the release year of the given title.

        Returns the best candidate for the release year for the given title by removing the improbable candidates.
        """
        release_year = None
        found = False

        if self._verbose:
            print(
                f'[{self._action_counter}] [FINDING RELEASE YEAR] in [SEARCH TERMS] "{search_terms}"\n'
            )
            self._action_counter += 1

        year_candidate_list = re.findall(
            r"\d{4}", search_terms
        )  # Find all possible "release year" candidates

        if len(year_candidate_list) > 0:  # If we found any results:
            if self._verbose:
                print(
                    f'[FOUND] {len(year_candidate_list)} [RELEASE YEAR CANDIDATES] "{year_candidate_list}"]\n'
                )

            for year in year_candidate_list:
                # Typically, we don't deal with movies before the 1900's
                # and this script will be future proof until the 2100's!
                if not 1900 < int(year) < 2100:
                    # If we found an invalid year candidate, remove it:
                    year_candidate_list.remove(str(year))

            # Make sure there is still at least one candidate
            if len(year_candidate_list) > 0:
                # Add only the last one as that is the most likely candidate of a real candidate (files don't typically start with the release year)
                release_year = year_candidate_list[
                    -1
                ]  # This will also be the only candidate if there is only one candidate.

                found = True

                if self._verbose:
                    print(f'[FOUND] [RELEASE YEAR] "{release_year}"\n')
        else:
            found = False

        if not found:
            if self._verbose:
                print("[DID NOT FIND] [RELEASE YEAR]\n")

        return release_year

    def _get_clean_title_candidate_and_release_year(self, search_terms):
        """

        :param str search_terms: The search terms to find the `title` and `release_year` in.
        :return tuple: A tuple containing the subset of the `search_terms` which contains the title and the `release_year` extracted from the `search_terms`.

        Given unformatted search terms, returns a title without punctuation and the release year.
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [FINDING CLEAN TITLE CANDIDATE] and [RELEASE YEAR] from [SEARCH TERMS] "{search_terms}"\n'
            )
            self._action_counter += 1

        # Prepare the title by stripping the punctuation:
        stripped_search_terms = self._strip_punctuation(phrase=search_terms)
        stripped_search_terms_list = stripped_search_terms.split(" ")
        release_year = self._get_release_year(search_terms=stripped_search_terms)
        if release_year is not None:
            release_year_index = stripped_search_terms_list.index(release_year)
            # If we found the release year, we know the text BEFORE that release year is the title:
            title_words_list = stripped_search_terms_list[:release_year_index]
        else:
            # If not, then it's in this list somewhere:
            title_words_list = stripped_search_terms_list

        title = " ".join(title_words_list)

        if self._verbose:
            print(
                f'[FOUND] [CLEAN TITLE CANDIDATE] "{title}" and [RELEASE YEAR] "{release_year}"\n'
            )

        return title, release_year

    def _strip_illegal_characters(self, phrase):
        """

        :param str phrase: The phrase to strip illegal characters from.
        :return str: The original phrase, stripped of illegal characters.

        Strips the given phrase of any characters that aren't allowed in folder/file names.
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [STRIPPING ILLEGAL CHARACTERS] from [PHRASE] "{phrase}"\n'
            )
            self._action_counter += 1

        return re.sub(r'[(<>:"/\\|?*)]', "", phrase)

    def _write_metadata(
        self, new_content, content_key, directory=None, metadata_filename=None
    ):
        """

        :param str directory: The directory containing the metadata file.
        :param str metadata_filename: The metadata filename.
        :param dict new_content: New content to write to the metadata file.
        :return: None

        Append new data to an existing JSON file that represents the content metadata of the given directory.

        i.e., Movie title information or entire IMDb metadata relating to a particular title.
        """
        if directory is None:
            directory = self._directory

        if metadata_filename is None:
            metadata_filename = self._metadata_filename

        metadata_filepath = os.path.join(directory, metadata_filename)
        if not os.path.exists(metadata_filepath):
            self.initialize_metadata_file(
                directory=directory, metadata_filename=metadata_filename
            )

        if self._verbose:
            print(
                f'[{self._action_counter}] [WRITING METADATA] for [CONTENT KEY] "{content_key}" to [FILE] "{metadata_filename}"\n'
            )
            self._action_counter += 1

        # Open file for reading:
        with open(metadata_filepath, mode="rb") as infile:
            # Load existing data into titles index list:
            contents_file = json.load(infile)

        # Check that the `content_key` exists:
        if contents_file.get(content_key) is not None:
            # Open file for writing:
            with open(metadata_filepath, mode="w") as outfile:
                # Append the new data to the titles index list:
                contents_file[content_key].append(new_content)
                # Write that updated list to the existing file:
                json.dump(contents_file, outfile, indent=4)
        else:
            raise KeyError(content_key)

    def _write_all_metadata(
        self,
        imdb_object,
        original_filename,
        final_title,
        directory=None,
        metadata_filename=None,
    ):
        """

        :param dict imdb_object: An IMDb object to collect metadata from.
        :param str original_filename: The original filename of the movie title prior to being formatted.
        :param str final_title: The filename of the movie title after being formatted.
        :return: None
        """
        if directory is None:
            directory = self._directory

        if metadata_filename is None:
            metadata_filename = self._metadata_filename

        metadata_filepath = os.path.join(directory, metadata_filename)
        if not os.path.exists(metadata_filepath):
            self.initialize_metadata_file(
                directory=directory, metadata_filename=metadata_filename
            )

        if self._verbose:
            print(
                f'[{self._action_counter}] [WRITING ALL METADATA] for [TITLE] "{final_title}" to [FILE] "{metadata_filename}"\n'
            )
            self._action_counter += 1

        title_metadata = {
            "original_filename": original_filename,
            "title": final_title,
            "imdb_id": imdb_object.get("imdbID"),
            "poster": imdb_object.get("Poster"),
        }
        self._write_metadata(
            new_content=title_metadata,
            content_key="titles",
            directory=directory,
            metadata_filename=metadata_filename,
        )
        self._write_metadata(
            new_content=imdb_object,
            content_key="metadata",
            directory=directory,
            metadata_filename=metadata_filename,
        )

    def _rename_file(
        self, current_filepath, original_filename, proposed_new_filename, counter=2
    ):
        """

        :param current_filepath: The filepath containing the file to be renamed.
        :param original_filename: The original filename of the file to rename.
        :param proposed_new_filename: The proposed new filename to name the file.
        :param counter: A counter to augment the filename if the file already exists.
        :return: None
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [RENAMING] [ORIGINAL FILENAME] "{original_filename}" to [NEW FILENAME] "{proposed_new_filename}"\n'
            )
            self._action_counter += 1

        old_filepath = os.path.join(current_filepath, original_filename)
        old_filename, extension = os.path.splitext(original_filename)
        new_filename = proposed_new_filename + extension
        new_filepath = os.path.join(current_filepath, new_filename)

        # Check if the file already exists and recursively rename the file if it does:
        if os.path.exists(new_filepath):
            if self._verbose:
                print(f'[ERROR] [DUPLICATE] [FILEPATH] "{new_filepath}"')
            # In case the conflicting filename is one we've dealt with before:
            original_new_filename = proposed_new_filename.split("_")[0]
            proposed_new_filename = "_".join([original_new_filename, str(counter)])
            # and try again!
            if self._verbose:
                print(f'[RETRYING] with [FILENAME] "{proposed_new_filename}"')
            self._rename_file(
                current_filepath=current_filepath,
                original_filename=original_filename,
                proposed_new_filename=proposed_new_filename,
                counter=counter + 1,
            )
        else:
            os.rename(old_filepath, new_filepath)
            if self._verbose:
                print(
                    f'[RENAMING] from [FILEPATH] "{old_filepath}" to [FILEPATH] "{new_filepath}"\n'
                )

    def rename_folder_and_contents(self, original_name, new_name, directory=None):
        """

        :param str original_name: The original name of the folder to be renamed.
        :param str new_name: The name to use to rename the folder and its contents.
        :param str directory: The directory containing the folder to be renamed.
        :return: None
        """
        if directory is None:
            directory = self._directory

        if self._verbose:
            print(
                f'[{self._action_counter}] [RENAMING] [FOLDER NAME] "{original_name}" and [CONTENTS] to [NEW NAME] "{new_name}"\n'
            )
            self._action_counter += 1

        # Rename the folder:
        original_filepath = os.path.join(directory, original_name)
        new_filepath = os.path.join(directory, new_name)
        os.rename(src=original_filepath, dst=new_filepath)
        if self._verbose:
            print(
                f'[RENAMED] [FILEPATH] "{original_filepath}" to [FILEPATH] "{new_filepath}"\n'
            )

        # Rename the contents of the folder:
        single_files = [
            file
            for file in os.listdir(new_filepath)
            if os.path.isfile(os.path.join(new_filepath, file))
        ]
        for single_file in single_files:
            self._rename_file(
                current_filepath=new_filepath,
                original_filename=single_file,
                proposed_new_filename=new_name,
            )

    def format(self, directory=None, metadata_filename=None, result_type=None):
        """

        :param str directory: The directory containing IMDb titles to format.
        :param str metadata_filename: The metadata filename.
        :param str result_type: What type of IMDb object you want returned. Valid Options: [`movie`, `series`, `episode`]
        :return: None

        Formats every folder/filename in the given directory according to the IMDb title closest to the folder/filename.
        """
        if directory is None:
            directory = self._directory

        if metadata_filename is None:
            metadata_filename = self._metadata_filename

        if result_type is None:
            result_type = self._result_type

        if self._verbose:
            print(
                f'[{self._action_counter}] [FORMATTING FOLDERS] in [DIRECTORY] "{directory}"\n'
            )
            self._action_counter += 1

        for title in os.listdir(directory):
            if title != self._metadata_filename:
                metadata = self.initialize_metadata_file()
                if self._verbose:
                    print(f'[{self._action_counter}] [FORMATTING] [FOLDER] "{title}"\n')
                    self._action_counter += 1

                # Let's not process the metadata file or duplicate our work:
                if str(title) not in metadata_filename and title not in [
                    entry.get("title") for entry in metadata.get("titles")
                ]:
                    # Retrieve the release year to increase dependability of search query results:
                    (
                        title_candidate,
                        release_year,
                    ) = self._get_clean_title_candidate_and_release_year(
                        search_terms=title
                    )
                    try:
                        imdb_object = self._omdb_service.get_imdb_object(
                            search_query=title_candidate,
                            release_year=release_year,
                            result_type=result_type,
                        )
                        final_title = (
                            f"{imdb_object.get('Title')} [{imdb_object.get('Year')}]"
                        )
                        final_title = self._strip_illegal_characters(phrase=final_title)
                        self._write_all_metadata(
                            imdb_object=imdb_object,
                            original_filename=title,
                            final_title=final_title,
                        )
                        self.rename_folder_and_contents(
                            directory=directory,
                            original_name=title,
                            new_name=final_title,
                        )
                    except Exception as error:
                        if self._verbose:
                            print(
                                f'[ERROR] No result for [FOLDER] "{title}"\n[ERROR] {error}\n'
                            )

                        error_data = {
                            "original_filename": title,
                            "title_candidate": title_candidate,
                        }
                        self._write_metadata(
                            new_content=error_data,
                            content_key="errors",
                            directory=directory,
                            metadata_filename=metadata_filename,
                        )
