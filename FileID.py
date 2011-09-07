import sys
import os

if sys.platform[:3].lower() == "win":
	import win32file
	
	def get_unique_id (hFile):
		(
			attributes,
			created_at, accessed_at, written_at,
			volume,
			file_hi, file_lo,
			n_links,
			index_hi, index_lo
		) = win32file.GetFileInformationByHandle (hFile)
		return volume, index_hi, index_lo
	
	def fileId (filename):
		try:
			hf = win32file.CreateFile (
				filename,
				win32file.GENERIC_READ,
				win32file.FILE_SHARE_READ,
				None,
				win32file.OPEN_EXISTING,
				0,
				None
			)
			rc = get_unique_id(hf)
			hf.Close ()
		except:
			rc = None
			
		return rc
else:
	def fileId(filename):
		try:
			rc = os.stat(filename).st_ino
		except:
			rc = None
			
		return rc
