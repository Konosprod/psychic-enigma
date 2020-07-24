#!/usr/bin/python3

import os
import sys
import argparse
import ffmpeg
import pathlib

def buildIndex(dirName):
    
    directories = [x[0] for x in os.walk(os.path.normpath(dirName))] 
    
    f = open("index.txt", "w")
    for elem in directories:
        f.write(elem+"\n")
    f.close()

    return

def getFiles(dirName):
    # create a list of file and sub directories 
    # names in the given directory 
    listOfFile = os.listdir(dirName)
    allFiles = list()
    # Iterate over all the entries
    for entry in listOfFile:
        # Create full path
        fullPath = os.path.join(dirName, entry)
        # If entry is a directory then get the list of files in this directory 
        if os.path.isfile(fullPath):
            if(fullPath.lower().endswith((".avi", ".mp4", ".mkv"))):
                allFiles.append(fullPath)
                
    return allFiles

def processDir(directory, outdir):
    
    f = open("last.txt", "w")
    f.write(directory+"\n")
    f.close()

    files = getFiles(directory)

    for file in files:
        convertFile(file, outdir)

    return

def convertFile(infile, outdir):
    fn = pathlib.Path(infile)
    outfile = outdir + fn.name

    input_args = {

    }

    output_args = {
        "loglevel", "warning",
        "c:v": "libx265",
        "c:a": "copy",
        "c:s": "copy",
        "crf": "23",
        "map": 0,
    }

    sys.stderr.write(infile+"\n");

    ffmpeg.input(infile, **input_args).output(outfile, **output_args).overwrite_output().run()

    return

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="Convert your videos into HEVC")
    parser.add_argument('-i', action="store_true", default=False, help="Wether you should build the directory index or not", dest="shouldBuildIndex")
    parser.add_argument('-d', action="store", dest="dir", help="Root directory of your videos")
    parser.add_argument("-o", action="store", dest="outdir", help="Output directory for your files", default="./out/")
    parser.add_argument("-c", action="store_true", default=False, help="Actually convert your files")

    res = parser.parse_args()

    if res.shouldBuildIndex:
        print("Build directory index")
        buildIndex(res.dir)

    if res.c:
        index = 0

        f = open("index.txt", "r")
        dirs = f.readlines()
        f.close()

        if os.path.exists("./last.txt"):
            f = open("./last.txt", "r") 
            last = f.readline()
            f.close()

            index = dirs.index(last)

        for i in range(index, len(dirs)):
            outdir = res.outdir
            
            if not res.outdir.endswith("/"):
                outdir += "/"

            path = outdir + dirs[i].rstrip("\n")

            if not path.endswith("/"):
                path += "/"

            pathlib.Path(path).mkdir(parents=True, exist_ok=True)
            processDir(dirs[i].rstrip("\n"), path)
        

