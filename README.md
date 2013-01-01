cecs-444
========

CECS 444 (Compiler Construction) Projects
Professor: Verne Konig
CSULB

All projects written in Python 2.7 with wxPython GUI. All projects have 
non-graphical fallbacks, used as follows:

assignment_#.py [verbose] input_file.txt

Projects
========

Assignment 2: Small Scanner
   The first programming project of the course, assignment 2 was to implement 
   a lexical scanner for a small subset of the scripting language we would 
   evenually be parsing. The language mostly consists of operators and variable
   names tokens. All table work (i.e. action, state, etc) was done on paper, so
   no tables are included for this project.
   
   Two test files are provided in the test directory:
   * source.txt is a valid example in the language and scans completely.
   * error.txt is invalid and will produce errors.
   
Assignment 3: Large Scanner
   The second programming project in the course was to expand the scanner from
   assignment 2 to scan the entire language. A list of valid tokens can be 
   found in tables/token_list.txt. 
   
   Table work for this project would have been to tedious to do by hand, so it
   was all done in Excel. The original XLS file, along with the state, action 
   and look-up CSV files it generated, are included in the tables directory.
   
   Three valid source files are included in the test directory. All should scan
   successfully.
   
Assignment 4: Parser
   The final project for the course was to implement a parser that gets tokens
   from the large scanner developed in assignment 3. The program parses the 
   context-free grammar we had been woring with all semester into a parse tree.
   The parser is an LL(1) top-down parser with error recovery.
   
   Tables are included in the tables directory. 
   
   Several test files are included in the test directory:
   * parser_konig.txt is a source file provided by the professor.
   * parser_large.txt is a source file I created which parses with no errors.
   * parser_error_recover.txt is a source file with recoverable errors in it.
     It will be parsed completely, and show how the errors were corrected.
   * parser_error_unrecoverable.txt is a source file with unrecoverable errors.
     The parser will display the error in the file and fail gracefully.