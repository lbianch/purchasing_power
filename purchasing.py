#!/usr/bin/env python3
from JSON import read_json
from TVM import mortgage_payment as MP

mortgage_years = 30
mortgage_rate = 3.49 # APR, average for Nov 2016
down_payment = 0.2 # As percentage of housing price


def get_housing(housing_file):
    if housing_file.lower().startswith("rent"):
        return {state: int(12 * rent) for state, rent in read_json(housing_file).items()}
    if housing_file.lower().startswith("hous"):
        return {state: int(12 * MP(mortgage_years, mortgage_rate, price * (1.0 - down_payment)))
                   for state, price in read_json(housing_file).items()}
    raise ValueError("Housing file name must start with 'rent' or 'hous'")


def convert_to_csv(housing_file, outputFile='data.csv'):
    housing = get_housing(housing_file)
    states = read_json('states.json')
    pph = read_json('householdsize.json')
    income = read_json('income.json')
    value = read_json('value.json')

    with open(outputFile, 'w', encoding='utf-8') as out:
        out.write('State,Housing,Household Size,Income,Value\n')
        for s in sorted(states):
            info = [states[s], housing[s], pph[s], income[s], value[s]]
            out.write(','.join(map(str, info)) + '\n')


if __name__ == '__main__':
    convert_to_csv('housingprices.json', 'mortgage.csv')
    convert_to_csv('rent.json', 'rent.csv')
