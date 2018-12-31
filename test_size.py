import os
import sys
import cv2
import csv
import json


def return_movie_file(files=None):
    movie_file_types = ['.avi', '.mkv', '.mp4', '.m4v']
    for file in files:
        for file_type in movie_file_types:
            # If the chosen file is a movie:
            if file.endswith(file_type):
                return file, True
                # print(file)
    return files, False


def return_weird_movie_file(files=None):
    weird_movie_file_types = ['.sub', '.m4v', '.divx', 'rmvb', '.AVI', '.VOB']
    weird_files = []
    for file in files:
        for file_type in weird_movie_file_types:
            if file.endswith(file_type):
                weird_files.append(file)
    if len(weird_files) > 0:
        return weird_files, True
    else:
        return weird_files, False

def get_low_resolution_files(input_directory):
    counter = 0
    results = []
    for file_folder in os.listdir(input_directory):
        try:
            current_folder = os.path.join(input_directory, file_folder)
            if os.path.isdir(current_folder):
                file_contents = os.listdir(current_folder)
                movie_file, has_movie = return_movie_file(files=file_contents)
                if not has_movie:
                    weird_movie_files, has_weird_movie_files = return_weird_movie_file(files=file_contents)
                    if has_weird_movie_files:
                        bad_files.append(weird_movie_files)
                else:
                    counter += 1
                    input_file = os.path.join(current_folder, movie_file)
                    movie_title, movie_file_extension = os.path.splitext(movie_file)
                    if verbose:
                        print('Checking {movie_title}\n'.format(movie_title=movie_title))
                    # with open(input_file) as infile:
                    # BMP file:
                    # infile.seek(18)

                    # bytes = infile.read(8)

                    # size = struct.unpack('<II', bytes)

                    # print('Image width: ' + str(size[0]))
                    # print('Image height: ' + str(size[1]))

                    video_capture = cv2.VideoCapture(input_file)

                    if video_capture.isOpened():
                        # get vcap property
                        # width = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
                        # height = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) # float

                        # or
                        width = video_capture.get(3)  # float
                        height = video_capture.get(4)  # float

                        # it gives me 0.0 :/
                        # fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
                        # print('FILENAME:', input_file)
                        # print('SIZE:{width}x{height}'.format(width=int(width), height=int(height)))
                        # print('\n')
                        # print(width)
                        # print(height)
                        if height < 1080 and width < 1920:
                            print('Found a low resolution file: {movie_title}\n'.format(movie_title=movie_title))
                            results_dict = {
                                'title': movie_file,
                                'width': width,
                                'height': height,
                                'error': '',
                                'imdb_id': imdb_id_map[movie_title]
                            }
                            results.append(results_dict)
        except Exception as e:
                # print('FILENAME:', input_file)
                print('CURRENT_FOLDER:', current_folder)
                print('MOVIE FILE:', movie_file)
                print('ERROR:', e)
                results_dict = {
                    'title': movie_file,
                    'width': '',
                    'height': '',
                    'error': str(e),
                    'imdb_id': imdb_id_map[movie_title]
                }
                
    return results

if __name__ == '__main__':
    input_directory = 'H:\\Films'
    file_type = 'json'
    filename = 'film_sizes' + '.' + file_type
    verbose = False
    

    bad_files = []

    input_content_file = os.path.join(input_directory, 'contents.json')

    with open(input_content_file, encoding="utf8") as infile:
        imdb_data = json.load(infile)

    imdb_id_map = {}
    for data in imdb_data['Titles']:
        if data['title'] not in imdb_id_map:
            if 'imdb_id' in data:
                imdb_id_map[data['title']] = data['imdb_id']
            else:
                print('IMDb data not found in contents.json file:')
                print(data)

    low_resolution_files = get_low_resolution_files(input_directory=input_directory)

    with open(filename, 'w+', newline='') as outfile:
        if file_type.lower() == 'csv':
            csv_writer = csv.writer(outfile)
            header_row = [
                'title',
                'width',
                'height',
                'error',
                'imdb_id'
            ]
            csv_writer.writerow(header_row)
            
            for low_resolution_file in low_resolution_files:
                row_to_write = [
                    low_resolution_file['title'],
                    low_resolution_file['width'],
                    low_resolution_file['height'],
                    low_resolution_file['error'],
                    low_resolution_file['imdb_id']
                ]
                csv_writer.writerow(row_to_write)
        elif file_type.lower() == 'json':
            json.dump(low_resolution_files, outfile, indent=4)