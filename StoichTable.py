# test equation 1: 2H2 + O2 -> 2H2O
# test equation 2: A + 2B -> 3C + 4D
# test equation 3: A + B -> C + D
# test equation 4: 0.5A + B -> 2C + 0.25D
# test equation 5: 2NaOH + H2SO4 -> Na2SO4 + 2H2O


# returns a list of coefficients from a list of chemical species
def get_coefficients(species):
    coefficients = []
    for s in species:  # iterate over all strings
        number = ''
        while s[0].isnumeric() or s[0] == '.':  # iterate over all characters until a letter is reached
            number += s[0]  # add the digit (or decimal) to the overall number
            s = s[1:]  # remove the first character of the string
        if len(number) < 1:  # if the number doesn't have a length, this implies no coefficient, so append 1
            coefficients.append(1)
        else:
            if '.' in number:
                coefficients.append(
                    float(number))  # if there is a decimal in the number convert the number to a float and append it
            else:
                coefficients.append(int(number))  # otherwise convert it to an int and append it
    return coefficients


# remove the coefficient from the beginning of each item in a list of chemical species
def remove_coefficients(species):
    no_coefficient_species = []
    for s in species:
        while not s[0].isalpha():
            s = s[1:]
        no_coefficient_species.append(s)
    return no_coefficient_species


# converts each number in a list of strings to a subscript number
def convert_subscripts(species):
    converted_species = []
    for s in species:
        s = str(s).translate(str.maketrans("0123456789", "₀₁₂₃₄₅₆₇₈₉"))
        converted_species.append(s)
    return converted_species


# converts a list of species and a list of coefficients into an equation
def convert_to_equation_half(species, coefficients):
    string = ''
    for index in range(len(species) - 1):
        if coefficients[index] != 1:
            string += str(coefficients[index])
        string += str(species[index]) + ' + '
    if coefficients[-1] != 1:
        string += str(coefficients[-1])
    string += str(species[-1])
    return string


# makes a row of the stoich table as a list of strings per each column
# species is the chemical formula of the species
# symbol is the stoich table symbol (A, B, C, etc...)
# negative coefficient means reactant, positive coefficient means product
# contains is if the reactor contains some of the species at time = 0
def make_stoich_table_row(species: str, symbol: str, coefficient, contains: bool):
    # make the initial column string
    initial = 'F' + symbol + '0' if contains else '0'

    # make the change column string
    if coefficient == 1:
        change = '+FA0 · X'
    elif coefficient == -1:
        change = '-FA0 · X'
    else:
        change = str(coefficient) + 'FA0 · X' if coefficient < 0 else '+' + str(coefficient) + 'FA0 · X'

    # make the outlet column string
    if symbol == 'A':
        outlet = f'FA0 · (1-X)'
    elif coefficient == 1:
        outlet = f'FA0 · ({theta_string + symbol}+X)'
    elif coefficient == -1:
        outlet = f'FA0 · ({theta_string + symbol}-X)'
    elif coefficient < 0:
        outlet = f'FA0 · ({theta_string + symbol}{coefficient}X)'
    else:
        outlet = f'FA0 · ({theta_string + symbol}+{coefficient}X)'

    # make the concentration column string
    if symbol == 'A':
        concentration = f'CA = CA0 · (1-X) / (1+{epsilon_string}X)'
    elif coefficient == 1:
        concentration = f'C{symbol} = CA0 · ({theta_string + symbol}+X) / (1+{epsilon_string}X)'
    elif coefficient == -1:
        concentration = f'C{symbol} = CA0 · ({theta_string + symbol}-X) / (1+{epsilon_string}X)'
    elif coefficient < 0:
        concentration = f'C{symbol} = CA0 · ({theta_string + symbol}{coefficient}X) / (1+{epsilon_string}X)'
    else:
        concentration = f'C{symbol} = CA0 · ({theta_string + symbol}+{coefficient}X) / (1+{epsilon_string}X)'

    # return the list of column strings
    return [species, symbol, initial, change, outlet, concentration]


# makes a row of the stoich table as a list of strings per each column
# species is the chemical formula of the species
# symbol is the stoich table symbol (A, B, C, etc...)
# negative coefficient means reactant, positive coefficient means product
# contains is if the reactor contains some of the species at time = 0
def make_latex_stoich_table_row(species: str, symbol: str, coefficient, contains: bool):
    # make the species column string
    c1 = '$\\ch{' + species.translate(str.maketrans("₀₁₂₃₄₅₆₇₈₉", "0123456789")) + '}$'

    # make the symbol string
    c2 = symbol

    # make the initial column string
    c3 = '$F_{' + symbol + '0' + '}$' if contains else '0'

    # make the change column string
    if coefficient == 1:
        c4 = '$+F_{A0}X$'
    elif coefficient == -1:
        c4 = '$-F_{A0}X$'
    else:
        c4 = '$' + str(coefficient) + 'F_{A0}X$' if coefficient < 0 else '$+' + str(coefficient) + 'F_{A0}X$'

    # make the outlet column string
    if symbol == 'A':
        c5 = '$F_{A0}(1-X)$'
    elif coefficient == 1:
        c5 = '$F_{A0}(\\Theta_{' + symbol + '}+X)$'
    elif coefficient == -1:
        c5 = '$F_{A0}(\\Theta_{' + symbol + '}-X)$'
    elif coefficient < 0:
        c5 = '$F_{A0}(\\Theta_{' + symbol + '}' + str(coefficient) + 'X)$'
    else:
        c5 = '$F_{A0}(\\Theta_{' + symbol + '}+' + str(coefficient) + 'X)$'

    # make the concentration column string
    if symbol == 'A':
        c6 = '$C_{A}=C_{A0}\\frac{1-X}{1+\\varepsilon{}X}$'  # C_A = C_{A0} \frac{-X}{1+eX}
    elif coefficient == 1:
        c6 = '$C_{' + symbol + '}=C_{A0}\\frac{\\Theta_{' + symbol + '}+X}{1+\\varepsilon{}X}$'
    elif coefficient == -1:
        c6 = '$C_{' + symbol + '}=C_{A0}\\frac{\\Theta_{' + symbol + '}-X}{1+\\varepsilon{}X}$'
    elif coefficient < 0:
        c6 = '$C_{' + symbol + '}=C_{A0}\\frac{\\Theta_{' + symbol + '}' + str(coefficient) + 'X}{1+\\varepsilon{}X}$'
    else:
        c6 = '$C_{' + symbol + '}=C_{A0}\\frac{\\Theta_{' + symbol + '}+' + str(coefficient) + 'X}{1+\\varepsilon{}X}$'

    # make the row string
    return c1 + ' & ' + c2 + ' & ' + c3 + ' & ' + c4 + ' & ' + c5 + ' & ' + c6


if __name__ == '__main__':  # the main runnable, apparently you need this lmao who would've thunk
    pass


theta_string = '\u03b8'
epsilon_string = '\u03b5'

chemical_equation_string = input('Enter your chemical equation:\n')  # get the input chemical equation
starting_materials = input('Which of these materials are present at time t=0?\n'
                           'Please enter a sequence of 1\'s and 0\'s, where 1\'s indicate starting presence.\n')

chemical_equation_string = chemical_equation_string.replace(" ", "")  # get rid of all the spaces in the equation
two_sides = chemical_equation_string.split('->', 2)  # split the equation into reactants and products
reactants_list = two_sides[0].split('+')  # split all the reactants up by the + sign
products_list = two_sides[1].split('+')  # split all the products up by the + sign

reactants_coefficients = get_coefficients(reactants_list)  # get the coefficients of the reactants
products_coefficients = get_coefficients(products_list)  # get the coefficients of the products
reactants_list = remove_coefficients(reactants_list)  # remove the coefficients from the list of reactants
products_list = remove_coefficients(products_list)  # remove the coefficients from the list of products

# if the first coefficient of the reactants isn't 1, multiply all the values such that it becomes 1
if reactants_coefficients[0] != 1:
    scale_factor = 1 / reactants_coefficients[0]  # get the scale factor
    for i in range(len(reactants_list)):
        value = reactants_coefficients[i] * scale_factor
        reactants_coefficients[i] = int(value) if value.is_integer() else value
    for i in range(len(products_list)):
        value = products_coefficients[i] * scale_factor
        products_coefficients[i] = int(value) if value.is_integer() else value

reactants_list = convert_subscripts(reactants_list)
products_list = convert_subscripts(products_list)

print('\nOverall reaction (scaled for first reactant):')
reactants_string = convert_to_equation_half(reactants_list, reactants_coefficients)
products_string = convert_to_equation_half(products_list, products_coefficients)
overall_string = reactants_string + ' -> ' + products_string
print(overall_string)

# convert all of the reactant coefficients to negative values
for i in range(len(reactants_list)):
    reactants_coefficients[i] *= -1

species_list = reactants_list + products_list  # add the reactants list and products list together
coefficient_list = reactants_coefficients + products_coefficients  # add the reactants coefficients list and products coefficients list together

# create a list of booleans determining if a species is present in the reactor at time t=0
starting_materials = starting_materials.ljust(len(species_list), '0')  # pad the string with extra 0's in case not enough integers were provided
presence_booleans = []
for i in range(len(starting_materials)):
    if starting_materials[i] == str(1):
        presence_booleans.append(True)
    elif starting_materials[i] == str(0):
        presence_booleans.append(False)

# make the stoich rows
stoich_rows = []
for i in range(len(species_list)):
    species_symbol = chr(ord('@') + i + 1)
    stoich_rows.append(make_stoich_table_row(species_list[i], species_symbol, coefficient_list[i], presence_booleans[i]))

# print out the stoich table
print('_' * 119)
print(
    f'| {"Species":<10} | {"Symbol":<10} | {"Initial":<10} | {"Change":<20} | {"Outlet":<20} | {"Concentration":<30} |')
for row in stoich_rows:
    print(f'|_{"_" * 10}_|_{"_" * 10}_|_{"_" * 10}_|_{"_" * 20}_|_{"_" * 20}_|_{"_" * 30}_|')
    print(f'| {row[0]:<10} | {row[1]:<10} | {row[2]:<10} | {row[3]:<20} | {row[4]:<20} | {row[5]:<30} |')
print(f'|_{"_" * 10}_|_{"_" * 10}_|_{"_" * 10}_|_{"_" * 20}_|_{"_" * 20}_|_{"_" * 30}_|')

print('\nLaTeX:\n')
# make the actual latex table
latex_table_string = '\\begin{tabular}{|c|c|c|c|c|c|}\n\t\\hline\n'
latex_table_string += '\tSpecies & Symbol & Initial & Change & Outlet & Concentration\\\\\n\t\\hline\n'
for i in range(len(species_list)):
    species_symbol = chr(ord('@') + i + 1)
    latex_table_string += '\t' + make_latex_stoich_table_row(species_list[i], species_symbol, coefficient_list[i], presence_booleans[i])
    latex_table_string += '\\\\\n\t\\hline\n'
latex_table_string += '\\end{tabular}'
print(latex_table_string)
