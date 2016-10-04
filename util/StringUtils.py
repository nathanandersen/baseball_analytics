# Module containing string manipulation routines

__all__ = ["reindent"]

def reindent(s,tabs):
	return "\n".join((tabs * "\t") + i for i in s.splitlines())