[![Current Version on
PyPI](https://img.shields.io/pypi/v/movie-file-fixer?style=for-the-badge&logo=pypi&label=Version)](https://pypi.org/project/movie-file-fixer/)
[![PyPI Format](https://img.shields.io/pypi/format/movie-file-fixer?style=for-the-badge&logo=pypi&label=Format)](https://pypi.org/project/movie-file-fixer/)
[![PyPI Status](https://img.shields.io/pypi/status/movie-file-fixer?style=for-the-badge&logo=pypi&label=Status)](https://pypi.org/project/movie-file-fixer/)
[![Supported Python
Versions](https://img.shields.io/pypi/pyversions/movie-file-fixer?style=for-the-badge&logo=pypi)](https://pypi.org/project/movie-file-fixer/)
[![GitHub Build](https://img.shields.io/github/workflow/status/blairg23/movie-file-fixer/Build%20/%20Deploy?style=for-the-badge)](https://github.com/blairg23/movie-file-fixer/actions/workflows/deploy.yml)
[![Coverage](https://img.shields.io/coveralls/github/blairg23/movie-file-fixer?style=for-the-badge&logo=coverage)](https://coveralls.io/github/blairg23/movie-file-fixer)
[![License](https://img.shields.io/pypi/l/movie-file-fixer?style=for-the-badge&logo=pypi)](https://github.com/blairg23/movie-file-fixer)
[![Code style:
black](https://img.shields.io/badge/code%20style-black-000000.svg?style=for-the-badge&logo=black)](https://github.com/psf/black)
[![GitHub Last Commit](https://img.shields.io/github/last-commit/blairg23/movie-file-fixer?style=for-the-badge&logo=github)](https://github.com/blairg23/movie-file-fixer/commits/)

# movie-file-fixer

Given a directory of poorly formatted movie files, `movie-file-fixer` will create a beautifully formatted directory of films folders, complete with posters, subtitles, and IMDb metadata.

## Algorithm
Given a directory string,
1. `folderize()` - Prepare the directory space.
    
    - Place all single files (except `contents.json` and `errors.json`) into folders using the file name. - [`Folderizer`]
    
    - Pull all subtitle files out of `subs` folders if they exist.
2. `cleanup()` - Folder cleanup.
    
    - Remove non-movie files, based on a list of "bad" extensions (i.e., .nfo, .txt, etc.) - [`FileRemover`]
3. `format()` - Format folders, movie files, and relevant metafiles based on IMDb movie titles.
    
    - Rename the movie file and folder (i.e., `<movie_title> [<year_of_release>]`) - [`Formatter`]
    
    - Create a `contents.json` file to store the metadata, including poster URLs.
    
    - Create an `errors.json` file to contain any files or folders that had issues being formatted.
4. `get_posters()` - Download the movie poster and name the file `poster.<extension>` (where `<extension>` is the original extension of the poster file) - [`PosterFinder`]
5. `get_subtitles()` - Download the subtitles using SubDb (http://thesubdb.com/) and an md5 hash of the movie file and name the file `<movie_title> [<year_of_release>].srt` - [`SubtitleFinder`]

