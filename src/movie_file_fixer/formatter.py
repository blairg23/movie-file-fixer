# -*- coding: utf-8 -*-
"""

Description: Formats all the files and folders in a given directory based on their movie title
and creates a title directory called "contents.json", which also contains poster information.
"""

import json
import os
import re

from fuzzywuzzy import fuzz

import omdb


class Formatter:
    def __init__(
        self, directory=None, metadata_filename="metadata.json", verbose=False
    ):
        self._directory = directory
        self._metadata_filename = metadata_filename
        self._verbose = verbose
        self._action_counter = 0

        if self._verbose:
            print("[CURRENT ACTION: FORMATTING MOVIE TITLES]\n")

        self._metadata = self._initialize_metadata_file()

    def _initialize_metadata_file(self, directory=None, metadata_filename=None):
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

        # If we couldn't find a metadata file containing the table of contents, create a new one:
        if not os.path.exists(os.path.join(directory, metadata_filename)):
            metadata = {"Titles": [], "Metadata": [], "Errors": []}
            with open(os.path.join(directory, metadata_filename), mode="w") as outfile:
                json.dump(metadata, outfile, indent=4)
        else:  # However, if it does exist,
            # Let's keep track of the files we've already indexed, so we don't duplicate our work:
            with open(
                os.path.join(directory, metadata_filename), encoding="UTF-8"
            ) as infile:
                metadata = json.load(infile)

        return metadata

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

        if self._verbose:
            print(
                f'[{self._action_counter}] [WRITING METADATA] to [FILE] "{metadata_filename}"\n'
            )
            self._action_counter += 1

        # Open file for reading:
        with open(os.path.join(directory, metadata_filename), mode="r") as infile:
            # Load existing data into titles index list:
            contents_file = json.load(infile)

        # Check that the `content_key` exists:
        if contents_file.get(content_key) is not None:
            # Open file for writing:
            with open(os.path.join(directory, metadata_filename), mode="w") as outfile:
                # Append the new data to the titles index list:
                contents_file[content_key].append(new_content)
                # Write that updated list to the existing file:
                json.dump(contents_file, outfile, indent=4)
        else:
            raise KeyError(content_key)

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

        return re.sub(r"[^\$#! | ^\w\d'\s]+", " ", phrase).replace("_", " ").strip()

    def _get_release_year(self, search_terms):
        """

        :param str search_terms: The search terms to find a release year in.
        :return str: The best candidate for the release year of the given title.

        Returns the best candidate for the release year for the given title by removing the improbable candidates.
        """
        release_year = None

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
                    f"[FOUND {len(year_candidate_list)} RELEASE YEAR CANDIDATES: {year_candidate_list}]"
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

                if self._verbose:
                    print(f"[FOUND RELEASE YEAR: {release_year}]\n")
            else:
                if self._verbose:
                    print("[DID NOT FIND RELEASE YEAR]\n")

        return release_year

    def _search(
        self,
        search_terms=None,
        imdb_id=None,
        title=None,
        result_type=None,
        release_year=None,
        plot="full",
        page=None,
        callback=None,
        season=None,
        episode=None,
    ):
        """

        :param str search_terms: Any search phrase that might identify a possible movie title. [optional]
        :param str imdb_id: A valid IMDb ID (e.g. tt1285016). [optional]
        :param str title: Movie title to search for. [optional]
        :param str result_type: Type of result to return. [optional]. Valid Options: [`movie`, `series`, `episode`]
        :param str release_year: Year of release. [optional]
        :param str plot: Return short or full plot. Default value: short. Valid Options: [`short`, `full`]
        :param int page: Page number to return (for paginated results). [optional]
        :param str callback: JSONP callback name. [optional]
        :param int season: Season to return a `series` result for.
        :param int episode: Episode to return a `series` result for.
        :return json: An OMDb API response containing IMDb objects that match the search criteria.

        Acts as a wrapper for the `omdbpy.search()` method from `omdbpy`,
        which searches the OMDb API for a title closest to the given search parameters.

        Example use cases include searching by `search_terms`, `imdb_id`, or `title`.
        Native support for searching for television episodes by `season` and `episode`.

        Will ignore missing parameters and will prioritize parameters in the following order if all are supplied: `search_terms` > `title` > `imdb_id`

        Providing the `release_year` is important to finding the right result when duplicate titles exist for the given search criteria.
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [SEARCHING FOR TITLE] using [SEARCH CRITERIA] "{search_terms}"\n'
                f'[{self._action_counter}] [SEARCHING FOR TITLE] using [IMDB ID] "{imdb_id}"\n'
                f'[{self._action_counter}] [SEARCHING FOR TITLE] using [TITLE] "{title}"\n'
                f'[{self._action_counter}] [SEARCHING FOR TITLE] with [RELEASE YEAR] "{release_year}"\n'
            )
            self._action_counter += 1

        response = None
        omdb_api_key = os.environ.get("OMDB_API_KEY")
        omdb_api = omdb.Api(apikey=omdb_api_key)
        omdb_response = omdb_api.search(
            search_terms=search_terms,
            imdb_id=imdb_id,
            title=title,
            result_type=result_type,
            release_year=release_year,
            plot=plot,
            return_type="json",
            page=page,
            callback=callback,
            season=season,
            episode=episode,
        )

        if omdb_response.status_code == 200:
            json_response = omdb_response.json()
            if json_response.get("Response") == "True":
                response = json_response

                if self._verbose:
                    total_results = (
                        json_response.get("titleResults")
                        if json_response.get("titleResults") is not None
                        else 1
                    )
                    title_text = "TITLES" if total_results > 1 else "TITLE"

                    print(
                        f"[FOUND {total_results} {title_text}]\n{json.dumps(json_response, indent=4)}\n"
                    )

        return response

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
        old_filepath = os.path.join(current_filepath, original_filename)
        old_filename, extension = os.path.splitext(original_filename)
        new_filename = proposed_new_filename + extension
        new_filepath = os.path.join(current_filepath, new_filename)

        # Check if the file already exists and recursively rename the file if it does:
        if os.path.exists(new_filepath):
            if self._verbose:
                print(
                    f'[{self._action_counter}] [ERROR] in [FILEPATH] "{new_filepath}" exists.'
                )
                self._action_counter += 1
            # In case the conflicting filename is one we've dealt with before:
            original_new_filename = proposed_new_filename.split("_")[0]
            proposed_new_filename = "_".join([original_new_filename, str(counter)])
            # and try again!
            if self._verbose:
                print(
                    f'[{self._action_counter}] [RETRYING] with [FILENAME] "{proposed_new_filename}"'
                )
                self._action_counter += 1
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
                    f'[{self._action_counter}] [RENAMING] from [FILEPATH] "{old_filepath}" to [FILEPATH] "{new_filepath}"\n'
                )
                self._action_counter += 1

    def search_by_search_terms(self, search_terms, release_year=None):
        """

        :param str search_terms: Criteria to search by.
        :param str release_year: Optional release year to make the search more specific.
        :return json: An OMDb API response containing IMDb objects that match the search criteria.
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [SEARCHING] by [SEARCH TERMS] "{search_terms}" and [RELEASE YEAR] "{release_year}"\n'
            )
            self._action_counter += 1

        if release_year is None:
            release_year = self._get_release_year(search_terms=search_terms)

        return self._search(search_terms=search_terms, release_year=release_year)

    def search_by_imdb_id(self, imdb_id):
        """

        :param str imdb_id: IMDb ID to search by.
        :return json: An OMDb API response containing IMDb objects that match the search criteria.
        """
        if self._verbose:
            print(f'[{self._action_counter}] [SEARCHING] by [IMDB ID] "{imdb_id}"\n')
            self._action_counter += 1

        return self._search(imdb_id=imdb_id)

    def search_by_title(self, title, release_year=None):
        """

        :param str title: Title to search by.
        :param str release_year: Optional release year to make the search more specific.
        :return json: An OMDb API response containing IMDb objects that match the search criteria.
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [SEARCHING] by [TITLE] "{title}" and [RELEASE YEAR] "{release_year}"\n'
            )
            self._action_counter += 1

        if release_year is None:
            release_year = self._get_release_year(search_terms=title)

        return self._search(title=title, release_year=release_year)

    def fuzzy_search(self, search_phrase, release_year):
        """

        :param str search_phrase: Query phrase to search by.
        :param str release_year: Optional release year to make the search more specific.
        :return json: An OMDb API response containing the most probable IMDb object that matches the search criteria.

        Performs fuzzy search over the 2 primary search methods' results to find the exact match.
        """
        if release_year is None:
            release_year = self._get_release_year(search_terms=search_phrase)

        results = []

        search_response = self.search_by_search_terms(
            search_terms=search_phrase, release_year=release_year
        )

    def format(self, directory=None, metadata_filename=None):
        """

        :param str directory: The directory containing IMDb titles to format.
        :param str metadata_filename: The metadata filename.
        :return: None

        Formats every folder/filename in the given directory according to the IMDb title closest to the folder/filename.
        """

        if self._verbose:
            print(
                f'[{self._action_counter}] [FORMATTING] folders in [DIRECTORY] "{directory}"\n'
            )
            self._action_counter += 1

        for title in os.listdir(directory):
            if self._verbose:
                print(f'[{self._action_counter}] [FORMATTING] [FOLDER] "{title}"\n')
                self._action_counter += 1

            # Let's not process the metadata file or duplicate our work:
            if str(title) not in metadata_filename and title not in [
                entry.get("title") for entry in self._metadata.get("Titles")
            ]:
                # Prepare the title by stripping the punctuation:
                new_title = self._strip_punctuation(phrase=title)

                # Limit the size of the new title to a maximum of X words (reducing this number increases recursion depth)
                max_number_of_words = 9

                if len(new_title.split(" ")) > max_number_of_words:
                    new_title = " ".join(new_title.split(" ")[0:max_number_of_words])

                # Retrieve the release year to increase dependability of search query results:
                release_year = self._get_release_year(search_terms=new_title)
                if release_year is not None:
                    new_title = new_title.replace(release_year, "").strip()


if __name__ == "__main__":
    directory = r"C:\Users\Neophile\Desktop\sandboxes\python\movie-file-fixer\src\tests\test_input"
    search_terms = "a beautiful mind"
    imdb_id = "tt0268978"
    title = "a beautiful mind"
    formatter = Formatter(directory=directory, verbose=True)
    formatter.search_by_search_terms(search_terms=search_terms)
    formatter.search_by_imdb_id(imdb_id=imdb_id)
    formatter.search_by_title(title=title)
