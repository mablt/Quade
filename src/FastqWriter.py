# -*- coding: utf-8 -*-

"""
@package    Quade
@brief      Contain a class that Handle fastq writing
@copyright  [GNU General Public License v2](http://www.gnu.org/licenses/gpl-2.0.html)
@author     Adrien Leger - 2014
* <adrien.leger@gmail.com>
* <adrien.leger@inserm.fr>
* <adrien.leger@univ-nantes.fr>
* [Github](https://github.com/a-slide)
* [Atlantic Gene Therapies - INSERM 1089] (http://www.atlantic-gene-therapies.fr/)
"""

# Standard library imports
from gzip import open as gopen

#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
class FastqWriter (object):
    """
    Handle creation of fastq files and writing via a str buffer to optimize the time of disk acces
    """
#~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#

    #~~~~~~~FUNDAMENTAL METHODS~~~~~~~#

    def __init__ (self, name="Unknown"):
        """Init the object with counters, empty buffers, and names of fastq files"""
        self.buffer_size = 20
        self.R1_fastq_name = name+"_R1.fastq.gz"
        self.R2_fastq_name = name+"_R2.fastq.gz"
        self.counter = -1
        self.R1_buffer = ""
        self.R2_buffer = ""

    # Fundamental class functions str and repr
    def __str__(self):
        msg = "FASTQ_WRITER CLASS\n"
        for key, value in self.__dict__.items():
            msg+="\t\t{}\t{}\n".format(key, value)
        return (msg)

    def __repr__(self):
        return "<Instance of {} from {} >\n".format(self.__class__.__name__, self.__module__)

    #~~~~~~~PUBLIC METHODS~~~~~~~#

    def __call__ (self, read1, read2, index, molecular=""):
        """
        Init files at first call and append in the files via str buffers
        read1, read2, index and molecular are FastqSeq sequence
        """

        # Create the file when the first pair of fastq sequence is added
        if self.counter == -1:
            self.init_files()
            self.counter = 0

        # Increment the sequence counter and fill the str buffers
        self.counter += 1
        if molecular:
            read1.name += ":{}:{}".format(index.seq, molecular.seq)
            read2.name += ":{}:{}".format(index.seq, molecular.seq)
        else:
            read1.name += ":{}".format(index.seq)
            read2.name += ":{}".format(index.seq)

        self.R1_buffer += read1.fastqstr
        self.R2_buffer += read2.fastqstr

        # Flush the buffers each time they reach the size of the max buffer size
        if self.counter == self.buffer_size:
            self.flush_buffers ()
            self.counter = 0

    def init_files (self):
        """Init empty files for R1 and R2.fastq.gz"""
        with gopen (self.R1_fastq_name, "wb") as fastq_file:
            print("\tCreate {} file".format(self.R1_fastq_name))
        with gopen (self.R2_fastq_name, "wb") as fastq_file:
            print("\tCreate {} file".format(self.R2_fastq_name))

    def flush_buffers (self):
        """Append to R1 and R2 fastq.gz files"""
        with gopen (self.R1_fastq_name, "ab") as fastq_file:
            fastq_file.write(self.R1_buffer)
            self.R1_buffer = ""
        with gopen (self.R2_fastq_name, "ab") as fastq_file:
            fastq_file.write(self.R2_buffer)
            self.R2_buffer = ""
