# -*- coding: utf-8 -*-
#@File name	: filehelper.py
#@Auther	: GhostFromHeaven[csdn]
#@date		: 2012-07-19
import collections

def isfilelike_r(f):
	"""
    Check if object 'f' is readable file-like 
	that it has callable attributes 'read' and 'close'
    """
	try:
		if isinstance(getattr(f, "read"), collections.Callable) \
			and isinstance(getattr(f, "close"), collections.Callable):
			return True
	except AttributeError:
		pass
	return False

def isfilelike_w(f):
	"""
    Check if object 'f' is readable file-like 
	that it has callable attributes 'write' and 'close'
    """
	try:
		if isinstance(getattr(f, "write"), collections.Callable) \
			and isinstance(getattr(f, "close"), collections.Callable):
			return True
	except AttributeError:
		pass
	return False

def isfilelike(f):
	"""
    Check if object 'f' is readable file-like 
	that it has callable attributes 'read' , 'write' and 'close'
    """
	try:
		if isinstance(getattr(f, "read"), collections.Callable) \
			and isinstance(getattr(f, "write"), collections.Callable) \
				and isinstance(getattr(f, "close"), collections.Callable):
			return True
	except AttributeError:
		pass
	return False

def fileinoutpattern(inp, out, callback=None, inmode="r", outmode="wb"):
	"""
	Make sure that 'inp' and 'out' has been 'converted' to file objects, 
	and call 'callback' with them, finally clear it up. 
	"""
	# Set up
	fin = inp
	if not isfilelike_r(fin):
		fin = open(inp, inmode)
	fout = out
	if not isfilelike_w(fout):
		fout = open(out, outmode)
	
	# Call the 'callback'
	result = None
	if callback != None:
		result = callback(fin, fout)

	# Clear up
	if not isfilelike_r(inp):
	    fin.close()
	if not isfilelike_w(out):
	    fout.close()
	
	return result
