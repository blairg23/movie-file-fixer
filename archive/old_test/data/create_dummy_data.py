# -*- coding: utf-8 -*-
'''
Name: create_dummy_data.py
Author: Blair Gemmer
Version: 20160618

Description: Creates dummy data to test results with movie_file_fixer.py
'''

import os

file_counter = 0


class CreateDummyData:
    def __init__(self, directory=None, verbose=False):
        self.verbose = verbose
        self.file_counter = 0

    def create_dummy_data(self, file_prefix='fake.file', directory='Fake_Directory', filetypes=['avi'], fileNames=['1', '2', '3', '4', '5']):

        def create_new_files(file_prefix=None, directory=None, filetypes=None):
            '''Creates files to match the given folder name and a list of file types.
            '''
            try:
                for fType in filetypes:  # For each of the file types:
                    # Create a new file name with that file prefix and file type:
                    new_file_name = '{fPrefix}.{fType}'.format(fPrefix=file_prefix, fType=fType)
                    new_file_path = "\\\\?\\" + os.path.join(os.getcwd(), directory, new_file_name)
                    if os.path.exists(new_file_path):
                        if self.verbose:
                            print('[{file_counter}] [Skipping File] \"{fileName}\" already exists in [Folder] \"{directory}\"'.format(file_counter=self.file_counter, fileName=new_file_name, directory=directory))
                        self.file_counter += 1
                    else:
                        with open(new_file_path, 'a+') as new_file:  # And create the new dummy file in that folder
                            if self.verbose:
                                print('[{file_counter}] [Writing File] \"{fileName}\" to [Folder] \"{directory}\"'.format(file_counter=self.file_counter, fileName=new_file_name, directory=directory))
                            self.file_counter += 1
            except Exception as e:
                print('[ERROR]', e)
                print('Size of Path:', len(os.path.join(os.getcwd(), new_file_path)))

        def create_inner_folders_and_files(file_prefix=None, directory=None, inner_folder_names=None, filetypes=None):
            '''Creates the inner folders from the list of folder names
            and the files to match those folder names and a list of
            file types.
            '''
            # Create a new file prefix implying we're in an inner folder:
            file_prefix = '{fPrefix}.from.folder'.format(fPrefix=file_prefix)
            try:
                for fName in inner_folder_names:  # For each of the inner folder names,
                    # Create a new file prefix for that folder name:
                    fPrefix = '{fPrefix}.{fName}'.format(fPrefix=file_prefix, fName=fName)
                    fPath = os.path.join(directory, fName)
                    if not os.path.exists(fPath):  # If the folder doesn't exist,
                        os.mkdir(fPath)  # Create it
                        # and create files based on that folder name and list of file types:
                        create_new_files(file_prefix=fPrefix, directory=fPath, filetypes=filetypes)
                    else:  # If the folder does exist,
                        # and create files based on the current folder name and list of file types:
                        create_new_files(file_prefix=fPrefix, directory=fPath, filetypes=filetypes)
            except Exception as e:
                print('[ERROR]', e)
                print('Size of Path:', len(os.path.join(os.getcwd(), fPath)))

        # Create the new folder:
        try:
            if not os.path.exists(directory):  # If the folder doesn't exist,
                os.mkdir(directory)  # Create it
                # Finally, create those inner folders and files:
                create_inner_folders_and_files(file_prefix=file_prefix, directory=directory, inner_folder_names=fileNames, filetypes=filetypes)
            else:  # If the folder does exist,
                # Finally, create those inner folders and files:
                create_inner_folders_and_files(file_prefix=file_prefix, directory=directory, inner_folder_names=fileNames, filetypes=filetypes)
        except Exception as e:
            print('[ERROR]', e)
        # Create outer files based on the file names and file types:
        # for fName in fileNames:
        #   # Create a new file prefix for that file name:
        #   fPrefix = '{fPrefix}.{fName}'.format(fPrefix=file_prefix, fName=fName)
        #   create_new_files(file_prefix=fPrefix, directory=directory, filetypes=filetypes)

    def run(self, directory='Fake_Directory', real_directory=None):
        file_prefix = 'single.file'
        filetypes = ['avi', 'mov', 'mp4', 'txt', 'dat', 'nfo', 'jpg', 'png', 'mkv']
        if real_directory != None:
            fileNames = os.listdir(real_directory)
        else:
            fileNames = [

                # Normal title:
                'The.Bay.2012.LiMiTED.BRRip.XviD.RoSubbed-playXD',
                'Hansel.&.Gretel.Witch.Hunters.2013.DVDRip.XviD-P2P',

                # For testing folder names with underscores in them
                'Ordinary_Decent_Criminal.DVDRip_devilwarez.pl',

                # For testing titles with hyphens in the name:
                # 'Kick-Ass (2010) R5 XViD-MAXSPEED',
                'Kick-Ass 2 (2013) [1080p]',
                'Bio-Dome (1996) - DVD Rip - XVID',

                # For testing titles that have numbers in them:
                '22.Jump.Street.2014.1080p.BluRay.x264.anoXmous',
                '30 Days Of Night[2007]',
                '\'71 (2014) [1080p]',

                # For testing titles that have purposeful periods in them:
                # 'G.I.Joe.The.Rise.of.Cobra.2009.HDRip', # Can't fix this yet
                # 'G.I. Joe Retaliation (2013) [1080p]', # Can't fix this yet.
                'Snatch.2000.1080p.BluRay.x264.anoXmous',
                # 'Fantastic.Mr.Fox.DVDRip.XviD-MOViERUSH', # Can't fix this yet
                # 'W.[2008]DvDrip-aXXo', # Can't fix this yet

                # For testing titles with colons in them:
                'Avengers Age of Ultron (2015) [1080p]',
                # 'Abraham.Lincoln.Vampire.Hunter.2012.DVDRip.XviD-ALLiANCE', # Can't fix this yet
                'Sherlock Holmes A Game of Shadows (2011) DVDRip XviD-MAXSPEED',

                # For testing titles with years (or numbers) as the title:
                '2012 (2009) DVDRip XviD-MAXSPEED',
                '1408[2007]DvDrip[Eng]-aXXo',
                '300[2006]DvDrip[Eng]-aXXo',

                # For testing duplicate names:
                'Red Dawn {2012} DVDRIP. Jaybob',
                'Red.Dawn.1984.720p.BrRip.x264.Obit11.ThumperDC',
                'Poltergeist (1982) [1080p]',
                'Poltergeist 2015 1080p HDRip x264 AC3-JYK',
                'The.Girl.With.The.Dragon.Tattoo[2009]',
                'The Girl With The Dragon Tattoo (2011) (HD)',

                # For testing crazy punctuation in titles:
                'What the #$! Do We (K)now!',
                'Fired Up! (2009)',
                'Ferris Bueller\'s Day Off (1986) [1080p]',
                'You.Don\'t.Mess.With.The.Zohan[2008][Unrated.Edition]DvDrip-aXXo',

                # Random known issues:
                'Howl\'s Moving Castle (2004) 720p',
                'I Hope They Serve Beer In Hell [2009] DvDrip H.264 AAC',
                'Rocketman 1997 DvDrip[Eng]'
            ]

        self.create_dummy_data(file_prefix=file_prefix, directory=directory, filetypes=filetypes, fileNames=fileNames)


if __name__ == '__main__':
    # Fake files:
    CDD = CreateDummyData(verbose=True)
    CDD.run()

    # If you want to clone a real directory to test it out:
    # real_directory = 'J:\Films'
    # CDD.run(real_directory=real_directory)
