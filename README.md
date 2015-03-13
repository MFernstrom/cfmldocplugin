# cfmldocplugin - version 0.1

A Sublime 2/3 plugin for generating JavaDoc/YUIDoc style comments in CFML (Both tags and script)

Simple and straight forward, you simply install the plugin and set a shortcut key.

Running it will create JavaDoc/YUIDoc style comments based off of your CFML code.

While it automatically pulls in information about the code, it's not quite psychic yet, so to add comments to the header,
simply use the hint or description!

So for example:

public array function myAwesomeFunction( required string awesome, maybeAwesome = "totally" ) hint="My text here" {
	return arguments.awesome;
}

becomes:

/**
  * My text here
  *
  * @method myAwesomeFunction
  * @public
  * @param {string} awesome (required) 
  * @param {any} [maybeAwesome = "totally" ]  
  * @return {myAwesome}
  */
public array function myAwesomeFunction( required string awesome, maybeAwesome = "totally" ) hint="My text here" {
	return arguments.awesome;
}

Working out a few kinks, then version 0.1 will be available.

Be nice, this is the first Python code I've ever written, outside of "Hello World"  ;)
