# test equation 1: 2NaOH + H2SO4 -> Na2SO4 + 2H2O

if __name__ == '__main__':  # the main runnable dunder
    pass

# take the user's input
chemical_equation = input('Please enter a chemical equation.\n')

# get rid of all the spaces in the code
chemical_equation = chemical_equation.replace(' ', '')

# begin by splitting the chemical equation into products and reactants:
[reactants, products] = chemical_equation.split('->', 2)

# split the products and reactants up into lists of strings representing each species
reactants = reactants.split('+')
products = products.split('+')
num_reactants = len(reactants)
num_products = len(products)

# combine the products and reactants lists into a species list
species = reactants + products

# separate the coefficients and species into two separate lists
# define two empty lists to store coefficients and the coefficientless species
coefficients = []
temp = []

for s in species:  # iterate over all the species
    number = ''  # make an empty temp number string

    while s[0].isnumeric() or s[0] == '.':  # check to see if the first character in the string is numeric or decimal
        number += s[0]  # add the first character of the string to a temp number string
        s = s[1:]  # remove the first character from the string
    if len(number) == 0:
        number = 1  # if there's no coefficient, set the temp number string to 1

    temp.append(s)  # add the coefficientless species to a temp list

    if number == 1:
        coefficients.append(1)  # if the coefficient is 1, append 1 to the list
    elif float(number).is_integer():
        coefficients.append(int(number))  # if the coefficient is an integer, append it to the list as an int
    else:
        coefficients.append(float(number))  # if the coefficient is a float, append it to the list as a float

species = temp

# split up the product and reactant coefficients
reactant_coeffs = coefficients[0:num_reactants]
product_coeffs = coefficients[-num_products:]

# split up the product and reactant coefficientless species
reactants = species[0:num_reactants]
products = species[-num_products:]

print('Reactants: ' + str(list(zip(reactant_coeffs, reactants))))
print('Products:  ' + str(list(zip(product_coeffs, products))))
