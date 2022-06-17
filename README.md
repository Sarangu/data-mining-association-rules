# CS6111 Advanced Database Systems - Data-mining-association-rules
# Team Members
Aishwarya Sarangu (als2389)

Rishabh Gupta (rg3334)

# Submitted Files
* **integrated_dataset.csv:** CSV File containing the Integrated dataset
* **run.py:** Script to generate frequent itemsets and high-confidence association rules
* **example-run.txt:** File containing output of the compelling sample run, listing all the frequent itemsets and association rules for that run

# Installing Dependencies

```
$ sudo apt-get update
$ pip3 install pandas
```

# Running the program

```
$ ./run.py <integrated dataset filename> <minimum support> <minimum confidence>
```

# Integrated Dataset

* In order to generate ```integrated_dataset.csv```, the following NYC Open Data set has been used: 

  https://data.cityofnewyork.us/Public-Safety/NYPD-Arrest-Data-Year-to-Date-/uip8-fykc
* The original file has been trimmed to retain the following fields that are relevant to our anaylsis:
   * PD_DESC	- Description of internal classification
   * OFNS_DESC - Description of internal classification (more general category than PD description)
   * LAW_CAT_CD - Level of offense: felony, misdemeanor, violation
   * ARREST_BORO - Borough of arrest. B(Bronx), S(Staten Island), K(Brooklyn), M(Manhattan), Q(Queens)
   * AGE_GROUP - Perpetrator’s age within a category
   * PERP_SEX - Perpetrator’s sex description
   * PERP_RACE - Perpetrator's race description
* The NYPD Arrest Data (Year to Date) provides a detailed insight into pattern of crime across NYC. It captures granular details, ranging from type of crime to age group, race, neighborhood, etc. There is tremendous potential to gain interesting and useful insights form this data. Identifying crime patterns can not only aid in improving public safety but can also help prevent such crimes by ensuring that commonly occurring patterns are not repeated. The goal of this anlysis is to identify such patterns and draw meaningful conclusions that can potentially help with crime control.
* The following changes have been made to the retained fields:
  * LAW_CAT_CD - Values in this field have been expanded to provide a better understanding of the level of offense
  * ARREST_BORO - Abbrevaitions have been expanded to better represent borough of arrest

# Project Design

The project has essentially one file called ```run.py``` which has all the logic of generating frequent itemsets and high-confidence association rules.

The code primarily contains two core procedures whose functionalities are as follows:
* **calculate_frequent_itemsets:** This function takes the data and a minimum support value and generates frequent itemsets that cross the minimum support threshold. The frequent itemsets is stored as a global dictionary containing <itemset (as frozenset), support> pairs. First, individual items are extracted from data. Following this, the first set of candidates **C<sub>1</sub>** is generated (individual items) and those that pass the support threshold are added to the frequent itemset **L<sub>1</sub>**. The itemset **L<sub>1</sub>** is also added to the global frequent itemsets dictionary. We then start iterating to generate itemsets of length 2 to the maximum possible length i.e. the number of unique items in the dataset and perform the following:
  * Create a new candidate set **C<sub>k</sub>** from previous frequent itemset **L<sub>k-1</sub>**
  * Prune those candidates from **C<sub>k</sub>** whose k-1 length subsets aren't present in **L<sub>k-1</sub>**
  * Following the pruning step, generate a new frequent itemset **L<sub>k</sub>** by adding candidates whose support is higher than the support threshold
  * Add frequent itemsets generated in each run to the global frequent itemsets dictionary
  * Function returns when no frequent itemset is generated in an iteration

* **calculate_high_conf_rules:** This function takes the frequent itemsets and a minimum confidence value and generates association rules with confidence higher than the minimum confidence threshold. The rules have exactly one item on the right side and at least one item on the left side, where the right-side item does not appear on the left side. We start iterating through the frequent itemsets dictionary and perform the following for each itemset **I**:
  * Generate a list **S** of **k-1** length subsets of itemset **I** where **k** is the length of itemset **I**
  * Every subset in the list **S** is itself an itemset **A**. Compute confidence of the rules which are of the format **A => B** where **B = I - A** by dividing the support of **I** by the support of **A**
  * Note that we do not have to go through the dataset again as the support values of the itemsets of interest are already present in the frequent itemsets dictionary
  * Return those rules whose confidence is higher than the minimum confidence threshold

# Observations
Upon observing the [example-run.txt](https://github.com/rishabh20/data-mining-association-rules/blob/main/example-run.txt), we note that there are quite a few association rules that provide useful insights into the crime patterns in NYC. An observation worth noting with regards to the data is that majority of the offenders are younger males. We can also argue that there is some sort of bias in data collection, since many of the association rules seem to be associated with Black males. Although this data is collected based on true incidents, we could argue that more incidents are recorded when the perpetrator of crime is Black/Hispanic, thus leading to racial profiling. Upon examining a few of the association rules, we draw the following observations:
  * ['CHILD, ENDANGERING WELFARE'] => ['SEX CRIMES'] (Conf: 100.000000%, Supp: 1.225025%)

     From this association rule, we see that most crimes endangering children are Sex Crimes, which is quite alarming. At the same time, this is an important piece of information that could        help reduce such crimes.
  * Age-wise Comparative study:
  
    ['<18'] => ['M'] (Conf: 82.395833%, Supp: 2.543294%)
  
    ['18-24'] => ['M'] (Conf: 81.900452%, Supp: 15.247545%)
    
    ['25-44'] => ['M'] (Conf: 82.492966%, Supp: 47.132926%)
    
    ['45-64'] => ['M'] (Conf: 84.869969%, Supp: 16.704714%)
    
    ['65+'] => ['M'] (Conf: 85.813751%, Supp: 1.268110%)

    We observe that the proportion of male criminals across different age groups takes the form of a normal distribution (approx.), with the crime rate gradually increasing and peaking at '25-44', and       again reducing as they age.
  * Despite the support level being quite low, we found that there are very few female offenders when compared to male offenders in NYC. Due to this, we were unable   to make much inferences regarding female offenders. Similarly, another pattern observed was the race of perps. Majority of the perpetrators are Black/Hispanic,       which speaks to the population demographic of NYC. For instance, Asian/Pacific Islanders are very few in number, and consequently, the number of crime records involving them as the perpetrtor is     also low in that instance. 
  * ['25-44', 'WHITE'] => ['M'] (Conf: 80.124963%, Supp: 5.195265%)
  
    ['45-64', 'WHITE'] => ['M'] (Conf: 85.261525%, Supp: 2.473844%)

    From these two rules, we observe how White male perps become half in number when we move from the age group '25-44' to '45-64'. This could be a key factor in               identifying perps in many situations.

  * ['Brooklyn', 'DANGEROUS WEAPONS'] => ['BLACK'] (Conf: 80.149078%, Supp: 1.313767%)
  
    ['Brooklyn', 'DANGEROUS WEAPONS', 'M'] => ['BLACK'] (Conf: 80.709343%, Supp: 1.199946%)

    ['DANGEROUS WEAPONS', 'Felony', 'M'] => ['WEAPONS POSSESSION 1 & 2'] (Conf: 83.047809%, Supp: 2.680908%)

    ['Brooklyn', 'DANGEROUS WEAPONS', 'Felony', 'M'] => ['WEAPONS POSSESSION 1 & 2'] (Conf: 84.527929%, Supp: 1.099629%)

    The crimes related to 'Dangerous Weapons' are dominant in Brooklyn, compared to any other borough, and the statistics below support the hypothesis further:

    **Dangerous Weapon Crimes = 7206**

    **In Brooklyn = 2549**

    **In Bronx: 1748**

    This is a very important insight, since it could potentially help with weapon control in particular areas, and thus help prevent/reduce crime in this category.  
   
   There are several other observations, but having highlighted the salient ones, we can state that these association rules have been quite helpful in bringing important crime patterns to light. Observing and understanding them could potentially lead to reduction in crime, if steps are taken to avoid situations described by these association rules.


    


# Reference Papers

* [Fast Algorithms for Mining Association Rules](http://www.cs.columbia.edu/~gravano/Qual/Papers/agrawal94.pdf)
