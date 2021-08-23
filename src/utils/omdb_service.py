import os
import omdb

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

class OmdbService:
    def __init__(self, omdb_api_key=None, verbose=False):
        self._verbose = verbose
        self._action_counter = 0

        omdb_api_key = omdb_api_key or OMDB_API_KEY
        if omdb_api_key:
            self._omdb_api = omdb.Api(apikey=omdb_api_key)
        else:
            raise Exception("Missing OMDB_API_KEY environment variable.")

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

        response = {
            "Response": "False"
        }
    
        omdb_response = self._omdb_api.omdb_api.search(
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
            response = json_response

            if response.get("Response") == "True":
                if self._verbose:
                    total_results = json_response.get("totalResults", 1)
                    title_text = "TITLES" if int(total_results) > 1 else "TITLE"

                    print(
                        f"[FOUND {total_results} {title_text}]\n{json.dumps(json_response, indent=4)}\n"
                    )
            else:
                if self._verbose:
                    print(
                        f'[DID NOT FIND] [TITLE] using [SEARCH CRITERIA] "{search_terms}"\n'
                        f'[DID NOT FIND] [TITLE] using [IMDB ID] "{imdb_id}"\n'
                        f'[DID NOT FIND] [TITLE] using [TITLE] "{title}"\n'
                    )

        return response

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

    def _fuzzy_search(
        self,
        search_query,
        search_key,
        search_list,
        result_key="imdbID",
        result_type=None,
    ):
        """

        :param str search_query: Query phrase to search by.
        :param str search_key: The object key to check fuzziness with.
        :param list search_list: List of IMDb objects to check the fuzziness of the `search_query` against.
        :param str result_key: The object key to use as the result value (usually the `imdbID`).
        :param str result_type: Type of result to return. [optional]. Valid Options: [`movie`, `series`, `episode`]
        :return tuple: A tuple containing the value found at the `result_key` of the object that best matches the given search criteria and the fuzziness score.

        Performs a fuzzy search over the given list of IMDb objects to find and return the best match as an IMDb object.
        """
        if self._verbose:
            print(
                f'[{self._action_counter}] [PERFORMING FUZZY SEARCH] on [SEARCH QUERY] "{search_query}" using [SEARCH KEY] "{search_key}" and returning the [RESULT KEY] "{result_key}"\n'
            )
            self._action_counter += 1

        result_values = {}
        for search_item in search_list:
            # Make sure our candidates are actually the type we want to search on (or that `result_type` wasn't provided)
            # Also ensure it has a poster (missing poster is a sure sign of a bad result):
            if (
                result_type is None or search_item.get("Type") == result_type
            ) and search_item.get("Poster") != "N/A":
                title = search_item.get(search_key)
                result_value = search_item.get(result_key)
                result_values[title] = result_value

        titles = result_values.keys()
        fuzziness_ratios_list = fuzzywuzzy_process.extract(search_query, titles)
        if self._verbose:
            print(
                f"[FOUND] Each title, ordered by fuzziness ratio: {fuzziness_ratios_list}\n"
            )

        fuzziest_title = fuzzywuzzy_process.extractOne(search_query, titles)
        if self._verbose:
            print(f'[FOUND] The fuzziest title: "{fuzziest_title}"\n')

        fuzzy_title, fuzzy_score = fuzziest_title

        final_result_value = result_values.get(fuzzy_title)

        if self._verbose:
            print(f'[FOUND] [RESULT KEY] ({result_key}) "{final_result_value}"')

        return final_result_value, fuzzy_score
        
    def get_imdb_object(
        self, search_query, imdb_id=None, release_year=None, result_type=None
    ):
        """

        :param str search_query: Query phrase to search by.
        :param str imdb_id: IMDb ID to search by.
        :param str release_year: Optional release year to make the search more specific.
        :param str result_type: What type of IMDb object you want returned. Valid Options: [`movie`, `series`, `episode`]
        :return json: An OMDb API response containing the most probable IMDb object that matches the search criteria.

        Recursively searches OMDb API for a list of IMDb objects closest to the given `title_candidate` and `release_year` and uses
        Fuzzy Searching to find the best possible match from the list of results.
        """

        # If the IMDb ID is provided, use it! It will be the most accurate result (assuming OMDb API doesn't fail)
        if imdb_id is not None:
            if self._verbose:
                print(
                    f'[{self._action_counter}] [FINDING IMDB OBJECT] from [IMDB ID] "{imdb_id}"\n'
                )
                self._action_counter += 1

            # And finally, return the IMDb object:
            if self._verbose:
                print(f"[FOUND] IMDb object with [IMDB ID] {imdb_id}\n")

            return self.search_by_imdb_id(imdb_id=imdb_id)
        else:
            if self._verbose:
                print(
                    f'[{self._action_counter}] [FINDING IMDB OBJECT] from [SEARCH QUERY] "{search_query}"\n'
                )
                self._action_counter += 1

            result_candidates = []
            original_search_query = search_query
            first_known_valid_search_query = None
            last_known_valid_search_query = None

            while search_query:
                if self._verbose:
                    print(f'[GETTING RESULTS] for [SEARCH QUERY] "{search_query}"\n')
                # Try searching by `title` first, as it has the most accurate results (besides searching by IMDb ID)
                search_by_title_response = self.search_by_title(
                    title=search_query, release_year=release_year
                )
                # If we found the title by searching by title, let's add it to our candidates list:
                if search_by_title_response.get("Response") == "True":
                    # Keep a breadcrumb of the first `search_query` that got results:
                    if last_known_valid_search_query is None:
                        first_known_valid_search_query = search_query

                    # Keep a breadcrumb of the last `search_query` that got results
                    last_known_valid_search_query = search_query
                    result_candidates.append(search_by_title_response)

                # Now let's search by `search_terms` to get a larger candidate population to choose from:
                search_by_search_terms_response = self.search_by_search_terms(
                    search_terms=search_query, release_year=release_year
                )
                # If that is successful,
                if search_by_search_terms_response.get("Response") == "True":
                    # Keep a breadcrumb of the first `search_query` that got results:
                    if last_known_valid_search_query is None:
                        first_known_valid_search_query = search_query

                    # Keep a breadcrumb of the last `search_query` that got results
                    last_known_valid_search_query = search_query
                    # then get all the objects from the search results:
                    search_results = search_by_search_terms_response.get("Search", [])
                    # Then add them all to the result candidates:
                    for search_result in search_results:
                        result_candidates.append(search_result)
                # If it was not successful, the search phrase might be malformed.
                # Or the title is just a substring. Either way, let's drop one of the words from the end
                # and try again!
                # Remove the last word from the title (usually it's a junk word that didn't get trimmed previously)
                search_query = " ".join(search_query.split()[:-1])

        # If there are any result candidates, do a Fuzzy Search over them to find the most probably IMDb object to return:
        fuzzy_scores = {}
        imdb_id_candidates = {}
        # The best `search_query` candidate will be either the original search query, the first valid one, or the last valid one:
        search_query_candidates = [
            original_search_query,
            first_known_valid_search_query,
            last_known_valid_search_query,
        ]
        if self._verbose:
            print(f"[FOUND] [SEARCH QUERY CANDIDATES]\n")
            print(f'[ORIGINAL SEARCH QUERY]: "{original_search_query}"\n')
            print(
                f'[FIRST KNOWN VALID SEARCH QUERY]: "{first_known_valid_search_query}"\n'
            )
            print(
                f'[LAST KNOWN VALID SEARCH QUERY]: "{last_known_valid_search_query}"\n'
            )
        if result_candidates:
            for search_query_candidate in search_query_candidates:
                if search_query_candidate is not None:
                    candidate_imdb_id, fuzzy_score = self._fuzzy_search(
                        search_query=search_query_candidate,
                        search_key="Title",
                        search_list=result_candidates,
                        result_key="imdbID",
                        result_type=result_type,
                    )
                    if fuzzy_score not in fuzzy_scores:
                        fuzzy_scores[fuzzy_score] = []
                    fuzzy_scores[fuzzy_score].append(candidate_imdb_id)
                    imdb_id_candidates[search_query_candidate] = candidate_imdb_id
            max_fuzzy_score = max(fuzzy_scores.keys())
            imdb_ids = fuzzy_scores[max_fuzzy_score]

            if self._verbose:
                print(
                    f'[MAX FUZZY SCORE] "{max_fuzzy_score}" with [IMDB IDS] "{imdb_ids}"\n'
                )

            # If both search queries have the same fuzziness score,
            if len(imdb_ids) > 1:
                # Then the first valid query wins.
                imdb_id = imdb_id_candidates[first_known_valid_search_query]
            else:
                imdb_id = imdb_ids[0]

            if self._verbose:
                print(f'[FOUND BEST MATCH] [IMDB ID] "{imdb_id}"')

            return self.get_imdb_object(search_query="", imdb_id=imdb_id)