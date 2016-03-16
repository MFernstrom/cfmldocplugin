##
#	About			: Auto javaDocify CFML tags and cfscript
#
#	Author		: Marcus Fernstrom
#
#	Website		: http://www.MarcusFernstrom.com/
#
#	Copyright	: Marcus Fernstrom, 2014
#
#	Version 	: 0.1.1
#
#	License		: GPL3
#
# Release		: Fixed a bug that caused the plugin to not run on Sublime 3
##

import sublime, sublime_plugin, re

class REMatcher(object):
    def __init__(self, matchstring):
        self.matchstring = matchstring

    def match(self,regexp):
        self.rematch = re.match(re.compile(regexp), self.matchstring)
        return bool(self.rematch)

    def group(self,i):
        return self.rematch.group(i)

class docifycfmlCommand(sublime_plugin.TextCommand):
	def run(self, edit):
		#	Clears the console output, incase you have it open.
		for num in range(1,200):
			print("")

		print("Auto javaDocify Plugin for CFML")
		print("===============================")

		print("Performing black magic..")
		self.DocTags(edit)
		self.docScript(edit)
		print("Assuming you did not lose all your stuff or turn into a toad, it worked!")
	
	##
	#	Below are the javaDoc functions for handling CFML tags
	##
	def DocTags(self, edit):
		print("Checking if we need to doc cftags")
		content = self.view.substr(sublime.Region(0, self.view.size()))
		allcontent = sublime.Region(0, self.view.size())

		#	I hand-built this bastard regex, yes I know it could use some work.
		content = re.sub(re.compile("(\/\*\*\n(?:\s*)(?:\*(?:.*)\n)?(?:\s*)\*\/\n(?:\s*--->)?(?:\s*)<cffunction)|(<cffunction.*?<\/cffunction>)", re.DOTALL | re.IGNORECASE), (lambda m: self.docTags(changeBlock=m)), content)
		self.view.replace(edit, allcontent, content)

	def docTags(self, changeBlock):
		if changeBlock.group(2):
			toChange = changeBlock.group(2)

			#	Initialize some variables
			block = ""
			returnTypeText = ""
			whitespace = ""
			defaultText = ""

			m = REMatcher(toChange)
			r = REMatcher(toChange)

			# Grabs the whitespace prefixing the function, used for lining up the comment block
			lines = toChange.splitlines()
			whitespace = ''
			for theline in lines:
				if "</cffunction>" in theline:
					whitespace = re.findall('(\s*)</cffunction', theline)[0]

			block = "%s/**" % (whitespace)

			# Grabs and processes the function name and hint/description text
			if m.match(re.compile('<cffunction.*name\s?=\s?"(\w*)".*>', re.IGNORECASE)):		

				# Grabs the hint/description
				if r.match(re.compile('<cffunction.*(?:hint|description)\s?=\s?"([\w\s]*)".*>', re.IGNORECASE)):
					block = block + "\n%s  * %s\n%s  *" % (whitespace, r.group(1), whitespace)

				# Grabs the returntype
				if r.match(re.compile('<cffunction.*(?:returntype)\s?=\s?"([\w\s]*)".*>', re.IGNORECASE)):
					returnTypeText = "{" + r.group(1) + "}"

				if r.match(re.compile('<cffunction.*access\s?=\s?"(\w*)".*>', re.IGNORECASE)):
					block = block + "\n%s  * @%s" % (whitespace, r.group(1))
				else:
					block = block + "\n%s  * @public" % whitespace
				
				block = block + "\n%s  * @method %s" % (whitespace, m.group(1))

				# Checks to see if the function has a defined returnformat
				returnFormatCheck = re.match(re.compile('.*returnformat\s?=\s?"(\w*)"', re.IGNORECASE), toChange)

			# Grabs and processes all the cfarguments and their information
			argMatches = re.findall(re.compile('(<cfargument.*name=.*>)', re.IGNORECASE), toChange)

			# For each cfargument, do:
			for match in argMatches:
				argTypeText = ""
				hintText = ""
				defaultText = ""

				# Checks if there is a hint text
				hintCheck = re.match(re.compile('.*(?:hint|description)\s?=\s?"(.*)".*>', re.IGNORECASE), match)
				if hintCheck:
					hintText = " %s" % hintCheck.group(1)

				# Checks to see if the argument is Required
				reqCheck = re.match(re.compile('.*required\s?=\s?"true"', re.IGNORECASE), match)
				if reqCheck:
					reqCheck = " (required) "
				else:
					reqCheck = ""

				# Checks to see if the argument has a defined type
				typeCheck = re.match(re.compile('.*type\s?=\s?"(\w*)"', re.IGNORECASE), match)
				if typeCheck:
					typeCheck = "{" + typeCheck.group(1) + "} "
				else:
					typeCheck = "{any} "

				# Checks to see if there are any defaults
				defaultCheck = re.match(re.compile('.*default\s?=\s?"(.*)"', re.IGNORECASE), match)
				if defaultCheck:
					if len(defaultCheck.group(1)) > 0:
						defaultText = " %s" % defaultCheck.group(1)
					else:
						defaultText = '""'

				# Grabs the name of the param
				name = re.match(re.compile('.*name\s?=\s?"(\w*)"', re.IGNORECASE), match)
				argTypeTextTemp = re.match(re.compile('.*type\s?=\s?"(\w*)"', re.IGNORECASE), match)
				if argTypeTextTemp:
					if argTypeTextTemp.group(1):
					 	argTypeText = '{' + argTypeTextTemp.group(1) + '} '

				# If there are default values, we display a different string than if there aren't.
				if len(defaultText) > 0:
					block = block + "\n%s  * @param %s%s[%s = %s]%s%s" % (whitespace, typeCheck, argTypeText, name.group(1), defaultText.strip(), reqCheck, hintText)
				else:
					block = block + "\n%s  * @param %s%s%s%s" % (whitespace, typeCheck, name.group(1), reqCheck, hintText)

			if returnFormatCheck:
				block = block + "\n%s  * @returnformat {%s}" % (whitespace, returnFormatCheck.group(1))

			# Pulls all the cfreturn values, note that there may be more than one
			returnMatch = re.findall(re.compile('<cfreturn\s?(.*)>', re.IGNORECASE), toChange)
			
			if len(returnMatch) > 0:
				block = block + "\n%s  * @return %s" % (whitespace, returnTypeText)

			block = "<!---\n" + block + "\n%s  */\n%s" % (whitespace, whitespace) + "--->\n"
			return block + toChange
		else:
			return changeBlock.group(1)

	##
	#	Below are the functions for handling cfscript
	##
	def docScript(self, edit):
		print("Checking if we need to doc cfscript")
		
		# Grabbing all the content of the window
		content = self.view.substr(sublime.Region(0, self.view.size()))
		allcontent = sublime.Region(0, self.view.size())

		# The below is a nasty trick, because Python split_by_newlines removes blank lines, causing issues.
		# This way, we retain all the lines intact.
		content = content.replace("\n", "\n@@@")
		self.view.replace(edit, allcontent, content)

		regions = [ sublime.Region(0, self.view.size()) ]
		lineCount = 1
		currentCodeBlock = ''
		javadocLineCheck = 0
		blockStartLine = 0
		blockEndLine = 0
		openBrackets = 0
		closingBrackets = 0
		latestLineAdd = 0
		quotes = 2

		# Splits content into lines
		for region in regions:
			lines = self.view.split_by_newlines(region)

			# Looping each line of the content
			lastSeen = True
			for line in lines:
				if blockEndLine < len(regions):
					if self.view.substr(line).count("*/") == 1:
						javadocLineCheck = lineCount

					# This basically checks the line to see if we found a cfscript function, a bit heavy handed but works for now.
					if self.view.substr(line).count("function") == 1 and self.view.substr(line).count("cffunction") == 0 and self.view.substr(line).count("(") > 0 and self.view.substr(line).count(")") > 0 and lineCount - javadocLineCheck > 0 and lastSeen:
						blockStartLine = lineCount

					# blockStartLine is defaulted to 0, so if the number is higher it means we have a function.
					if blockStartLine > 0:
						for char in self.view.substr(line):
							if char == '"' or char == "'":
								quotes += 1

							if quotes % 2 == 0:
								if char == '{':
									openBrackets += 1

								if char == '}':
									closingBrackets += 1

							if closingBrackets == openBrackets and openBrackets > 0:
								## 
								# Hitting this block means that we have a complete cfscript function in the variable currentCodeBlock.
								##
								blockEndLine = lineCount
								blockStartLine = 0
								blockEndLine = 0
								openBrackets = 0
								closingBrackets = 0
								whitespace = ''
								varInfo = ''
								theHint = ''
								
								# Begin black magic voodoo stuff..
								k= REMatcher(currentCodeBlock)

								# Setting var defaults
								functionName = ''
								functionReturnType = 'any'
								functionReturnVariable = ''
								functionAccess = ''

								# This sets the whitespace variable to the whitespace prefixing the function to ensure
								# that the javadoc code is in line and tabbed out to the same distance as the function
								whitespace = re.findall(re.compile('\n?(\s*)(?:\w.*)?\s?function', re.IGNORECASE), currentCodeBlock)
								if whitespace:
									whitespace = whitespace[0]
								else:
									whitespace = ""

								# Grabs the name of the function
								if k.match(re.compile('.*function\s(\w*)', re.IGNORECASE)):
									functionName = k.group(1)

								# Grabs the returntype of the function
								k = re.findall(re.compile('.*?(?:public|private|remote|package)\s?|(\w*)\s?function', re.IGNORECASE), currentCodeBlock)
								if k:
									print k
									if k[1]:
										functionReturnType = k[1]

								# Grabs the functions returnformat, if it's defined
								tagReturnFormat = re.match(re.compile('.*function.*returnformat\s?=\s?"(\w*)"', re.IGNORECASE | re.DOTALL), currentCodeBlock)
								if tagReturnFormat:
									tagReturnFormat = "\n%s  * @returnformat {%s}" % (whitespace, tagReturnFormat.group(1))
								else:
									tagReturnFormat = ""

								# Grabs the return variable
								lines = currentCodeBlock.splitlines()
								functionReturnVariable = ''
								for theline in lines:
									theMatch = re.findall(re.compile(".*return\s(.*);"), theline)
									if theMatch:
										functionReturnVariable = "\n%s  * @return {%s}" % (whitespace, functionReturnType)

								# Grabs the hint, if one exists
								theHintBlock = re.findall(re.compile('\n?.*function.*(?:hint|description)\s?=\s?"(.*)"\s*{', re.IGNORECASE | re.DOTALL), currentCodeBlock)
								if theHintBlock:
									for match in theHintBlock:
										theHint = "  * %s\n%s  *\n%s" % (match, whitespace, whitespace)
								else:
									theHint = ""

								# Grabs the functions access level
								functionAccess = re.findall(re.compile('\s?(public|private|remote|package)\s?(?:\w*)\s?function', re.IGNORECASE | re.DOTALL), currentCodeBlock)
								if len(functionAccess):
									for match in functionAccess:
										functionAccess = match
								else:
									functionAccess = 'public'

								# Find and grab all the params, then convert to a python list so we can loop it nicely.
								functionParams = re.findall(re.compile('.*function.*\((.*)\)', re.IGNORECASE), currentCodeBlock)
								if len(functionParams) > 0:
									functionParams = functionParams[0].split(",")

									# Loop and process each parameter as needed, and append.
									for each in functionParams:
										if len(each.strip()) > 0:
											if len(each.split()) == 1:
												varInfo = varInfo + '\n%s  * @param {any} %s' % (whitespace, each.strip())
											else:
												if "required" in each:
													reqVar = " (required) "
													each = each.replace("required", "")
												else:
													reqVar = ""
												theTypes = ["array", "string", "struct", "boolean", "numeric"]
												type = [x for x in theTypes if x in each]
												if type:
													each = each.replace(type[0], "")
													type = type[0]
												else:
													type = "any"
												
												if "=" in each:
													defValue = re.findall(re.compile('=\s?(.*)', re.IGNORECASE), each)
													each = each.replace("=", "")
													if defValue:
														each = each.replace(defValue[0], "")
														defValue = "[%s = %s]" % (each.strip(), defValue[0])
													each = each.replace('"', "")
													each = each.strip()

												else:
													defValue = ""
												theVal = each.strip()

												if defValue:
													varInfo = varInfo + '\n%s  * @param {%s} %s' % (whitespace, type, defValue)
												else:
													varInfo = varInfo + '\n%s  * @param {%s} %s%s' % (whitespace, type, theVal, reqVar)

									# Now we finally assemble the javadoc/yuidoc block in its entirety.
									tempBlock = '%s/**\n%s%s  * @method %s\n%s  * @%s%s  %s%s\n%s  */\n' % (whitespace, whitespace, theHint, functionName, whitespace, functionAccess, varInfo, tagReturnFormat, functionReturnVariable, whitespace)

									# Update the content variable, which contains all the changed text
									content = content.replace(currentCodeBlock, tempBlock + currentCodeBlock)
									currentCodeBlock = ''
							else:
								# At this point, there was nothing of interest, so we continue on the next line
								if latestLineAdd != lineCount:
									currentCodeBlock = currentCodeBlock + self.view.substr(line) + '\n'
									latestLineAdd = lineCount

					#	This block checks to make sure we're not YuiDocing a function that's already documented
					if self.view.substr(line).count("*/") == 1:
						lastSeen = False
					else:
						lastSeen = True
				lineCount = lineCount + 1
		# And finally change the text in the view to the modified text.
		# At some point, I would like to retain the current location for the user,
		# but that will have to include accounting for the new lines up to that point.
		content = content.replace("@@@", "")
		allcontent = sublime.Region(0, self.view.size())
		self.view.replace(edit, allcontent, content)