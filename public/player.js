/*
 * The player object is used to keep track of the players for the game and 
 * all related functions
 */
function Player(nameParam) {
    this.name = nameParam;
    this.score = 0;
    this.tokens = 0;
}

Player.prototype = {
    setScore: function(scoreParam) // set the score of player based on scoreParam
    {
        this.score = scoreParam;
    },
    
    addSubtractScore: function(scoreParam) // add or subtract the scoreParam to the player's score 
    {
        this.score = this.score + scoreParam;
    },
    
    incrementToken: function()
    {
        this.tokens++;
    },
    
    decrementToken: function()
    {
        if (this.tokens > 0)
        {
            this.tokens--;
        }
    }
};

