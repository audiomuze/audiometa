""" this script compares FLAC file metadata against a set of sanctioned tagnames and removes any not appearing in the sanctioned list"""

import os
import sys
from mutagen.flac import FLAC

try:
    from os import scandir
except ImportError:
    from scandir import scandir  # use scandir PyPI module on Python < 3.5


""" function to clear screen """
cls = lambda: os.system('clear')


def get_prohibited_tags(taglist, permitted_tags):

    return [tag for tag in taglist if tag not in permitted_tags]



permitted_tags = {
    "__accessed",
    "__app",
    "__bitrate",
    "__bitrate_num",
    "__bitspersample",
    "__channels",
    "__created",
    "__dirname",
    "__dirpath",
    "__ext",
    "__file_access_date",
    "__file_access_datetime",
    "__file_access_datetime_raw",
    "__file_create_date",
    "__file_create_datetime",
    "__file_create_datetime_raw",
    "__file_mod_date",
    "__file_mod_datetime",
    "__file_mod_datetime_raw",
    "__file_size",
    "__file_size_bytes",
    "__file_size_kb",
    "__file_size_mb",
    "__filename",
    "__filename_no_ext",
    "__filetype",
    "__frequency",
    "__frequency_num",
    "__image_mimetype",
    "__image_type",
    "__layer",
    "__length",
    "__length_seconds",
    "__md5sig",
    "__mode",
    "__modified",
    "__num_images",
    "__parent_dir",
    "__path",
    "__size",
    "__tag",
    "__tag_read",
    "__version",
    "acousticbrainz_mood",
    "acoustid_id",
    "album",
    "albumartist",
    "amg_album_id",
    "amg_boxset_url",
    "amg_url",
    "amgtagged",
    "analysis",
    "arranger",
    "artist",
    "bootleg",
    "catalog",
    "catalognumber",
    "compilation",
    "composer",
    "conductor",
    "country",
    "date",
    "discnumber",
    "discogs_artist_url",
    "discogs_release_url",
    "discsubtitle",
    "engineer",
    "ensemble",
    "fingerprint",
    "genre",
    "label",
    "live",
    "lyricist",
    "lyrics",
    "mixer",
    "mood",
    "musicbrainz_albumartistid",
    "musicbrainz_albumid",
    "musicbrainz_artistid",
    "musicbrainz_discid",
    "musicbrainz_releasegroupid",
    "musicbrainz_releasetrackid",
    "musicbrainz_trackid",
    "musicbrainz_workid",
    "originaldate",
    "originalreleasedate",
    "originalyear",
    "part",
    "performancedate",
    "performer",
    "personnel",
    "producer",
    "rating",
    "recordinglocation",
    "recordingstartdate",
    "reflac",
    "releasetype",
    "remixer",
    "review",
    "roonalbumtag",
    "roonradioban",
    "roontracktag",
    "roonid",
    "sqlmodded",
    "style",
    "subtitle",
    "theme",
    "title",
    "tracknumber",
    "upc",
    "version",
    "work",
    "writer"
}


def scantree(path):
    """Recursively yield DirEntry objects for given directory."""
    for entry in scandir(path):
        if entry.is_dir(follow_symlinks=False):
            yield from scantree(entry.path)
        else:
            if entry.name.endswith('.flac'):
                """or entry.name.endswith('.ape')  or entry.name.endswith('.wv') or entry.name.endswith('.dsf') or entry.name.endswith('.mp3')"""
                yield entry


if __name__ == '__main__':

    cls()
    prohibited_tags = []
    modded = 0
    for entry in scantree(sys.argv[1] if len(sys.argv) > 1 else '.'):
        info = entry.stat()
        audio = FLAC(entry.path)
        taglist = []
        for a, b in audio.tags:
            taglist.extend([str.lower(a)])

        prohibited_tags = get_prohibited_tags(taglist, permitted_tags)
        has_pics = audio.pictures

        if len(prohibited_tags) > 0:
            prohibited_tags = list(set(prohibited_tags))  # remove duplicates from prohibited tags
            prohibited_tags.sort()
            print(f"Removing unsanctioned tags from file:'{entry.path}'")
            for i in prohibited_tags:
                print(f"- {i}")
                audio.pop(i)
            modded = 1

        if has_pics:
            print(f"Removing artwork from file:'{entry.path}'")
            audio.clear_pictures()
            modded = 1

        if modded == 1:
            mod_time = entry.stat().st_mtime
            audio.save(entry)
            os.utime(entry,(mod_time, mod_time)) # preserve original file mod time
