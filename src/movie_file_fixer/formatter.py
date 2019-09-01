# -*- coding: utf-8 -*-
"""

Description: Formats all the files and folders in a given directory based on their movie title
and creates a title directory called "contents.json", which also contains poster information.
"""

import json
import os
import re
import omdb

import requests


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
                f"[{self._action_counter}] [WRITING METADATA] to [FILE] {metadata_filename}\n"
            )
            self._action_counter += 1

        # Open file for reading:
        with open(os.path.join(directory, metadata_filename), mode="r") as infile:
            # Load existing data into titles index list:
            contents_file = json.load(infile)
        # Open file for writing:
        with open(os.path.join(directory, metadata_filename), mode="w") as outfile:
            # Append the new data to the titles index list:
            contents_file[content_key].append(new_content)
            # Write that updated list to the existing file:
            json.dump(contents_file, outfile, indent=4)

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

        if self._verbose:
            print(f"[FOUND RELEASE YEAR: {release_year}]\n")

        # TODO: Add functionality

        return release_year

    def _strip_illegal_characters(self, title):
        """

        :param str title: The title to strip illegal characters from.
        :return str: The original title, stripped of illegal character.

        Strips the given title of any characters that aren't allowed in folder/file names.
        """
        # TODO: Add functionality

        return title

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
                response = json_response

        return response

    def search_by_search_terms(self, search_terms):
        """

        :param str search_terms: Criteria to search by.
        :return json: An OMDb API response containing IMDb objects that match the search criteria.
        """
        release_year = self._get_release_year(search_terms=search_terms)

        return self._search(search_terms=search_terms, release_year=release_year)

    def search_by_imdb_id(self, imdb_id):
        """

        :param str imdb_id: IMDb ID to search by.
        :return json: An OMDb API response containing IMDb objects that match the search criteria.
        """
        return self._search(imdb_id=imdb_id)

    def search_by_title(self, title):
        """

        :param str title: Title to search by.
        :return json: An OMDb API response containing IMDb objects that match the search criteria.
        """
        release_year = self._get_release_year(search_terms=title)

        return self._search(title=title, release_year=release_year)

    def format(self, directory=None, metadata_filename=None):
        """

        :param str directory: The directory containing movie titles to format.
        :param str metadata_filename: The metadata filename.
        :return:

        Formats every folder/filename in the given directory according to the movie title closest to the folder/filename.
        """

        # TODO: Add functionality
        pass


if __name__ == "__main__":
    directory = r"C:\Users\Neophile\Desktop\sandboxes\python\movie-file-fixer\src\tests\test_input"
    search_terms = "a beautiful mind"
    imdb_id = "tt0268978"
    title = "a beautiful mind"
    formatter = Formatter(directory=directory, verbose=True)
    formatter.search_by_search_terms(search_terms=search_terms)
    formatter.search_by_imdb_id(imdb_id=imdb_id)
    formatter.search_by_title(title=title)
