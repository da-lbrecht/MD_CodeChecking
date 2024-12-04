********************************************************************************
****************** Example Do-File H1: #ManyDaughters Project ******************
********************************************************************************

* Authors: Tina Wang, David Albrecht

* ============================
* Setup
* ============================

clear all
version 17 // indicate the version of stata you are using here
capture log close // close log session, if one is still runnning
set maxvar 10000 // extend the maximum number of variables to 10,000

* INSTALL PACKAGES *
ssc install outreg2 // install all packages you need here, outreg2 is needed for export of results

* CONFIGURE FILE PARGS *
global ROOT "`c(pwd)'/ManyDaughters_RT_AnalysisPackage"
global IN "$ROOT/data/raw" // folder, in which the original datasets are stored
global DATA "$ROOT/data" // folder for datasets
global OUT "$ROOT/out" // folder for output (results, tables)
global LOG "$ROOT/log" // folder for log-files

* LOGGING *
log using "$LOG/example.smcl", replace // start log session





* ============================
* Data Preparation
* ============================

* LOAD AND MERGE DATA *

use "$IN/ppathl.dta", clear

* Merge ppathl with all datasets, that you deem relevant for your analysis. (Tip: use keepusing() to specify which variables to keep from the using dataset; the default is all.)

* biobirth contains information on fertility history
merge m:1 pid using "$IN\biobirth.dta", nogen keep(master matches)
* bioparen contains biographical entries on the parents' and respondent's background
merge m:1 pid using "$IN\bioparen.dta", nogen keep(master matches)
* pgen contains user-friendly data on the individual level that are consolidated from different sources
merge 1:1 pid syear using "$IN\pgen.dta", nogen keep(master matches)
* pl contains all variables from the individual questionnaire
merge 1:1 pid syear using "$IN\pl.dta", nogen keep(master matches)






* ============================
* Analysis
* ============================

* FILTERS *

* Example: only keep participants from private households
keep if inlist(pop,1,2)


* GENERATE VARIABLES *

	* Example: generate dummy variable for whether participant has at least one daughter
	gen d_daughter = 0
	foreach i in 01 02 03 04 05 06 07 08 09 10 11 12 13 14 15 16 17 18 19 {
		replace d_daughter = 1 if kidsex`i'==2
	}


* REGRESSION ANALYSIS * 

	* For illustrative purposes, let's assume that that regularly working at night (plb0080) is a good measure of support for gender equality (hypothesis 1), 
	* if regularly working at night, the respondent is more likely to support gender equality.
	* A minimum working example of an analysis that satisfies the requirements of the project we could run a linear OLS regression analysis
	* with plb0080 as dependent variable and the dummy variable d_daughter as independent variable
	reg plb0080 d_daughter


* EXPORT RESULTS *

	* Extract the required statistics

	 	* p-value
		local p_value = _b[d_daughter] / _se[d_daughter]
		local p_value = 2 * ttail(e(df_r), abs(`p_value'))
		di `p_value'

		* number of observations
		local num_obs = e(N)

		* number of participants
		levelsof pid if e(sample), local(unique_pids)
		local num_participants : word count of `unique_pids'
		di `num_participants'

		* degrees of freedom
		local df = e(df_r)

		* interpretation of directionality
		local interpretation = cond(_b[d_daughter] > 0, "in line with hypothesis", "not in line with hypothesis")

	* Open a file for writing
	file open myfile using "$OUT/hypothesis-1_results.csv", write replace
	file write myfile "p_value,num_obs,num_participants,df,interpretation" _n
	file write myfile "`p_value',`num_obs',`num_participants',`df',`interpretation'" _n
	file close myfile





********************************************************************************

* close log file and translate it into log-format:
log close
translate "$LOG\merge.smcl" "$LOG\merge.log", replace

exit
