import logging
import os
import re
from logging import info

import pandas as pd


class CensusTransformer:
    """
    Transforms a census file into a population.csv file.
    """

    def get_location(self, file):
        """
        Reads the file and gets back the name of the location.
        :pre: Must be a Canadian census file in standard format
        :return:
        """
        return pd.read_csv(file, encoding="ISO-8859-1", nrows=1).columns[3]

    def __init__(self):
        pass

    def for_each_file(self, action, directory: str, output: str) -> None:
        """
        Takes all files in the subdirectory and converts them to a single population file.
        :param directory:
        :return:
        """
        df = None
        n = 0
        for file in os.listdir(directory):
            next_file = directory + "/" + file
            if os.path.isfile(next_file):
                next_df = action(next_file)
                if n == 0:
                    df = next_df
                else:
                    df = df.append(next_df)
                n += 1
        df.to_csv(output, index=False, header=True)

    def to_population_attributes(self, file: str) -> pd.DataFrame:
        """
        Converts the file to a dataframe suitable for area_attributes.csv
        :param file: The file to transform
        :return:
        """

        # Read the file.
        # The first row is metadata.
        df = pd.read_csv(file, encoding="ISO-8859-1", skiprows=1);

        # Narrow down to the information we need.
        df = df[df['Topic'].notna()]
        num_households = int(df[
                                 df['Topic'].str.match("Household and dwelling characteristics")
                                 & df['Characteristics'].str.match(
                                     r".*Total - Private households by household size - 100% data")].Total.iloc[0]
                             )

        marital_df = df[df['Topic'].str.match("Marital status")]
        total_partnerable_male = float(marital_df[marital_df['Characteristics'].str.match(
            r"Total - Marital status for the population aged 15 years and over - 100% data")].Male.iloc[0])
        total_partnerable_female = float(marital_df[marital_df['Characteristics'].str.match(
            r"Total - Marital status for the population aged 15 years and over - 100% data")].Female.iloc[0])
        num_partnered_male = int(
            marital_df[marital_df['Characteristics'].str.match(r".*Married or living common law")].Male.iloc[0])
        num_partnered_female = int(
            marital_df[marital_df['Characteristics'].str.match(r".*Married or living common law")].Female.iloc[0])
        p_partnered_male = num_partnered_male / total_partnerable_male if total_partnerable_male > 0 else 0
        p_partnered_female = num_partnered_female / total_partnerable_female if total_partnerable_female > 0 else 0

        # Discern whether these are rural or urban properties.
        location = self.get_location(file)
        is_rural = False
        if re.match(r".*Rural Municipality.*", location) or re.match(r".*Municipal district.*", location):
            is_rural = True

        # Get household distributions.
        households_df = df[
            df['Topic'].str.match("Household and dwelling characteristics") & df['Characteristics'].str.match(
                r".*\d.*persons?")]
        households_sizes = [int(x.strip()) for x in households_df.Total]
        households_size_labels = ["Household Size " + str(x) for x in range(1, 5)] + ["Household Size 5+"]

        # Retain any manually added properties.
        manual_attr_df = df[df['Topic'].str.match("Manual Attribute")]
        manual_attr_keys = manual_attr_df[df['Topic'].str.match("Manual Attribute")]['Characteristics'].tolist()
        manual_attr_values = manual_attr_df[df['Topic'].str.match("Manual Attribute")]['Total'].tolist()

        # Stitch together
        result = pd.DataFrame({
            'locationId': location,
            'attribute': [
                             'Number of Households',
                             'P(Partnered Male)',
                             'P(Partnered Female)',
                             'Is Rural Population',
                         ]
                         + households_size_labels
                         + manual_attr_keys,
            'value': [
                         int(num_households),
                         p_partnered_male,
                         p_partnered_female,
                         is_rural
                     ]
                     + households_sizes
                     + manual_attr_values
        })
        return result

    def to_populations(self, file: str) -> pd.DataFrame:
        """
        Converts the file to a dataframe suitable for populations.csv
        :param file: The file to transform
        :return:
        """

        # Read the file.
        # The first row is metadata.
        df = pd.read_csv(file, encoding="ISO-8859-1", skiprows=1)

        # Narrow down to the information we care about (i.e. age band data)
        df = df[df['Topic'].notna() & df['Topic'].str.match('Age characteristics')]
        df = df.rename(columns={"Characteristics": "AgeBand", "Total": "count"})

        # Calculate five-year age bands.
        df = df[df["AgeBand"].str.match(r".+?(\d+) to (\d+)\D*")]
        df['startAge'] = df["AgeBand"].str.replace(r".+?(\d+) to (\d+)\D*", r"\1").astype(int)
        df['endAge'] = df["AgeBand"].str.replace(r".+?(\d+) to (\d+)\D*", r"\2").astype(int) + 1
        df['count'] = df['count'].apply(pd.to_numeric)
        df['count'] = df['count'].astype(int)
        df = df[df["startAge"] + 5 == df["endAge"]]
        df = df[["startAge", "endAge", "count"]]

        # Append useful information.
        df["locationId"] = self.get_location(file)
        df["segment"] = "All"

        # Done.
        return df


if __name__ == "__main__":
    """
    An example of how to use this class and its methods. Make sure to run this in your own file. 
    You can create a sandbox/ directory, which should be ignored by git.
    """
    logging.basicConfig(level=logging.INFO)
    logging.info('Logging set to appropriate level.')

    # Example locations.
    input = "data/BrooksAB/rawInputs/"
    output = "data/BrooksAB/"

    transformer = CensusTransformer()
    transformer.for_each_file(transformer.to_population_attributes, input, output + "/population_attributes.csv")
    transformer.for_each_file(transformer.to_populations, input, output + "/populations.csv")

    info("Some general notes:")
    info(
        "- Population age brackets DO NOT add up to the total number of people. Stats Canada seems to do this to protect identities (rightly so).")
