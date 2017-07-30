import os
import sys
import cv2


def return_movie_file(files=None):
    movie_file_types = ['.avi', '.mkv', '.mp4', '.m4v']
    for file in files:
        for file_type in movie_file_types:
            # If the chosen file is a movie:
            if file.endswith(file_type):
                return file, True
                #print(file)
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

if __name__ == '__main__':
    counter = 0
    input_directory = 'H:\\Films'
    
    bad_files = []
    
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
                #with open(input_file) as infile:
                    # BMP file:
                    # infile.seek(18)

                    # bytes = infile.read(8)

                    # size = struct.unpack('<II', bytes)

                    # print('Image width: ' + str(size[0]))
                    # print('Image height: ' + str(size[1]))

                    video_capture = cv2.VideoCapture(input_file)

                    if video_capture.isOpened():
                         # get vcap property 
                        #width = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_WIDTH)   # float
                        #height = video_capture.get(cv2.cv.CV_CAP_PROP_FRAME_HEIGHT) # float

                        # or
                        width = video_capture.get(3)  # float
                        height = video_capture.get(4) # float

                    # it gives me 0.0 :/
                    #fps = video_capture.get(cv2.cv.CV_CAP_PROP_FPS)
                        print('FILENAME:', input_file)
                        print('SIZE:{width}x{height}'.format(width=int(width), height=int(height)))
                        print('\n')
                        # print(width)
                        # print(height)
        except Exception as e:
            # print('FILENAME:', input_file)
            print('CURRENT_FOLDER:', current_folder)
            print('MOVIE FILE:', movie_file)
            print('ERROR:', e)
            sys.exit(0)
