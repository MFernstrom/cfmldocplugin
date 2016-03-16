# cfmldocplugin - version 0.1

A Sublime 2/3 plugin for generating JavaDoc/YUIDoc style comments in CFML (Both tags and script)

Simple and straight forward, you simply install the plugin and set a shortcut key.

Running it will create JavaDoc/YUIDoc style comments based off of your CFML code.

While it automatically pulls in information about the code, it's not quite psychic yet, so to add comments to the header, simply use the hint or description!

So for example:
```
public array function myAwesomeFunction( required string awesome, maybeAwesome = "totally" ) hint="My text here" {
	return arguments.awesome;
}
```
becomes:
```
/**
  * My text here
  *
  * @method myAwesomeFunction
  * @public
  * @param {string} awesome (required) 
  * @param {any} [maybeAwesome = "totally" ]  
  * @return {array}
  */

public array function myAwesomeFunction( required string awesome, maybeAwesome = "totally" ) hint="My text here" {
	return arguments.awesome;
}
```

The output comment blocks are pretty standard, I've tested with YUIDoc but not JavaDoc for generating documentation from it, and of course tested with the cfml documentation generator I'm about to release.

This is the first release, if you find bugs please let me know so I can take a look at it.

## Installing
My plan is to get this added to the Sublime package manager, in the mean time (Or if you just like doing things manually), download the DocifyCfml folder, and drop it into your Sublime package folder.

Set up a key shortcut to the command docifycfml, like so:

```
{ "keys": ["ctrl+shift+2"], "command": "docifycfml" }
```

And that's pretty much it.

Be nice, this is the first Python code I've ever written, outside of "Hello World"  ;)
