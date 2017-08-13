/* 
 * To change this license header, choose License Headers in Project Properties.
 * To change this template file, choose Tools | Templates
 * and open the template in the editor.
 */

// game properties
var gameTimerDefault = 5; // in seconds
var spinsLeftDefault = 50;

// list of wheel options
var category_bankrupt = "Bankrupt";
var category_loseTurn = "Lose Turn";
var category_freeTurn = "Free Turn";
var category_spinAgain = "Spin Again";
var category_playerChoice = "Player's Choice";
var category_opponentChoice = "Opponent's Choice";

function GameController(wheelParam, playerListParam)
{
    this.wheel = wheelParam;
    this.spinsLeft = spinsLeftDefault;
    this.gameTimer = gameTimerDefault; // in seconds
    this.round = 1;
    this.currentPlayerIndex = 0; // index of the player whose turn it is
    this.playerList = playerListParam; 
}

GameController.prototype = {
    startGame: function ()
    {
        this.setPlayerNames();
        this.updateSpinsLeft();
        this.updateCurrentPlayer();
    },
    
    startCountdownTimer: function ()
    {
        var self = this;
        self.gameTimer = gameTimerDefault;
        
        var outputId = "timer";
        var x = setInterval(function () {
			//disable spin until the question is answered or time is update
			self.disableSpinButtons()
            // Display the result in the element with outputId
            document.getElementById(outputId).innerHTML = self.gameTimer;
            // If the count down is finished, write some text 
            if (self.gameTimer <= 0) {
                clearInterval(x);
                document.getElementById(outputId).innerHTML = "0";
                // play timeup sound
                var audio = new Audio('sound/timeUp.mp3');
                audio.play();
				
				//enable the currentPlayer to spin
				self.enableSpinButton(self.currentPlayerIndex)
            }
            self.gameTimer--;
        }, 1000);
    },

    // sets the player's names on the screen
    setPlayerNames: function()
    {
        var self = this;
        
        document.getElementById("player0Name").innerHTML = self.playerList[0].name;
        document.getElementById("player1Name").innerHTML = self.playerList[1].name;
        document.getElementById("player2Name").innerHTML = self.playerList[2].name;
    },

    // updates spins left on the screen
    updateSpinsLeft: function ()
    {
        var self = this;
        var outputId = "spinsLeft";
        
        document.getElementById(outputId).innerHTML = self.spinsLeft;
    },
    
    // updates Category title on the screen
    updateCategory: function(categoryTitle)
    {
        var self = this;
        var outputId = "category";
        document.getElementById(outputId).textContent = categoryTitle; // display category
    },
    
    // update current player name on the screen based on name
    updateCurrentPlayer: function ()
    {
        var self = this;
        var outputId = "currentPlayerName";
        
        var currentPlayer = self.playerList[self.currentPlayerIndex];
        document.getElementById(outputId).innerHTML = currentPlayer.name;
    },
    
    // updates score for player on the screen
    updatePlayerScore: function(playerIndex) // playerIndex: 0-2 
    {
        var self = this;
        var outputId = "player"+playerIndex+"Score";
        
        var selectedPlayer = self.playerList[playerIndex];
        document.getElementById(outputId).innerHTML = selectedPlayer.score;
    },
    
    // updates tokens for player on the screen
    updatePlayerTokens: function(playerIndex) // playerIndex: 0-2 
    {
        var self = this;
        var outputId = "player"+playerIndex+"Tokens";
        
        var selectedPlayer = self.playerList[playerIndex];
        document.getElementById(outputId).innerHTML = selectedPlayer.tokens;
    },
    
    incrementPlayer: function()
    {
        var self = this;
        self.currentPlayerIndex++;
        if (self.currentPlayerIndex > 2)
        {
            self.currentPlayerIndex = 0;
        }
    },
    
    disableSpinButtons: function()
    {
        document.getElementById("player0Spin").disabled = true;
        document.getElementById("player1Spin").disabled = true;
        document.getElementById("player2Spin").disabled = true;
    },
    
    enableSpinButton: function(playerIndex) // options are: player0Spin|player1Spin|player2Spin
    {
        document.getElementById("player"+playerIndex+"Spin").disabled = false;
    },
    
    processWheelCategory: function(categoryText)
    {
        var self = this;
        
        // update spinsLeft and current Category for every case
        this.updateSpinsLeft();
        this.updateCategory(categoryText);
        
        if (categoryText === category_bankrupt)
        {
            var currentPlayer = self.playerList[self.currentPlayerIndex];
            currentPlayer.setScore(-10);
            self.updatePlayerScore(self.currentPlayerIndex);
            
            self.incrementPlayer();
            self.updateCurrentPlayer();
            
            self.enableSpinButton(self.currentPlayerIndex);
        }
        else if (categoryText === category_loseTurn)
        {
            // TODO - need to code using token
            
            self.incrementPlayer();
            self.updateCurrentPlayer();
            self.enableSpinButton(self.currentPlayerIndex);
        }
        else if (categoryText === category_freeTurn)
        {
            var currentPlayer = self.playerList[self.currentPlayerIndex];
            currentPlayer.incrementToken();
            self.updatePlayerTokens(self.currentPlayerIndex);
            
            self.enableSpinButton(self.currentPlayerIndex);
        }
        else if (categoryText === category_spinAgain)
        {
            self.enableSpinButton(self.currentPlayerIndex);
        }
        else if (categoryText === category_playerChoice)
        {
            
        }
        else if (categoryText === category_opponentChoice)
        {
            
        }
        else // one of the jeopardy categories selected
        {
            this.startCountdownTimer();
            self.incrementPlayer();
            self.updateCurrentPlayer();
            self.enableSpinButton(self.currentPlayerIndex);
        }
    }
};

