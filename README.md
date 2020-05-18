# Regional COVID-19 Response Simulation (RCRS)
![Luminesim Logo](./LUMINESIM-Logo-Docs.png)</br>
  
  
(c) *Luminesim Simulation and Analytics*, 2020.

Please consider contributing to our [GoFundMe campaign.](http://gf.me/u/x28ahx) For more information, contact us via [our website](http://www.luminesim.com/contact-us)


## Important:
**By using this simulation you understand and acknowledge that no simulation is a perfect representation of the real world. Local conditions, nuances, and phenomena not captured in the simulation mean the tool may deviate from real-world outcomes. This tool is therefore for your information only, should be run several times to see representative outcomes, and should be interpreted only after reading and understanding its documentation. Its results should only be used after planning for local conditions, consulting local authorities and stakeholders, and gaining the consent of local residents and organizations. Under no circumstances should you change local COVID-19 strategies without first consulting and gaining the consent of provincial and federal health authorities.**

## Overview
The Regional COVID-19 Response Simulation is a simulation of COVID-19 spread designed to be rapidly deployed for smaller towns, cities, and surrounding rural areas responding to an outbreak. The simulation is designed to test strategies that may reduce COVID-19 spread and to explore the consequences of removing existing strategies (e.g. removing social distancing, reopening schools, etc.). As small communities by definition have small populations, its results can vary based on the exact community members and locations that are infected. The simulation's results should therefore be used as guides only: it should not be used to predict the exact date that COVID-19 will enter the population, nor exact dates on which it will leave, nor the exact damage it will cause. The simulation is tailored to be quickly deployed in the Canadian context, but can be altered for use in other countries.

## Key Takeaway
This simulation helps identify strategies that a small community could employ to reduce the human impact of COVID-19 as local conditions evolve. It does not predict the timing nor the exact length of a COVID-19 outbreak. 

## How Does This Work?
This is an [agent based simulation.](https://en.wikipedia.org/wiki/Agent-based_model) In agent based simulations, people are distinct entities (agents) who have attributes and change over time. In this simulation, they have an age, a sex, a home, workplace or school, non-work places, and family members. People can become infected with COVID-19 and be either asymptomatic or symptomatic. Symptomatic people may be admitted to hospital and may recover or die. People also move between locations containing other people (e.g. work): if infected, they can contaminate surfaces and may expose others to COVID-19 through speaking interactions. The simulation is usually run for a small number of months. In that time, interventions (e.g. social distancing) can be implemented or removed, which allows other outcomes to be forecast (e.g. number of new infections).

## What Does the Simulation Include?
Simulations are designed to adapt to new information and conditions. The simulation therefore includes a core set of critical mechanics, which are readily expanded and tuned based on community needs. To summarize:
- People go to daytime activities (e.g. school, work, weekend activity), evening activities (e.g. shops), and then home. 
- People talk with others at those places. Infection can be spread during conversation
- People touch surfaces at those places and may contaminate them if sick. A person can be infected after touching a contaminated surface
- Interventions, like wearing masks, sanitizing surfaces, social distancing, and closing schools and non-essential businesses can reduce the likelihood of infection

Please read the rest of this document to ensure you understand the full list of features the simulation includes and does not include.

## Improvements & Contributions
We welcome new data, bug reports, corrections, and suggestions for improvement. Please visit www.luminesim.com/rcrs to contribute.

## Who Are You?
[Luminesim](http://www.luminesim.com) is a two-person simulation and analytics team. We have extensive history in health simulation, but we are not ourselves epidemiologists nor COVID-19 experts. We [welcome and seek input from these groups](http://www.luminesim.com/rcrs), especially those already familiar with agent-based simulation and modeling. Our goal is simply to provide a locally-tailored policy testing tool that can assist smaller communities already working with provincial and federal health authorities to address the impact of  COVID-19. **This means that under no circumstances should any community change local COVID-19 strategies without first consulting and gaining the consent of provincial and federal health authorities.**

## How Do I Open The Simulation?
The simulation was built in [AnyLogic](http://www.anylogic.com) with supporting tools built in Java and Python. To view the model's structure, open `RCRS.alp` in [AnyLogic 8.5.x](http://www.anylogic.com). To compile and run the model you will need to follow the instructions at the end of this guide.

## How Do You Know That This Works?
There are two branches to ensuring a simulation works: verification and validation. In short, verification is ensuring that the simulation works as designed; validation is ensuring that the simulation produces sensible results.

Verification of RCRS is performed through manual and automatic means. In support code (e.g. census data reading), automated tests are performed when code is changed. These are expanded with new code or when bugs are found and are always supplemented with manual inspections and sense checks (e.g. is the simulation producing the right number of people, even if census reading tests come back OK?). Where automated testing is not time-effective, we heavily favor manual inspections of outputs and code reviews. We performed many manual verification efforts on the [Unity, Saskatchewan](https://en.wikipedia.org/wiki/Unity,_Saskatchewan) area due to the team's familiarity with the region.

Validation of RCRS is performed through approximating a real-world scenario (e.g. a town with ubiquitous handwashing and shut schools) and comparing the results of hypothetical scenarios (e.g. keep handwashing but reopen schools) to that baseline. We have chosen to focus heavily on the [Brooks, Alberta outbreak](https://brooksbulletin.com/covid-19-updates/) as the number of identified cases is well documented, the community is a size well-suited to the simulation, testing regiments can be inferred from news reports, and areas such as commercial districts, industrial districts, and many schools can be taken from town maps. This appears to be producing satisfactory results in many interventions: as smaller centers can have different demographics and contact patterns than larger centers, we expect that the impacts of some interventions may not match those in cities (precisely one of the reasons for this simulation being built!). We [welcome any findings or data](https://www.luminesim.com/rcrs) that show where the simulation can be improved. (*Note:* No simulation is a perfect recreation of the real world. *Exactly* reproducing known scenarios risks [overfitting](https://en.wikipedia.org/wiki/Overfitting), which we aim to avoid.)


# Implementation

## Terminology

- **Location.** A location such as a town, county, suburb, or lot. These may have associated populations.
- **Point of Interest (POI).** A place within a location. These include schools, businesses, assisted living facilities, etc. Some POI, such as assisted living facilities, may have permanent residents in addition to employees.
- **Home.** A place where people live not counting assisted living facilities. 
- **Close Contact Group.** A place where individuals can interact. All POIs and homes are close contact groups.
- **Population.** The people in the simulation.
- **GIS Region and GIS Point.** The shape (or point) on a map that defines the boundary (or exact position) of a location.

## Important Files
- `locations.csv.` The locations in the simulation.
- `location_attributes.csv.` Contains any important attributes tied to each location (e.g. rural vs urban area).
- `populations.csv.` The populations associated with each location, if any.
- `population_attributes.csv.` The attributes of each population, if any (e.g. household size distribution).
- `hierarchy.csv.` The nesting of locations, if any. Population counts in lower levels of the hierarchy are removed from their parent locations when people are created in the simulation.
- `areas.csv.` Defines the GIS regions and points of each location.
- `poi_groups.csv.` The points of interest (POI) groups in each location. POIs can be specified individually or in bulk (e.g. small businesses with 1-10 employees).


## Before Running: Population & Region Setup
The model's population, locations, GIS regions, and POI must be defined. While locations, GIS regions, and POI must be manually specified, population data can be derived from regional Statistics Canada census files using tools that accompany the model. Many population attributes are derived from census files (e.g. household size distribution) but manual attributes can also be added (e.g. flag as assisted living population). For critical sub-populations, e.g. long term care populations in group homes, sub-population census files must be created. These must be manually specified in the population hierarchy file to ensure the model does not create individuals twice. Since only a subset of information is drawn from each census file, manually created files are typically very small.

## Initialization
When the simulation begins, the following setup occurs:

### Region Seeding

Populations and GIS points and regions for each location are created. This is required before employment, households, points of interest, etc. can be established.

People are created for each location in `locations.csv`. People are divided into farm and non-farm families as selection of workplaces and likelihood of going out each day is assumed to differ for these groups. Empty homes are created according to census data. Any locations marked as assisted living facilities do not have homes created. These are assumed to be workplaces with permanent residents as well as employees.

Visualizations (dots) are added for the population. To improve simulation runtime, only a randomly-selected subset of the population is visualized. For example, there may be 30,000 people but only 500 dots. This dramatically reduces runtime while still demonstrating population movements and outbreaks.

### Household Initialization
The homes created above are randomly assigned a desired number of people (1, 2, 3, 4, 5+) in the proportions dictated by `population_attributes.csv`. Households are then shuffled. Students and adults *not* in assisted living are sorted by ascending age and assigned to households according to the following algorithm:

1. A primary adult in the household is chosen.
2. If more than two people live in the household, the person is paired with the next remaining member of the opposite sex according to known partnership probabilities. (*Notes:* Opposite-sex pairing is a simplifying assumption as no census data on same-sex living arrangements was readily available at design time. This can be rectified when data becomes available. Partnered individuals are generally very close to the same age.)
3. If more household members are required, youth are randomly selected to fill the gap. Parents are assumed to have children at 15 at the earliest; child age must match this constraint (e.g. a 20 year old parent cannot have a 10 year old child.)
4. If more household members are required, adults are randomly selected with uniform probability to fill the gap (e.g. live-in grandparents, roommates, etc.). 
5. Once all households have had members assigned, households are again shuffled to receive any remaining adults. This means some households will have more than their desired number of members.

This continues until there are no more adults to place. If any youth remain unallocated, an error is thrown.

### Point of Interest Allocation
`poi_groups.csv` contains points of interest (e.g. businesses) grouped by attributes and location (e.g. 10 businesses with 1-10 employees in Town CBD). They are created using the following algorithm:

1. For each group (e.g. small businesses) in each location (Town CBD):
	1. Repeat for the number of items in the group (e.g. 10 businesses):
		1. If a hospital, create a hospital. Note the number of employees. Move to the next item. *Note:* hospitals are created separately as they are anticipated to contain internal dynamics in the future, e.g. PPE specific to care staff, overcapacity levels leading to change in care outcomes, etc.
		1. Otherwise, if a workplace, create the workplace. Record the number of employees.
		1. If the workplace is assisted living, mark as such. Record the number of people living in those locations.
		1. If the workplace is a school, mark as such. 
		
Employees are then assigned:		

1. Identify the set of possible employees (i.e. adults 18-65 who do not work on a farm.)
1. Identify the desired range of employees for each workplace. Identify employee candidates, i.e., From the pool of unallocated possible employees, select either the desired number of employees or the remaining unallocated employees. If too few candidates exist, print out warning message. *Note:* in line with business data we have seen, workplace marked as having zero employees are assumed to be owner-operator and will thus have one person working.
1. Individuals who are employed are recorded as such.
1. Populations marked as assisted living populations are assigned to facilities randomly with a weight according to the known numbers living in those facilities. E.g. if facility A has 100 real-world residents and facility B has 10, facility A will receive residents in a 10:1 ratio.

Schools are then filled by grouping families with an assumed strong preference for nearby schools. I.e.:

1. Families are assumed to prefer nearby schools than those further away. For each family with children, a primary and secondary school are randomly selected with a weight: this weight is based on distance bands that rapidly decline with each new band. E.g. if the band size is 10km (see simulation parameters for current value), all schools within 0-10km will receive a high weight, all schools within 10-20km will receive a small weight, all schools within 20-30km will receive an extremely small weight, etc. *Note:* this behaviour is meant to favour nearby schools but not discount those further away. We use this approach as we currently have no data on school catchments,  preferences for religious vs public schools, nor readily-digestible data on school numbers. See model code for the weighting formula.
1. Families are assumed to send their primary-age children to the same randomly-selected primary schools and their secondary-age children to the same randomly-selected secondary schools. 

Youth too young to attend school do not go to school.

**Important Notes:**
* For speed of initialization, employees can come from any location in the simulation. This generally suffices as the locations of interest have historically been a community and surrounding rural area. This must be resolved if the model's scope increases beyond a small region. 
* All people are assumed to be full-time employees of their workplace. This is a simplifying assumption.
* School student counts are currently selected based on proximity, not on real-world numbers. This is due to lack of readily available school data.
* Primary school students are assumed to be youth 13 and younger.

### Position Setup
POI and homes are positioned within their GIS region or points. Where GIS regions overlap, any POI or home from the larger GIS region is repositioned if placed inside the smaller GIS region. For example, imagine town A has a reserved area for assisted living facilities. If a non-assisted living home is placed within the assisted living GIS region, its location is reassigned.

Once a home is placed, its members are placed nearby. This is to allow unique family members to be shown in visualizations.

**Warning:** this algorithm was used for ease of implementation: if GIS areas significantly overlap, this can dramatically slow simulation initialization.

### Finalization of Key Locations
People have all unallocated places assigned:

* People who work on a farm are assigned their home as their work location.
* People without an explicit daytime place (e.g. assisted living residents) are assigned their home as their daytime place.
* People are assigned a set of places that they may visit while not at work or school. This is a random subset of all workplaces accepting visitors: this is meant to represent people visiting schools for after-school activities, hospitals to visit patients, workplaces to buy groceries and other goods, etc. Empty workplaces, if any, are not allowed as a place to visit. Places outside a reasonable distance (see model parameter values) are not allowed. Of the remaining options, a small subset is selected. When individuals visit locations on evenings and weekends, they visit one of these locations randomly with a weight proportional to employee count, i.e., the number of employees is used as a proxy for how busy the location is. (*Note:* this assumption breaks down in centres with large office building populations: these workplaces can currently be marked as not accepting visitors.) People too far from any non-work location are assumed to stay home.
* A sanity check is performed to ensure all individuals have a home and places to visit during the day, evenings, and weekends.

## People: States and Behaviour

People in the simulation move between close contact groups (home, school, work, non-work locations) and have COVID-19 related state (susceptible, asymptomatic, symptomatic, recovered, dead).

### Movement Patterns 
People begin the simulation at home. The following general pattern repeats until the person is isolated or dies. Exceptions are noted below:

**General Pattern: Weekday**

1. At 8:00am, the person moves to their daytime place (workplace or school) for eight hours if (1) their workplace is open and (2) they are allowed to leave their home; if these conditions are not true, they remain at home. If the daytime place is their current place, no movement occurs.
1. The person may attempt to move to an evening place that is not their workplace. This happens with a given probability each evening (e.g. 50% chance of going out) provided the place is open. The place is selected randomly from a pre-weighted list of locations (see initialization algorithms) specific to each person. If the selected evening place is not open or probability dictates that the person does not go out, the person moves to their home location. If the person is already home, no movement occurs.
1. People sleep after 10pm or one hour after they return home, whichever comes first.

**General Pattern: Weekend**

1. The person may attempt to move to a daytime place that is not their workplace. This happens with a given probability each evening (e.g. 50% chance of going out) provided the place is open. The place is selected randomly from a pre-weighted list of locations (see initialization algorithms) specific to each person. If the selected evening place is not open or probability dictates that the person does not go out, the person moves to their home location. If the person is already home, no movement occurs.
1. The person attempts to move to an evening place that is not their workplace using the above algorithm.
1. People sleep after 10pm or one hour after they return home, whichever comes first.

**Exceptions**

1. If a person is hopsitalized, they are marked as being in an "atypical" location. They remain in this location until told to leave. 
1. If a person is told to stay at home if sick, they can still infect members of their household as per normal.

### COVID-19 State
People move through the following COVID-19 illness states:

1. **Susceptible.** All people are susceptible to COVID-19. They remain in this state unless one of the following occurs:
	1. They are infected via conversation (e.g. droplets from an infected person). This can be made less likely if the person has taken steps to reduce airborne transmission (e.g. wearing a mask).
	1. They are infected via a contaminated surface (e.g. by touching the surface then their mouth, nose, or eyes). This can be made less likely if the person has taken steps to reduce surface transmission (e.g. aggressive handwashing).
	1. They are specifically selected for infection (e.g. the simulation instructs the person to become infected, representing phenomena such as infections acquired through travel outside the community). This cannot be prevented by individuals.
1. **Asymptomatic Infectious.** The person is infected with COVID-19 through one of the above mechanisms. While infected, they can contaminate surfaces and transmit the infection via direct conversation. These modes of transmission can be reduced by masks and surface decontamination. People cannot infect others while sleeping. Each conversation can infect a maximum number of people (i.e. it is assumed that a limited number of people can be close enough to risk meaningful exposure during conversation).
1. **Symptomatic Infectious.** After a number of days spent asymptomatic (exact number drawn from a Poisson distribution; see parameter values), the person has a chance to become symptomatic. While symptomatic, the person continues to expose others using the methods listed above. If they do not develop symptoms, they are assumed to recover. The person also has a chance of being admitted to hospital and/or may be instructed to stay at home as they are sick. People cannot infect others while sleeping. Each conversation can infect a maximum number of people (i.e. it is assumed that a limited number of people can be close enough at once to risk exposure).
1. **Choice point: Death or Recovery.** After a number of days spent  infectious (exact number drawn from a Poisson distribution; see parameter values), the person either recovers or, if symptomatic, possibly dies. If the person is in hospital, their likelihood of dying increases dramatically (and drops if not hospitalized): this is meant to represent severity of illness symptoms. The base rate of death is based on reported death rates by age.
1. **Dead.** If the person dies from COVID-19, they are marked as dead, stop interacting with others, and are moved outside of the general population's GIS regions.
1. **Recovered.** If the person recovers, they are assumed to be immune from further infection. Life resumes as per normal.

*Note:* People are assumed to go back to normal movement after they cease to exhibit symptoms of COVID-19. This is a large number of days (see parameter values). This may need to be augmented with a post-illness isolation period.

## Close Contact Groups: Work, School, Care Centres, and Activities
Workplaces, schools, assisted living facilities, etc. are termed *close contact groups* in the model. These groups can be "closed" to prevent people from visiting them for work, leisure, education, etc. Their surfaces can be contaminated by people infected with COVID-19 and thus become a mode of transmitting the virus to others. After a period of time (drawn from a Poisson distribution; see parameter values), the surfaces cease to be infectious; if contaminated during this time, the timer is reset. Interventions can be applied that periodically decontaminate the group, removing the contamination. Surfaces can be recontaminated in the future.

When a close contact group is contaminated, a visual indicator is placed on the map. Otherwise, they are not displayed to reduce simulation runtime.

## True COVID-19 Cases vs Identified Cases
As the simulation knows the number of people symptomatic, asymptomatic, and recovered, it can report both the true number of COVID-19 cases at any moment as well the cumulative number of cases identified by the health system. In the simulation, all individuals hospitalized with COVID-19 are tested, a large number of non-hospitalized symptomatic people are tested, and, if enabled, random daily tests can be carried out in the general population. Tests are assumed to be 100% accurate. Testing probability can be time-based (e.g. testing blitzes).

One of the example scenarios included with the model demonstrates the impacts of a changing testing rate inspired by real-world news reports and clinics.

*Note:* The true number of cases is always greater than the identified number of cases. It is assumed that the random community testing rate is constant, that there are no test shortages, and that everyone randomly selected will submit to a test.

## Predetermined COVID-19 Cases 
While normally a generic model, the current release is tailored to reproduce outcomes seen in a real-world community. Specifically, the model begins by infecting a number of employees working at large employers. These employees then avoid work due to an outbreak. Work eventually resumes with all employees returning. 

In general operation, the model simply infects a new non-infected person on average once per day. This is to mimic the fact that in the real world communities generally cannot stop infections from appearing from the outside world.

## Interventions
The model is designed to support any type of intervention that can affect the behaviour of people and their interaction with their surroundings. Several are included as stock interventions and are described below. Unless otherwise specified, the values used are documented in the model's landing page. 

1. **Social Distancing.** Outside of home, the likelihood of infecting another person during conversation is reduced. 
1. **Masks.** Outside of home, the likelihood of contaminating surfaces is reduced, and the likelihood of exposing others to infection is reduced. *Note:* this is easily extended to reduce the likelihood of being infected by others, but our current understanding is that non-medical PPE is primarily used to prevent exposing others.
1. **Stay home if sick.** If a person is symptomatic and not hospitalized, they can be instructed to stay at home until no longer symptomatic.
1. **Stop school.** Schools shut, meaning that youth stay at home every day until the evening.
1. **Business disinfects surfaces.** Businesses clean down surfaces multiple times per hour, removing any contamination.
1. **Aggressive handwashing.** The likelihood of being infected by a contaminated surface is reduced.
1. **Stop non-essential small businesses.** Most small businesses cease operating. Large businesses are unaffected as, anecdotally, many are continuing to operate with social distancing in place. *Note:* this behaviour will need to be updated if the simulation is used in centres with large office building presence as these workplaces can remain open while people work from home.
1. **Reduce trips outside.** Individuals are less likely to go out (excludes work and school).

# Important Caveats
There are a few items that are worthwhile noting:

* The simulation is designed for short time frames. People do not age, do not die of non-COVID causes, and no one is born. This can be resolved if the model is used for longer projections.
* Business numbers are hard to obtain without local contacts in each community. Workable estimates are therefore derived by hand as placeholders.
* Economic impacts are not yet factored in to the model. This is an expected future extension.
* Parks and recreational areas are not explicitly modeled as they are assumed to be closed. This is easily resolved (i.e. they are another POI close contact group) and is a expected near-term feature as provinces are opening recreational areas slowly.
* Tertiary schools can be represented but are not yet included in the simulation.
* Employed individuals are full-time employees that work day shifts. This should be improved.
* Many health statistics (e.g. death rates) are reported as averages. When broken into sub-populations (e.g. death rate for those hospitalized and those not hospitalized), the average values may not be sufficient. When de-aggregation is required for sub-populations, we have attempted to apply reasonable scaling factors.
* Data on infection rates, hospitalization rates, death rates, etc. is drawn from a variety of sources both academic and non-academic (e.g. news articles reporting on early research). As numbers become more firm and more widely available, our inputs can be improved.

# Building & Improving the Simulation
This section is intended for simulation engineers, health modelers, and others interested in the internals of the model.

## Notes for Engineers & Other Modelers
The simulation's developers felt time was of the essence in developing and releasing this simulation. We have therefore focused heavily on simple mechanisms, simple state transitions, and simple individual behaviour. Design has been iterative to prioritize facets of emerging, real-world circumstances: while the simulation's results are constantly being internally verified and validated, this approach has come at the cost of engineering elegance. As time permits these are being improved.

This model is built using [AnyLogic Professional](http://www.anylogic.com) (for the simulation ALP); Java, Gradle, and IntelliJ (for supporting code artifacts); and Python and PyCharm (for census data manipulation). At a minimum, you will need AnyLogic to view and run the simulation: based on your license type you may be limited to the size of community you can run in the simulation.

The simulation will require you to download and compile the three packages in [ModelUtilities project](https://github.com/Luminesim/ModelUtilities) and acquire the following JARs, which are downloaded upon compiling said project using Gradle.

* citeproc-java-2.0.0.jar
* citeproc-java-2.0.0-sources.jar
* jgrapht-core-1.4.0.jar
* lightning-csv-8.2.2.jar
* ow2-asm-6.2.jar
* sfm-2.14.1.jar
* sfm-converter-8.2.2.jar
* sfm-csv-8.2.2.jar
* sfm-map-8.2.2.jar
* sfm-reflect-8.2.2.jar
* sfm-util-8.2.2.jar
* sfm-util-8.2.2-sources.jar

## Notes for Those Interested in the Data
Where possible, known data has been used and referenced. Where not possible, reasonable placeholders have been assigned. If any mechanism or data in this simulation is contradicted by or should be updated to use information available to you, [please let us know through our website.](http://www.luminesim.com/rcrs)

## Notes for Epidemiologists
This model has focused heavily on the probability of infecting individuals via conversation and via contaminated surfaces. Other data, such as the number of conversations per hour, the rate at which COVID-19 expires on surfaces, etc. have been used to supplement these probabilities, relying on emergence to produce infection rates consistent with the real world. The model is therefore sensitive to these values, but we have attempted to pin down as many as possible (e.g. conversations per hour) and work backward from known infection rates to arrive at reasonable estimates. If you have data regarding these values or any new information regarding reproductive rates (e.g. `R0`), [please contact us through our website.](http://www.luminesim.com/rcrs)


# Where Does this Differ From Other Simulations?
Our assumptions (e.g. people go home, sleep, avoid locations, do not distance nor wear masks in the home) mean that our simulation will deviate from simulations that make difference assumptions or do not include these factors. We are therefore beginning to collect research that differs substantially from the findings of RCRS; this list is expanded when simulation users and/or developers find such research and will therefore be incomplete. **The inclusions of these research lines do not indicate value judgments.** The reader is encouraged to investigate each research line independently and assess where their findings are best applied.

[We welcome feedback from the authors](http://luminesim.com/contact-us) should any of these descriptions misrepresent the published research.

## Universal Masking is Urgent in the COVID-19 Pandemic: SEIR and Agent Based Models, Empirical Validation, Policy Recommendations
*Kai et al, 2020. https://arxiv.org/pdf/2004.13553.pdf*

Our results deviate **in magnitude** from the paper's two models (one compartmental, one agent-based). Much like RCRS, the models are [SEIR-based](https://en.wikipedia.org/wiki/Compartmental_models_in_epidemiology).  The paper's models indicates that mask coverage of at least 80% can dramatically reduce or eliminate infection if implemented by Day 50 (Figures 1 and 2).  Early results from RCRS indicate that universal public mask coverage can result in a reduction in cases from a no-intervention scenario of about 40-50% in one of our test communities experiencing a large outbreak (Brooks, Alberta). Further testing and sensitivity analysis is needed for a more precise comparison figure.

The difference in results appears to come from the following factors:

1. The paper's models assume a fixed contact network, which can be reduced through 
interventions. In RCRS, individuals may have a core contact network (e.g. 
family, workplace) but additionally visit evening and weekend locations, 
which are meant to mimic essential or maintained activities such as visiting grocery stores, acquiring medical supplies, visiting locations for physical activity, etc. Limiting the core contact network, even under lockdown circumstances, will not stop random contacts in the broader population.
1. The models do not include differences between home and public life. Universal application of masks in the model would imply that individuals in the real world also wear masks at home. [Some secondary sources](https://www.theglobeandmail.com/world/article-out-of-home-quarantine-measures-in-china-helped-limit-spread-of/) indicate that "[in China], about 80 per cent of transmission happened in the homes, because that’s where the people were and that’s where they were most face to face with others." If this is true, this difference presents a critical, if not the key, difference between RCRS and the models. 
1. The models represent social distancing as "the degree distribution of the contact network of an individual." In RCRS, social distancing reduces the likelihood of infection between individuals interacting.

We believe that wearing masks all the time vs wearing them only in public is the most substantial difference between the models. Early testing indicates that by turning on masks *both at home and in public* in a location with existing outbreak there is a roughly 70% reduction in cases from the no-intervention case (vs 40-50% in the masks-in-public scenario). The size of the communities RCRS is designed to investigate vs the national populations noted in the paper may also explain some deviations from larger trends in this regard (e.g. masks may be more effective in dense populations). Further testing and sensitivity analysis is needed for a more precise comparison.

# Core Parameter Values
The following parameters are embedded in the simulation. They represent items assumed constant such as likelihood of contaminating a surface, social distancing efficacy, base death rate, etc. Local areas define their own local parameters (e.g. number of businesses, schools, population size, etc.). These values can be updated as required. **All parameters are from the no-intervention case: interventions applied in the model (e.g. those applied by ticking checkboxes) will update these values.** If you have better parameter data available to you, [please report it through our website](http://luminesim.com/contact-us).

**Important:** We have frequently been limited to secondary sources (e.g. news reports on number of COVID-19 cases in a community, news reports on unpublished peer review data, conversations regarding likely infection sources and rates, etc.). If you have primary sources available to you, [please report them through our website](http://luminesim.com/contact-us).

# Initial Parameters

An *operational value* is a value chosen by the simulation team; ideally, these estimates should have little value on simulation results. A *placeholder value* is a parameter used by the simulation that should be improved with better data. These values may have more substantial effect on simulation results.

*Last updated: May 18, 2020*

Label|Authority|Title|URL|Note|Value
-----|-----|-----|-----|-----|-----|-----|-----
Age below which youth are considered infants.|Operational Value||||4
Assumption #1||||Individuals not in assisted living or who are infants go to workplaces at night for necessities, entertainment, etc. This behaviour should be expanded.|N/A
Average number of days that coronavirus can survive on surfaces|Harvard Health Publishing|How long can the coronavirus that causes COVID-19 survive on surfaces?|https://www.health.harvard.edu/diseases-and-conditions/covid-19-basics|The given range says 'up to' a few hours or days, depending on material. This average will produce that range because rates (where this value is used) are drawn from a poisson distribution. Quote: COVID-19 coronavirus can survive up to four hours on copper, up to 24 hours on cardboard, and up to two to three days on plastic and stainless steel. The researchers also found that this virus can hang out as droplets in the air for up to three hours before they fall. But most often they will fall more quickly.|1.0
Death rate for all cases by age group||Age, Sex, Existing Conditions of COVID-19 Cases and Deaths|https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/|The table in the cited URL is based on (1) The Report of the WHO-China Joint Mission published on Feb. 28 by WHO, which is based on 55,924 laboratory confirmed cases and (2) A paper by the Chinese CCDC released on Feb. 17, which is based on 72,314 confirmed, suspected, and asymptomatic cases of COVID-19 in China as of Feb. 11, and was published in the Chinese Journal of Epidemiology. Quote: 'Death Rate = (number of deaths / number of cases) = probability of dying if infected by the virus (%).'|Table Function; Linear  interpolation; If argument is out of range: uses nearest argument's value; 9 rows; 0	0; 10	0.2; 20	0.2; 30	0.2; 40	0.4; 50	1.3; 60	3.6; 70	8; 80	14.8; 
Death rate in confirmed COVID cases in 80+ category||Age, Sex, Existing Conditions of COVID-19 Cases and Deaths|https://www.worldometers.info/coronavirus/coronavirus-age-sex-demographics/|This value is used for sense-checking results and is to be used when examining confirmed COVID cases (which we assume to be symptomatic)|21.9
Factor applied to death rate if person sick enough to be admitted to hospital.|Placeholder|||Death rates are often reported on average; averages will mask the fact that hospitalization increases likelihood of death (and vice versa)|5.0
Factor applied to death rate if sick person was not ill enough to be admitted to hospital|Placeholder|||Death rates are often reported on average; averages will mask the fact that hospitalization increases likelihood of death (and vice versa)|0.2
Hour at which people leave the house in the morning|Operational Value||||8
Hour at which people sleep|Operational Value||||22
Hours that a person spends at their daytime location each day (e.g. school, work)|Operational Value||||8
Hours that a person spends at their evening location (e.g. going to shop, going to restaurant, etc.)|Operational Value||||2
Maximum distance (km) that someone will drive for a day job.|Placeholder||||50.0
Maximum distance (km) that someone will drive to non-work locations.|Placeholder||||100.0
Maximum distance (km) that someone will drive to school.|Placeholder||||100.0
Maximum number of non-work options.|Placeholder||||10.0
Maximum number of people exposed in each conversation to COVID (if the speaker has it)|Placeholder||||5
Multiplier for probability of infecting another person outside of the home|Placeholder|||Used for implementing masks, which act to reduce likelihood of transmission|1.0
Number of speaking interactions per hour (on average) at a person's daytime location|Placeholder|mConverse: Inferring Conversation Episodes fromRespiratory Measurements Collected in the Field|https://dl.acm.org/doi/abs/10.1145/2077546.2077557|Amount inspired by this paper with the sum (50) of Figure 12 (Average number of conversations of agiven duration, per person, per day) divided over 16 hours, which is roughly three conversations per hour.|3
Number of speaking interactions per hour (on average) at a person's evening location|Placeholder|mConverse: Inferring Conversation Episodes fromRespiratory Measurements Collected in the Field|https://dl.acm.org/doi/abs/10.1145/2077546.2077557|Amount inspired by this paper with the sum (50) of Figure 12 (Average number of conversations of agiven duration, per person, per day) divided over 16 hours, which is roughly three conversations per hour.|3
Number of speaking interactions per hour (on average) at a person's home (while awake)|Placeholder|mConverse: Inferring Conversation Episodes fromRespiratory Measurements Collected in the Field|https://dl.acm.org/doi/abs/10.1145/2077546.2077557|Amount inspired by this paper with the sum (50) of Figure 12 (Average number of conversations of agiven duration, per person, per day) divided over 16 hours, which is roughly three conversations per hour.|3
Number of speaking interactions per hour (on average) when the location is unspecified.|Placeholder|||We use this for places like hospitals.|1
P(Block COVID infection that would have otherwise resulted from infected person speaking directly into mouth, eyes, nose (i.e. direct aerosol exposure))|Placeholder|||This parameter is meant to represent how likely someone is to catch COVID if someone is speaking in their face.|0.0
P(Contaminate surfaces at close-contact group in any hour \| Infected)|Placeholder||||0.1
P(Expose someone during conversation \| Location where social distancing NOT possible)|Placeholder||||0.02
P(Go out in evening \| Rural Family)|Placeholder|||A simplifying assumption.|0.2
P(Go out in evening \| Urban Family)|Placeholder|||A simplifying assumption.|0.5
P(Hospitalization \| Symptomatic)||Odds of Hospitalization, Death with COVID-19 Rise Steadily With Age: Study|https://www.usnews.com/news/health-news/articles/2020-03-30/odds-of-hospitalization-death-with-covid-19-rise-steadily-with-age-study||Table Function; Linear  interpolation; If argument is out of range: uses nearest argument's value; 9 rows; 0	0; 10	0.1; 20	1; 30	3.4; 40	4.3; 50	8.2; 60	11.8; 70	16.6; 80	19; 
P(Infect someone during conversation \| Location where social distancing is possible)|Placeholder||||0.02
P(Infected by contaminated surface in a close-contact location)|Placeholder||||0.2
P(Recover without becoming symptomatic \| Asymptomatic carrier)|||https://www.usatoday.com/story/news/world/2020/04/10/coronavirus-covid-19-small-nations-iceland-big-data/2959797001/|The article notes that 50% of people are asymptomatic from a random test sample. Quote: 'celand's randomized tests revealed that between 0.3%-0.8% of Iceland's population is infected with the respiratory illness, that about 50% of those who test positive for the virus are asymptomatic when they are tested'. Other sources note that this may be as high as 80% when very mild symptoms are included. We therefore tune this value a bit.|0.7
P(Stay home if sick until recovered \| Symptomatic)|Placeholder||||0.9
P(Test person once symptomatic \| Area = Brooks & Not Hospitalized)|Brooks Bulletin Editor|COVID-19 UPDATES|https://brooksbulletin.com/covid-19-updates/|Inspired by known testing blitzes in Brooks.|Table Function; Linear  interpolation; If argument is out of range: uses nearest argument's value; 3 rows; 0	0.8; 42	0.8; 90	0.8; 
P(Test person once symptomatic \| Not Hospitalized)|Placeholder|||This may be overridden by the specific community. Check for revisions OR a probability with the community's name flagged.|Table Function; Linear  interpolation; If argument is out of range: uses nearest argument's value; 2 rows; 0	0.8; 999	0.8; 
P(Test person) each day if testing is switched on|Placeholder||||0.25
Times per hour at a close-contact group that common surfaces are sanitized|Placeholder||||0.0
While asymptomatic: Average amount number of days to either develop symptoms or recover|Harvard Health Publishing|COVID-19 basics|https://www.health.harvard.edu/diseases-and-conditions/covid-19-basics|Using upper average for incubation. Quote: Recently published research found that on average, the time from exposure to symptom onset (known as the incubation period) is about five to six days. However, studies have shown that symptoms could appear as soon as three days after exposure to as long as 13 days later. These findings continue to support the CDC recommendation of self-quarantine and monitoring of symptoms for 14 days post exposure.|6
While symptomatic: Average number of days to either recover or die|WHO|Report of the WHO-China Joint Mission on Coronavirus Disease 2019 (COVID-19) |https://www.who.int/docs/default-source/coronaviruse/who-china-joint-mission-on-covid-19-final-report.pdf|Using low end of serious disease band. Quote: 'Using available preliminary data, the median time from onset to clinical recovery for mild cases is approximately 2 weeks and is 3-6 weeks for patients with severe or critical disease. Preliminary data suggests that the time period from onset to the development of severe disease, including hypoxia, is 1 week. Among patients who have died, the time from symptom onset to outcome ranges from 2-8 weeks'|21
