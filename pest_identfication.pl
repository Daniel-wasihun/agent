% Pest Identification Program (deq.pl)
% Enhanced CLI interface for pest identification and report generation

:- use_module(library(lists)).
:- use_module(library(filesex)).
:- use_module(library(charsio)).
:- use_module(library(system)).

% Load pest knowledge base
:- consult('pest_knowledge.pl').

% Pest-related keywords
pest_keyword("pest").
pest_keyword("insect").
pest_keyword("bug").
pest_keyword("bugs").
pest_keyword("mite").
pest_keyword("worm").
pest_keyword("caterpillar").
pest_keyword("aphid").
pest_keyword("whitefly").
pest_keyword("mealybug").
pest_keyword("spider mite").
pest_keyword("leaf").
pest_keyword("leaves").
pest_keyword("stem").
pest_keyword("root").
pest_keyword("fruit").
pest_keyword("flower").
pest_keyword("yellowing").
pest_keyword("wilting").
pest_keyword("sticky").
pest_keyword("mold").
pest_keyword("spots").
pest_keyword("holes").
pest_keyword("crop").
pest_keyword("plant").
pest_keyword("tomato").
pest_keyword("maize").
pest_keyword("corn").
pest_keyword("cotton").
pest_keyword("cucumber").
pest_keyword("pepper").
pest_keyword("eggplant").
pest_keyword("lettuce").
pest_keyword("cabbage").
pest_keyword("damage").
pest_keyword("infestation").
pest_keyword("infested").
pest_keyword("chewed").
pest_keyword("control").
pest_keyword("spray").
pest_keyword("trap").
pest_keyword("webbing").
pest_keyword("honeydew").
pest_keyword("stunted").
pest_keyword("white").
pest_keyword("tiny").
pest_keyword("flying").

% Check if description is pest-related
is_pest_related(Description) :-
    atom_chars(Description, Chars),
    downcase_chars(Chars, LowerChars),
    atom_chars(LowerDesc, LowerChars),
    (   sub_atom(LowerDesc, _, _, _, Keyword), pest_keyword(Keyword), !
    ;   pest(PestName, _, _, symptoms(Symptoms), _, _, _, appearance(Appearance), _, _),
        (   member(Symptom, Symptoms),
            atom_string(SymptomAtom, Symptom),
            sub_atom(LowerDesc, _, _, _, SymptomAtom)
        ;   Appearance = appearance(color(Colors), size(Sizes)),
            (   member(Color, Colors), sub_atom(LowerDesc, _, _, _, Color)
            ;   member(Size, Sizes), sub_atom(LowerDesc, _, _, _, Size)
            )
        ),
        PestName \= none, !
    ).

% Tokenize description into words
tokenize_description(Description, Tokens) :-
    atom_chars(Description, Chars),
    split_chars(Chars, [], Tokens).

% Split characters into words (space-separated)
split_chars([], [], []) :- !.
split_chars([], Acc, [Word]) :- 
    Acc \= [], 
    atom_chars(Word, Acc), !.
split_chars([C|Rest], Acc, Tokens) :-
    char_type(C, space),
    Acc \= [],
    atom_chars(Word, Acc),
    split_chars(Rest, [], RestTokens),
    Tokens = [Word|RestTokens], !.
split_chars([C|Rest], [], Tokens) :-
    char_type(C, space),
    split_chars(Rest, [], Tokens), !.
split_chars([C|Rest], Acc, Tokens) :-
    split_chars(Rest, [C|Acc], Tokens).

% Downcase a list of characters
downcase_chars([], []).
downcase_chars([C|Rest], [LC|LowerRest]) :-
    downcase_atom(C, LC),
    downcase_chars(Rest, LowerRest).

% Score a pest based on description tokens
score_pest(Pest, Tokens, Score) :-
    pest(Pest, crops(Crops), _, symptoms(Symptoms), _, _, _, appearance(Appearance), _, _),
    % Symptom matches (weight: 0.4 per match)
    bagof(0.4, (
        member(Token, Tokens),
        member(Symptom, Symptoms),
        atom_string(SymptomAtom, Symptom),
        sub_atom(Token, _, _, _, SymptomAtom)
    ), SymptomScores, []),
    sum_list(SymptomScores, SymptomTotal),
    % Crop matches (weight: 0.2 per match)
    bagof(0.2, (
        member(Token, Tokens),
        member(Crop, Crops),
        sub_atom(Token, _, _, _, Crop)
    ), CropScores, []),
    sum_list(CropScores, CropTotal),
    % Appearance matches (color, size; weight: 0.2 per match)
    Appearance = appearance(color(Colors), size(Sizes)),
    bagof(0.2, (
        member(Token, Tokens),
        (   member(Color, Colors), sub_atom(Token, _, _, _, Color)
        ;   member(Size, Sizes), sub_atom(Token, _, _, _, Size)
        )
    ), AppearanceScores, []),
    sum_list(AppearanceScores, AppearanceTotal),
    % Total score
    Score is SymptomTotal + CropTotal + AppearanceTotal.

% Analyze description and find top pests
analyze_description(Description, Result) :-
    % Sanitize input
    atom_chars(Description, Chars),
    include(safe_char, Chars, SafeChars),
    atom_chars(SanitizedDesc, SafeChars),
    % Check description length (max 1000 chars)
    atom_length(SanitizedDesc, Length),
    Length =< 1000, !,
    % Check if description is empty
    (   SanitizedDesc \= '' ->
        % Check if pest-related
        (   is_pest_related(SanitizedDesc) ->
            tokenize_description(SanitizedDesc, Tokens),
            findall(pest_score(Pest, Score), (
                pest(Pest, _, _, _, _, _, _, _, _, _),
                score_pest(Pest, Tokens, Score),
                Score > 0.3
            ), PestScores),
            sort(2, @>=, PestScores, SortedScores),
            take(3, SortedScores, TopPests),
            (   TopPests \= [] ->
                TopPests = [pest_score(LikelyPest, TopScore)|_],
                generate_report(SanitizedDesc, LikelyPest, TopScore, TopPests, Report, ReportPath),
                user_guidance(Guidance),
                Result = result(pest(LikelyPest), report(Report), pests(TopPests), report_path(ReportPath), user_guidance(Guidance))
            ;   user_guidance(Guidance),
                Result = result(pest(none), report('No pests identified with sufficient confidence. Try including symptoms (e.g., yellowing leaves) or crops (e.g., tomato).'), pests([]), report_path('None'), user_guidance(Guidance))
            )
        ;   user_guidance(Guidance),
            Result = result(pest(none), report('This doesn\'t seem pest-related. Try including symptoms or crops.'), pests([]), report_path('None'), user_guidance(Guidance))
        )
    ;   user_guidance(Guidance),
        Result = result(pest(none), report('Description cannot be empty.'), pests([]), report_path('None'), user_guidance(Guidance))
    ).
analyze_description(Description, Result) :-
    atom_length(Description, Length),
    Length > 1000,
    user_guidance(Guidance),
    Result = result(pest(none), report('Description exceeds maximum length of 1000 characters.'), pests([]), report_path('None'), user_guidance(Guidance)).

% Safe characters for sanitization
safe_char(C) :- char_type(C, alnum); member(C, [' ', ',', '.', '-', '\'']).

% Take first N elements from a list
take(N, List, Taken) :- 
    length(Taken, N), 
    append(Taken, _, List), !.
take(_, List, List).

% Generate user guidance
user_guidance([
    'For better accuracy, include details like:',
    '- Symptoms (e.g., yellow leaves, holes, sticky residue)',
    '- Crops affected (e.g., tomato, maize)',
    '- Pest traits (e.g., color, size, flying)',
    'Example: My tomato plants have yellowing leaves and tiny white bugs.',
    'Type "help" to see this guidance again, or "exit" to quit.'
]).

% Generate report and save to file
generate_report(Description, Pest, Confidence, TopPests, Report, ReportPath) :-
    % Generate unique ID (use timestamp)
    get_time(Time),
    format_time(atom(ID), '%Y%m%d%H%M%S%3f', Time),
    atom_concat('reports/pest_report_', ID, BasePath),
    atom_concat(BasePath, '.txt', ReportPath),
    % Build report
    pest(Pest, crops(Crops), regions(Regions), symptoms(Symptoms), control_measures(Control), life_cycle(LifeCycle),
         economic_impact(Impact), environmental_conditions(Env), appearance(Appearance), synonyms(Synonyms)),
    format(string(Report), 
           'Pest Identification Report\n\nIdentified Pest: ~w\nDescription: ~w\nConfidence: ~2f\n\nDetails:\n' +
           '  Crops: ~w\n  Regions: ~w\n  Symptoms: ~w\n  Control Measures:\n' +
           '    Chemical: ~w\n    Biological: ~w\n    Cultural: ~w\n' +
           '  Life Cycle: ~w\n  Economic Impact: ~w\n  Environmental Conditions:\n' +
           '    Temperature: ~w\n    Humidity: ~w\n    Soil Type: ~w\n' +
           '  Appearance:\n    Color: ~w\n    Size: ~w\n  Synonyms: ~w\n\n' +
           'Other Possible Pests:\n~w',
           [Pest, Description, Confidence, Crops, Regions, Symptoms,
            Control.chemical, Control.biological, Control.cultural,
            LifeCycle, Impact, Env.temperature, Env.humidity, Env.soil_type,
            Appearance.color, Appearance.size, Synonyms, TopPests]),
    % Save report
    (   ensure_directory('reports'),
        setup_call_cleanup(
            open(ReportPath, write, Stream),
            write(Stream, Report),
            close(Stream)
        )
    ->  true
    ;   Report = 'Error: Failed to save report.', ReportPath = 'None'
    ).

% Print formatted result
print_result(result(pest(Pest), report(Report), pests(Pests), report_path(ReportPath), user_guidance(Guidance))) :-
    write('\n====================================\n'),
    write('=== Pest Identification Result ===\n'),
    write('====================================\n\n'),
    format('Identified Pest: ~w\n', [Pest]),
    (   Pests \= [] ->
        write('\nPossible Pests:\n'),
        print_pests(Pests)
    ;   write('\nNo pests identified.\n')
    ),
    format('\nDetailed Report (Saved to: ~w):\n', [ReportPath]),
    write('------------------------------------\n'),
    write(Report), write('\n'),
    write('------------------------------------\n'),
    write('\nUser Guidance:\n'),
    print_guidance(Guidance),
    (   Pests \= [] ->
        write('\nConfidence Scores (for visualization):\n'),
        print_pests(Pests)
    ;   write('\nNo chart data available.\n')
    ),
    write('====================================\n').

print_pests([]).
print_pests([pest_score(Pest, Score)|Rest]) :-
    Percent is Score * 100,
    format('- ~w (~0f%)\n', [Pest, Percent]),
    print_pests(Rest).

print_guidance([]).
print_guidance([G|Rest]) :-
    format('- ~w\n', [G]),
    print_guidance(Rest).

% Display welcome message and examples
welcome :-
    write('====================================\n'),
    write('Welcome to the Pest Identification System!\n'),
    write('====================================\n\n'),
    write('Enter a description of the pest issue to identify potential pests.\n'),
    write('Type "exit" to quit or "help" to see guidance.\n\n'),
    write('Example Descriptions:\n'),
    write('- My tomato plants have yellowing leaves and sticky residue.\n'),
    write('- Small white flying insects on my cucumber plants.\n'),
    write('- Holes in cabbage leaves and green worms.\n'),
    write('- Tiny red mites on pepper plant stems with webbing.\n\n').

% Main loop for continuous prompting
main_loop :-
    welcome,
    main_loop_inner.

main_loop_inner :-
    write('Enter description (or type "exit" or "help"): '),
    flush_output,
    read_line_to_string(user_input, Input),
    % Validate input
    (   Input \= end_of_file,
        atom_chars(Input, Chars),
        forall(member(C, Chars), char_type(C, ascii)) ->
        (   Input = 'exit' ->
            write('Exiting Pest Identification System.\n'),
            halt
        ;   Input = 'help' ->
            user_guidance(Guidance),
            write('\nUser Guidance:\n'),
            print_guidance(Guidance),
            main_loop_inner
        ;   Input \= '' ->
            analyze_description(Input, Result),
            print_result(Result),
            main_loop_inner
        ;   write('Error: Description cannot be empty. Please try again.\n'),
            main_loop_inner
        )
    ;   write('Error: Invalid input (non-ASCII or EOF). Please enter a valid description.\n'),
        main_loop_inner
    ).

% Entry point
:- initialization(main).

% CLI argument support
main :-
    current_prolog_flag(argv, Argv),
    (   Argv = [DescAtom|_] ->
        atom_string(DescAtom, Description),
        atom_chars(Description, Chars),
        forall(member(C, Chars), char_type(C, ascii)),
        Description \= '',
        write('====================================\n'),
        write('=== Pest Identification System ===\n'),
        write('====================================\n\n'),
        analyze_description(Description, Result),
        print_result(Result)
    ;   main_loop
    ).