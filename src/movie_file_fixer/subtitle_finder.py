# -*- coding: utf-8 -*-
"""

Description: Reads the "metadata.json" file and downloads the subtitle for each title, given a language of preference.
"""

import hashlib
import json
import os

import requests


class SubtitleFinder:
    def __init__(
        self,
        directory=None,
        metadata_filename="metadata.json",
        language="en",
        verbose=False,
    ):
        self._directory = directory
        self._metadata_filename = metadata_filename
        self._language = language
        self._verbose = verbose
        self._action_counter = 0

        if self._verbose:
            print("[CURRENT ACTION: LOCATING MOVIE SUBTITLES]\n")

    def _is_movie_file(self, filename):
        """
        
        :param filename: The filename to assess. 
        :return bool: Whether the given filename is a movie file or not.

        This method returns True if the given filename is a movie file and False if not.
        """
        movie_file_extensions = [".avi", ".mp4", ".mkv", ".mov"]
        filename, extension = os.path.splitext(filename)
        if extension in movie_file_extensions:
            return True
        else:
            return False

    def _get_hash(self, filepath):
        """
        
        :param filepath: The path to the file to be hashed.
        :return str: The `md5` hash of the file at the given filepath.

        This hash function receives the name of the file and returns the hash code.
        """
        readsize = 64 * 1024
        with open(filepath, "rb") as f:
            size = os.path.getsize(filepath)
            data = f.read(readsize)
            f.seek(-readsize, os.SEEK_END)
            data += f.read(readsize)

        return hashlib.md5(data).hexdigest()

    def _download(
        self, url="http://api.thesubdb.com/", payload=None, headers=None
    ):
        """

        :param str url: The SubDb API URL.
        :param dict headers: A dictionary containing custom headers. Default only contains the `User-Agent`.
        :return requests.Response: A `requests.Response` object containing the file being requested.

        This method performs a GET request on the given URL, using the given payload and headers (if desired).
        """
        if headers is None:
            headers = {
                "User-Agent": "SubDB/1.0 (Windows; U; Windows NT 5.1; it; rv:1.8.1.11) Gecko/20071127 Firefox/2.0.0.11; https://github.com/blairg23/movie-file-fixer"
            }
        return requests.get(url=url, params=payload, headers=headers)
        # if response.status_code == 200:
        #     print("[REQUESTING FROM URL] {url}\n".format(url=response.url))
        #     response = response.text
        # else:
        #     print(
        #         "[ERROR] {url} failed with status code {status_code}\n".format(
        #             url=response.url, status_code=response.status_code
        #         )
        #     )

    def _search_subtitles(self, hashcode=None):
        """

        :param str hashcode: The `md5` hash of the file to use to search for available subtitles.
        :return str: A comma-separated list of available languages (two character language code).
        """
        payload = {"action": "search", "hash": hashcode}
        response = self._download(payload=payload)

        return response

    def _download_subtitles(self, language="en", hashcode=None):
        """

        :param str language: The language of the subtitle to download (as a two character language code, i.e., 'en' for English).
        :param str hashcode: The `md5` hash of the file to download the subtitle for.
        :return file: An `.srt` file containing the subtitle for the given file, named `<hashcode>.srt`.
        """
        payload = {"action": "download", "hash": hashcode, "language": language}
        response = self._download(payload=payload)

        return response

    def download_subtitles(self, directory=None, metadata_filename=None, language="en"):
        full_filepath = os.path.join(directory, metadata_filename)
        if os.path.exists(full_filepath):
            if self._verbose:
                print("[PROCESSING FILE: {full_filepath}]\n".format(full_filepath=full_filepath))

            # Open file for reading:
            with open(full_filepath, mode="r", encoding="UTF-8") as infile:
                # Load existing data into titles index list:
                titles_index = json.load(infile)

            for title in titles_index["titles"]:
                title_path = os.path.join(directory, title["title"])
                if os.path.exists(title_path):
                    file_path = None
                    for filename in os.listdir(title_path):
                        if self._is_movie_file(filename=filename):
                            file_path = os.path.join(title_path, filename)

                    if file_path is not None:
                        print(
                            "[PROCESSING TITLE: {title}]\n".format(
                                title=str(title["title"])
                            )
                        )

                        try:
                            hashcode = self._get_hash(filepath=file_path)
                        except Exception as e:
                            print("[ERROR] File is Corrupt or Missing.")
                            print(e)
                            print("\n")

                        subtitle_path = os.path.join(
                            directory,
                            title["title"],
                            "{language}_subtitles.srt".format(language=language),
                        )
                        if not os.path.exists(subtitle_path):
                            subtitles_available = self._search_subtitles(
                                hashcode=hashcode
                            )
                            if (
                                subtitles_available not in ["", None, " "]
                                and language in subtitles_available
                            ):
                                if self._verbose:
                                    print(
                                        f"[ADDING SUBTITLE FILE: {language}_subtitles.srt]\n"
                                    )

                                try:
                                    subtitles = self._download_subtitles(
                                        language=language, hashcode=hashcode
                                    )
                                    print("[DOWNLOAD COMPLETE]\n")
                                    print(
                                        "[WRITING FILE] -> {filepath}...\n".format(
                                            filepath=subtitle_path
                                        )
                                    )
                                    with open(
                                        subtitle_path, "w+", encoding="UTF-8"
                                    ) as outfile:
                                        outfile.writelines(subtitles)
                                except Exception as e:
                                    print(e)
                            else:
                                print(
                                    "[ERROR] No Subtitles Available for that language ({language}).\n".format(
                                        language=language
                                    )
                                )
                        else:
                            print("Subtitle already exists. Skipping...")
                    else:
                        print("[ERROR] No movie file exists.\n")

                    print("------------------------------------------------")
            print("[COMPLETE]")
