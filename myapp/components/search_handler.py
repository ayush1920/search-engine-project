import os
import time
import datetime
import threading
import asyncio
from random import randint
from os import scandir
# from .models import RunningSearch

if os.name == 'nt':
    import win32api
    import win32con


class TempSearch:
    def __init__(self):
        self.file_name = 'hue.py'
        self.search_space = [r'C:\Users\aykumar\Downloads', r'C:\Users\aykumar\Desktop']


class DirTranverser:
    '''Custom Implementation of os.walk for searching files with support for threading.'''

    def __init__(self, path='.'):
        self.file_count = 0
        self.result = []
        self.interrupted = False
        self.generator = scandir(path)
##        self.precompute_limit = precompute_limit

    def walk(self, file_name, path, include_hidden=True):
        try:
            dir_generator = scandir(path)
        except OSError as ex:
            return
        while True and not self.interrupted:
            try:
                obj = next(dir_generator)
            except:
                break

            if obj.is_file():
                self.file_count += 1
                if file_name in obj.name.lower():
                    file_path = obj.path
                    include_file = True if include_hidden else (not self.is_file_hidden(file_path))
                    if include_file:
                        self.result.append(obj.path)
            else:
                self.walk(file_name, obj.path)

    def walk_precompute(self, path):
        precompute_dirs = []
        dir_generator = scandir(path)
        pass

    def is_file_hidden(self, file_path):
        if os.name == 'nt':
            attribute = win32api.GetFileAttributes(p)
            return attribute & (win32con.FILE_ATTRIBUTE_HIDDEN | win32con.FILE_ATTRIBUTE_SYSTEM)
        else:
            return p.startswith('.')


# def next_folder(self):
##        '''Recursively generates folders'''
# while True:
# try:
##                directory = next(self.generators[-1])
# if not directory.is_dir():
# continue
##                dir_path = directory.path
# self.generators.append(scandir(dir_path))
# return dir_path
# except:
# if self.generators:
# self.generators.pop()

    def next_folder(self):
        '''Recursively generate folders'''

        while True:
            try:
                directory = next(self.generator)
                if not directory.is_dir():
                    continue
                return directory.path
            except:
                return None


class SearchTask:
    __TIMEOUT = 0
    __SKIP_HIDDEN = False
    __SKIP_SYSTEM_FILES = False
    __THREAD_COUNT = 5
    __PRECOMPUTE_MODE = False
    __PRECOMPUTE_LIMIT = 150

    def __init__(self, file_name, search_space, _id, pre_compute_mode=__PRECOMPUTE_MODE, skip_hidden=__SKIP_HIDDEN,
                 skip_system_files=__SKIP_SYSTEM_FILES, timeout=__TIMEOUT, thread_count=__THREAD_COUNT):
        self.timeout = timeout
        self.start_time = time.monotonic()
        self.start_time_utc = datetime.datetime.utcnow()
        self.search_time = None
        self.metadata_calc_time = 0
        self.file_name = file_name
        self.search_space = search_space
        self.skip_hidden = skip_hidden
        self.skip_system_files = skip_system_files
        self.total_files = 0
        self.total_directories = 0
        self.searched_files = 0
        self.result = []
        self.interrupted = False
        self.comment = 'Running'
        self.thread_count = int(max(1, thread_count))
        self.thread_dict = {}
        self._id = _id
        self.base_traverser = [DirTranverser(search_dirs) for search_dirs in search_space]
        self.traverser_index = 0

    def generate_search_metadata(self):
        for path, subdirs, files in os.walk(self.search_space):
            self.total_files += len(files)
            self.total_directories += 1

        self.metadata_calc_time = time.monotonic() - self.start_time

    def is_underutilized(self):
        return len(self.thread_dict) < self.thread_count

    def main_thread_search(self):
        # self.generate_search_metadata()
        self.search_file()

    def search_file(self):
        while True:
            if self.interrupted:
                self.comment = 'Interrupted by User'
                break

            if self.timeout and time.monotonic() - self.start_time > self.timeout:
                self.comment = 'Search Timed out'
                break

            if self.is_underutilized():
                folder_path = self.base_traverser[self.traverser_index].next_folder()
                if not folder_path:
                    if self.traverser_index + 1 == len(self.base_traverser):
                        break
                    else:
                        self.traverser_index += 1
                        continue

                dir_traverser = DirTranverser()
                thread_key = time.monotonic_ns() + randint(200, 2000)
                self.thread_dict[thread_key] = {
                    'dir_traverser': dir_traverser,
                    'thread': threading.Thread(target=self.thread_search, args=(dir_traverser, thread_key, folder_path))
                }

                self.thread_dict[thread_key]['thread'].start()
            else:
                # sleep the main thread for .1 second
                time.sleep(.1)

        # with for dict to be empty, simulates join thread
        while len(self.thread_dict) != 0:
            time.sleep(.1)
        self.search_time = time.monotonic() - self.start_time
        if not self.interrupted:
            self.comment = 'Completed'
        self.commit_result()

    def thread_search(self, dir_traverser, thread_key, folder_path):
        # print(folder_path)
        dir_traverser.walk(self.file_name, folder_path)
        self.result += dir_traverser.result
        del self.thread_dict[thread_key]

    def stop_threads(self):
        threads = self.thread_dict.values()
        for thread in threads:
            try:
                threads['dir_traverser'].interrupted = True
            except Exception as ex:
                print(ex)

    def commit_result(self):
        print(self.search_time)
        print('commit-final')
        print(self.result)


def SearchMulti(file_name, search_space, thread_count):
    x = SearchTask(file_name, search_space, _id=0, thread_count=thread_count)
    x.main_thread_search()
    return (x.result, x.search_time)
