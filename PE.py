# ---------------------------------------------------------------------------------------
# Class : PE
# EXTRACTION OF PE ATTRIBUTES
# ---------------------------------------------------------------------------------------

import pefile
import peutils

class PE:

    def __init__(self,filename):
        self.pe=pefile.PE(filename)
        return

    def getDOS_HEADER(self):
        return self.pe.DOS_HEADER

    def getFILE_HEADER(self):
        return self.pe.FILE_HEADER

    def getOPTIONAL_HEADER(self):
        return self.pe.OPTIONAL_HEADER

    def getPE_TYPE(self):
        return self.pe.PE_TYPE

    def getDIRECTORY_ENTRY_IMPORT(self):
        return self.pe.DIRECTORY_ENTRY_IMPORT

    def getDIRECTORY_ENTRY_EXPORT(self):
        return self.pe.DIRECTORY_ENTRY_EXPORT

def peIdentify(filename):

    # Load PE Signature Database & Sample PE
    sigs=peutils.SignatureDatabase(SIGS_DB)
    pe=pefile.PE(filename)

    # Match PE against signature database
    matches=sigs.match_all(pe, ep_only=True)
    return matches