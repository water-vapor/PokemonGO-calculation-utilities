# PokemonGO Calculation Utilities
Performs further analysis of your Pokemon data with Pokemon information from pokeiv.net, requires json file from pokeiv.net to read your pokemon data. 
Only total stardust cost is implemented, since this information may not be easily obtained by existing tools. 

Steps to obtain Pokemon json file:

1. Open Chrome, goto pokeiv.net and login
2. Open console and type in `angular.element('[ng-controller=AppCtrl]').scope().pokemons`
3. Right click on the array object returned and choose "save as global variable"
4. There should be a variable name like `temp1` returned
5. Type in `copy(temp1)` in the console, or replace `temp1` if it is not the same name as yours
6. Open a text editor and paste, save it to a new file, and remember its path

Usage:

- Stardust cost in total:

1. `cd` to the path you download this script along with `PKMBase.csv`
2. `python pkmgo_calc.py -f /path/to/yourfile.json -s`

