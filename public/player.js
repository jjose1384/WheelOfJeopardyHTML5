/*
 * The player object is used to keep track of the players for the game and 
 * all related functions
 */
function Player(nameParam) {
    this.name = nameParam;
    this.scoreR1 = 0; // round 1 score
    this.scoreR2 = 0; // round 2 score
    this.tokens = 0;
}

Player.prototype = {
    getScore: function(roundParam) // set the score of player based on scoreParam
    {
        if (roundParam === 2)
        {
            return this.scoreR2;
        }
        else
        {
           return this.scoreR1;
        }
        
    },
    
    setScore: function(scoreParam, roundParam) // set the score of player based on scoreParam
    {
        if (roundParam === 2)
        {
            this.scoreR2 = scoreParam;
        }
        else
        {
            this.scoreR1 = scoreParam;
        }
        
    },
    
    /*
     *  add or subtract the scoreParam to the player's score
     *  based on the round
     *  
     *  roundParam can be 1 or 2 
     */
    addSubtractScore: function(scoreParam, roundParam) 
    {
        if (roundParam === 2)
        {
            this.scoreR2 = this.scoreR2 + scoreParam;
        }
        else
        {
            this.scoreR1 = this.scoreR1 + scoreParam;
        }
    }
};

