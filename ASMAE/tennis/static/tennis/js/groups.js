'use strict';


/*******************  
* Tournament class *
*******************/
function Tournament(pairs, courts, groups) {    
    // pairs
    if (pairs == undefined)
        this.pairs = [];
    else
        this.pairs = pairs;

    // courts
    if (courts == undefined)
        this.courts = [];
    else
        this.courts = courts;

    // groups
    if (groups == undefined)
        this.groups = [];
    else
        this.groups = groups;
}

/***********************************************
* Tournament class: create_empty_groups method *
***********************************************/
Tournament.prototype.create_empty_groups = function(group_num, group_size) {
    this.groups = []
    var groups = this.groups;
    var nbrePairs = this.pairs.length - group_num*group_size;
    //var nbreGroupe = Math.ceil(nbrePairs / group_size);
    for (var group_i = 0; group_i < group_num; group_i++) {
        var group = new Group(group_size);
        groups.push(group);
    }
    if (nbrePairs > 0) {
        var new_group = new Group(nbrePairs);
        groups.push(new_group);
    }
}

/***************************************************
* Tournament class: try_naively_fill_groups method *
***************************************************/
Tournament.prototype.try_naively_fill_groups = function() {
    var pairs_num = this.pairs.length;
    var courts_num = this.courts.length;
    var current_pair_index = 0;
    var current_court_index = 0;
    var group1 = this.groups[0];
    var group_size = group1.gsize;
    var group_num = this.groups.length;
    //this.create_empty_groups(group_num, group_size);
    var groups = this.groups;
    for (var group_i in groups) {
        var group = groups[group_i];
        var group_size = group.gsize;
        // insert court if still courts to insert
        if (current_court_index < courts_num) {
            var court = this.courts[current_court_index];
            group.court = court;
            current_court_index++;
        }
        // insert pairs
        for (var group_index = 0; group_index < group_size; group_index++) {
            // insert pair if still pairs to insert
            if (current_pair_index < pairs_num) {
                var pair = this.pairs[current_pair_index];
                group.pairs.push(pair);
                current_pair_index++;
            }
        }
    }
}

/************************************************************
* Tournament class: try_naively_select_group_leaders method *
************************************************************/
Tournament.prototype.try_naively_select_group_leaders = function() {
    var groups = this.groups;
    for (var group_i in groups) {
        var group = groups[group_i];
        var pairs = group.pairs;
        var group_pairs_num = group.pairs.length;
        // select a leader only if the group is non-empty
        if (group_pairs_num > 0) {
            // select the first pair as leader
            group.leader = pairs[0];
        }
    }
}

/****************************************************
* Tournament class: try_swap_pairs_in_groups method *
****************************************************/
Tournament.prototype.try_swap_pairs_in_groups = function(group1_id, group2_id, group1_index, group2_index) {
    var groups = this.groups;
    var group_num = groups.length;
    if (group1_id < group_num && group2_id < group_num) {
        var group1 = groups[group1_id];
        var group2 = groups[group2_id];
        var group1_pairs_num = group1.pairs.length;
        var group2_pairs_num = group2.pairs.length;
        // check if group_indexes are valid
        if (group1_index < group1_pairs_num && group2_index < group2_pairs_num) {
            // swap pairs
            var temp = group1.pairs[group1_index];
            group1.pairs[group1_index] = group2.pairs[group2_index];
            group2.pairs[group2_index] = temp;
        }
        else if (group1_index < group1_pairs_num && group2_pairs_num < group2.gsize) {
            // group2_index does not exist and group2 is not full
            // move the pair from group1 to group2
            var pair1 = group1.pairs[group1_index];
            group2.pairs.push(pair1);
            group1.pairs.splice(group1_index, 1);
        }
        else if (group2_index < group2_pairs_num && group1_pairs_num < group1.gsize) {
            // group1_index does not exist and group1 is not full
            // move the pair from group2 to group1
            var pair2 = group2.pairs[group2_index];
            group1.pairs.push(pair2);
            group2.pairs.splice(group2_index, 1);
        }
    }
};

Tournament.prototype.str_groups = function() {
    var groups = this.groups;
    if (groups.length == 0) {
        return "This tournament has no groups";
    }
    var str_groups = "Tournament has the following groups: grp1: leader is " + groups[0].leader + ", pairs are (" + groups[0].pairs.toString() + "), court is [" + groups[0].court + "]";
    for (var group_i=1; group_i < groups.length; group_i++) {
        var group = groups[group_i];
        str_groups += " <AND> grp" + (group_i+1) + ": leader is " + group.leader + ", pairs are (" + group.pairs.toString() + "), court is [" + group.court + "]";
    }
    str_groups += "."
    return str_groups;
};

/**************  
* Group class *
**************/
function Group(gsize, pairs, court, leader) {
    // gsize
    if (gsize == undefined)
        this.gsize = 0;
    else
        this.gsize = gsize;

    // pairs
    if (pairs == undefined)
        this.pairs = [];
    else
        this.pairs = pairs;

    // court
    this.court = court;
    
    // leader
    this.leader = leader;
}