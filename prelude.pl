% :- dynamic datapoint(Id).
% :- dynamic datapoint_description(Id, Description).
% :- dynamic datapoint_value(Id, Value).
% :- dynamic datapoint_unit(Id, Unit).
% :- dynamic datapoint_magnitude(Id, Magnitude).
% :- dynamic datapoint_interval_start(Id, Start).
% :- dynamic datapoint_interval_end(Id, End).
% :- dynamic datapoint_point_in_time(Id, Time).
% :- dynamic datapoint_name(Id, Name).
% :- dynamic datapoint_source_url(Id, URL).
% :- dynamic datapoint_source_description(Id, Description).
:- dynamic datapoint/2.
:- dynamic datapoint_description/2.
:- dynamic datapoint_value/2.
:- dynamic datapoint_unit/2.
:- dynamic datapoint_magnitude/2.
:- dynamic datapoint_interval_start/2.
:- dynamic datapoint_interval_end/2.
:- dynamic datapoint_point_in_time/2.
:- dynamic datapoint_name/2.
:- dynamic datapoint_source_url/2.
:- dynamic datapoint_source_description/2.

datapoint_interval_valid(Id) :-
   datapoint_interval_start(Id, Start),
   datapoint_interval_end(Id, End),
   Start < End.

cagr(Year1, Year2, Value1, Value2, CAGR) :-
    CAGR is ((Value2 / Value1) ** (1 / (Year2 - Year1)) - 1) * 100.