Copy the set of demand nodes.
Copy the set of possible facilities.
While (the COPY set of the demand nodes is not 0) {
	Check which facility(ies) can cover each demand node.
If (demand node is covered by a facility) {
	yi = 1 
	Add yi to the COPY of selected demand nodes.
}else{
	yi = 0 
}
COPY set of demand nodes minus 1
}
While (the output X <= p number of facilities to be located) {
    “Greedy function of j” equals to the sum of wi value of each 
    yi (the demand nodes) in the COPY of selected demand nodes, located in 
    j facility that are in the COPY of the set of possible facilities.
	Select the j that has the maximum wi value
	Establish xj as 1 of that facility
    Establish for the nodes in j selected, yi as 1 
	Put the j that was selected in the set X
	Put the yi that are in j selected in the set Y
	Erase the selected facility from the copy set of possible facilities.
    Erase the nodes that are in the selected facility from the COPY of selected demand nodes 
}
return X, Y
