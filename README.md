# cfmldocplugin - version 0.1.3

A Sublime plugin for generating CFDoc comments in CFML (Both tags and script)

Simple and straight forward, you simply install the plugin and set a shortcut key.

Running it will create CFDoc style comments based off of your CFML code.

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

If you find bugs please let me know so I can take a look at it.

## Installing
Install with the Sublime Package Manager, under CFMLDocPlugin

Set up a key shortcut to the command docifycfml, like so:

```
{ "keys": ["ctrl+shift+2"], "command": "docifycfml" }
```
