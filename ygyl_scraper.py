"""
A scraper for ygyl threads on /gif/ and /wsg/ on www.4chan.org .
"""

import basc_py4chan as basc

from ygyl_helper import *

WEBM = ".webm"
BOARD_LIST = ["wsg", "gif"]

def main():
    #boards_info()
    i = "Will look for webms and other file formats in various 4chan boards.\nPress enter to continue, or H for more info. "
    if str( input( i ) ) == "H":
        more_info()
    
    for board in BOARD_LIST:
        if str(input("Search /"+board+"/ for files?(Y for yes) ")) == "Y":
            search_board(board)
    
    pass

"""
Allows user to write links of files from a given board to a file.
Allows user to download files of a given board.
@param target_board_name the board of focus to look for ygyl threads.
"""
def search_board( target_board_name):
    print( "Board of focus: "+target_board_name )
    all_threads = basc.Board(target_board_name).get_all_threads() 
    target_threads = [ thread for thread in all_threads if search_for_ygyl( thread.topic ) ]
    if not target_threads: # check if there are any threads those topic post contain "ygyl"
        print( "No current ygyl threads in /"+target_board_name+"/.")
        return
    all_target_posts = []
    for thread in target_threads:
        thread_files = thread.all_posts
        all_target_posts+=thread_files
    files_from_posts = [ post.file for post in all_target_posts if post.has_file]

    files_object_dictionary = f_o_dict( files_from_posts )
    files_url_dictionary = file_url_dict( files_from_posts )

    save_links( target_board_name, files_url_dictionary)
   
    to_download( target_board_name, files_object_dictionary)

"""
User decides whether or not to save file urls from the given board.
@param board_name name of board to save the files from.
@param file_urls the set of file urls intended to writted to a file.
"""
def save_links( board_name, file_urls):
    if not str( input( "Press enter to save webm links, enter anything else to not: " ) ):
        wf_name = str( input( 
            "File to save webm links to. Press enter to save to webms.txt: " ))
        if not wf_name:
            wf_name = "webms.txt"
        write_links( wf_name, board_name, WEBM, file_urls )
    if not str( input( "Press enter to save non-webm links, enter anything else to not: ") ):
        nwf_name = str( input(
            "File to save non-webms to. Press enter to save to others.txt:"
        ))
        if not nwf_name:
            nwf_name = "others.txt"    
        write_links( nwf_name, board_name, "", file_urls )


"""
Writes files of extension type file_ext to a file named file_name.
@param file_name the name of file to save file url to.
@param board_name the name of the current board where the files are located.
@param file_ext the file extension for the files of interest. "" for non-webms.
@param file_urls a dictionary of file extensions to lists of files with that file type.
"""
def write_links( file_name, board_name, file_ext, file_urls ):
    FILE_MODE = "a"
    url_file = open( file_name, FILE_MODE )

    links_being_written = "webm" if file_ext == WEBM else "non-webm"
    print("Writing "+links_being_written+" links to "+file_name+"...")

    url_file.write("/"+board_name+"/:\n")

    f_u = {}
    if file_ext == WEBM:
        f_u = { WEBM: file_urls[WEBM]}
    else:
        f_u = file_urls
        f_u.pop(WEBM)

    for file_ext in f_u.keys():
            url_file.write("\t"+file_ext+":\n")
            for f in f_u[file_ext]:
                url_file.write("\t\t"+f+"\n")
    
    url_file.close()




main()