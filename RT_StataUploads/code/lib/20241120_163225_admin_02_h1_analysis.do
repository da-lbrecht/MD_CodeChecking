********************************************************************************
**** Example analysis H1 based on SOEP datasets: #ManyDaughters Project ********
********************************************************************************

* Authors: Tina Wang, David Albrecht

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

	* For illustrative purposes, let's assume that that gripstrength is a good measure of support for gender equality (hypothesis 1), 
	* the higher the grip strength, the more likely the person is to support gender equality.
	* A minimum working example of an analysis that satisfies the requirements of the project we could run a linear OLS regression analysis
	* with grip strength as dependent variable and the dummy variable d_daughter as independent variable
	reg gs03 d_daughter


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
