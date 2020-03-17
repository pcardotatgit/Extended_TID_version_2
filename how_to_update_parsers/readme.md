# How to write parsers for Extended TID

In this section we are going to talk about how parsers for ETID are built.

The ETID's architecture allows this tool to be updated with new feeds. Or we can come across the fact that the format of a feed changed. Making parsing rules obsolete for this feed.

So it is possible to update or add new feeds.

Parsers rules are stored into a SQLite Database names <b>./bases/python_parsers.db</b>

All parsers have a unique name which must be designated in the feeds definition ( etid.cd )

Example : 

	http : //mirror1.malwaredomains.com/files/domains.txt,parser_3,domain,malwaredomains_list,1

	( feed location / parser name for this feed / a prefix for temp file in the ./scripts/output folder ,  1 = Selected or 0 = Not Selected  )
	
	
In the above example of a feed definition, parser_3 is the name of the parser.

And here under we have the needed parser's parameters :

| **PARAMETER**         | **DESCRIPTION**                                       |
|:---------------------|:------------------------------------------------------|
| **PARSER NAME**      | Parser Name                                           |
| **delimiter**        | delimiter to use in the read line to seperate words. Ex : ;  or , or SPACE or <==>  |
| **words_ok**         | we keep this read line only if we find one of these words into it ( separator must be , ). ex : string1 , string2 , string3,... ALLWORDS = keep all lines      |
| **words_Nok**        | but if we find one of these word into it, then we don t keep this line ex : string1 , string2 , string3|
| **start_to_parse_when_found**| Start to parse the lines in the file when we find this string at the begining fo the line. parse all lines in the file if equal to : ALL_LINES  |
| **stop_to_parse_when_found** | stop to parse the file, when this string is found in the line |
| **parse_first_line**   | 0 = By default the first line of the file is not parsed, 1 = parse the first line |
| **add_eol_after_each_readed_line**   | 1 = Add a Carriage Return to resulting line after every parsed lines, 0 = Add a Carriage Return only when the add_a_new_line_when_found string is found |
| **parse_first_line**   |  Add a Carriage Return only when this word is found |
| **add_a_new_line_when_found**   | 0 = By default the first line of the file is not parsed, 1 =  |
| **Parse_group_only_one_time**   | 1  <<< 0 = stop to parse file when stop_to_parse_when_found is found, 1 = start again when start_to_parse_when_found is found again |

Example :

        PARSER NAME :  parser_3
        delimiter : >> ; << delimiter to use in the read line to seperate words
        words_ok :  ['ALLWORDS'] <<< we keep this read line only if we find one of these words into it ( separator must be , ). ALLWORDS = keep all lines
        words_Nok :  ['localhost'] <<< but if we find one of these word into it, then we don t keep this line
        start_to_parse_when_found : Start to parse the lines in the file when we find this word at the begining fo the line. parse all lines if equal to : ALL_LINES
        AND THEN stop_to_parse_when_found :  ***** <<< stop to parse the file, when this word is found in the line
        Columns to keep :  [999] <<< all result will be stored into csv like columns. Give the Column number to keep. 999 = Keep all columns
        parse_first_line :  0 <<< By default the first line of the file is not parsed
        add_eol_after_each_readed_line :  1 <<< 1 = Add a Carriage Return to resulting line after every parsed lines, 0 = Add a Carriage Return only when the add_a_new_line_when_found  word is found
        add_a_new_line_when_found :  *****???***** <<< Add a Carriage Return only when this word is found
        Parse_group_only_one_time :  1  <<< 0 = stop to parse file when stop_to_parse_when_found is found, 1 = start again when start_to_parse_when_found is found again
		
As parser is a major topic by itself, we don't provide with here within ETID more explanation and tools for creating them .

Parsers details and how to create/modify a them for ETID is described in detail into the **Universal Parser** project. 

If you want to add a new parser to ETID. Go to the **Universal Parser** project, develop and test your new parser based on instructions. 
And when your new parser is working, then :

- Add it with a unique name, to the python_parsers database **./bases/python_parsers.db** . Tools for this are provided in the **Universal Parser** project
- Add a new line into the **./files/feeds.txt** files, containing the feed location, and it's parser name