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

    // uninserted_pairs
    this.uninserted_pairs = [];

}

/***********************************************
* Tournament class: create_empty_groups method *
***********************************************/
Tournament.prototype.create_empty_groups = function(group_num, group_size) {

    // create groups
    this.groups = [];
    var pairs = this.pairs;
    var groups = this.groups;
    for (var group_i = 0; group_i < group_num; group_i++) {
        var group = new Group(group_size);
        groups.push(group);
    }

    // create uninserted pairs
    for (var pair_i in pairs) {
        var pair = pairs[pair_i];
        this.uninserted_pairs.push(pair);
    }
}

/****************************************
* Tournament class: adapt_groups method *
*****************************************/
Tournament.prototype.adapt_groups = function(group_num, group_size) {
    // groups is considered as non-empty (create_empty_groups called otherwise)
    var groups = this.groups;
    if(groups.length == 0)
        this.create_empty_groups(group_num, group_size);
    else {
        // group_size
        var first_group = groups[0];
        if (group_size != first_group.gsize) {
            // set group_size for all groups
            for (var group_i in groups) {
                var group = groups[group_i];
                group.gsize = group_size;
                if (group.pairs.length > group_size) {
                    var to_remove_num = group.pairs.length - group_size;
                    // make these pairs as uninserted
                    for (var i = 0; i < to_remove_num; i++) {
                        var group_pair_index = parseInt(group_size) + parseInt(i);
                        var pair = group.pairs[group_pair_index];
                        this.uninserted_pairs.push(pair);
                    }
                    // remove these pairs from the group (group shrinks)
                    group.pairs.splice(group_size, to_remove_num);
                }
            }
        }
        // group_num
        if (group_num > groups.length) {
            // create new groups
            var new_group_num = group_num - groups.length;
            for (var i = 0; i < new_group_num; i++) {
                var group = new Group(group_size);
                groups.push(group);
            }
        }
        else if (group_num < groups.length) {
            // remove some groups
            // move the pairs to uninserted pairs
            for (var group_i = group_num; group_i < groups.length; group_i++) {
                var group = groups[group_i];
                for (var pair_i in group.pairs) {
                    var pair = group.pairs[pair_i];
                    this.uninserted_pairs.push(pair);
                }
            }
            // remove the exceeding groups
            var group_to_remove = groups.length - group_num;
            groups.splice(group_num, group_to_remove);
        }
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
    var groups = this.groups;
    // reset uninserted pairs
    this.uninserted_pairs = [];
    // reset groups
    for (var group_i in groups) {
        var group = groups[group_i];
        group.pairs = [];
        group.court = undefined;
        group.leader = undefined;
    }

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
                this.uninserted_pairs.splice(this.uninserted_pairs.indexOf(pair), 1);
                current_pair_index++;
            }
        }
    }

    // insert next pairs to uninserted pairs
    while(current_pair_index < pairs_num) {
    	var pair = this.pairs[current_pair_index];
    	this.uninserted_pairs.push(pair);
    	current_pair_index++;
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
    // uninserted pairs "=" group with id -1
    var groups = this.groups;
    var group_num = groups.length;
    if (group1_id < group_num && group2_id < group_num) {
        // group swap
        var group1_pairs = undefined;
        var group1_pairs_num = undefined;
        var group1_size = undefined;
        if (group1_id == -1) {
            group1_pairs = this.uninserted_pairs;
            group1_pairs_num = this.uninserted_pairs.length;
            group1_size = group1_pairs_num;
        }
        else {
            group1_pairs = groups[group1_id].pairs;
            group1_pairs_num = groups[group1_id].pairs.length;
            group1_size = groups[group1_id].gsize;            
        }
        var group2_pairs = undefined;
        var group2_pairs_num = undefined;
        var group2_size = undefined;
        if (group2_id == -1) {
            group2_pairs = this.uninserted_pairs;
            group2_pairs_num = this.uninserted_pairs.length;
            group2_size = group2_pairs_num;
        }
        else {
            group2_pairs = groups[group2_id].pairs;
            group2_pairs_num = groups[group2_id].pairs.length;
            group2_size = groups[group2_id].gsize;
        }
        // check if group_indexes both have pairs
        if (group1_index < group1_pairs_num && group2_index < group2_pairs_num) {
            // swap the two pairs
            var temp = group1_pairs[group1_index];
            group1_pairs[group1_index] = group2_pairs[group2_index];
            group2_pairs[group2_index] = temp;
        }
        else if (group1_index < group1_pairs_num && ((group2_id === -1) || (group2_id != -1 && group2_pairs_num < group2_size))) {
            // group2_index does not exist and group2 is not full
            // move the pair from group1 to group2
            var pair1 = group1_pairs[group1_index];
            group2_pairs.push(pair1);
            group1_pairs.splice(group1_index, 1);
        }
        else if (group2_index < group2_pairs_num && ((group1_id === -1) || (group1_id != -1 && group1_pairs_num < group1_size))) {
            // group1_index does not exist and group1 is not full
            // move the pair from group2 to group1
            var pair2 = group2_pairs[group2_index];
            group1_pairs.push(pair2);
            group2_pairs.splice(group2_index, 1);
        }
    }
};


/**************************************
* Tournament class: str_groups method *
***************************************/
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
    if (this.uninserted_pairs.length == 0) {
        str_groups += " It has no uninserted pairs."
    }
    else {
        str_groups += " These are the uninserted pairs: " + this.uninserted_pairs[0];
        for (var pair_i = 1; pair_i < this.uninserted_pairs.length; pair_i++) {
            str_groups += ", " + this.uninserted_pairs[pair_i];
        }
        str_groups += "."
    }
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