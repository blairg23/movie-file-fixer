import omdb

OMDB_API_KEY = os.environ.get("OMDB_API_KEY")

class omdb_service:
    def __init__(self, omdb_api_key=None):
        omdb_api_key = omdb_api_key or OMDB_API_KEY
        if omdb_api_key:
            self._omdb_api = omdb.Api(apikey=omdb_api_key)
        else:
            raise Exception("Missing OMDB_API_KEY environment variable.")

    def search(
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